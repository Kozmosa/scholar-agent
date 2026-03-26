from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

import pytest

from ainrf.agents import ClaudeCodeAdapter
from ainrf.agents.base import AgentExecutionError
from ainrf.agents.claude_code import _REMOTE_RUNNER_SOURCE
from ainrf.engine.models import AtomicTaskSpec
from ainrf.execution import CommandResult, CommandTimeoutError, ContainerConfig
from ainrf.execution import SSHExecutor


class FakeSSHExecutor:
    latest_request: dict[str, object] | None = None
    all_commands: list[str] = []
    all_uploads: list[str] = []
    ensure_calls: int = 0

    def __init__(self, container: ContainerConfig) -> None:
        self.container = container
        self.commands: list[str] = []
        self.uploads: list[tuple[Path, str]] = []
        self.downloads: list[tuple[str, Path]] = []
        self._first_import = True

    async def __aenter__(self) -> FakeSSHExecutor:
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None

    async def ensure_claude_code(self) -> str:
        FakeSSHExecutor.ensure_calls += 1
        return "2.0.0"

    async def run_command(
        self,
        cmd: str,
        timeout: int | None = None,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
    ) -> CommandResult:
        _ = timeout, cwd, env
        self.commands.append(cmd)
        FakeSSHExecutor.all_commands.append(cmd)
        if cmd == "python3 -c 'import claude_code_sdk'" and self._first_import:
            self._first_import = False
            raise RuntimeError("missing sdk")
        return CommandResult(exit_code=0, stdout="", stderr="")

    async def upload(self, local: str | Path, remote: str) -> None:
        local_path = Path(local)
        self.uploads.append((local_path, remote))
        FakeSSHExecutor.all_uploads.append(remote)
        if local_path.name == "request.json":
            FakeSSHExecutor.latest_request = json.loads(local_path.read_text(encoding="utf-8"))

    async def download(self, remote: str, local: str | Path) -> None:
        self.downloads.append((remote, Path(local)))
        local_path = Path(local)
        request = FakeSSHExecutor.latest_request or {}
        if request.get("action") == "plan_reproduction":
            response = {
                "summary": "Plan",
                "milestones": ["m1"],
                "estimated_steps": 1,
                "strategy": "implement-from-paper",
                "target_paper_id": "pc-001",
                "success_criteria": ["done"],
                "steps": [
                    {
                        "step_id": "s1",
                        "kind": "implement_module",
                        "title": "Implement",
                        "payload": {"module": "core"},
                    }
                ],
            }
        else:
            response = {
                "status": "succeeded",
                "summary": "Executed step",
                "messages": ["ok"],
                "artifacts": [],
                "resource_usage": {"gpu_hours": 1.0},
                "step_updates": {},
                "error": None,
            }
        local_path.write_text(json.dumps(response), encoding="utf-8")


def _container() -> ContainerConfig:
    return ContainerConfig(host="gpu-server-01", user="researcher", project_dir="/workspace/project")


def test_bootstrap_installs_sdk_and_uploads_runner() -> None:
    FakeSSHExecutor.all_commands = []
    FakeSSHExecutor.all_uploads = []
    FakeSSHExecutor.ensure_calls = 0
    adapter = ClaudeCodeAdapter(executor_factory=FakeSSHExecutor)

    asyncio.run(adapter.bootstrap(_container()))

    assert "python3 -m pip install --user claude-code-sdk" in FakeSSHExecutor.all_commands
    assert any(item.endswith("/.ainrf-runtime/claude_code_runner.py") for item in FakeSSHExecutor.all_uploads)


def test_plan_reproduction_parses_remote_runner_response() -> None:
    FakeSSHExecutor.ensure_calls = 0
    adapter = ClaudeCodeAdapter(executor_factory=FakeSSHExecutor)

    result = asyncio.run(
        adapter.plan_reproduction(
            container=_container(),
            prompt="plan",
            context={"paper_card": {"artifact_id": "pc-001"}},
        )
    )

    assert result.summary == "Plan"
    assert result.steps[0].kind == "implement_module"


