# Terminal Bench MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a ttyd-backed terminal bench MVP that lets the user start, view, and stop a single browser terminal session into the daemon host/container shell.

**Architecture:** AINRF remains the control plane: FastAPI owns terminal session state and process lifecycle, while ttyd is the browser-terminal provider. The frontend extends the current health-only shell with a small terminal panel that calls a three-endpoint API and embeds the running terminal view.

**Tech Stack:** Python, FastAPI, Typer, subprocess-based provider control, React, React Query, TypeScript, ttyd, pytest, npm build/lint.

---

## File Structure / Target Surface Map

### New backend runtime modules
- Create: `src/ainrf/terminal/models.py` — terminal session dataclasses, enums, and response-shaping helpers
- Create: `src/ainrf/terminal/ttyd.py` — ttyd provider start/inspect/stop helpers
- Create: `src/ainrf/api/routes/terminal.py` — FastAPI terminal session endpoints
- Create: `tests/test_api_terminal.py` — API contract tests for GET/POST/DELETE `/terminal/session`
- Create: `tests/test_terminal_ttyd.py` — provider lifecycle tests for ttyd command construction and cleanup

### Existing backend modules to modify
- Modify: `src/ainrf/api/app.py` — register terminal router
- Modify: `src/ainrf/api/config.py` — load ttyd-related runtime config and expose terminal defaults
- Modify: `src/ainrf/api/schemas.py` — add terminal session response schema(s)
- Modify: `src/ainrf/server.py` — optionally expose small helpers used by the terminal provider tests only if actually needed
- Modify: `src/ainrf/README.md` — document terminal bench runtime surface and ttyd dependency
- Modify: `tests/test_api_auth.py` — assert terminal endpoints remain API-key protected as appropriate
- Modify: `tests/test_api_v1_routes.py` — ensure terminal route appears while task routes remain absent

### Existing frontend modules to modify
- Modify: `frontend/src/types/index.ts` — add terminal session types alongside health type
- Modify: `frontend/src/api/endpoints.ts` — add terminal session GET/POST/DELETE helpers
- Modify: `frontend/src/api/mock.ts` — add health-compatible mock terminal session behavior for dev mode
- Modify: `frontend/src/pages/DashboardPage.tsx` — add terminal bench panel below health section
- Create: `frontend/src/components/terminal/TerminalBenchCard.tsx` — terminal status, actions, and embedded terminal container
- Create: `frontend/src/components/terminal/index.ts` — export terminal components
- Modify: `frontend/src/components/index.ts` — export terminal component barrel
- Modify: `frontend/src/components/common/Layout.tsx` — adjust copy from pure health-only shell to health + terminal bench shell

### Docs / worklog
- Modify: `docs/LLM-Working/worklog/2026-04-13.md` — append completed implementation slices and validation results

---

### Task 1: Add backend terminal session schemas and ttyd config

**Files:**
- Modify: `src/ainrf/api/config.py`
- Modify: `src/ainrf/api/schemas.py`
- Test: `tests/test_api_terminal.py`

- [ ] **Step 1: Write the failing API config/schema test**

Add these tests to `tests/test_api_terminal.py`:

```python
from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key


@pytest.mark.anyio
async def test_terminal_session_starts_idle(tmp_path: Path) -> None:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/terminal/session", headers={"X-API-Key": "secret-key"})

    assert response.status_code == 200
    assert response.json()["status"] == "idle"
    assert response.json()["provider"] == "ttyd"
    assert response.json()["target_kind"] == "daemon-host"
```

- [ ] **Step 2: Run the test to verify it fails correctly**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_terminal.py::test_terminal_session_starts_idle -q
```

Expected: FAIL because `/terminal/session` does not exist yet.

- [ ] **Step 3: Add minimal terminal config and schema support**

Update `src/ainrf/api/config.py` to carry minimal ttyd settings:

```python
@dataclass(slots=True)
class ApiConfig:
    api_key_hashes: frozenset[str]
    state_root: Path
    container_config: ContainerConfig | None = None
    terminal_host: str = "127.0.0.1"
    terminal_port: int = 7681
    terminal_command: tuple[str, ...] = ("/bin/sh",)
```

And add terminal schemas to `src/ainrf/api/schemas.py`:

```python
class TerminalSessionStatus(StrEnum):
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"


class TerminalSessionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str | None = None
    provider: str = "ttyd"
    target_kind: str = "daemon-host"
    status: TerminalSessionStatus
    created_at: str | None = None
    started_at: str | None = None
    closed_at: str | None = None
    terminal_url: str | None = None
    detail: str | None = None
