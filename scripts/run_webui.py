from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from json import JSONDecodeError
from pathlib import Path
from secrets import token_urlsafe
from typing import Final, Literal, Protocol, TextIO, cast

import httpx

from ainrf.api.config import hash_api_key

DEFAULT_UV_CACHE_DIR: Final[str] = "/tmp/uv-cache"
WEBUI_API_KEY_ENV: Final[str] = "AINRF_WEBUI_API_KEY"
WEBUI_ENV_FILENAME: Final[str] = "webui.env"
CONFIG_FILENAME: Final[str] = "config.json"
BACKEND_PORT: Final[int] = 8000
FRONTEND_DEV_PORT: Final[int] = 5173
FRONTEND_PREVIEW_PORT: Final[int] = 4173
HEALTHCHECK_HOST: Final[str] = "127.0.0.1"
HEALTHCHECK_POLL_INTERVAL_SECONDS: Final[float] = 0.2
PROCESS_STOP_TIMEOUT_SECONDS: Final[float] = 5.0

Mode = Literal["dev", "preview"]


class UserFacingError(RuntimeError):
    """Raised for CLI failures that should not print a traceback."""


class ProcessHandle(Protocol):
    pid: int
    stdout: TextIO | None

    def poll(self) -> int | None: ...

    def wait(self, timeout: float | None = None) -> int: ...


@dataclass(frozen=True, slots=True)
class WebuiOptions:
    mode: Mode = "dev"
    backend_public: bool = False


@dataclass(slots=True)
class ManagedProcess:
    name: str
    process: ProcessHandle
    output_threads: tuple[threading.Thread, ...] = field(default_factory=tuple)


class ProcessSupervisorProtocol(Protocol):
    def start(
        self,
        name: str,
        command: Sequence[str],
        cwd: Path,
        env: Mapping[str, str],
    ) -> ManagedProcess: ...

    def stop_all(self, *, exclude_pid: int | None = None) -> None: ...

    def wait(self) -> int: ...


CommandRunner = Callable[[str, Sequence[str], Path, Mapping[str, str]], None]
BackendHealthChecker = Callable[[str, ProcessHandle], None]
SupervisorFactory = Callable[[], ProcessSupervisorProtocol]


def parse_args(argv: Sequence[str]) -> WebuiOptions:
    parser = argparse.ArgumentParser(
        prog="scripts/webui.sh",
        description="Launch the AINRF WebUI frontend and backend together.",
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=("dev", "preview"),
        default="dev",
        help="Frontend mode to launch (default: dev).",
    )
    parser.add_argument(
        "--backend-public",
        action="store_true",
        help="Expose the backend API on 0.0.0.0:8000 instead of 127.0.0.1:8000.",
    )
    namespace = parser.parse_args(list(argv))
    return WebuiOptions(
        mode=cast(Mode, namespace.mode),
        backend_public=bool(namespace.backend_public),
    )


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parent.parent


def state_root_for(repo_root: Path) -> Path:
    return repo_root / ".ainrf"


def webui_env_path(state_root: Path) -> Path:
    return state_root / WEBUI_ENV_FILENAME


def build_base_env(base_env: Mapping[str, str] | None = None) -> dict[str, str]:
    env = dict(base_env if base_env is not None else os.environ)
    env.setdefault("UV_CACHE_DIR", DEFAULT_UV_CACHE_DIR)
    return env


def build_frontend_env(
    api_key: str,
    base_env: Mapping[str, str] | None = None,
) -> dict[str, str]:
    env = build_base_env(base_env)
    env[WEBUI_API_KEY_ENV] = api_key
    return env


def backend_bind_host(options: WebuiOptions) -> str:
    return "0.0.0.0" if options.backend_public else "127.0.0.1"


def build_backend_command(options: WebuiOptions, state_root_arg: str = ".ainrf") -> list[str]:
    return [
        "uv",
        "run",
        "ainrf",
        "serve",
        "--host",
        backend_bind_host(options),
        "--port",
        str(BACKEND_PORT),
        "--state-root",
        state_root_arg,
    ]


def build_frontend_build_command() -> list[str]:
    return ["npm", "run", "build"]


def build_frontend_command(options: WebuiOptions) -> list[str]:
    if options.mode == "preview":
        return [
            "npm",
            "run",
            "preview",
            "--",
            "--host",
            "0.0.0.0",
            "--port",
            str(FRONTEND_PREVIEW_PORT),
        ]
    return [
        "npm",
        "run",
        "dev",
        "--",
        "--host",
        "0.0.0.0",
        "--port",
        str(FRONTEND_DEV_PORT),
    ]