def test_execute_step_parses_remote_runner_response() -> None:
    FakeSSHExecutor.ensure_calls = 0
    adapter = ClaudeCodeAdapter(executor_factory=FakeSSHExecutor)
    step = AtomicTaskSpec(step_id="s1", kind="run_validation", title="Validate")

    result = asyncio.run(
        adapter.execute_step(
            container=_container(),
            step=step,
            context={"task_id": "t-001"},
        )
    )

    assert result.status == "succeeded"
    assert result.resource_usage["gpu_hours"] == 1.0


def test_remote_runner_uses_sdk_dispatch_instead_of_unconditional_fallback() -> None:
    legacy_snippet = """try:
        import claude_code_sdk  # noqa: F401
    except Exception:
        result = _fallback_response(request)
    else:
        result = _fallback_response(request)"""

    assert "def _invoke_with_sdk" in _REMOTE_RUNNER_SOURCE
    assert legacy_snippet not in _REMOTE_RUNNER_SOURCE


def test_execute_step_propagates_error_field_from_runner_response() -> None:
    class FakeSSHExecutorError(FakeSSHExecutor):
        async def download(self, remote: str, local: str | Path) -> None:
            _ = remote
            response = {
                "status": "failed",
                "summary": "Execution failed",
                "messages": ["Unsupported action"],
                "artifacts": [],
                "resource_usage": {"gpu_hours": 0.0},
                "step_updates": {},
                "error": "Unsupported action: unknown_action",
            }
            Path(local).write_text(json.dumps(response), encoding="utf-8")

    adapter = ClaudeCodeAdapter(executor_factory=FakeSSHExecutorError)
    step = AtomicTaskSpec(step_id="s1", kind="unknown_action", title="Unknown")

    result = asyncio.run(
        adapter.execute_step(
            container=_container(),
            step=step,
            context={"task_id": "t-001"},
        )
    )

    assert result.status == "failed"
    assert result.error == "Unsupported action: unknown_action"


def test_health_check_returns_false_when_sdk_missing() -> None:
    FakeSSHExecutor.ensure_calls = 0
    adapter = ClaudeCodeAdapter(executor_factory=FakeSSHExecutor)

    result = asyncio.run(adapter.health_check(_container()))

    assert result is False
    assert FakeSSHExecutor.ensure_calls == 0


def test_health_check_returns_true_when_sdk_available() -> None:
    class FakeSSHExecutorHealthy(FakeSSHExecutor):
        def __init__(self, container: ContainerConfig) -> None:
            super().__init__(container)
            self._first_import = False

    FakeSSHExecutor.ensure_calls = 0
    adapter = ClaudeCodeAdapter(executor_factory=FakeSSHExecutorHealthy)

    result = asyncio.run(adapter.health_check(_container()))

    assert result is True
    assert FakeSSHExecutor.ensure_calls == 0


def test_execute_step_raises_retryable_error_on_timeout() -> None:
    class FakeSSHExecutorTimeout(FakeSSHExecutor):
        async def run_command(
            self,
            cmd: str,
            timeout: int | None = None,
            cwd: str | None = None,
            env: dict[str, str] | None = None,
        ) -> CommandResult:
            _ = timeout, cwd, env
            if cmd.startswith("cd ") and "claude_code_runner.py" in cmd:
                raise CommandTimeoutError("runner timeout")
            return await super().run_command(cmd, timeout=timeout, cwd=cwd, env=env)

    adapter = ClaudeCodeAdapter(executor_factory=FakeSSHExecutorTimeout)
    step = AtomicTaskSpec(step_id="s1", kind="run_validation", title="Validate")

    try:
        asyncio.run(
            adapter.execute_step(
                container=_container(),
                step=step,
                context={"task_id": "t-001"},
            )
        )
    except AgentExecutionError as exc:
        assert exc.retryable is True
    else:
        raise AssertionError("Expected AgentExecutionError")