```

- [ ] **Step 4: Run the test again and confirm the route still fails for the expected reason**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_terminal.py::test_terminal_session_starts_idle -q
```

Expected: still FAIL, but now because the route is missing rather than schema imports failing.

- [ ] **Step 5: Commit**

```bash
git add tests/test_api_terminal.py src/ainrf/api/config.py src/ainrf/api/schemas.py
git commit -m "feat: add terminal session config and schemas"
```

---

### Task 2: Implement ttyd provider lifecycle

**Files:**
- Create: `src/ainrf/terminal/models.py`
- Create: `src/ainrf/terminal/ttyd.py`
- Test: `tests/test_terminal_ttyd.py`

- [ ] **Step 1: Write the failing provider lifecycle tests**

Create `tests/test_terminal_ttyd.py` with:

```python
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


def test_terminal_url_returns_local_http_address() -> None:
    assert terminal_url("127.0.0.1", 7681) == "http://127.0.0.1:7681"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_terminal_ttyd.py -q
```

Expected: FAIL with module import error because `ainrf.terminal` does not exist yet.

- [ ] **Step 3: Add minimal terminal provider implementation**

Create `src/ainrf/terminal/models.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class TerminalSessionStatus(StrEnum):
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"


@dataclass(slots=True)
class TerminalSessionRecord:
    session_id: str | None
    provider: str
    target_kind: str
    status: TerminalSessionStatus
    created_at: datetime | None = None
    started_at: datetime | None = None
    closed_at: datetime | None = None
    terminal_url: str | None = None
    detail: str | None = None
    pid: int | None = None


def utc_now() -> datetime:
    return datetime.now(UTC)
```

Create `src/ainrf/terminal/ttyd.py`:

```python
from __future__ import annotations

from pathlib import Path


def build_ttyd_command(
    host: str,
    port: int,
    credential: str,
    shell_command: tuple[str, ...],
    working_directory: Path,
) -> list[str]:
    _ = working_directory
    return [
        "ttyd",
        "--port",
        str(port),
        "--interface",
        host,
        "--credential",
        credential,
        *shell_command,
    ]


def terminal_url(host: str, port: int) -> str:
    return f"http://{host}:{port}"
```

- [ ] **Step 4: Run the provider tests and make sure they pass**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_terminal_ttyd.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_terminal_ttyd.py src/ainrf/terminal/models.py src/ainrf/terminal/ttyd.py
git commit -m "feat: add ttyd terminal provider scaffolding"
```

---

### Task 3: Add terminal session API routes

**Files:**
- Create: `src/ainrf/api/routes/terminal.py`
- Modify: `src/ainrf/api/app.py`
- Modify: `src/ainrf/api/routes/__init__.py`
- Test: `tests/test_api_terminal.py`

- [ ] **Step 1: Expand the failing API tests for the three-endpoint contract**

Append to `tests/test_api_terminal.py`:

```python
@pytest.mark.anyio
async def test_terminal_session_requires_api_key(tmp_path: Path) -> None:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/terminal/session")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_terminal_session_create_and_delete_round_trip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

    running = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=utc_now(),
        started_at=utc_now(),
        terminal_url="http://127.0.0.1:7681",
    )

    monkeypatch.setattr("ainrf.api.routes.terminal.start_terminal_session", lambda app: running)
    monkeypatch.setattr("ainrf.api.routes.terminal.stop_terminal_session", lambda app: None)

    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        create_response = await client.post("/terminal/session", headers={"X-API-Key": "secret-key"})
        delete_response = await client.delete("/terminal/session", headers={"X-API-Key": "secret-key"})

    assert create_response.status_code == 200
    assert create_response.json()["status"] == "running"
    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "idle"
```

- [ ] **Step 2: Run terminal API tests to verify they fail correctly**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_terminal.py -q
```

Expected: FAIL because `ainrf.api.routes.terminal` and the route wiring do not exist.

- [ ] **Step 3: Implement minimal terminal route wiring**

Create `src/ainrf/api/routes/terminal.py`:

