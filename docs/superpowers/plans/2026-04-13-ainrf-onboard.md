# AINRF Onboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an explicit `ainrf onboard` command and make `ainrf serve` auto-run local-first interactive onboarding when `./.ainrf/config.json` is missing.

**Architecture:** Keep onboarding in the CLI layer instead of `ApiConfig.from_env()`. Add a focused onboarding helper module that owns config discovery, interactive prompts, overwrite confirmation, and config persistence; then wire `serve` and the new `onboard` command through that helper while preserving existing config-loading compatibility.

**Tech Stack:** Python 3.13, Typer, pathlib, json, pytest, Typer CliRunner.

---

## File Structure / Target Surface Map

### New runtime module
- Create: `src/ainrf/onboarding.py` — state-root config discovery, interactive onboarding flow, overwrite confirmation, and config write helpers

### Existing runtime modules to modify
- Modify: `src/ainrf/cli.py` — add `onboard` command, switch default state root to current working directory `.ainrf`, and call onboarding from `serve`
- Modify: `src/ainrf/state/__init__.py` — return `Path.cwd() / ".ainrf"` for deterministic current-directory defaults
- Modify: `src/ainrf/README.md` — document first-run onboarding and current-directory `.ainrf` behavior

### Existing tests to modify
- Modify: `tests/test_cli.py` — add onboarding command coverage, auto-onboard `serve` coverage, overwrite prompt coverage, and non-interactive failure coverage
- Modify: `tests/test_api_auth.py` — keep config compatibility assertions aligned with onboard-generated config if needed

### Docs / worklog
- Modify: `docs/LLM-Working/worklog/2026-04-13.md` — append one changelog entry with validation results after implementation completes

---

### Task 1: Switch the default state root to the current working directory

**Files:**
- Modify: `src/ainrf/state/__init__.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write the failing default-state-root test**

Add this test near the top of `tests/test_cli.py`:

```python
from pathlib import Path

from ainrf.state import default_state_root


def test_default_state_root_uses_current_working_directory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("ainrf.state.Path.cwd", lambda: Path("/tmp/workspace"))

    assert default_state_root() == Path("/tmp/workspace/.ainrf")
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_default_state_root_uses_current_working_directory -q
```

Expected: FAIL because `default_state_root()` still returns `Path(".ainrf")`.

- [ ] **Step 3: Implement the current-directory default**

Update `src/ainrf/state/__init__.py` to:

```python
from __future__ import annotations

from pathlib import Path



def default_state_root() -> Path:
    return Path.cwd() / ".ainrf"


__all__ = ["default_state_root"]
```

- [ ] **Step 4: Run the test again and confirm it passes**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_default_state_root_uses_current_working_directory -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/ainrf/state/__init__.py tests/test_cli.py
git commit -m "refactor: anchor default state root to cwd"
```

---

### Task 2: Add focused onboarding helpers for config discovery and base config creation

**Files:**
- Create: `src/ainrf/onboarding.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing helper-flow tests**

Append to `tests/test_cli.py`:

```python
from ainrf.onboarding import ensure_onboarded, onboard_state_root


def test_onboard_state_root_writes_minimal_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr("ainrf.onboarding.typer.prompt", lambda *args, **kwargs: "bootstrap-secret")
    monkeypatch.setattr("ainrf.onboarding.typer.confirm", lambda *args, **kwargs: False)

    config_path = onboard_state_root(tmp_path)

    payload = json.loads(config_path.read_text(encoding="utf-8"))
    assert config_path == tmp_path / "config.json"
    assert payload["api_key_hashes"] == [hash_api_key("bootstrap-secret")]


def test_ensure_onboarded_returns_existing_config_path(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps({"api_key_hashes": [hash_api_key("ready")]}), encoding="utf-8")

    assert ensure_onboarded(tmp_path) == config_path
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_onboard_state_root_writes_minimal_config tests/test_cli.py::test_ensure_onboarded_returns_existing_config_path -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'ainrf.onboarding'`.

- [ ] **Step 3: Implement the base onboarding helper module**

Create `src/ainrf/onboarding.py` with:

```python
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import typer

from ainrf.api.config import hash_api_key


ConfigPayload = dict[str, Any]


def config_path_for(state_root: Path) -> Path:
    return state_root / "config.json"


def load_runtime_config(config_path: Path) -> ConfigPayload:
    if not config_path.exists():
        return {}
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise typer.BadParameter(f"Invalid runtime config at {config_path}")
    return payload


