from __future__ import annotations

import asyncio
import json
from pathlib import Path

from ainrf.agents import ClaudeCodeAdapter
from ainrf.engine.models import AtomicTaskSpec
from ainrf.execution import CommandResult, ContainerConfig


class FakeSSHExecutor:
    latest_request: dict[str, object] | None = None
    all_commands: list[str] = []
    all_uploads: list[str] = []

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
    adapter = ClaudeCodeAdapter(executor_factory=FakeSSHExecutor)

    asyncio.run(adapter.bootstrap(_container()))

    assert "python3 -m pip install --user claude-code-sdk" in FakeSSHExecutor.all_commands
    assert any(item.endswith("/.ainrf-runtime/claude_code_runner.py") for item in FakeSSHExecutor.all_uploads)


def test_plan_reproduction_parses_remote_runner_response() -> None:
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
