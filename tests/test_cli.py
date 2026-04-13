from __future__ import annotations

import io
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import typer
from typer.testing import CliRunner

from ainrf import __version__
from ainrf.api.config import hash_api_key
from ainrf.cli import _parse_ssh_command, app
from ainrf.onboarding import (
    config_path_for,
    ensure_onboarded,
    load_runtime_config,
    onboard_state_root,
    save_runtime_config,
)
from ainrf.state import default_state_root


runner = CliRunner()


def test_default_state_root_uses_current_working_directory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("ainrf.state.Path.cwd", lambda: Path("/tmp/workspace"))

    assert default_state_root() == Path("/tmp/workspace/.ainrf")


class FakeTTY(io.StringIO):
    def __init__(self, is_tty: bool) -> None:
        super().__init__()
        self._is_tty = is_tty

    def isatty(self) -> bool:
        return self._is_tty


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


def test_serve_rejects_malformed_config_with_validation_error(tmp_path: Path) -> None:
    config_path = config_path_for(tmp_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("{invalid", encoding="utf-8")

    result = runner.invoke(app, ["serve", "--state-root", str(tmp_path)])

    assert result.exit_code != 0
    assert "Invalid runtime config" in result.output
    assert str(config_path) in result.output


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


def test_onboard_state_root_minimal_writes_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr("ainrf.onboarding.typer.prompt", lambda *args, **kwargs: "bootstrap-secret")
    monkeypatch.setattr("ainrf.onboarding.typer.confirm", lambda *args, **kwargs: False)

    config_path = onboard_state_root(tmp_path)

    assert config_path == config_path_for(tmp_path)
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    assert payload["api_key_hashes"] == [hash_api_key("bootstrap-secret")]
    assert "container_profiles" not in payload


def test_ensure_onboarded_returns_existing_config_path(tmp_path: Path) -> None:
    config_path = config_path_for(tmp_path)
    save_runtime_config(config_path, {"api_key_hashes": ["existing-hash"]})

    resolved = ensure_onboarded(tmp_path)

    assert resolved == config_path


@pytest.mark.parametrize(
    ("stdin_isatty", "stdout_isatty"),
    [(False, True), (True, False), (False, False)],
)
def test_ensure_onboarded_rejects_non_tty_streams(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    stdin_isatty: bool,
    stdout_isatty: bool,
) -> None:
    monkeypatch.setattr(
        "ainrf.onboarding.click.get_text_stream",
        lambda name: FakeTTY(stdin_isatty if name == "stdin" else stdout_isatty),
    )
    monkeypatch.setattr(
        "ainrf.onboarding.typer.prompt",
        lambda *args, **kwargs: pytest.fail(
            "prompt should not run for non-interactive onboarding"
        ),
    )

    with pytest.raises(typer.BadParameter, match="interactively"):
        ensure_onboarded(tmp_path)


def test_load_runtime_config_rejects_invalid_payload(tmp_path: Path) -> None:
    config_path = config_path_for(tmp_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("[]", encoding="utf-8")

    with pytest.raises(typer.BadParameter, match="Invalid runtime config"):
        load_runtime_config(config_path)


def test_load_runtime_config_rejects_malformed_json(tmp_path: Path) -> None:
    config_path = config_path_for(tmp_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("{invalid", encoding="utf-8")

    with pytest.raises(typer.BadParameter, match="Invalid runtime config"):
        load_runtime_config(config_path)


def test_onboard_state_root_rejects_empty_api_key(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr("ainrf.onboarding.typer.prompt", lambda *args, **kwargs: "   ")

    with pytest.raises(typer.BadParameter, match="API key cannot be empty"):
        onboard_state_root(tmp_path)


def test_onboard_state_root_confirm_true_writes_optional_container_profile(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    prompts = iter(
        [
            "bootstrap-secret",
            "gpu-main",
            "ssh -p 2222 researcher@gpu-server-01 -i /tmp/id_ed25519",
            "/workspace/project-a",
            "secret-pass",
        ]
    )
    monkeypatch.setattr("ainrf.onboarding.typer.prompt", lambda *args, **kwargs: next(prompts))
    monkeypatch.setattr("ainrf.onboarding.typer.confirm", lambda *args, **kwargs: True)

    config_path = onboard_state_root(tmp_path)

    payload = json.loads(config_path.read_text(encoding="utf-8"))
    profile = payload["container_profiles"]["gpu-main"]
    assert payload["default_container_profile"] == "gpu-main"
    assert profile["host"] == "gpu-server-01"
    assert profile["port"] == 2222
    assert profile["user"] == "researcher"
    assert profile["ssh_key_path"] == "/tmp/id_ed25519"
    assert profile["ssh_password"] == "secret-pass"
    assert profile["project_dir"] == "/workspace/project-a"
    assert config_path == config_path_for(tmp_path)


def test_onboard_state_root_preserves_existing_config_keys(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config_path = config_path_for(tmp_path)
    save_runtime_config(
        config_path,
        {
            "unrelated": {"enabled": True},
            "default_container_profile": "existing",
            "container_profiles": {"existing": {"host": "old", "user": "worker", "port": 22}},
        },
    )
    monkeypatch.setattr("ainrf.onboarding.typer.prompt", lambda *args, **kwargs: "bootstrap-secret")
    monkeypatch.setattr("ainrf.onboarding.typer.confirm", lambda *args, **kwargs: False)

    onboard_state_root(tmp_path)

    payload = json.loads(config_path.read_text(encoding="utf-8"))
    assert payload["api_key_hashes"] == [hash_api_key("bootstrap-secret")]
    assert payload["unrelated"] == {"enabled": True}
    assert payload["default_container_profile"] == "existing"
    assert payload["container_profiles"] == {"existing": {"host": "old", "user": "worker", "port": 22}}


def test_onboard_command_rejects_non_tty_use(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        "ainrf.onboarding.click.get_text_stream",
        lambda name: FakeTTY(False if name == "stdin" else True),
    )
    monkeypatch.setattr(
        "ainrf.onboarding.typer.confirm",
        lambda *args, **kwargs: pytest.fail("confirm should not run for non-interactive onboarding"),
    )
    monkeypatch.setattr(
        "ainrf.onboarding.typer.prompt",
        lambda *args, **kwargs: pytest.fail("prompt should not run for non-interactive onboarding"),
    )

    result = runner.invoke(app, ["onboard", "--state-root", str(tmp_path)])

    assert result.exit_code != 0
    assert "AINRF runtime config is not configured" in result.output
    assert "Run onboarding" in result.output
    assert "interactively" in result.output


def test_onboard_command_writes_config(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr("ainrf.onboarding.click.get_text_stream", lambda name: FakeTTY(True))
    result = runner.invoke(
        app,
        ["onboard", "--state-root", str(tmp_path)],
        input="bootstrap-secret\nbootstrap-secret\nn\n",
    )

    assert result.exit_code == 0
    payload = json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))
    assert payload["api_key_hashes"] == [hash_api_key("bootstrap-secret")]


def test_onboard_command_prompts_before_overwrite(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr("ainrf.onboarding.click.get_text_stream", lambda name: FakeTTY(True))
    config_path = tmp_path / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps({"api_key_hashes": [hash_api_key("existing")]}), encoding="utf-8")

    result = runner.invoke(
        app,
        ["onboard", "--state-root", str(tmp_path)],
        input="n\n",
    )

    assert result.exit_code == 0
    assert json.loads(config_path.read_text(encoding="utf-8"))["api_key_hashes"] == [
        hash_api_key("existing")
    ]



def test_onboard_command_overwrites_invalid_existing_config(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr("ainrf.onboarding.click.get_text_stream", lambda name: FakeTTY(True))
    config_path = tmp_path / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("{invalid", encoding="utf-8")

    result = runner.invoke(
        app,
        ["onboard", "--state-root", str(tmp_path)],
        input="y\nbootstrap-secret\nbootstrap-secret\nn\n",
    )

    assert result.exit_code == 0
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    assert payload["api_key_hashes"] == [hash_api_key("bootstrap-secret")]
    assert "container_profiles" not in payload


def test_parse_ssh_command_supports_user_flag_and_inline_port() -> None:
    parsed = _parse_ssh_command("ssh -p2200 -l worker gpu-server-02")

    assert parsed.host == "gpu-server-02"
    assert parsed.user == "worker"
    assert parsed.port == 2200

