from __future__ import annotations

import json
import os
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any

import typer

from ainrf import __version__
from ainrf.api.config import hash_api_key
from ainrf.server import run_server, run_server_daemon
from ainrf.state import default_state_root


app = typer.Typer(
    add_completion=False,
    help="AINRF daemon-oriented runtime CLI.",
    no_args_is_help=True,
)

container_app = typer.Typer(help="Manage reusable container profiles.")
app.add_typer(container_app, name="container")


def version_callback(value: bool) -> None:
    if not value:
        return
    typer.echo(f"ainrf {__version__}")
    raise typer.Exit()


@app.callback()
def main_callback(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show the installed ainrf version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    _ = version


@app.command()
def serve(
    host: Annotated[str, typer.Option(help="Bind host for the API server.")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Bind port for the API server.")] = 8000,
    daemon: Annotated[bool, typer.Option(help="Run the API server in the background.")] = False,
    state_root: Annotated[
        Path,
        typer.Option(help="State root for API configuration and daemon runtime files."),
    ] = default_state_root(),
    pid_file: Annotated[
        Path | None,
        typer.Option(help="Optional pid file path for daemon mode."),
    ] = None,
    log_file: Annotated[
        Path | None,
        typer.Option(help="Optional log file path for daemon mode."),
    ] = None,
) -> None:
    _ensure_api_key_hashes_configured(state_root)
    if daemon:
        runtime_dir = state_root / "runtime"
        resolved_pid_file = pid_file or runtime_dir / "ainrf-api.pid"
        resolved_log_file = log_file or runtime_dir / "ainrf-api.log"
        daemon_pid = run_server_daemon(host, port, state_root, resolved_pid_file, resolved_log_file)
        typer.echo(f"AINRF API daemon started (pid={daemon_pid}, port={port})")
        return
    run_server(host, port, state_root)


@container_app.command("add")
def container_add(
    state_root: Annotated[
        Path,
        typer.Option(help="State root where container profiles are stored."),
    ] = default_state_root(),
    name: Annotated[
        str,
        typer.Option(help="Profile name used for lookup.", prompt="Container profile name"),
    ] = "default",
    ssh_command: Annotated[
        str,
        typer.Option(
            "--ssh",
            help="SSH command, e.g. ssh -p 22 user@host -i ~/.ssh/id_rsa",
            prompt="SSH command",
        ),
    ] = "",
    project_dir: Annotated[
        str,
        typer.Option(
            help="Remote project directory used by AINRF.",
            prompt="Remote project directory",
        ),
    ] = "/workspace/projects",
    password: Annotated[
        str,
        typer.Option(
            help="SSH password (optional; leave empty when key-based auth is used).",
            prompt="SSH password (optional)",
            hide_input=True,
            confirmation_prompt=False,
        ),
    ] = "",
    set_default: Annotated[
        bool,
        typer.Option(help="Set this profile as the default container profile."),
    ] = True,
) -> None:
    parsed = _parse_ssh_command(ssh_command)
    profile = {
        "host": parsed.host,
        "port": parsed.port,
        "user": parsed.user,
        "ssh_key_path": parsed.ssh_key_path,
        "project_dir": project_dir,
        "ssh_password": password or None,
    }
    config_path = state_root / "config.json"
    payload = _load_runtime_config(config_path)
    profiles = payload.get("container_profiles")
    if not isinstance(profiles, dict):
        profiles = {}
    profiles[name] = profile
    payload["container_profiles"] = profiles
    if set_default:
        payload["default_container_profile"] = name
    _save_runtime_config(config_path, payload)
    typer.echo(
        f"Saved container profile `{name}` -> {parsed.user}@{parsed.host}:{parsed.port} "
        f"(project_dir={project_dir})"
    )


def main() -> None:
    app()


@dataclass(slots=True)
class ParsedSSHCommand:
    host: str
    user: str
    port: int = 22
    ssh_key_path: str | None = None


def _parse_ssh_command(command: str) -> ParsedSSHCommand:
    tokens = shlex.split(command)
    if not tokens:
        raise typer.BadParameter("SSH command cannot be empty")
    if tokens[0] == "ssh":
        tokens = tokens[1:]
    port = 22
    user: str | None = None
    ssh_key_path: str | None = None
    host: str | None = None
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "-p":
            index += 1
            if index >= len(tokens):
                raise typer.BadParameter("Invalid SSH command: missing value for -p")
            port = int(tokens[index])
        elif token.startswith("-p") and token != "-p":
            port = int(token[2:])
        elif token == "-l":
            index += 1
            if index >= len(tokens):
                raise typer.BadParameter("Invalid SSH command: missing value for -l")
            user = tokens[index]
        elif token == "-i":
            index += 1
            if index >= len(tokens):
                raise typer.BadParameter("Invalid SSH command: missing value for -i")
            ssh_key_path = tokens[index]
        elif token.startswith("-"):
            if token in {"-o", "-J"}:
                index += 1
        else:
            host = token
        index += 1
    if host is None:
        raise typer.BadParameter("Invalid SSH command: missing target host")
    if "@" in host:
        parsed_user, parsed_host = host.split("@", 1)
        if parsed_user:
            user = parsed_user
        host = parsed_host
    if user is None:
        raise typer.BadParameter("Invalid SSH command: missing user (use user@host or -l user)")
    return ParsedSSHCommand(host=host, user=user, port=port, ssh_key_path=ssh_key_path)


def _load_runtime_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise typer.BadParameter(f"Invalid runtime config at {config_path}")
    return payload


def _save_runtime_config(config_path: Path, payload: dict[str, Any]) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def _ensure_api_key_hashes_configured(state_root: Path) -> None:
    env_hashes = os.environ.get("AINRF_API_KEY_HASHES", "").strip()
    if env_hashes:
        return
    config_path = state_root / "config.json"
    payload = _load_runtime_config(config_path)
    hashes = payload.get("api_key_hashes")
    if isinstance(hashes, list) and any(isinstance(item, str) and item for item in hashes):
        return
    typer.echo("No API key hashes configured. Starting interactive bootstrap.")
    try:
        api_key = typer.prompt(
            "API key for AINRF clients",
            hide_input=True,
            confirmation_prompt=True,
        ).strip()
    except (
        EOFError,
        typer.Abort,
    ) as exc:  # pragma: no cover - defensive for non-interactive shells
        raise typer.BadParameter(
            "AINRF API key hashes are not configured. Set AINRF_API_KEY_HASHES or run `ainrf serve` interactively."
        ) from exc
    if not api_key:
        raise typer.BadParameter("API key cannot be empty.")
    payload["api_key_hashes"] = [hash_api_key(api_key)]
    _save_runtime_config(config_path, payload)
    typer.echo(f"Saved API key hash to `{config_path}`.")