def _parse_env_payload(env_path: Path) -> dict[str, str]:
    payload: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator:
            raise UserFacingError(f"Invalid env line in {env_path}: {raw_line}")
        payload[key.strip()] = value.strip()
    return payload


def ensure_webui_api_key(state_root: Path) -> str:
    state_root.mkdir(parents=True, exist_ok=True)
    env_path = webui_env_path(state_root)
    if env_path.exists():
        payload = _parse_env_payload(env_path)
        existing_value = payload.get(WEBUI_API_KEY_ENV, "").strip()
        if existing_value:
            return existing_value

    api_key = token_urlsafe(32)
    env_path.write_text(f"{WEBUI_API_KEY_ENV}={api_key}\n", encoding="utf-8")
    os.chmod(env_path, 0o600)
    return api_key


def _load_runtime_payload(config_path: Path) -> dict[str, object]:
    if not config_path.exists():
        return {}
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except JSONDecodeError as exc:
        raise UserFacingError(f"Invalid runtime config at {config_path}") from exc
    if not isinstance(payload, dict):
        raise UserFacingError(f"Invalid runtime config at {config_path}")
    return cast(dict[str, object], payload)


def _save_runtime_payload(config_path: Path, payload: Mapping[str, object]) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(dict(payload), ensure_ascii=True, indent=2),
        encoding="utf-8",
    )


def ensure_webui_api_key_hash(config_path: Path, api_key: str) -> str:
    payload = _load_runtime_payload(config_path)
    api_key_hash = hash_api_key(api_key)
    raw_hashes = payload.get("api_key_hashes")
    if raw_hashes is None:
        hashes: list[str] = []
    elif isinstance(raw_hashes, list):
        hashes = []
        for item in raw_hashes:
            if not isinstance(item, str) or not item:
                raise UserFacingError(
                    f"Invalid runtime config at {config_path}: api_key_hashes must contain strings"
                )
            hashes.append(item)
    else:
        raise UserFacingError(
            f"Invalid runtime config at {config_path}: api_key_hashes must be a list"
        )

    if api_key_hash not in hashes:
        hashes.append(api_key_hash)
        payload["api_key_hashes"] = hashes
        _save_runtime_payload(config_path, payload)
    elif not config_path.exists():
        payload["api_key_hashes"] = hashes
        _save_runtime_payload(config_path, payload)

    return api_key_hash


def _stream_output(name: str, stream: TextIO, sink: TextIO) -> None:
    try:
        for line in iter(stream.readline, ""):
            sink.write(f"[{name}] {line}")
            sink.flush()
    finally:
        stream.close()


def _spawn_managed_process(
    name: str,
    command: Sequence[str],
    cwd: Path,
    env: Mapping[str, str],
    *,
    sink: TextIO = sys.stdout,
) -> ManagedProcess:
    process: subprocess.Popen[str] = subprocess.Popen(
        list(command),
        cwd=str(cwd),
        env=dict(env),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        start_new_session=True,
    )
    output_threads: list[threading.Thread] = []
    if process.stdout is not None:
        thread = threading.Thread(
            target=_stream_output,
            args=(name, process.stdout, sink),
            daemon=True,
        )
        thread.start()
        output_threads.append(thread)
    return ManagedProcess(
        name=name,
        process=cast(ProcessHandle, process),
        output_threads=tuple(output_threads),
    )


def _join_output_threads(managed_process: ManagedProcess) -> None:
    for thread in managed_process.output_threads:
        thread.join(timeout=1.0)


def _terminate_process_group(
    process: ProcessHandle,
    timeout_seconds: float = PROCESS_STOP_TIMEOUT_SECONDS,
) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return

    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if process.poll() is not None:
            return
        time.sleep(0.1)

    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    process.wait(timeout=timeout_seconds)


def run_prefixed_command(
    name: str,
    command: Sequence[str],
    cwd: Path,
    env: Mapping[str, str],
) -> None:
    managed_process = _spawn_managed_process(name, command, cwd, env)
    try:
        return_code = managed_process.process.wait()
    except KeyboardInterrupt:
        _terminate_process_group(managed_process.process)
        raise
    finally:
        _join_output_threads(managed_process)

    if return_code != 0:
        rendered_command = " ".join(command)
        raise UserFacingError(f"{name} exited with code {return_code}: {rendered_command}")


def ensure_frontend_dependencies(
    frontend_dir: Path,
    env: Mapping[str, str],
    command_runner: CommandRunner = run_prefixed_command,
) -> None:
    if (frontend_dir / "node_modules").exists():
        return
    command_runner("frontend-deps", ["npm", "ci"], frontend_dir, env)