def save_runtime_config(config_path: Path, payload: ConfigPayload) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def ensure_interactive_onboarding_available() -> None:
    if sys.stdin is not None and sys.stdin.isatty():
        return
    raise typer.BadParameter(
        "AINRF is not configured for this directory. Run `ainrf onboard` interactively or provide config first."
    )


def prompt_api_key() -> str:
    api_key = typer.prompt(
        "API key for AINRF clients",
        hide_input=True,
        confirmation_prompt=True,
    ).strip()
    if not api_key:
        raise typer.BadParameter("API key cannot be empty.")
    return api_key


def onboard_state_root(state_root: Path) -> Path:
    typer.echo(f"Initializing AINRF in `{state_root}`.")
    payload: ConfigPayload = {"api_key_hashes": [hash_api_key(prompt_api_key())]}
    config_path = config_path_for(state_root)
    save_runtime_config(config_path, payload)
    typer.echo(f"Saved AINRF config to `{config_path}`.")
    if typer.confirm("Configure a default container profile now?", default=False):
        typer.echo("Container profile onboarding is not implemented yet.")
    return config_path


def ensure_onboarded(state_root: Path) -> Path:
    config_path = config_path_for(state_root)
    if config_path.exists():
        return config_path
    ensure_interactive_onboarding_available()
    return onboard_state_root(state_root)
```

- [ ] **Step 4: Run the helper tests and confirm they pass**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_onboard_state_root_writes_minimal_config tests/test_cli.py::test_ensure_onboarded_returns_existing_config_path -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/ainrf/onboarding.py tests/test_cli.py
git commit -m "feat: add onboarding config helpers"
```

---

### Task 3: Support optional container-profile onboarding in the helper module

**Files:**
- Modify: `src/ainrf/onboarding.py`
- Modify: `src/ainrf/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing container-onboarding tests**

Append to `tests/test_cli.py`:

```python
def test_onboard_state_root_can_add_default_container_profile(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answers = iter([
        "bootstrap-secret",
        "gpu-main",
        "ssh -p 2222 researcher@gpu-server-01 -i /tmp/id_ed25519",
        "/workspace/project-a",
        "secret-pass",
    ])
    monkeypatch.setattr("ainrf.onboarding.typer.prompt", lambda *args, **kwargs: next(answers))
    monkeypatch.setattr("ainrf.onboarding.typer.confirm", lambda *args, **kwargs: True)

    config_path = onboard_state_root(tmp_path)

    payload = json.loads(config_path.read_text(encoding="utf-8"))
    assert payload["default_container_profile"] == "gpu-main"
    profile = payload["container_profiles"]["gpu-main"]
    assert profile["host"] == "gpu-server-01"
    assert profile["port"] == 2222
    assert profile["user"] == "researcher"
    assert profile["ssh_key_path"] == "/tmp/id_ed25519"
    assert profile["project_dir"] == "/workspace/project-a"
    assert profile["ssh_password"] == "secret-pass"
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_onboard_state_root_can_add_default_container_profile -q
```

Expected: FAIL because onboarding does not yet persist container profiles.

- [ ] **Step 3: Reuse the existing container parsing path in onboarding**

In `src/ainrf/cli.py`, add a reusable helper below `_parse_ssh_command()`:

```python
def build_container_profile(
    name: str,
    ssh_command: str,
    project_dir: str,
    password: str,
) -> tuple[str, dict[str, object]]:
    parsed = _parse_ssh_command(ssh_command)
    profile = {
        "host": parsed.host,
        "port": parsed.port,
        "user": parsed.user,
        "ssh_key_path": parsed.ssh_key_path,
        "project_dir": project_dir,
        "ssh_password": password or None,
    }
    return name, profile
```

Then replace `container_add()` profile assembly with:

```python
    name, profile = build_container_profile(name, ssh_command, project_dir, password)
```

In `src/ainrf/onboarding.py`, import and use that helper:

```python
from ainrf.cli import build_container_profile
```

Add this function:

```python
def prompt_optional_container_profile() -> tuple[str, dict[str, object]] | None:
    if not typer.confirm("Configure a default container profile now?", default=False):
        return None
    name = typer.prompt("Container profile name", default="default").strip()
    ssh_command = typer.prompt(
        "SSH command",
        default="ssh researcher@gpu-server-01 -i ~/.ssh/id_ed25519",
    ).strip()
    project_dir = typer.prompt("Remote project directory", default="/workspace/projects").strip()
    password = typer.prompt(
        "SSH password (optional)",
        default="",
        hide_input=True,
        confirmation_prompt=False,
    )
    return build_container_profile(name, ssh_command, project_dir, password)
```

Update `onboard_state_root()` to merge the profile when present:

```python
    payload: ConfigPayload = {"api_key_hashes": [hash_api_key(prompt_api_key())]}
    profile_entry = prompt_optional_container_profile()
    if profile_entry is not None:
        name, profile = profile_entry
        payload["container_profiles"] = {name: profile}
        payload["default_container_profile"] = name
```

- [ ] **Step 4: Run the test again and confirm it passes**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_onboard_state_root_can_add_default_container_profile -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/ainrf/onboarding.py src/ainrf/cli.py tests/test_cli.py
git commit -m "feat: add optional container onboarding"
```

---

### Task 4: Add the `ainrf onboard` command and overwrite confirmation flow

**Files:**
- Modify: `src/ainrf/cli.py`
- Modify: `src/ainrf/onboarding.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing command-behavior tests**

Append to `tests/test_cli.py`:

```python
def test_onboard_command_writes_config(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        ["onboard", "--state-root", str(tmp_path)],
        input="bootstrap-secret\nbootstrap-secret\nn\n",
    )

    assert result.exit_code == 0
    payload = json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))
    assert payload["api_key_hashes"] == [hash_api_key("bootstrap-secret")]


