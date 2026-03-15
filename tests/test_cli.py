from __future__ import annotations

import subprocess
import sys

from typer.testing import CliRunner

from ainrf import __version__
from ainrf.cli import app


runner = CliRunner()


def test_help_shows_commands() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "serve" in result.stdout
    assert "run" in result.stdout


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


def test_serve_stub_runs() -> None:
    result = runner.invoke(app, ["serve"])

    assert result.exit_code == 0
    assert "AINRF serve stub" in result.stdout


def test_run_stub_runs() -> None:
    result = runner.invoke(app, ["run"])

    assert result.exit_code == 0
    assert "AINRF run stub" in result.stdout


def test_python_module_entrypoint() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ainrf", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "serve" in result.stdout
    assert "run" in result.stdout
