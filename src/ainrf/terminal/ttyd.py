from __future__ import annotations

from pathlib import Path


class TtydCommand(list[str]):
    def __init__(self, args: list[str], working_directory: Path) -> None:
        super().__init__(args)
        self.working_directory = working_directory.resolve(strict=True)


def build_ttyd_command(
    host: str,
    port: int,
    credential: str,
    shell_command: tuple[str, ...],
    working_directory: Path,
) -> TtydCommand:
    return TtydCommand(
        [
            "ttyd",
            "--port",
            str(port),
            "--interface",
            host,
            "--credential",
            credential,
            *shell_command,
        ],
        working_directory=working_directory,
    )


def terminal_url(host: str, port: int) -> str:
    return f"http://{host}:{port}"
