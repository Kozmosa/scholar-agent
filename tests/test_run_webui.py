from __future__ import annotations

import importlib.util
import json
import signal
import sys
from pathlib import Path
from types import ModuleType

import pytest

from ainrf.api.config import hash_api_key


def _load_run_webui_module() -> ModuleType:
    module_path = Path(__file__).resolve().parent.parent / "scripts" / "run_webui.py"
    spec = importlib.util.spec_from_file_location("run_webui_for_tests", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


run_webui = _load_run_webui_module()
DEFAULT_UV_CACHE_DIR = run_webui.DEFAULT_UV_CACHE_DIR
WEBUI_API_KEY_ENV = run_webui.WEBUI_API_KEY_ENV
ManagedProcess = run_webui.ManagedProcess
ProcessSupervisor = run_webui.ProcessSupervisor
WebuiOptions = run_webui.WebuiOptions
build_backend_command = run_webui.build_backend_command
build_frontend_command = run_webui.build_frontend_command
build_frontend_env = run_webui.build_frontend_env
build_frontend_build_command = run_webui.build_frontend_build_command
ensure_frontend_dependencies = run_webui.ensure_frontend_dependencies
ensure_webui_api_key = run_webui.ensure_webui_api_key
ensure_webui_api_key_hash = run_webui.ensure_webui_api_key_hash
launch_webui = run_webui.run_webui


class FakeProcess:
    def __init__(self, pid: int, poll_results: list[int | None]) -> None:
        self.pid = pid
        self.stdout = None
        self._poll_results = poll_results
        self._index = 0

    def poll(self) -> int | None:
        if self._index < len(self._poll_results):
            result = self._poll_results[self._index]
            self._index += 1
            return result
        return self._poll_results[-1]

    def wait(self, timeout: float | None = None) -> int:
        _ = timeout
        result = self.poll()
        return 0 if result is None else result


def test_ensure_webui_api_key_creates_local_env_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state_root = tmp_path / ".ainrf"
    monkeypatch.setattr(run_webui, "token_urlsafe", lambda size: "generated-webui-key")

    api_key = ensure_webui_api_key(state_root)

    assert api_key == "generated-webui-key"
    assert (state_root / "webui.env").read_text(encoding="utf-8") == (
        "AINRF_WEBUI_API_KEY=generated-webui-key\n"
    )


def test_ensure_webui_api_key_hash_preserves_existing_runtime_config(tmp_path: Path) -> None:
    config_path = tmp_path / ".ainrf" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(
            {
                "api_key_hashes": ["existing-hash"],
                "container_profiles": {
                    "gpu-main": {
                        "host": "gpu.example.com",
                        "port": 2222,
                        "user": "researcher",
                        "project_dir": "/workspace/project",
                    }
                },
                "default_container_profile": "gpu-main",
            }
        ),
        encoding="utf-8",
    )

    api_key_hash = ensure_webui_api_key_hash(config_path, "webui-secret")
    payload = json.loads(config_path.read_text(encoding="utf-8"))

    assert api_key_hash == hash_api_key("webui-secret")
    assert payload["api_key_hashes"] == ["existing-hash", hash_api_key("webui-secret")]
    assert payload["container_profiles"]["gpu-main"]["host"] == "gpu.example.com"
    assert payload["default_container_profile"] == "gpu-main"


def test_build_commands_cover_dev_preview_and_backend_public() -> None:
    assert build_backend_command(WebuiOptions()) == [
        "uv",
        "run",
        "ainrf",
        "serve",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
        "--state-root",
        ".ainrf",
    ]
    assert build_frontend_command(WebuiOptions()) == [
        "npm",
        "run",
        "dev",
        "--",
        "--host",
        "0.0.0.0",
        "--port",
        "5173",
    ]
    assert build_frontend_build_command() == ["npm", "run", "build"]
    assert build_frontend_command(WebuiOptions(mode="preview")) == [
        "npm",
        "run",
        "preview",
        "--",
        "--host",
        "0.0.0.0",
        "--port",
        "4173",
    ]
    assert build_backend_command(WebuiOptions(mode="preview", backend_public=True)) == [
        "uv",
        "run",
        "ainrf",
        "serve",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--state-root",
        ".ainrf",
    ]