```python
from __future__ import annotations

from fastapi import APIRouter, Request

from ainrf.api.schemas import TerminalSessionResponse, TerminalSessionStatus
from ainrf.terminal.models import TerminalSessionRecord

router = APIRouter(prefix="/terminal", tags=["terminal"])


def get_terminal_session(app: object) -> TerminalSessionRecord:
    session = getattr(app.state, "terminal_session", None)
    if session is None:
        return TerminalSessionRecord(
            session_id=None,
            provider="ttyd",
            target_kind="daemon-host",
            status=TerminalSessionStatus.IDLE,
        )
    return session


def start_terminal_session(app: object) -> TerminalSessionRecord:
    return get_terminal_session(app)


def stop_terminal_session(app: object) -> None:
    app.state.terminal_session = None


@router.get("/session", response_model=TerminalSessionResponse)
async def read_terminal_session(request: Request) -> TerminalSessionResponse:
    session = get_terminal_session(request.app)
    return TerminalSessionResponse.model_validate(session.__dict__)


@router.post("/session", response_model=TerminalSessionResponse)
async def create_terminal_session(request: Request) -> TerminalSessionResponse:
    session = start_terminal_session(request.app)
    request.app.state.terminal_session = session
    return TerminalSessionResponse.model_validate(session.__dict__)


@router.delete("/session", response_model=TerminalSessionResponse)
async def delete_terminal_session(request: Request) -> TerminalSessionResponse:
    stop_terminal_session(request.app)
    return TerminalSessionResponse(
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.IDLE,
    )
```

Register it in `src/ainrf/api/app.py`:

```python
from ainrf.api.routes.terminal import router as terminal_router

...
app.include_router(terminal_router)
app.include_router(terminal_router, prefix="/v1")
```

And export it in `src/ainrf/api/routes/__init__.py`:

```python
from . import health, terminal

__all__ = ["health", "terminal"]
```

- [ ] **Step 4: Run terminal API tests again and confirm they pass**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_terminal.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_api_terminal.py src/ainrf/api/routes/terminal.py src/ainrf/api/app.py src/ainrf/api/routes/__init__.py
git commit -m "feat: add terminal session API routes"
```

---

### Task 4: Replace route stubs with real ttyd process lifecycle

**Files:**
- Modify: `src/ainrf/terminal/ttyd.py`
- Modify: `src/ainrf/api/routes/terminal.py`
- Test: `tests/test_terminal_ttyd.py`
- Test: `tests/test_api_terminal.py`

- [ ] **Step 1: Add failing lifecycle tests for process startup and cleanup**

Append to `tests/test_terminal_ttyd.py`:

```python
from ainrf.terminal.models import TerminalSessionStatus
from ainrf.terminal.ttyd import start_ttyd_session, stop_ttyd_session


class FakeProcess:
    def __init__(self, pid: int) -> None:
        self.pid = pid


def test_start_ttyd_session_returns_running_record(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "ainrf.terminal.ttyd.subprocess.Popen",
        lambda *args, **kwargs: FakeProcess(4321),
    )

    session = start_ttyd_session(
        host="127.0.0.1",
        port=7681,
        credential="token:secret",
        shell_command=("/bin/sh",),
        working_directory=tmp_path,
    )

    assert session.status == TerminalSessionStatus.RUNNING
    assert session.pid == 4321
    assert session.terminal_url == "http://127.0.0.1:7681"


def test_stop_ttyd_session_marks_record_idle(monkeypatch: pytest.MonkeyPatch) -> None:
    terminated: list[int] = []
    monkeypatch.setattr("ainrf.terminal.ttyd.os.kill", lambda pid, sig: terminated.append(pid))

    running = start_ttyd_session.__globals__["TerminalSessionRecord"](
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        terminal_url="http://127.0.0.1:7681",
        pid=4321,
    )

    idle = stop_ttyd_session(running)

    assert terminated == [4321]
    assert idle.status == TerminalSessionStatus.IDLE
    assert idle.pid is None
```

- [ ] **Step 2: Run lifecycle tests and verify they fail**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_terminal_ttyd.py -q
```

Expected: FAIL because lifecycle functions do not exist.

- [ ] **Step 3: Implement minimal ttyd process control**

Update `src/ainrf/terminal/ttyd.py`:

