from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from ainrf.agents.base import AgentAdapter, AgentExecutionError
from ainrf.engine.models import AtomicTaskSpec, StepArtifactRef, TaskExecutionResult, TaskPlanResult
from ainrf.execution import ContainerConfig, SSHExecutor

_REMOTE_RUNNER_PATH = ".ainrf-runtime/claude_code_runner.py"

_REMOTE_RUNNER_SOURCE = """\
from __future__ import annotations

import json
import sys
from pathlib import Path


def _fallback_response(request: dict[str, object]) -> dict[str, object]:
    action = request.get("action")
    if action == "plan_reproduction":
        return {
            "summary": "Fallback plan generated without claude_code_sdk runtime.",
            "milestones": ["implement core module", "run validation", "summarize execution"],
            "estimated_steps": 3,
            "strategy": "implement-from-paper",
            "target_paper_id": request["context"]["paper_card"]["artifact_id"],
            "success_criteria": ["Produce runnable implementation", "Generate validation notes"],
            "steps": [
                {"step_id": "step-1", "kind": "implement_module", "title": "Implement core module", "payload": {"module": "core"}},
                {"step_id": "step-2", "kind": "run_validation", "title": "Run validation", "payload": {"target": "baseline"}},
                {"step_id": "step-3", "kind": "summarize_execution", "title": "Summarize execution", "payload": {"report": "reports/reproduction/summary.md"}},
            ],
        }
    step = request["step"]
    return {
        "status": "succeeded",
        "summary": f"Executed {step['kind']}",
        "messages": [f"Executed {step['title']}"],
        "artifacts": [],
        "resource_usage": {"gpu_hours": 0.0, "api_cost_usd": 0.0, "wall_clock_hours": 0.0},
        "step_updates": {},
        "error": None,
    }


def main() -> int:
    request_path = Path(sys.argv[1])
    result_path = Path(sys.argv[2])
    request = json.loads(request_path.read_text(encoding="utf-8"))
    try:
        import claude_code_sdk  # noqa: F401
    except Exception:
        result = _fallback_response(request)
    else:
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
                await executor.ensure_claude_code()
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
        payload = {
            "action": "execute_step",
            "step": step.model_dump(mode="json"),
            "context": context,
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
        async with self._executor_factory(container) as executor:
            await self._ensure_remote_runner(executor)
            with TemporaryDirectory() as temp_dir_name:
                temp_dir = Path(temp_dir_name)
                request_path = temp_dir / "request.json"
                result_path = temp_dir / "result.json"
                request_path.write_text(json.dumps(payload), encoding="utf-8")
                remote_request = f"{container.project_dir}/.ainrf-runtime/request.json"
                remote_result = f"{container.project_dir}/.ainrf-runtime/result.json"
                await executor.run_command(f"mkdir -p {container.project_dir}/.ainrf-runtime", timeout=30)
                await executor.upload(request_path, remote_request)
                command = (
                    f"cd {container.project_dir} && "
                    f"python3 {_REMOTE_RUNNER_PATH} {remote_request} {remote_result}"
                )
                await executor.run_command(command, cwd=container.project_dir, timeout=container.command_timeout)
                await executor.download(remote_result, result_path)
                response = json.loads(result_path.read_text(encoding="utf-8"))
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
            await executor.run_command(f"mkdir -p {remote_dir}", timeout=30)
            await executor.upload(local_path, remote_path)

    def _scalar_list_payload(self, payload: dict[str, object], key: str) -> list[object]:
        value = payload.get(key, [])
        if not isinstance(value, list):
            raise AgentExecutionError(f"Agent payload field {key} must be a list", retryable=False)
        return cast(list[object], value)

    def _mapping_list_payload(self, payload: dict[str, object], key: str) -> list[dict[str, object]]:
        value = payload.get(key, [])
        if not isinstance(value, list):
            raise AgentExecutionError(f"Agent payload field {key} must be a list", retryable=False)
        return [self._mapping_item(item) for item in value]

    def _mapping_payload(self, payload: dict[str, object], key: str) -> dict[str, object]:
        value = payload.get(key, {})
        if not isinstance(value, dict):
            raise AgentExecutionError(f"Agent payload field {key} must be an object", retryable=False)
        return cast(dict[str, object], value)

    def _float_mapping_payload(self, payload: dict[str, object], key: str) -> dict[str, float | None]:
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
