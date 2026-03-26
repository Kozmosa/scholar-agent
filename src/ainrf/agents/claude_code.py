from __future__ import annotations

import json
import os
import re
import shlex
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from ainrf.agents.base import AgentAdapter, AgentExecutionError
from ainrf.agents.skill_profiles import build_step_skill_payload
from ainrf.engine.models import AtomicTaskSpec, StepArtifactRef, TaskExecutionResult, TaskPlanResult
from ainrf.execution import (
    CommandTimeoutError,
    ContainerConfig,
    SSHConnectionError,
    SSHExecutor,
    TransferError,
)

_REMOTE_RUNNER_PATH = ".ainrf-runtime/claude_code_runner.py"


_STEP_SKILL_MAPPING: dict[str, str] = {
    "prioritize_references": "research-lit",
    "update_knowledge_graph": "idea-discovery",
    "check_termination": "auto-review-loop",
    "diagnose_deviation": "analyze-results",
    "generate_quality_assessment": "research-review",
}


@dataclass(slots=True)
class SkillRuntimeConfig:
    skills_root: Path
    enabled_skills: frozenset[str]
    step_timeout_seconds: int
    strict_mode: bool

    @classmethod
    def from_env(cls, state_root: Path | None = None) -> "SkillRuntimeConfig":
        resolved_state_root = state_root or Path(".ainrf")
        raw_skills_root = os.environ.get("AINRF_SKILLS_ROOT")
        skills_root = Path(raw_skills_root) if raw_skills_root else resolved_state_root / "skills"
        raw_enabled = os.environ.get("AINRF_ENABLED_SKILLS", "")
        enabled_skills = frozenset(item.strip() for item in raw_enabled.split(",") if item.strip())
        step_timeout_seconds = int(os.environ.get("AINRF_STEP_TIMEOUT_SECONDS", "300"))
        strict_mode = os.environ.get("AINRF_STRICT_MODE", "false").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        return cls(
            skills_root=skills_root,
            enabled_skills=enabled_skills,
            step_timeout_seconds=step_timeout_seconds,
            strict_mode=strict_mode,
        )


def _skill_for_step(step_kind: str) -> str | None:
    return _STEP_SKILL_MAPPING.get(step_kind)


def _skill_payload_for_step(
    step: AtomicTaskSpec,
    context: dict[str, object],
) -> dict[str, object] | None:
    return build_step_skill_payload(step, context)


def _extract_json_object(candidate: str) -> dict[str, object] | None:
    text = candidate.strip()
    if not text:
        return None
    candidates = [text]
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    candidates.extend(fenced)
    for item in candidates:
        try:
            parsed = json.loads(item)
        except Exception:
            continue
        if isinstance(parsed, dict):
            return parsed
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        parsed = json.loads(text[start : end + 1])
    except Exception:
        return None
    if isinstance(parsed, dict):
        return parsed
    return None


def _normalize_skill_step_updates(
    result: object,
    request: dict[str, object],
) -> dict[str, object] | None:
    skill = request.get("skill")
    if not isinstance(skill, dict):
        return None
    skill_mapping = cast(dict[str, object], skill)
    output_key = skill_mapping.get("output_key")
    if not isinstance(output_key, str) or not output_key:
        return None
    if isinstance(result, dict):
        result_mapping = cast(dict[str, object], result)
        if output_key in result_mapping:
            return result_mapping
        for field_name in ("message", "content", "text"):
            field = result_mapping.get(field_name)
            if isinstance(field, str):
                parsed = _extract_json_object(field)
                if parsed is not None:
                    if output_key in parsed:
                        return parsed
                    return {output_key: parsed}
        return {output_key: result_mapping}
    if isinstance(result, str):
        parsed = _extract_json_object(result)
        if parsed is not None:
            if output_key in parsed:
                return parsed
            return {output_key: parsed}
        if result.strip():
            return {output_key: {"text": result.strip()}}
        return None
    if isinstance(result, list):
        return {output_key: cast(list[object], result)}
    if isinstance(result, int | float | bool):
        return {output_key: result}
    return None