```python
from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path
from uuid import uuid4

from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

...

def start_ttyd_session(
    host: str,
    port: int,
    credential: str,
    shell_command: tuple[str, ...],
    working_directory: Path,
) -> TerminalSessionRecord:
    process = subprocess.Popen(
        build_ttyd_command(host, port, credential, shell_command, working_directory),
        cwd=working_directory,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        text=False,
    )
    started_at = utc_now()
    return TerminalSessionRecord(
        session_id=f"term-{uuid4().hex[:12]}",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=started_at,
        started_at=started_at,
        terminal_url=terminal_url(host, port),
        pid=process.pid,
    )


def stop_ttyd_session(session: TerminalSessionRecord) -> TerminalSessionRecord:
    if session.pid is not None:
        os.kill(session.pid, signal.SIGTERM)
    closed_at = utc_now()
    return TerminalSessionRecord(
        session_id=session.session_id,
        provider=session.provider,
        target_kind=session.target_kind,
        status=TerminalSessionStatus.IDLE,
        created_at=session.created_at,
        started_at=session.started_at,
        closed_at=closed_at,
        detail=session.detail,
        terminal_url=None,
        pid=None,
    )
```

Then update `src/ainrf/api/routes/terminal.py` so `POST` uses `start_ttyd_session(...)` and `DELETE` uses `stop_ttyd_session(...)` with values from `request.app.state.api_config`.

- [ ] **Step 4: Run provider and API tests to verify the real lifecycle passes**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_terminal_ttyd.py tests/test_api_terminal.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_terminal_ttyd.py tests/test_api_terminal.py src/ainrf/terminal/ttyd.py src/ainrf/api/routes/terminal.py
git commit -m "feat: wire ttyd terminal session lifecycle"
```

---

### Task 5: Protect terminal routes and surface them in runtime docs/tests

**Files:**
- Modify: `tests/test_api_auth.py`
- Modify: `tests/test_api_v1_routes.py`
- Modify: `src/ainrf/README.md`
- Test: `tests/test_api_auth.py`
- Test: `tests/test_api_v1_routes.py`

- [ ] **Step 1: Write the failing auth and route-registration tests**

Add to `tests/test_api_auth.py`:

```python
@pytest.mark.anyio
async def test_terminal_session_requires_api_key(tmp_path: Path) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get("/terminal/session")

    assert response.status_code == 401
```

Add to `tests/test_api_v1_routes.py`:

```python
@pytest.mark.anyio
async def test_openapi_includes_terminal_session_routes(tmp_path: Path) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get("/openapi.json")

    payload = response.json()
    assert "/terminal/session" in payload["paths"]
    assert "/v1/terminal/session" in payload["paths"]
```

- [ ] **Step 2: Run the targeted tests and verify they fail if route/auth behavior is missing**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_auth.py tests/test_api_v1_routes.py -q
```

Expected: if anything is missing, FAIL on terminal assertions.

- [ ] **Step 3: Update docs to describe terminal bench runtime surface**

Add to `src/ainrf/README.md` a short section like:

```md
## Terminal Bench MVP

AINRF now exposes a minimal terminal bench control surface:

- `GET /terminal/session`
- `POST /terminal/session`
- `DELETE /terminal/session`

This controls a single ttyd-backed browser terminal into the daemon host/container shell.
```

- [ ] **Step 4: Re-run the targeted tests and confirm they pass**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_auth.py tests/test_api_v1_routes.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_api_auth.py tests/test_api_v1_routes.py src/ainrf/README.md
git commit -m "docs: describe terminal bench runtime surface"
```

---

### Task 6: Add frontend terminal session types and API helpers

**Files:**
- Modify: `frontend/src/types/index.ts`
- Modify: `frontend/src/api/endpoints.ts`
- Modify: `frontend/src/api/mock.ts`
- Test via TypeScript build: `frontend`

- [ ] **Step 1: Write the failing frontend type contract check**

Create `frontend/src/terminal-contract.test.ts` with:

```ts
import type { TerminalSession, TerminalSessionStatus } from './types';

const runningStatus: TerminalSessionStatus = 'running';

const runningSession: TerminalSession = {
  session_id: 'term-1',
  provider: 'ttyd',
  target_kind: 'daemon-host',
  status: runningStatus,
  terminal_url: 'http://127.0.0.1:7681',
  created_at: '2026-04-13T00:00:00Z',
  started_at: '2026-04-13T00:00:01Z',
  closed_at: null,
  detail: null,
};

void runningSession;
```

- [ ] **Step 2: Run TypeScript build to verify it fails before the type exists**

Run:

```bash
cd frontend && npx tsc --noEmit --pretty false --project tsconfig.app.json
```

Expected: FAIL because `TerminalSession` and `TerminalSessionStatus` do not exist.

- [ ] **Step 3: Add minimal frontend terminal types and helpers**

Update `frontend/src/types/index.ts`:

```ts
export type TerminalSessionStatus = 'idle' | 'starting' | 'running' | 'stopping' | 'failed';

