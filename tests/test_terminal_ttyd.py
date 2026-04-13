from __future__ import annotations

from pathlib import Path

from ainrf.terminal.ttyd import build_ttyd_command, terminal_url


def test_build_ttyd_command_uses_expected_flags(tmp_path: Path) -> None:
    command = build_ttyd_command(
        host="127.0.0.1",
        port=7681,
        credential="token:secret",
        shell_command=("/bin/sh",),
        working_directory=tmp_path,
    )

    assert command == [
        "ttyd",
        "--port",
        "7681",
        "--interface",
        "127.0.0.1",
        "--credential",
        "token:secret",
        "/bin/sh",
    ]
    assert getattr(command, "working_directory") == tmp_path.resolve()


def test_terminal_url_returns_local_http_address() -> None:
    assert terminal_url("127.0.0.1", 7681) == "http://127.0.0.1:7681"