def test_build_frontend_env_sets_service_key_and_default_uv_cache(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("UV_CACHE_DIR", raising=False)

    env = build_frontend_env("service-key", {"PATH": "/usr/bin"})

    assert env["PATH"] == "/usr/bin"
    assert env["UV_CACHE_DIR"] == DEFAULT_UV_CACHE_DIR
    assert env[WEBUI_API_KEY_ENV] == "service-key"


def test_ensure_frontend_dependencies_runs_npm_ci_when_node_modules_missing(
    tmp_path: Path,
) -> None:
    frontend_dir = tmp_path / "frontend"
    frontend_dir.mkdir()
    calls: list[tuple[str, list[str], Path, dict[str, str]]] = []

    def fake_command_runner(
        name: str,
        command: list[str],
        cwd: Path,
        env: dict[str, str],
    ) -> None:
        calls.append((name, command, cwd, env))

    ensure_frontend_dependencies(
        frontend_dir, {"UV_CACHE_DIR": DEFAULT_UV_CACHE_DIR}, fake_command_runner
    )

    assert calls == [
        (
            "frontend-deps",
            ["npm", "ci"],
            frontend_dir,
            {"UV_CACHE_DIR": DEFAULT_UV_CACHE_DIR},
        )
    ]


def test_run_webui_waits_for_backend_health_before_starting_frontend(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(run_webui, "token_urlsafe", lambda size: "generated-webui-key")
    monkeypatch.delenv("UV_CACHE_DIR", raising=False)
    frontend_dir = tmp_path / "frontend" / "node_modules"
    frontend_dir.mkdir(parents=True)
    events: list[str] = []
    commands: dict[str, list[str]] = {}
    envs: dict[str, dict[str, str]] = {}

    class RecordingSupervisor:
        def start(
            self,
            name: str,
            command: list[str],
            cwd: Path,
            env: dict[str, str],
        ) -> ManagedProcess:
            _ = cwd
            events.append(f"start:{name}")
            commands[name] = command
            envs[name] = env
            return ManagedProcess(
                name=name,
                process=FakeProcess(100 if name == "backend" else 200, [None, None, None]),
            )

        def stop_all(self, *, exclude_pid: int | None = None) -> None:
            events.append(f"stop:{exclude_pid}")

        def wait(self) -> int:
            events.append("wait")
            return 0

    def fake_health_checker(health_url: str, backend_process: FakeProcess) -> None:
        events.append("health")
        assert health_url == "http://127.0.0.1:8000/health"
        assert backend_process.pid == 100

    exit_code = launch_webui(
        WebuiOptions(),
        repo_root=tmp_path,
        supervisor_factory=RecordingSupervisor,
        command_runner=lambda *args, **kwargs: pytest.fail("command runner should not be used"),
        health_checker=fake_health_checker,
    )

    config_path = tmp_path / ".ainrf" / "config.json"
    payload = json.loads(config_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert events == ["start:backend", "health", "start:frontend", "wait"]
    assert commands["backend"] == build_backend_command(WebuiOptions())
    assert commands["frontend"] == build_frontend_command(WebuiOptions())
    assert envs["backend"]["UV_CACHE_DIR"] == DEFAULT_UV_CACHE_DIR
    assert envs["frontend"]["UV_CACHE_DIR"] == DEFAULT_UV_CACHE_DIR
    assert envs["frontend"][WEBUI_API_KEY_ENV] == "generated-webui-key"
    assert payload["api_key_hashes"] == [hash_api_key("generated-webui-key")]
    assert (tmp_path / ".ainrf" / "webui.env").exists()


def test_process_supervisor_stops_remaining_process_when_one_child_exits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    supervisor = ProcessSupervisor(poll_interval_seconds=0.0)
    supervisor._processes = [
        ManagedProcess(name="backend", process=FakeProcess(101, [1])),
        ManagedProcess(name="frontend", process=FakeProcess(202, [None, None])),
    ]
    terminated: list[int] = []
    monkeypatch.setattr(
        run_webui,
        "_terminate_process_group",
        lambda process, timeout_seconds=run_webui.PROCESS_STOP_TIMEOUT_SECONDS: terminated.append(
            process.pid
        ),
    )

    exit_code = supervisor.wait()

    assert exit_code == 1
    assert terminated == [202]


def test_process_supervisor_stops_all_children_on_sigint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    supervisor = ProcessSupervisor(poll_interval_seconds=0.0)
    supervisor._processes = [
        ManagedProcess(name="backend", process=FakeProcess(101, [None, None, None])),
        ManagedProcess(name="frontend", process=FakeProcess(202, [None, None, None])),
    ]
    terminated: list[int] = []
    triggered = {"value": False}

    monkeypatch.setattr(
        run_webui,
        "_terminate_process_group",
        lambda process, timeout_seconds=run_webui.PROCESS_STOP_TIMEOUT_SECONDS: terminated.append(
            process.pid
        ),
    )

    def fake_sleep(seconds: float) -> None:
        _ = seconds
        if not triggered["value"]:
            triggered["value"] = True
            supervisor.request_stop(signal.SIGINT)

    monkeypatch.setattr(run_webui.time, "sleep", fake_sleep)

    exit_code = supervisor.wait()

    assert exit_code == 130
    assert terminated == [101, 202]