export interface TerminalSession {
  session_id: string | null;
  provider: 'ttyd';
  target_kind: 'daemon-host';
  status: TerminalSessionStatus;
  created_at: string | null;
  started_at: string | null;
  closed_at: string | null;
  terminal_url: string | null;
  detail: string | null;
}
```

Update `frontend/src/api/endpoints.ts`:

```ts
import type { SystemHealth, TerminalSession } from '../types';
...
export const getTerminalSession = (): Promise<TerminalSession> =>
  USE_MOCK ? Promise.resolve(mockGetTerminalSession()) : api.get<TerminalSession>('/terminal/session');

export const createTerminalSession = (): Promise<TerminalSession> =>
  USE_MOCK ? Promise.resolve(mockCreateTerminalSession()) : api.post<TerminalSession>('/terminal/session', {});

export const deleteTerminalSession = (): Promise<TerminalSession> =>
  USE_MOCK ? Promise.resolve(mockDeleteTerminalSession()) : api.delete<TerminalSession>('/terminal/session');
```

Update `frontend/src/api/mock.ts` with a small module-level terminal session variable and three helpers returning idle/running states.

- [ ] **Step 4: Run TypeScript build again and confirm it passes**

Run:

```bash
cd frontend && npx tsc --noEmit --pretty false --project tsconfig.app.json
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/terminal-contract.test.ts frontend/src/types/index.ts frontend/src/api/endpoints.ts frontend/src/api/mock.ts
git commit -m "feat: add frontend terminal session contract"
```

---

### Task 7: Add the terminal bench frontend panel

**Files:**
- Create: `frontend/src/components/terminal/TerminalBenchCard.tsx`
- Create: `frontend/src/components/terminal/index.ts`
- Modify: `frontend/src/components/index.ts`
- Modify: `frontend/src/pages/DashboardPage.tsx`
- Modify: `frontend/src/components/common/Layout.tsx`
- Test via lint/build: `frontend`

- [ ] **Step 1: Write the failing UI usage by wiring a missing component import**

Update `frontend/src/pages/DashboardPage.tsx` temporarily to import and render a non-existent `TerminalBenchCard`:

```tsx
import { TerminalBenchCard } from '../components';
...
<TerminalBenchCard />
```

- [ ] **Step 2: Run frontend build and verify it fails due to missing component/export**

Run:

```bash
cd frontend && npm run build
```

Expected: FAIL because `TerminalBenchCard` does not exist yet.

- [ ] **Step 3: Implement minimal terminal bench UI**

Create `frontend/src/components/terminal/TerminalBenchCard.tsx`:

```tsx
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { createTerminalSession, deleteTerminalSession, getTerminalSession } from '../../api';

function TerminalBenchCard() {
  const queryClient = useQueryClient();
  const sessionQuery = useQuery({ queryKey: ['terminal-session'], queryFn: getTerminalSession });

  const startMutation = useMutation({
    mutationFn: createTerminalSession,
    onSuccess: (session) => queryClient.setQueryData(['terminal-session'], session),
  });

  const stopMutation = useMutation({
    mutationFn: deleteTerminalSession,
    onSuccess: (session) => queryClient.setQueryData(['terminal-session'], session),
  });

  const session = sessionQuery.data;
  const isRunning = session?.status === 'running' && !!session.terminal_url;

  return (
    <section className="space-y-4 rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="space-y-1">
        <h2 className="text-lg font-medium text-gray-900">Terminal Bench</h2>
        <p className="text-sm text-gray-600">
          Single-session ttyd terminal into the daemon host/container environment.
        </p>
      </div>
      <div className="text-sm text-gray-700">
        Status: {sessionQuery.isLoading ? 'loading' : session?.status ?? 'idle'}
      </div>
      {session?.detail ? <p className="text-sm text-red-600">{session.detail}</p> : null}
      <div className="flex gap-3">
        <button
          type="button"
          onClick={() => startMutation.mutate()}
          disabled={startMutation.isPending || isRunning}
          className="rounded bg-[var(--accent)] px-4 py-2 text-sm text-white disabled:opacity-50"
        >
          Start terminal
        </button>
        <button
          type="button"
          onClick={() => stopMutation.mutate()}
          disabled={stopMutation.isPending || !session || session.status !== 'running'}
          className="rounded border border-gray-300 px-4 py-2 text-sm text-gray-700 disabled:opacity-50"
        >
          Stop terminal
        </button>
      </div>
      {isRunning ? (
        <iframe
          title="Terminal Bench"
          src={session.terminal_url ?? undefined}
          className="h-[420px] w-full rounded border border-gray-200"
        />
      ) : null}
    </section>
  );
}