def test_onboard_command_prompts_before_overwrite(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps({"api_key_hashes": [hash_api_key("existing")]}), encoding="utf-8")

    result = runner.invoke(
        app,
        ["onboard", "--state-root", str(tmp_path)],
        input="n\n",
    )

    assert result.exit_code == 0
    assert json.loads(config_path.read_text(encoding="utf-8"))["api_key_hashes"] == [hash_api_key("existing")]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_onboard_command_writes_config tests/test_cli.py::test_onboard_command_prompts_before_overwrite -q
```

Expected: FAIL because the `onboard` command does not exist.

- [ ] **Step 3: Implement overwrite-aware onboarding entrypoints**

In `src/ainrf/onboarding.py`, add:

```python
def run_onboarding(state_root: Path) -> Path | None:
    config_path = config_path_for(state_root)
    if config_path.exists() and not typer.confirm(
        f"AINRF config already exists at `{config_path}`. Overwrite it?",
        default=False,
    ):
        typer.echo("Keeping existing AINRF config.")
        return None
    return onboard_state_root(state_root)
```

In `src/ainrf/cli.py`, import the helper:

```python
from ainrf.onboarding import ensure_onboarded, run_onboarding
```

Add the command above `container_app.command("add")`:

```python
@app.command()
def onboard(
    state_root: Annotated[
        Path,
        typer.Option(help="State root where AINRF config will be initialized."),
    ] = default_state_root(),
) -> None:
    run_onboarding(state_root)
```

- [ ] **Step 4: Run the tests again and confirm they pass**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_onboard_command_writes_config tests/test_cli.py::test_onboard_command_prompts_before_overwrite -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/ainrf/cli.py src/ainrf/onboarding.py tests/test_cli.py
git commit -m "feat: add explicit onboard command"
```

---

### Task 5: Make `ainrf serve` auto-trigger onboarding and preserve non-interactive failure semantics

