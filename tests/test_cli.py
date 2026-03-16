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
    result = runner.invoke(app, ["run"])

    assert result.exit_code == 0
    assert "AINRF run stub" in result.stdout


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