export default TerminalBenchCard;
```

Create `frontend/src/components/terminal/index.ts`:

```ts
export { default as TerminalBenchCard } from './TerminalBenchCard';
```

Update `frontend/src/components/index.ts`:

```ts
export * from './common';
export * from './dashboard';
export * from './terminal';
```

Update `frontend/src/pages/DashboardPage.tsx` to render `<TerminalBenchCard />` under the health section.

Update `frontend/src/components/common/Layout.tsx` copy from “health-only UI” to wording like “Health and terminal shell during realignment.”

- [ ] **Step 4: Run lint and build to verify the UI passes**

Run:

```bash
cd frontend && npm run lint
cd frontend && npm run build
```

Expected: both PASS (build may still emit the existing Tailwind/lightningcss warnings without failing).

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/terminal/TerminalBenchCard.tsx frontend/src/components/terminal/index.ts frontend/src/components/index.ts frontend/src/pages/DashboardPage.tsx frontend/src/components/common/Layout.tsx
git commit -m "feat: add terminal bench frontend panel"
```

---

### Task 8: Final verification, docs, and worklog

**Files:**
- Modify: `src/ainrf/README.md`
- Modify: `docs/LLM-Working/worklog/2026-04-13.md`
- Review: `docs/superpowers/specs/2026-04-13-terminal-bench-mvp-design.md`

- [ ] **Step 1: Update runtime README with ttyd dependency and terminal bench usage**

Add a concise section to `src/ainrf/README.md`:

```md
## Terminal Bench MVP

Terminal Bench uses a single ttyd-backed session into the daemon host/container shell.

Required dependency:

```bash
ttyd --version
```

Runtime API:
- `GET /terminal/session`
- `POST /terminal/session`
- `DELETE /terminal/session`
```

- [ ] **Step 2: Append worklog entry with validation evidence**

Append to `docs/LLM-Working/worklog/2026-04-13.md` a completed-slice entry including:
- summary of terminal bench MVP
- backend test results
- frontend lint/build results
- real smoke result if completed in the implementation session

Use this structure:

```md
- 2026-04-13 HH:MM `terminal-bench-mvp`：完成 ttyd-backed terminal bench MVP，新增单会话 terminal session API、provider 生命周期管理与 frontend terminal panel；验证结果为 ...
```

- [ ] **Step 3: Run the full intended verification set**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_terminal_ttyd.py tests/test_api_terminal.py tests/test_api_auth.py tests/test_api_health.py tests/test_api_v1_routes.py tests/test_cli.py tests/test_server.py tests/test_execution_ssh.py -q
python -m compileall src/ainrf
cd frontend && npm run lint
cd frontend && npm run build
```

Expected:
- pytest PASS
- compileall PASS
- frontend lint PASS
- frontend build PASS (existing non-fatal Tailwind/lightningcss warnings may still appear)

- [ ] **Step 4: Perform real smoke validation**

Run this manual sequence:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf serve --host 127.0.0.1 --port 8000
```

Then in the browser/frontend:
- open the frontend shell
- start terminal session
- run `pwd`
- run `whoami`
- run `claude --version` if present
- stop the session
- start it again

Expected: terminal opens, commands execute, stop/start cycle works.

- [ ] **Step 5: Commit**

```bash
git add src/ainrf/README.md docs/LLM-Working/worklog/2026-04-13.md
git commit -m "docs: record terminal bench MVP verification"
```

---

## Spec Coverage Check

- **Terminal-first MVP:** covered by Tasks 2, 3, 4, and 7.
- **AINRF as control plane, ttyd as provider:** covered by Tasks 1–4.
- **Single target / single active session:** encoded in Tasks 1, 3, and 4.
- **Frontend launcher + status + embedded terminal view:** covered by Tasks 6 and 7.
- **Controlled security boundary and non-goals:** reflected in the limited three-endpoint API and absence of multi-session/project logic across all tasks.
- **Validation requirements:** covered by Task 8, including automated checks and real smoke.

## Self-review

- Placeholder scan: removed all TBD/TODO language from implementation steps.
- Type consistency: terminal session naming is consistent across backend (`TerminalSessionResponse`, `TerminalSessionStatus`) and frontend (`TerminalSession`, `TerminalSessionStatus`).
- Scope check: focused on a single terminal bench MVP rather than broader project/workspace/session management.
