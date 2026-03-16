from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

import pytest
from typer.testing import CliRunner

from ainrf import __version__
from ainrf.cli import app


runner = CliRunner()


def test_help_shows_commands() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "serve" in result.stdout
    assert "run" in result.stdout
    assert "webui" in result.stdout


def test_version_outputs_package_version() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == f"ainrf {__version__}"


def test_serve_help_lists_expected_flags() -> None:
    result = runner.invoke(app, ["serve", "--help"])

    assert result.exit_code == 0
    assert "--host" in result.stdout
    assert "--port" in result.stdout
    assert "--daemon" in result.stdout
    assert "--state-root" in result.stdout


def test_serve_runs_uvicorn(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    captured: dict[str, object] = {}

    def fake_run_server(host: str, port: int, state_root: Path) -> None:
        captured["host"] = host
        captured["port"] = port
        captured["state_root"] = state_root

    monkeypatch.setattr("ainrf.cli.run_server", fake_run_server)
    monkeypatch.setenv(
        "AINRF_API_KEY_HASHES",
        "2bb80d537b1da3e38bd30361aa855686bde0baef694f41fbabd9831f0a0ff5ff",
    )

    result = runner.invoke(app, ["serve", "--state-root", str(tmp_path)])

    assert result.exit_code == 0
    assert captured == {"host": "127.0.0.1", "port": 8000, "state_root": tmp_path}


def test_serve_daemon_runs_background_process(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state_root = tmp_path / "state"
    captured: dict[str, object] = {}

    def fake_run_server_daemon(
        host: str,
        port: int,
        state_root: Path,
        pid_file: Path,
        log_file: Path,
    ) -> int:
        captured["host"] = host
        captured["port"] = port
        captured["state_root"] = state_root
        captured["pid_file"] = pid_file
        captured["log_file"] = log_file
        return 4321

    monkeypatch.setattr("ainrf.cli.run_server_daemon", fake_run_server_daemon)
    result = runner.invoke(
        app,
        ["serve", "--host", "127.0.0.1", "--port", "8765", "--daemon", "--state-root", str(state_root)],
        env={
            **os.environ,
            "AINRF_API_KEY_HASHES": "2bb80d537b1da3e38bd30361aa855686bde0baef694f41fbabd9831f0a0ff5ff",
        },
    )

    assert result.exit_code == 0
    assert "pid=4321" in result.stdout
    assert captured["host"] == "127.0.0.1"
    assert captured["port"] == 8765
    assert captured["state_root"] == state_root
    assert captured["pid_file"] == state_root / "runtime" / "ainrf-api.pid"
    assert captured["log_file"] == state_root / "runtime" / "ainrf-api.log"


def test_run_stub_runs() -> None:
    class FakeEngine:
        async def run_once(self) -> bool:
            return False

    def fake_build_task_engine(_state_root: Path) -> FakeEngine:
        return FakeEngine()

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr("ainrf.cli.build_task_engine", fake_build_task_engine)
    result = runner.invoke(app, ["run", "--once"])
    monkeypatch.undo()

    assert result.exit_code == 0
    assert "AINRF worker found no runnable tasks." in result.stdout


def test_run_once_processes_task(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeEngine:
        async def run_once(self) -> bool:
            captured["ran"] = True
            return True

    def fake_build_task_engine(state_root: Path) -> FakeEngine:
        captured["state_root"] = state_root
        return FakeEngine()

    monkeypatch.setattr("ainrf.cli.build_task_engine", fake_build_task_engine)
    result = runner.invoke(app, ["run", "--once", "--state-root", str(tmp_path)])

    assert result.exit_code == 0
    assert captured["state_root"] == tmp_path
    assert captured["ran"] is True
    assert "AINRF worker processed one task." in result.stdout


def test_python_module_entrypoint() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ainrf", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "serve" in result.stdout
    assert "run" in result.stdout


def test_webui_help_lists_expected_flags() -> None:
    result = runner.invoke(app, ["webui", "--help"])

    assert result.exit_code == 0
    assert "--host" in result.stdout
    assert "--port" in result.stdout
    assert "--api-base-url" in result.stdout
    assert "--state-root" in result.stdout


def test_webui_launches_with_expected_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def fake_launch_webui(config: object) -> None:
        captured["config"] = config

    monkeypatch.setattr("ainrf.cli.launch_webui", fake_launch_webui)

    result = runner.invoke(app, ["webui"])

    assert result.exit_code == 0
    config = captured["config"]
    assert getattr(config, "host") == "127.0.0.1"
    assert getattr(config, "port") == 7860
    assert getattr(config, "api_base_url") == "http://127.0.0.1:8000"
    assert getattr(config, "state_root") == Path(".ainrf")


def test_webui_launches_with_custom_options(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def fake_launch_webui(config: object) -> None:
        captured["config"] = config

    monkeypatch.setattr("ainrf.cli.launch_webui", fake_launch_webui)

    result = runner.invoke(
        app,
        [
            "webui",
            "--host",
            "0.0.0.0",
            "--port",
            "9900",
            "--api-base-url",
            "http://ainrf.local:8000",
            "--state-root",
            str(Path("/tmp/webui-state")),
        ],
    )

    assert result.exit_code == 0
    config = captured["config"]
    assert getattr(config, "host") == "0.0.0.0"
    assert getattr(config, "port") == 9900
    assert getattr(config, "api_base_url") == "http://ainrf.local:8000"
    assert getattr(config, "state_root") == Path("/tmp/webui-state")
