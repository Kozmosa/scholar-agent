from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from ainrf import __version__
from ainrf.logging import configure_logging
from ainrf.server import run_server, run_server_daemon
from ainrf.state import default_state_root


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
def run() -> None:
    typer.echo("AINRF run stub: task execution wiring is planned for P7/P8.")


def main() -> None:
    app()
