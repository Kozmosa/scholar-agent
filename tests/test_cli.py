from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from typer.testing import CliRunner

from ainrf import __version__
from ainrf.api.config import hash_api_key
from ainrf.cli import _parse_ssh_command, app


runner = CliRunner()


def test_help_shows_commands() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "daemon-oriented runtime CLI" in result.stdout
    assert "serve" in result.stdout
    assert "container" in result.stdout
    assert "│ run" not in result.stdout
    assert "webui" not in result.stdout


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
        [
            "serve",
            "--host",
            "127.0.0.1",
            "--port",
            "8765",
            "--daemon",
            "--state-root",
            str(state_root),
        ],
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


def test_serve_bootstraps_api_key_hashes_interactively(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    captured: dict[str, object] = {}

    def fake_run_server(host: str, port: int, state_root: Path) -> None:
        captured["host"] = host
        captured["port"] = port
        captured["state_root"] = state_root

    monkeypatch.delenv("AINRF_API_KEY_HASHES", raising=False)
    monkeypatch.setattr("ainrf.cli.run_server", fake_run_server)

    result = runner.invoke(
        app,
        ["serve", "--state-root", str(tmp_path)],
        input="bootstrap-secret\nbootstrap-secret\n",
    )

    assert result.exit_code == 0
    assert captured == {"host": "127.0.0.1", "port": 8000, "state_root": tmp_path}
    payload = json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))
    assert payload["api_key_hashes"] == [hash_api_key("bootstrap-secret")]


def test_serve_daemon_bootstraps_api_key_hashes_interactively(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
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
        return 9001

    monkeypatch.delenv("AINRF_API_KEY_HASHES", raising=False)
    monkeypatch.setattr("ainrf.cli.run_server_daemon", fake_run_server_daemon)

    result = runner.invoke(
        app,
        ["serve", "--daemon", "--state-root", str(tmp_path)],
        input="daemon-secret\ndaemon-secret\n",
    )

    assert result.exit_code == 0
    assert "pid=9001" in result.stdout
    payload = json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))
    assert payload["api_key_hashes"] == [hash_api_key("daemon-secret")]


def test_python_module_entrypoint() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ainrf", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "serve" in result.stdout
    assert "container" in result.stdout
    assert "│ run" not in result.stdout
    assert "webui" not in result.stdout


def test_container_add_interactive_persists_profile(tmp_path: Path) -> None:
    state_root = tmp_path / "state"
    result = runner.invoke(
        app,
        ["container", "add", "--state-root", str(state_root)],
        input="gpu-main\nssh -p 2222 researcher@gpu-server-01 -i /tmp/id_ed25519\n/workspace/project-a\nsecret-pass\n",
    )

    assert result.exit_code == 0
    config_path = state_root / "config.json"
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    profile = payload["container_profiles"]["gpu-main"]
    assert payload["default_container_profile"] == "gpu-main"
    assert profile["host"] == "gpu-server-01"
    assert profile["port"] == 2222
    assert profile["user"] == "researcher"
    assert profile["ssh_key_path"] == "/tmp/id_ed25519"
    assert profile["ssh_password"] == "secret-pass"
    assert profile["project_dir"] == "/workspace/project-a"


def test_parse_ssh_command_supports_user_flag_and_inline_port() -> None:
    parsed = _parse_ssh_command("ssh -p2200 -l worker gpu-server-02")

    assert parsed.host == "gpu-server-02"
    assert parsed.user == "worker"
    assert parsed.port == 2200
