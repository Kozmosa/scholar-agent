from __future__ import annotations

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


class FakeProcess:
    def __init__(self, pid: int) -> None:
        self.pid = pid


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


def test_supervisor_degrades_when_probe_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("ainrf.code_server.subprocess.Popen", lambda *args, **kwargs: FakeProcess(4321))
    monkeypatch.setattr("ainrf.code_server._wait_until_ready", lambda host, port: False)
    terminated: list[int] = []
    monkeypatch.setattr("ainrf.code_server._terminate_process", lambda pid: terminated.append(pid))

    supervisor = CodeServerSupervisor(
        host="127.0.0.1",
        port=18080,
        workspace_dir=tmp_path,
        state_root=tmp_path,
    )
    supervisor.start()

    assert supervisor.status().status is CodeServerLifecycleStatus.UNAVAILABLE
    assert terminated == [4321]