def wait_for_backend_health(
    health_url: str,
    backend_process: ProcessHandle,
    timeout_seconds: float = 15.0,
) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        return_code = backend_process.poll()
        if return_code is not None:
            raise UserFacingError(f"backend exited before becoming healthy (code={return_code})")
        try:
            response = httpx.get(health_url, timeout=1.0)
            if response.status_code in {200, 503}:
                return
        except httpx.HTTPError:
            pass
        time.sleep(HEALTHCHECK_POLL_INTERVAL_SECONDS)
    raise UserFacingError(f"backend did not become healthy at {health_url}")


class ProcessSupervisor:
    def __init__(self, *, poll_interval_seconds: float = 0.2) -> None:
        self._processes: list[ManagedProcess] = []
        self._poll_interval_seconds = poll_interval_seconds
        self._stop_signal: int | None = None

    def start(
        self,
        name: str,
        command: Sequence[str],
        cwd: Path,
        env: Mapping[str, str],
    ) -> ManagedProcess:
        managed_process = _spawn_managed_process(name, command, cwd, env)
        self._processes.append(managed_process)
        return managed_process

    def request_stop(self, signum: int) -> None:
        self._stop_signal = signum

    def stop_all(self, *, exclude_pid: int | None = None) -> None:
        for managed_process in self._processes:
            if exclude_pid is not None and managed_process.process.pid == exclude_pid:
                continue
            _terminate_process_group(managed_process.process)
        for managed_process in self._processes:
            _join_output_threads(managed_process)

    def wait(self) -> int:
        previous_sigint_handler = signal.getsignal(signal.SIGINT)
        previous_sigterm_handler = signal.getsignal(signal.SIGTERM)

        def _handle_signal(signum: int, _frame: object) -> None:
            self.request_stop(signum)

        signal.signal(signal.SIGINT, _handle_signal)
        signal.signal(signal.SIGTERM, _handle_signal)
        try:
            while True:
                if self._stop_signal is not None:
                    self.stop_all()
                    return 128 + self._stop_signal
                for managed_process in self._processes:
                    return_code = managed_process.process.poll()
                    if return_code is None:
                        continue
                    self.stop_all(exclude_pid=managed_process.process.pid)
                    return return_code
                time.sleep(self._poll_interval_seconds)
        finally:
            signal.signal(signal.SIGINT, previous_sigint_handler)
            signal.signal(signal.SIGTERM, previous_sigterm_handler)
            for managed_process in self._processes:
                _join_output_threads(managed_process)


def run_webui(
    options: WebuiOptions,
    *,
    repo_root: Path | None = None,
    supervisor_factory: SupervisorFactory = ProcessSupervisor,
    command_runner: CommandRunner = run_prefixed_command,
    health_checker: BackendHealthChecker = wait_for_backend_health,
) -> int:
    resolved_repo_root = repo_root or repo_root_from_script()
    frontend_dir = resolved_repo_root / "frontend"
    state_root = state_root_for(resolved_repo_root)
    base_env = build_base_env()

    api_key = ensure_webui_api_key(state_root)
    ensure_webui_api_key_hash(state_root / CONFIG_FILENAME, api_key)

    ensure_frontend_dependencies(frontend_dir, base_env, command_runner)
    frontend_env = build_frontend_env(api_key, base_env)
    if options.mode == "preview":
        command_runner("frontend-build", build_frontend_build_command(), frontend_dir, frontend_env)

    supervisor = supervisor_factory()
    backend_process: ManagedProcess | None = None
    try:
        backend_process = supervisor.start(
            "backend",
            build_backend_command(options),
            resolved_repo_root,
            base_env,
        )
        health_checker(
            f"http://{HEALTHCHECK_HOST}:{BACKEND_PORT}/health",
            backend_process.process,
        )
        supervisor.start(
            "frontend",
            build_frontend_command(options),
            frontend_dir,
            frontend_env,
        )
        service_key_path = webui_env_path(state_root)
        print(f"[webui] service key file: {service_key_path}")
        if options.backend_public:
            print(f"[webui] backend API exposed on 0.0.0.0:{BACKEND_PORT}")
        return supervisor.wait()
    except KeyboardInterrupt:
        supervisor.stop_all()
        return 130
    except Exception:
        supervisor.stop_all()
        raise


def main(argv: Sequence[str] | None = None) -> int:
    options = parse_args(argv if argv is not None else sys.argv[1:])
    try:
        return run_webui(options)
    except UserFacingError as exc:
        print(f"[webui] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