def test_execute_step_raises_non_retryable_error_on_non_object_response() -> None:
    class FakeSSHExecutorBadResponse(FakeSSHExecutor):
        async def download(self, remote: str, local: str | Path) -> None:
            _ = remote
            Path(local).write_text(json.dumps(["not", "object"]), encoding="utf-8")

    adapter = ClaudeCodeAdapter(executor_factory=FakeSSHExecutorBadResponse)
    step = AtomicTaskSpec(step_id="s1", kind="run_validation", title="Validate")

    try:
        asyncio.run(
            adapter.execute_step(
                container=_container(),
                step=step,
                context={"task_id": "t-001"},
            )
        )
    except AgentExecutionError as exc:
        assert exc.retryable is False
    else:
        raise AssertionError("Expected AgentExecutionError")


def test_remote_runner_fallback_plan_contains_p8_atomic_steps() -> None:
    for step_kind in [
        "analyze_method",
        "plan_implementation",
        "implement_module",
        "run_baseline",
        "diagnose_deviation",
        "run_full_experiment",
        "compare_tables",
        "generate_quality_assessment",
    ]:
        assert f'"kind": "{step_kind}"' in _REMOTE_RUNNER_SOURCE


def test_remote_runner_fallback_plan_contains_p9_atomic_steps() -> None:
    for step_kind in [
        "clarify_research_goal",
        "extract_references",
        "prioritize_references",
        "explore_paper",
        "update_knowledge_graph",
        "summarize_method_cluster",
        "evaluate_user_idea",
        "propose_idea_directions",
        "check_termination",
        "generate_discovery_report",
    ]:
        assert f'"kind": "{step_kind}"' in _REMOTE_RUNNER_SOURCE


def test_execute_step_parses_compare_tables_step_updates() -> None:
    class FakeSSHExecutorCompare(FakeSSHExecutor):
        async def download(self, remote: str, local: str | Path) -> None:
            _ = remote
            response = {
                "status": "succeeded",
                "summary": "Compared tables",
                "messages": ["done"],
                "artifacts": [],
                "resource_usage": {"gpu_hours": 0.0, "api_cost_usd": 0.0, "wall_clock_hours": 0.0},
                "step_updates": {
                    "table_comparisons": [
                        {
                            "table_id": "table-1",
                            "metric": "accuracy",
                            "paper_value": 0.9,
                            "reproduced_value": 0.88,
                        }
                    ]
                },
                "error": None,
            }
            Path(local).write_text(json.dumps(response), encoding="utf-8")

    adapter = ClaudeCodeAdapter(executor_factory=FakeSSHExecutorCompare)
    step = AtomicTaskSpec(step_id="s-compare", kind="compare_tables", title="Compare tables")

    result = asyncio.run(
        adapter.execute_step(container=_container(), step=step, context={"task_id": "t-001"})
    )

    assert result.status == "succeeded"
    assert "table_comparisons" in result.step_updates


@pytest.mark.skipif(
    not os.environ.get("AINRF_CONTAINER_HOST"),
    reason="AINRF_CONTAINER_HOST not set; real adapter smoke test requires container access",
)
def test_claude_code_adapter_e2e_smoke_with_real_runtime() -> None:
    adapter = ClaudeCodeAdapter(executor_factory=SSHExecutor)
    container = ContainerConfig.from_env()

    asyncio.run(adapter.bootstrap(container))
    assert asyncio.run(adapter.health_check(container)) is True

    plan = asyncio.run(
        adapter.plan_reproduction(
            container=container,
            prompt="Generate a minimal runnable reproduction plan.",
            context={
                "task_id": "smoke-task",
                "task_mode": "deep_reproduction",
                "paper_card": {"artifact_id": "pc-smoke"},
                "task_config": {"config": {"mode_2": {"target_tables": []}}},
            },
        )
    )
    assert plan.steps

    result = asyncio.run(
        adapter.execute_step(
            container=container,
            step=plan.steps[0],
            context={"task_id": "smoke-task", "config": {}},
        )
    )
    assert result.status in {"succeeded", "failed"}
