from __future__ import annotations

from typing import Annotated

import typer

from ainrf import __version__
from ainrf.logging import configure_logging


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
        bool, typer.Option(help="Reserved flag for future daemonized server startup.")
    ] = False,
) -> None:
    typer.echo(
        "AINRF serve stub: API server wiring is planned for P4. "
        f"(host={host}, port={port}, daemon={daemon})"
    )


@app.command()
def run() -> None:
    typer.echo("AINRF run stub: task execution wiring is planned for P7/P8.")


def main() -> None:
    app()
