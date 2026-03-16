from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated

import typer

from ainrf.agents import ClaudeCodeAdapter
from ainrf import __version__
from ainrf.engine.engine import EngineContext, TaskEngine
from ainrf.events import JsonlTaskEventStore, TaskEventService
from ainrf.gates import HumanGateManager, WebhookDispatcher
from ainrf.logging import configure_logging
from ainrf.parsing import MinerUClient, MinerUConfig
from ainrf.runtime import WebhookSecretStore
from ainrf.server import run_server, run_server_daemon
from ainrf.state import JsonStateStore, default_state_root
from ainrf.webui import WebUiConfig, launch_webui


app = typer.Typer(
    add_completion=False,
    help="AINRF orchestration CLI scaffold.",
    no_args_is_help=True,
)


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
    configure_logging()


@app.command()
def serve(
    host: Annotated[str, typer.Option(help="Bind host for the future API server.")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Bind port for the future API server.")] = 8000,
    daemon: Annotated[
        bool, typer.Option(help="Run the API server in the background.")
    ] = False,
    state_root: Annotated[
        Path,
        typer.Option(help="State root for task records, artifacts, and daemon runtime files."),
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
    if daemon:
        runtime_dir = state_root / "runtime"
        resolved_pid_file = pid_file or runtime_dir / "ainrf-api.pid"
        resolved_log_file = log_file or runtime_dir / "ainrf-api.log"
        daemon_pid = run_server_daemon(host, port, state_root, resolved_pid_file, resolved_log_file)
        typer.echo(f"AINRF API daemon started (pid={daemon_pid}, port={port})")
        return
    run_server(host, port, state_root)


@app.command()
def run(
    state_root: Annotated[
        Path,
        typer.Option(help="State root for task records, artifacts, and runtime metadata."),
    ] = default_state_root(),
    once: Annotated[
        bool,
        typer.Option(help="Run one scheduling iteration and exit."),
    ] = False,
    poll_interval: Annotated[
        float,
        typer.Option(help="Polling interval in seconds when running continuously."),
    ] = 5.0,
) -> None:
    engine = build_task_engine(state_root)
    if once:
        ran = asyncio.run(async_once(engine))
        typer.echo("AINRF worker processed one task." if ran else "AINRF worker found no runnable tasks.")
        return
    asyncio.run(async_forever(engine, poll_interval))


@app.command()
def webui(
    host: Annotated[str, typer.Option(help="Bind host for the WebUI server.")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Bind port for the WebUI server.")] = 7860,
    api_base_url: Annotated[
        str,
        typer.Option(help="Base URL for an already running AINRF API server."),
    ] = "http://127.0.0.1:8000",
    state_root: Annotated[
        Path,
        typer.Option(help="Local state root for WebUI project records and run registry."),
    ] = default_state_root(),
) -> None:
    launch_webui(WebUiConfig(host=host, port=port, api_base_url=api_base_url, state_root=state_root))


async def async_once(engine: TaskEngine) -> bool:
    return await engine.run_once()


async def async_forever(engine: TaskEngine, poll_interval: float) -> None:
    await engine.run_forever(poll_interval)


def build_task_engine(state_root: Path) -> TaskEngine:
    state_store = JsonStateStore(state_root)
    event_service = TaskEventService(JsonlTaskEventStore(state_root))
    secret_store = WebhookSecretStore(state_root)
    gate_manager = HumanGateManager(
        store=state_store,
        event_service=event_service,
        webhook_dispatcher=WebhookDispatcher(),
        secret_registry=secret_store,
        gate_timeout_seconds=3600,
    )
    parser = MinerUClient(MinerUConfig.from_env())
    adapter = ClaudeCodeAdapter()
    return TaskEngine(
        EngineContext(
            state_store=state_store,
            event_service=event_service,
            gate_manager=gate_manager,
            parser=parser,
            agent_adapter=adapter,
            runtime_root=state_root,
        )
    )


def main() -> None:
    app()
