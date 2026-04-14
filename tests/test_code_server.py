from __future__ import annotations

import errno
import subprocess
from pathlib import Path

import pytest

from ainrf.code_server import (
    CodeServerLifecycleStatus,
    CodeServerSupervisor,
    build_code_server_command,
)


def test_build_code_server_command_uses_workspace_and_loopback(tmp_path: Path) -> None:
    command = build_code_server_command(
        host="127.0.0.1",
        port=18080,
        workspace_dir=tmp_path,
    )

    assert command == [
        "code-server",
        "--bind-addr",
        "127.0.0.1:18080",
        "--auth",
        "none",
        str(tmp_path),
    ]


def test_supervisor_without_workspace_is_unavailable(tmp_path: Path) -> None:
    supervisor = CodeServerSupervisor(
        host="127.0.0.1",
        port=18080,
        workspace_dir=None,
        state_root=tmp_path,
    )

    supervisor.start()

    assert supervisor.status().status is CodeServerLifecycleStatus.UNAVAILABLE
    assert supervisor.status().detail == "workspace directory is not configured"


def test_supervisor_missing_workspace_path_is_unavailable(tmp_path: Path) -> None:
    supervisor = CodeServerSupervisor(
        host="127.0.0.1",
        port=18080,
        workspace_dir=tmp_path / "missing",
        state_root=tmp_path,
    )

    supervisor.start()

    assert supervisor.status().status is CodeServerLifecycleStatus.UNAVAILABLE
    assert "does not exist" in (supervisor.status().detail or "")


def test_supervisor_file_workspace_path_is_unavailable(tmp_path: Path) -> None:
    workspace_file = tmp_path / "workspace.txt"
    workspace_file.write_text("not a directory", encoding="utf-8")

    supervisor = CodeServerSupervisor(
        host="127.0.0.1",
        port=18080,
        workspace_dir=workspace_file,
        state_root=tmp_path,
    )

    supervisor.start()

    assert supervisor.status().status is CodeServerLifecycleStatus.UNAVAILABLE
    assert "is not a directory" in (supervisor.status().detail or "")


class FakeProcess:
    def __init__(self, pid: int, returncode: int | None = None) -> None:
        self.pid = pid
        self.returncode = returncode
        self.actions: list[str] = []
        self.wait_timeouts: list[float] = []
        self.wait_side_effects: list[BaseException] = []

    def poll(self) -> int | None:
        return self.returncode

    def terminate(self) -> None:
        self.actions.append("terminate")

    def kill(self) -> None:
        self.actions.append("kill")

    def wait(self, timeout: float) -> int:
        self.wait_timeouts.append(timeout)
        if self.wait_side_effects:
            raise self.wait_side_effects.pop(0)
        if self.returncode is None:
            self.returncode = 0
        return self.returncode



def test_supervisor_marks_ready_after_successful_probe(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("ainrf.code_server.subprocess.Popen", lambda *args, **kwargs: FakeProcess(4321))
    monkeypatch.setattr("ainrf.code_server._wait_until_ready", lambda host, port: True)

    supervisor = CodeServerSupervisor(
        host="127.0.0.1",
        port=18080,
        workspace_dir=tmp_path,
        state_root=tmp_path,
    )
    supervisor.start()

    assert supervisor.status().status is CodeServerLifecycleStatus.READY
    assert supervisor.status().pid == 4321



def test_supervisor_degrades_when_spawn_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_spawn_error(*args, **kwargs):
        raise OSError(errno.ENOENT, "code-server not found")

    monkeypatch.setattr("ainrf.code_server.subprocess.Popen", raise_spawn_error)

    supervisor = CodeServerSupervisor(
        host="127.0.0.1",
        port=18080,
        workspace_dir=tmp_path,
        state_root=tmp_path,
    )

    supervisor.start()

    assert supervisor.status().status is CodeServerLifecycleStatus.UNAVAILABLE
    assert supervisor.status().pid is None
    assert "failed to start code-server" in (supervisor.status().detail or "")
    assert "code-server not found" in (supervisor.status().detail or "")



def test_supervisor_degrades_when_probe_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    process = FakeProcess(4321)
    monkeypatch.setattr("ainrf.code_server.subprocess.Popen", lambda *args, **kwargs: process)
    monkeypatch.setattr("ainrf.code_server._wait_until_ready", lambda host, port: False)

    supervisor = CodeServerSupervisor(
        host="127.0.0.1",
        port=18080,
        workspace_dir=tmp_path,
        state_root=tmp_path,
    )
    supervisor.start()

    assert supervisor.status().status is CodeServerLifecycleStatus.UNAVAILABLE
    assert process.actions == ["terminate"]
    assert process.wait_timeouts == [5.0]



def test_supervisor_stop_terminates_and_reaps_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    process = FakeProcess(4321)
    monkeypatch.setattr("ainrf.code_server.subprocess.Popen", lambda *args, **kwargs: process)
    monkeypatch.setattr("ainrf.code_server._wait_until_ready", lambda host, port: True)

    supervisor = CodeServerSupervisor(
        host="127.0.0.1",
        port=18080,
        workspace_dir=tmp_path,
        state_root=tmp_path,
    )
    supervisor.start()
    supervisor.stop()

    assert process.actions == ["terminate"]
    assert process.wait_timeouts == [5.0]
    assert supervisor.status().status is CodeServerLifecycleStatus.UNAVAILABLE
    assert supervisor.status().detail == "code-server stopped"



def test_supervisor_stop_kills_after_terminate_timeout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    process = FakeProcess(4321)
    process.wait_side_effects = [subprocess.TimeoutExpired(cmd="code-server", timeout=5.0)]
    monkeypatch.setattr("ainrf.code_server.subprocess.Popen", lambda *args, **kwargs: process)
    monkeypatch.setattr("ainrf.code_server._wait_until_ready", lambda host, port: True)

    supervisor = CodeServerSupervisor(
        host="127.0.0.1",
        port=18080,
        workspace_dir=tmp_path,
        state_root=tmp_path,
    )
    supervisor.start()
    supervisor.stop()

    assert process.actions == ["terminate", "kill"]
    assert process.wait_timeouts == [5.0, 5.0]



def test_supervisor_reuses_existing_running_process_on_repeated_start(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    popen_calls = 0

    def fake_popen(*args, **kwargs) -> FakeProcess:
        nonlocal popen_calls
        popen_calls += 1
        return FakeProcess(4321)

    monkeypatch.setattr("ainrf.code_server.subprocess.Popen", fake_popen)
    monkeypatch.setattr("ainrf.code_server._wait_until_ready", lambda host, port: True)

    supervisor = CodeServerSupervisor(
        host="127.0.0.1",
        port=18080,
        workspace_dir=tmp_path,
        state_root=tmp_path,
    )

    supervisor.start()
    first_status = supervisor.status()
    supervisor.start()
    second_status = supervisor.status()

    assert popen_calls == 1
    assert first_status.status is CodeServerLifecycleStatus.READY
    assert second_status.status is CodeServerLifecycleStatus.READY
    assert second_status.pid == 4321