**Files:**
- Modify: `src/ainrf/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing serve/onboarding tests**

Replace the old bootstrap tests in `tests/test_cli.py` with these new cases:

```python
def test_serve_auto_onboards_before_running_server(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    captured: dict[str, object] = {}

    def fake_run_server(host: str, port: int, state_root: Path) -> None:
        captured["host"] = host
        captured["port"] = port
        captured["state_root"] = state_root

    monkeypatch.delenv("AINRF_API_KEY_HASHES", raising=False)
    monkeypatch.setattr("ainrf.cli.run_server", fake_run_server)

    result = runner.invoke(
        app,
        ["serve", "--state-root", str(tmp_path)],
        input="bootstrap-secret\nbootstrap-secret\nn\n",
    )

    assert result.exit_code == 0
    assert captured == {"host": "127.0.0.1", "port": 8000, "state_root": tmp_path}
    payload = json.loads((tmp_path / "config.json").read_text(encoding="utf-8"))
    assert payload["api_key_hashes"] == [hash_api_key("bootstrap-secret")]


def test_serve_fails_fast_without_interactive_input(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("AINRF_API_KEY_HASHES", raising=False)
    monkeypatch.setattr("ainrf.onboarding.sys.stdin", None)

    result = runner.invoke(app, ["serve", "--state-root", str(tmp_path)])

    assert result.exit_code != 0
    assert "Run `ainrf onboard` interactively" in result.stdout
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_serve_auto_onboards_before_running_server tests/test_cli.py::test_serve_fails_fast_without_interactive_input -q
```

Expected: FAIL because `serve` still calls `_ensure_api_key_hashes_configured()` instead of the onboarding helper.

- [ ] **Step 3: Replace inline bootstrap logic with onboarding orchestration**

In `src/ainrf/cli.py`, update `serve()` to:

```python
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
    if not os.environ.get("AINRF_API_KEY_HASHES", "").strip():
        ensure_onboarded(state_root)
    if daemon:
        runtime_dir = state_root / "runtime"
        resolved_pid_file = pid_file or runtime_dir / "ainrf-api.pid"
        resolved_log_file = log_file or runtime_dir / "ainrf-api.log"
        daemon_pid = run_server_daemon(host, port, state_root, resolved_pid_file, resolved_log_file)
        typer.echo(f"AINRF API daemon started (pid={daemon_pid}, port={port})")
        return
    run_server(host, port, state_root)
```

Then delete `_ensure_api_key_hashes_configured()` from `src/ainrf/cli.py`.

- [ ] **Step 4: Run the tests again and confirm they pass**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_serve_auto_onboards_before_running_server tests/test_cli.py::test_serve_fails_fast_without_interactive_input -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/ainrf/cli.py tests/test_cli.py
git commit -m "feat: auto-run onboarding from serve"
```

---

### Task 6: Verify config compatibility and update runtime docs

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `tests/test_api_auth.py`
- Modify: `src/ainrf/README.md`
- Modify: `docs/LLM-Working/worklog/2026-04-13.md`

- [ ] **Step 1: Add failing compatibility and help-surface tests**

Append to `tests/test_cli.py`:

```python
def test_help_shows_onboard_command() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "onboard" in result.stdout
```

Append to `tests/test_api_auth.py`:

```python
def test_api_config_reads_onboard_minimal_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AINRF_API_KEY_HASHES", raising=False)
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"api_key_hashes": [hash_api_key("bootstrap-secret")]}),
        encoding="utf-8",
    )

    config = ApiConfig.from_env(tmp_path)

    assert config.verify_api_key("bootstrap-secret") is True
    assert config.state_root == tmp_path
```

- [ ] **Step 2: Run the tests to verify they fail or capture gaps**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py::test_help_shows_onboard_command tests/test_api_auth.py::test_api_config_reads_onboard_minimal_config -q
```

Expected: CLI help test FAILS before docs/command surface is complete; config compatibility test should PASS once the earlier tasks are done.

- [ ] **Step 3: Update runtime README and worklog**

Update `src/ainrf/README.md` to add a first-run onboarding section under the startup/config area, covering:

```md
### 3.2 首次初始化（onboard）

AINRF 默认把当前工作目录下的 `./.ainrf/` 作为 state root。

第一次在某目录运行 `ainrf serve` 时，如果 `./.ainrf/config.json` 不存在，CLI 会自动进入交互式 onboarding：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf serve
```

你也可以显式执行：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf onboard
```

onboarding 会至少创建：

- `./.ainrf/config.json`

其中最小配置只包含 `api_key_hashes`；如果你选择继续，还可以在同一次流程里写入默认 container profile。
```

Append this worklog entry to `docs/LLM-Working/worklog/2026-04-13.md` after implementation and validation complete:

```md
- 2026-04-13 HH:MM `ainrf-onboard-implementation`：按 TDD 新增显式 `ainrf onboard` 命令，并将默认 state root 收敛到当前工作目录 `.ainrf`；`ainrf serve` 在缺失 `config.json` 时会自动进入本地优先的交互式初始化，最小写入 API key hash，可选补充默认 container profile，且已存在配置时先确认是否覆盖。验证结果为 `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py tests/test_api_auth.py tests/test_server.py -q` 通过，相关 README 已同步更新。
```

- [ ] **Step 4: Run the final targeted verification**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_cli.py tests/test_api_auth.py tests/test_server.py -q
```

Expected: PASS.

Then run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_cli.py tests/test_api_auth.py src/ainrf/README.md docs/LLM-Working/worklog/2026-04-13.md
git commit -m "feat: add first-run onboarding flow"
```

---

## Self-Review

- **Spec coverage:** covered current-directory `.ainrf` default, explicit `onboard` command, auto-onboard from `serve`, overwrite confirmation, optional container profile, non-interactive failure, config compatibility, docs, and worklog.
- **Placeholder scan:** removed TBD/TODO language from executable tasks; every code-changing step contains concrete snippets and exact commands.
- **Type consistency:** the plan consistently uses `onboard_state_root`, `ensure_onboarded`, `run_onboarding`, `build_container_profile`, and `default_state_root` across later tasks.