def _normalize_skill_execution_result(
    result: object,
    request: dict[str, object],
) -> dict[str, object] | None:
    step_obj = request.get("step")
    step = cast(dict[str, object], step_obj) if isinstance(step_obj, dict) else {}
    step_kind = step.get("kind") if isinstance(step.get("kind"), str) else "unknown"
    step_updates = _normalize_skill_step_updates(result, request)
    if step_updates is None:
        return None
    return {
        "status": "succeeded",
        "summary": f"Executed {step_kind} via skill profile",
        "messages": [f"Executed {step_kind} via skill profile"],
        "artifacts": [],
        "resource_usage": {"gpu_hours": 0.0, "api_cost_usd": 0.0, "wall_clock_hours": 0.0},
        "step_updates": step_updates,
        "error": None,
    }


_REMOTE_RUNNER_SOURCE = """\
from __future__ import annotations

import json
import asyncio
import inspect
import re
import sys
import time
from pathlib import Path


def _fallback_response(request: dict[str, object]) -> dict[str, object]:
    action = request.get("action")
    if action == "plan_reproduction":
        context = request.get("context")
        paper_card = context.get("paper_card") if isinstance(context, dict) else {}
        artifact_id = paper_card.get("artifact_id") if isinstance(paper_card, dict) else "unknown"
        task_config = context.get("task_config") if isinstance(context, dict) else {}
        task_mode = context.get("task_mode") if isinstance(context, dict) else "deep_reproduction"
        mode_one = task_config.get("config", {}).get("mode_1", {}) if isinstance(task_config, dict) else {}
        mode_two = task_config.get("config", {}).get("mode_2", {}) if isinstance(task_config, dict) else {}
        expected_metrics = mode_two.get("expected_metrics") if isinstance(mode_two, dict) else None
        if not isinstance(expected_metrics, dict):
            expected_metrics = {"accuracy": 0.9}
        if task_mode in {"research_discovery", "literature_exploration"}:
            focus_directions = (
                mode_one.get("focus_directions") if isinstance(mode_one, dict) else []
            )
            if not isinstance(focus_directions, list):
                focus_directions = []
            return {
                "summary": "Fallback P9 discovery plan generated without claude_code_sdk runtime.",
                "milestones": [
                    "clarify research goal",
                    "expand and rank references",
                    "update discovery graph",
                    "evaluate opportunities",
                    "check termination and report",
                ],
                "estimated_steps": 10,
                "strategy": "research-discovery",
                "target_paper_id": artifact_id,
                "success_criteria": [
                    "Produce exploration graph with visited and queued papers",
                    "Generate candidate claims and idea directions",
                    "Emit discovery report with termination reason",
                ],
                "steps": [
                    {
                        "step_id": "step-1",
                        "kind": "clarify_research_goal",
                        "title": "Clarify research goal",
                        "payload": {
                            "domain_context": mode_one.get("domain_context", ""),
                            "focus_directions": focus_directions,
                        },
                    },
                    {
                        "step_id": "step-2",
                        "kind": "extract_references",
                        "title": "Extract candidate references",
                        "payload": {"max_candidates": 5},
                    },
                    {
                        "step_id": "step-3",
                        "kind": "prioritize_references",
                        "title": "Rank references",
                        "payload": {"top_k": 2},
                    },
                    {
                        "step_id": "step-4",
                        "kind": "explore_paper",
                        "title": "Explore top paper",
                        "payload": {"paper_id": "pc-ref-001", "depth": 1},
                    },
                    {
                        "step_id": "step-5",
                        "kind": "update_knowledge_graph",
                        "title": "Update knowledge graph",
                        "payload": {"cluster": "core-methods"},
                    },
                    {
                        "step_id": "step-6",
                        "kind": "summarize_method_cluster",
                        "title": "Summarize method cluster",
                        "payload": {"cluster": "core-methods"},
                    },
                    {
                        "step_id": "step-7",
                        "kind": "evaluate_user_idea",
                        "title": "Evaluate user idea",
                        "payload": {"idea": "parameter-efficient adaptation"},
                    },
                    {
                        "step_id": "step-8",
                        "kind": "propose_idea_directions",
                        "title": "Propose idea directions",
                        "payload": {},
                    },
                    {
                        "step_id": "step-9",
                        "kind": "check_termination",
                        "title": "Check discovery termination",
                        "payload": {"max_no_claim_rounds": 3},
                    },
                    {
                        "step_id": "step-10",
                        "kind": "generate_discovery_report",
                        "title": "Generate discovery report",
                        "payload": {"output_path": "reports/discovery/discovery-report.md"},
                    },
                ],
            }
        return {
            "summary": "Fallback P8 plan generated without claude_code_sdk runtime.",
            "milestones": [
                "analyze method",
                "plan implementation",
                "implement modules",
                "run baseline",
                "diagnose deviations",
                "run full experiment",
                "compare tables",
                "generate quality assessment",
            ],
            "estimated_steps": 8,
            "strategy": "implement-from-paper",
            "target_paper_id": artifact_id,
            "success_criteria": [
                "Produce runnable implementation",
                "Complete baseline and full reproduction",
                "Output quality assessment with evidence",
            ],
            "steps": [
                {
                    "step_id": "step-1",
                    "kind": "analyze_method",
                    "title": "Analyze paper method",
                    "payload": {"focus": "method_summary"},
                },
                {
                    "step_id": "step-2",
                    "kind": "plan_implementation",
                    "title": "Plan implementation",
                    "payload": {"scope": "core-only"},
                },
                {
                    "step_id": "step-3",
                    "kind": "implement_module",
                    "title": "Implement core module",
                    "payload": {"module": "core"},
                },
                {
                    "step_id": "step-4",
                    "kind": "run_baseline",
                    "title": "Run baseline",
                    "payload": {
                        "expected_metrics": expected_metrics,
                        "deviation_threshold_percent": 5.0,
                    },
                },
                {
                    "step_id": "step-5",
                    "kind": "diagnose_deviation",
                    "title": "Diagnose deviation",
                    "payload": {"max_loops": 3},
                },
                {
                    "step_id": "step-6",
                    "kind": "run_full_experiment",
                    "title": "Run full experiment",
                    "payload": {
                        "expected_metrics": expected_metrics,
                        "deviation_threshold_percent": 5.0,
                    },
                },
                {
                    "step_id": "step-7",
                    "kind": "compare_tables",
                    "title": "Compare target tables",
                    "payload": {"target_tables": mode_two.get("target_tables", []) if isinstance(mode_two, dict) else []},
                },
                {
                    "step_id": "step-8",
                    "kind": "generate_quality_assessment",
                    "title": "Generate quality assessment",
                    "payload": {"dimensions": ["gold_nugget", "reproducibility", "scientific_rigor"]},
                },
            ],
        }
    step = request.get("step")
    step_kind = step.get("kind") if isinstance(step, dict) else "unknown"
    step_title = step.get("title") if isinstance(step, dict) else "unknown"
    if step_kind == "run_baseline":
        step_updates = {"metrics": {"accuracy": 0.86, "f1": 0.83}}
    elif step_kind == "run_full_experiment":
        step_updates = {"metrics": {"accuracy": 0.9, "f1": 0.88}}
    elif step_kind == "diagnose_deviation":
        step_updates = {
            "diagnosis": {
                "summary": "Deviation likely caused by preprocessing mismatch.",
                "actions": ["align tokenization", "retune learning rate"],
            }
        }
    elif step_kind == "compare_tables":
        step_updates = {
            "table_comparisons": [
                {
                    "table_id": "table-1",
                    "metric": "accuracy",
                    "paper_value": 0.91,
                    "reproduced_value": 0.9,
                    "deviation_percent": 1.0989,
                }
            ]
        }
    elif step_kind == "generate_quality_assessment":
        step_updates = {
            "quality_assessment": {
                "gold_nugget": 4.2,
                "reproducibility": 4.0,
                "scientific_rigor": 3.8,
            }
        }
    elif step_kind == "clarify_research_goal":
        step_updates = {
            "problem_profile": {
                "research_goal": "Map high-leverage adaptation directions",
                "focus_directions": ["efficient finetuning", "evaluation robustness"],
                "ignore_directions": ["infrastructure-only"],
            }
        }
    elif step_kind == "extract_references":
        step_updates = {
            "reference_candidates": [
                {
                    "paper_id": "pc-ref-001",
                    "title": "Adapter Tuning",
                    "score": 0.86,
                    "novelty": 0.71,
                    "method_diff": 0.64,
                    "citation_count": 124,
                },
                {
                    "paper_id": "pc-ref-002",
                    "title": "LoRA",
                    "score": 0.82,
                    "novelty": 0.66,
                    "method_diff": 0.59,
                    "citation_count": 98,
                },
                {
                    "paper_id": "pc-ref-003",
                    "title": "Prefix Tuning",
                    "score": 0.77,
                    "novelty": 0.6,
                    "method_diff": 0.55,
                    "citation_count": 73,
                },
            ]
        }
    elif step_kind == "prioritize_references":
        step_updates = {
            "ranked_references": [
                {
                    "paper_id": "pc-ref-001",
                    "rank": 1,
                    "score": 0.86,
                    "novelty": 0.72,
                    "method_diff": 0.64,
                    "citation_count": 124,
                },
                {
                    "paper_id": "pc-ref-002",
                    "rank": 2,
                    "score": 0.82,
                    "novelty": 0.65,
                    "method_diff": 0.59,
                    "citation_count": 98,
                },
            ]
        }
    elif step_kind == "explore_paper":
        step_updates = {
            "exploration": {
                "paper_id": "pc-ref-001",
                "visited_paper_ids": ["pc-ref-001"],
                "queued_paper_ids": ["pc-ref-002", "pc-ref-003"],
                "current_depth": 1,
                "new_claims": [
                    {
                        "statement": "Low-rank adaptation preserves baseline quality with lower cost.",
                        "confidence": 0.74,
                    }
                ],
            }
        }
    elif step_kind == "update_knowledge_graph":
        step_updates = {
            "knowledge_graph_update": {
                "claims": [
                    {
                        "statement": "Combining adapter families improves cross-domain transfer.",
                        "confidence": 0.68,
                    }
                ]
            }
        }
    elif step_kind == "summarize_method_cluster":
        step_updates = {
            "method_cluster": {
                "cluster": "core-methods",
                "summary": "Most methods trade tiny quality loss for major compute savings.",
            }
        }
    elif step_kind == "evaluate_user_idea":
        step_updates = {
            "idea_evaluation": {
                "feasibility": "medium",
                "risks": ["dataset mismatch", "evaluation leakage"],
            }
        }
    elif step_kind == "propose_idea_directions":
        step_updates = {
            "idea_candidates": [
                {
                    "title": "Hybrid adapter routing",
                    "rationale": "Combine orthogonal adapter mechanisms based on task families.",
                }
            ]
        }
    elif step_kind == "check_termination":
        step_updates = {
            "termination": {
                "should_terminate": False,
                "reason": "continue_exploration",
                "new_claims_count": 0,
            }
        }
    elif step_kind == "generate_discovery_report":
        step_updates = {
            "report": {
                "path": "reports/discovery/discovery-report.md",
                "summary": "Generated discovery report with idea directions and method map.",
            }
        }
    else:
        step_updates = {}
    return {
        "status": "succeeded",
        "summary": f"Executed {step_kind}",
        "messages": [f"Executed {step_title}"],
        "artifacts": [],
        "resource_usage": {"gpu_hours": 0.0, "api_cost_usd": 0.0, "wall_clock_hours": 0.0},
        "step_updates": step_updates,
        "error": None,
    }


def _unknown_action_response(action: object) -> dict[str, object]:
    return {
        "status": "failed",
        "summary": "Unsupported action",
        "messages": [f"Unsupported action: {action}"],
        "artifacts": [],
        "resource_usage": {"gpu_hours": 0.0, "api_cost_usd": 0.0, "wall_clock_hours": 0.0},
        "step_updates": {},
        "error": f"Unsupported action: {action}",
    }


def _build_skill_prompt(request: dict[str, object]) -> str | None:
    skill = request.get("skill")
    if not isinstance(skill, dict):
        return None
    output_key = skill.get("output_key")
    skill_name = skill.get("skill_name")
    objective = skill.get("objective")
    step_kind = skill.get("step_kind")
    step_title = skill.get("step_title")
    step_payload = skill.get("step_payload") if isinstance(skill.get("step_payload"), dict) else {}
    task_context = skill.get("task_context") if isinstance(skill.get("task_context"), dict) else {}
    guidance = skill.get("guidance") if isinstance(skill.get("guidance"), list) else []
    if not isinstance(output_key, str) or not output_key:
        return None
    guidance_lines = []
    for item in guidance:
        if isinstance(item, str) and item:
            guidance_lines.append(f"- {item}")
    parts = [
        "You are executing an AINRF atomic research step using an internal skill-inspired profile.",
        f"Skill inspiration: {skill_name}" if isinstance(skill_name, str) and skill_name else "Skill inspiration: unspecified",
        f"Objective: {objective}" if isinstance(objective, str) and objective else "Objective: produce the requested structured update.",
        f"Step kind: {step_kind}" if isinstance(step_kind, str) and step_kind else "Step kind: unknown",
        f"Step title: {step_title}" if isinstance(step_title, str) and step_title else "Step title: unknown",
        "Step payload:",
        json.dumps(step_payload, ensure_ascii=False, sort_keys=True),
        "Task context:",
        json.dumps(task_context, ensure_ascii=False, sort_keys=True),
        "Guidance:",
        "\n".join(guidance_lines) if guidance_lines else "- Return only what is necessary to satisfy the step.",
        "STRICT: return only a JSON object with this exact shape and no surrounding prose:",
        json.dumps({output_key: {"summary": "fill with structured data"}}, ensure_ascii=False),
    ]
    return "\n\n".join(parts)


def _extract_json_object(candidate: str) -> dict[str, object] | None:
    text = candidate.strip()
    if not text:
        return None
    candidates = [text]
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    candidates.extend(fenced)
    for item in candidates:
        try:
            parsed = json.loads(item)
        except Exception:
            continue
        if isinstance(parsed, dict):
            return parsed
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        parsed = json.loads(text[start : end + 1])
    except Exception:
        return None
    if isinstance(parsed, dict):
        return parsed
    return None


def _normalize_skill_step_updates(result: object, request: dict[str, object]) -> dict[str, object] | None:
    skill = request.get("skill")
    if not isinstance(skill, dict):
        return None
    output_key = skill.get("output_key")
    if not isinstance(output_key, str) or not output_key:
        return None
    if isinstance(result, dict):
        if output_key in result:
            return result
        message_obj = result.get("message")
        if isinstance(message_obj, str):
            parsed = _extract_json_object(message_obj)
            if parsed is not None:
                if output_key in parsed:
                    return parsed
                return {output_key: parsed}
        content_obj = result.get("content")
        if isinstance(content_obj, str):
            parsed = _extract_json_object(content_obj)
            if parsed is not None:
                if output_key in parsed:
                    return parsed
                return {output_key: parsed}
        text_obj = result.get("text")
        if isinstance(text_obj, str):
            parsed = _extract_json_object(text_obj)
            if parsed is not None:
                if output_key in parsed:
                    return parsed
                return {output_key: parsed}
        return None
    if isinstance(result, str):
        parsed = _extract_json_object(result)
        if parsed is not None:
            if output_key in parsed:
                return parsed
            return {output_key: parsed}
    return None


def _normalize_skill_execution_result(result: object, request: dict[str, object]) -> dict[str, object] | None:
    step = request.get("step") if isinstance(request.get("step"), dict) else {}
    step_kind = step.get("kind") if isinstance(step, dict) else "unknown"
    step_updates = _normalize_skill_step_updates(result, request)
    if step_updates is None:
        return None
    return {
        "status": "succeeded",
        "summary": f"Executed {step_kind} via skill profile",
        "messages": [f"Executed {step_kind} via skill profile"],
        "artifacts": [],
        "resource_usage": {"gpu_hours": 0.0, "api_cost_usd": 0.0, "wall_clock_hours": 0.0},
        "step_updates": step_updates,
        "error": None,
    }


def _invoke_candidate(target: object, method_name: str, kwargs: dict[str, object]) -> object | None:
    method = getattr(target, method_name, None)
    if not callable(method):
        return None
    result = method(**kwargs)
    if inspect.isawaitable(result):
        return asyncio.run(result)
    return result


def _normalize_plan_result(result: object) -> dict[str, object] | None:
    if not isinstance(result, dict):
        return None
    required = {
        "summary",
        "milestones",
        "estimated_steps",
        "strategy",
        "target_paper_id",
        "success_criteria",
        "steps",
    }
    if not required.issubset(result.keys()):
        return None
    return result


def _normalize_execution_result(result: object) -> dict[str, object] | None:
    if not isinstance(result, dict):
        return None
    required = {
        "status",
        "summary",
        "messages",
        "artifacts",
        "resource_usage",
        "step_updates",
    }
    if not required.issubset(result.keys()):
        return None
    if "error" not in result:
        result["error"] = None
    return result


_MODE1_PRIORITY_STEP_KINDS = {
    "clarify_research_goal",
    "prioritize_references",
    "explore_paper",
    "check_termination",
}


def _invoke_with_sdk(request: dict[str, object]) -> dict[str, object] | None:
    try:
        import claude_code_sdk
    except Exception:
        return None

    action = request.get("action")
    if action == "plan_reproduction":
        kwargs = {
            "prompt": request.get("prompt", ""),
            "context": request.get("context", {}),
        }
        candidates = (
            (claude_code_sdk, "plan_reproduction"),
            (claude_code_sdk, "plan"),
            (claude_code_sdk, "create_plan"),
        )
        client = getattr(claude_code_sdk, "Client", None)
        if callable(client):
            client_instance = client()
            candidates += (
                (client_instance, "plan_reproduction"),
                (client_instance, "plan"),
                (client_instance, "create_plan"),
            )
        for target, method_name in candidates:
            try:
                result = _invoke_candidate(target, method_name, kwargs)
                normalized = _normalize_plan_result(result)
                if normalized is not None:
                    return normalized
            except Exception:
                continue
        return None

    if action == "execute_step":
        step = request.get("step")
        step_kind = step.get("kind") if isinstance(step, dict) else None
        mode1_priority = isinstance(step_kind, str) and step_kind in _MODE1_PRIORITY_STEP_KINDS
        skill_prompt = _build_skill_prompt(request)
        kwargs_variants = []
        if skill_prompt is not None:
            kwargs_variants.append(
                {
                    "step": request.get("step", {}),
                    "context": request.get("context", {}),
                    "prompt": skill_prompt,
                }
            )
        kwargs_variants.append(
            {
                "step": request.get("step", {}),
                "context": request.get("context", {}),
            }
        )
        candidates = (
            (claude_code_sdk, "execute_step"),
            (claude_code_sdk, "execute"),
            (claude_code_sdk, "run_step"),
        )
        client = getattr(claude_code_sdk, "Client", None)
        if callable(client):
            client_instance = client()
            candidates += (
                (client_instance, "execute_step"),
                (client_instance, "execute"),
                (client_instance, "run_step"),
            )
        for kwargs in kwargs_variants:
            for target, method_name in candidates:
                try:
                    result = _invoke_candidate(target, method_name, kwargs)
                    normalized = _normalize_execution_result(result)
                    if normalized is None:
                        normalized = _normalize_skill_execution_result(result, request)
                    if normalized is not None:
                        if mode1_priority:
                            normalized["sdk_path"] = "mode1_priority"
                        if skill_prompt is not None:
                            normalized["sdk_path"] = str(normalized.get("sdk_path", "sdk")) + "+skill_profile"
                        return normalized
                except Exception:
                    continue
        return None

    return _unknown_action_response(action)


def main() -> int:
    request_path = Path(sys.argv[1])
    result_path = Path(sys.argv[2])
    request = json.loads(request_path.read_text(encoding="utf-8"))
    result = _invoke_with_sdk(request)
    if result is None:
        result = _fallback_response(request)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""


class ClaudeCodeAdapter(AgentAdapter):
    def __init__(self, executor_factory: type[SSHExecutor] | type[Any] = SSHExecutor) -> None:
        self._executor_factory = executor_factory

    async def bootstrap(self, container: ContainerConfig) -> None:
        async with self._executor_factory(container) as executor:
            await executor.ensure_claude_code()
            try:
                await executor.run_command("python3 -c 'import claude_code_sdk'", timeout=30)
            except Exception:
                await executor.run_command(
                    "python3 -m pip install --user claude-code-sdk",
                    timeout=300,
                )
            await self._ensure_remote_runner(executor)

    async def health_check(self, container: ContainerConfig) -> bool:
        async with self._executor_factory(container) as executor:
            try:
                await executor.run_command("python3 -c 'import claude_code_sdk'", timeout=30)
            except Exception:
                return False
        return True

    async def plan_reproduction(
        self,
        *,
        container: ContainerConfig,
        prompt: str,
        context: dict[str, object],
    ) -> TaskPlanResult:
        payload: dict[str, object] = {
            "action": "plan_reproduction",
            "prompt": prompt,
            "context": context,
        }
        response = await self._invoke(container=container, payload=payload)
        steps_payload = self._mapping_list_payload(response, "steps")
        steps = [
            AtomicTaskSpec(
                step_id=str(item["step_id"]),
                kind=str(item["kind"]),
                title=str(item["title"]),
                payload=self._mapping_payload(item, "payload"),
            )
            for item in steps_payload
        ]
        return TaskPlanResult(
            summary=str(response["summary"]),
            milestones=[str(item) for item in self._scalar_list_payload(response, "milestones")],
            estimated_steps=int(cast(int | str, response["estimated_steps"])),
            strategy=str(response["strategy"]),
            target_paper_id=str(response["target_paper_id"]),
            success_criteria=[
                str(item) for item in self._scalar_list_payload(response, "success_criteria")
            ],
            steps=steps,
        )

    async def execute_step(
        self,
        *,
        container: ContainerConfig,
        step: AtomicTaskSpec,
        context: dict[str, object],
    ) -> TaskExecutionResult:
        skill_payload = _skill_payload_for_step(step, context)
        payload = {
            "action": "execute_step",
            "step": step.model_dump(mode="json"),
            "context": context,
            "skill": skill_payload,
        }
        response = await self._invoke(container=container, payload=payload)
        artifacts_payload = self._mapping_list_payload(response, "artifacts")
        return TaskExecutionResult(
            status=str(response["status"]),
            summary=str(response["summary"]),
            messages=[str(item) for item in self._scalar_list_payload(response, "messages")],
            artifacts=[
                StepArtifactRef(
                    artifact_type=str(item["artifact_type"]),
                    artifact_id=str(item["artifact_id"]),
                    path=str(item["path"]),
                )
                for item in artifacts_payload
            ],
            resource_usage=self._float_mapping_payload(response, "resource_usage"),
            step_updates=self._mapping_payload(response, "step_updates"),
            error=str(response["error"]) if response.get("error") is not None else None,
        )

    async def _invoke(
        self,
        *,
        container: ContainerConfig,
        payload: dict[str, object],
    ) -> dict[str, object]:
        try:
            async with self._executor_factory(container) as executor:
                await self._ensure_remote_runner(executor)
                with TemporaryDirectory() as temp_dir_name:
                    temp_dir = Path(temp_dir_name)
                    request_path = temp_dir / "request.json"
                    result_path = temp_dir / "result.json"
                    request_path.write_text(json.dumps(payload), encoding="utf-8")
                    remote_request = f"{container.project_dir}/.ainrf-runtime/request.json"
                    remote_result = f"{container.project_dir}/.ainrf-runtime/result.json"
                    quoted_runtime_dir = shlex.quote(f"{container.project_dir}/.ainrf-runtime")
                    await executor.run_command(f"mkdir -p {quoted_runtime_dir}", timeout=30)
                    await executor.upload(request_path, remote_request)
                    command = (
                        f"cd {shlex.quote(container.project_dir)} && "
                        f"python3 {shlex.quote(_REMOTE_RUNNER_PATH)} "
                        f"{shlex.quote(remote_request)} {shlex.quote(remote_result)}"
                    )
                    await executor.run_command(
                        command,
                        cwd=container.project_dir,
                        timeout=container.command_timeout,
                    )
                    await executor.download(remote_result, result_path)
                    response = json.loads(result_path.read_text(encoding="utf-8"))
        except (
            CommandTimeoutError,
            TransferError,
            SSHConnectionError,
            json.JSONDecodeError,
        ) as exc:
            raise AgentExecutionError(f"Agent invocation failed: {exc}", retryable=True) from exc
        except Exception as exc:
            raise AgentExecutionError(f"Agent invocation failed: {exc}", retryable=False) from exc
        if not isinstance(response, dict):
            raise AgentExecutionError("Agent response must be a JSON object", retryable=False)
        return cast(dict[str, object], response)

    async def _ensure_remote_runner(self, executor: SSHExecutor) -> None:
        container = executor.container
        with TemporaryDirectory() as temp_dir_name:
            local_path = Path(temp_dir_name) / "claude_code_runner.py"
            local_path.write_text(_REMOTE_RUNNER_SOURCE, encoding="utf-8")
            remote_dir = f"{container.project_dir}/.ainrf-runtime"
            remote_path = f"{container.project_dir}/{_REMOTE_RUNNER_PATH}"
            await executor.run_command(f"mkdir -p {shlex.quote(remote_dir)}", timeout=30)
            await executor.upload(local_path, remote_path)

    def _scalar_list_payload(self, payload: dict[str, object], key: str) -> list[object]:
        value = payload.get(key, [])
        if not isinstance(value, list):
            raise AgentExecutionError(f"Agent payload field {key} must be a list", retryable=False)
        return cast(list[object], value)

    def _mapping_list_payload(
        self, payload: dict[str, object], key: str
    ) -> list[dict[str, object]]:
        value = payload.get(key, [])
        if not isinstance(value, list):
            raise AgentExecutionError(f"Agent payload field {key} must be a list", retryable=False)
        return [self._mapping_item(item) for item in value]

    def _mapping_payload(self, payload: dict[str, object], key: str) -> dict[str, object]:
        value = payload.get(key, {})
        if not isinstance(value, dict):
            raise AgentExecutionError(
                f"Agent payload field {key} must be an object", retryable=False
            )
        return cast(dict[str, object], value)

    def _float_mapping_payload(
        self, payload: dict[str, object], key: str
    ) -> dict[str, float | None]:
        raw_mapping = self._mapping_payload(payload, key)
        normalized: dict[str, float | None] = {}
        for item_key, item_value in raw_mapping.items():
            if item_value is None:
                normalized[item_key] = None
            else:
                normalized[item_key] = float(cast(float | int, item_value))
        return normalized

    def _mapping_item(self, item: object) -> dict[str, object]:
        if not isinstance(item, dict):
            raise AgentExecutionError("Agent list item must be an object", retryable=False)
        return cast(dict[str, object], item)
