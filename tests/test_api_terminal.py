from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import httpx
import pytest
from starlette.websockets import WebSocketState

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key


def test_terminal_session_record_supports_open_and_viewer_state() -> None:
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus

    session = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        browser_open_token="open-token",
        viewer_session_token="viewer-token",
        viewer_cookie_name="ainrf_terminal_viewer",
    )

    assert session.browser_open_token == "open-token"
    assert session.viewer_session_token == "viewer-token"
    assert session.viewer_cookie_name == "ainrf_terminal_viewer"


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
async def test_terminal_session_create_uses_api_config_for_lifecycle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

    captured: dict[str, object] = {}
    running = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=utc_now(),
        started_at=utc_now(),
        terminal_url="http://testserver/terminal/session/term-1/open?token=open-token",
        pid=4321,
        browser_open_token="open-token",
        browser_open_expires_at=utc_now() + timedelta(minutes=5),
        browser_open_consumed_at=None,
        viewer_session_token=None,
        viewer_session_expires_at=None,
        viewer_cookie_name="ainrf_terminal_viewer",
    )

    def fake_start_ttyd_session(**kwargs):
        captured.update(kwargs)
        return running

    monkeypatch.setattr("ainrf.api.routes.terminal.start_ttyd_session", fake_start_ttyd_session)

    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
            terminal_host="127.0.0.1",
            terminal_port=9001,
            terminal_command=("/bin/bash", "-lc", "pwd"),
        )
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.post("/terminal/session", headers={"X-API-Key": "secret-key"})

    assert response.status_code == 200
    assert captured == {
        "host": "127.0.0.1",
        "port": 9001,
        "auth_header_name": "X-AINRF-Terminal-Auth",
        "shell_command": ("/bin/bash", "-lc", "pwd"),
        "working_directory": tmp_path,
        "api_base_url": "http://testserver",
    }
    assert app.state.terminal_session == running
    assert response.json()["terminal_url"] == "http://testserver/terminal/session/term-1/open?token=open-token"


@pytest.mark.anyio
async def test_terminal_open_sets_viewer_cookie_and_redirects_to_proxy(
    tmp_path: Path,
) -> None:
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

    now = utc_now()
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
            terminal_host="127.0.0.1",
            terminal_port=9001,
        )
    )
    app.state.terminal_session = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=now,
        started_at=now,
        terminal_url="http://testserver/terminal/session/term-1/open?token=open-token",
        pid=4321,
        browser_open_token="open-token",
        browser_open_expires_at=now + timedelta(minutes=5),
        browser_open_consumed_at=None,
        viewer_session_token=None,
        viewer_session_expires_at=None,
        viewer_cookie_name="ainrf_terminal_viewer",
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
        follow_redirects=False,
    ) as client:
        response = await client.get("/terminal/session/term-1/open?token=open-token")

    assert response.status_code == 303
    assert response.headers["location"] == "/terminal/session/term-1/proxy/"
    assert "ainrf_terminal_viewer=" in response.headers["set-cookie"]
    assert app.state.terminal_session.browser_open_consumed_at is not None
    assert app.state.terminal_session.viewer_session_token is not None


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("token", "expires_delta", "consumed", "viewer_token", "expected_status"),
    [
        ("wrong-token", timedelta(minutes=5), None, None, 403),
        ("open-token", timedelta(minutes=-1), None, None, 410),
        ("open-token", timedelta(minutes=5), timedelta(seconds=1), None, 409),
        ("open-token", timedelta(minutes=5), None, "viewer-token", 409),
    ],
)
async def test_terminal_open_rejects_invalid_or_reused_state(
    tmp_path: Path,
    token: str,
    expires_delta: timedelta,
    consumed: timedelta | None,
    viewer_token: str | None,
    expected_status: int,
) -> None:
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

    now = utc_now()
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )
    app.state.terminal_session = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=now,
        started_at=now,
        terminal_url="http://testserver/terminal/session/term-1/open?token=open-token",
        browser_open_token="open-token",
        browser_open_expires_at=now + expires_delta,
        browser_open_consumed_at=now + consumed if consumed is not None else None,
        viewer_session_token=viewer_token,
        viewer_session_expires_at=now + timedelta(minutes=30) if viewer_token else None,
        viewer_cookie_name="ainrf_terminal_viewer",
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get(f"/terminal/session/term-1/open?token={token}")

    assert response.status_code == expected_status


@pytest.mark.anyio
async def test_terminal_proxy_requires_valid_viewer_cookie(tmp_path: Path) -> None:
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

    now = utc_now()
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )
    app.state.terminal_session = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=now,
        started_at=now,
        terminal_url="http://testserver/terminal/session/term-1/open?token=open-token",
        browser_open_token="open-token",
        browser_open_expires_at=now + timedelta(minutes=5),
        browser_open_consumed_at=now,
        viewer_session_token="viewer-token",
        viewer_session_expires_at=now + timedelta(minutes=30),
        viewer_cookie_name="ainrf_terminal_viewer",
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/terminal/session/term-1/proxy/")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_terminal_http_proxy_rejects_wrong_session_id(tmp_path: Path) -> None:
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

    now = utc_now()
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )
    app.state.terminal_session = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=now,
        started_at=now,
        terminal_url="http://testserver/terminal/session/term-1/open?token=open-token",
        browser_open_token="open-token",
        browser_open_expires_at=now + timedelta(minutes=5),
        browser_open_consumed_at=now,
        viewer_session_token="viewer-token",
        viewer_session_expires_at=now + timedelta(minutes=30),
        viewer_cookie_name="ainrf_terminal_viewer",
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
        cookies={"ainrf_terminal_viewer": "viewer-token"},
    ) as client:
        response = await client.get("/terminal/session/wrong-id/proxy/")

    assert response.status_code == 404


@pytest.mark.anyio
async def test_terminal_websocket_proxy_forwards_upstream_messages(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from ainrf.api.routes import terminal as terminal_routes
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

    now = utc_now()
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
            terminal_host="127.0.0.1",
            terminal_port=9001,
        )
    )
    app.state.terminal_session = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=now,
        started_at=now,
        terminal_url="http://testserver/terminal/session/term-1/open?token=open-token",
        browser_open_token="open-token",
        browser_open_expires_at=now + timedelta(minutes=5),
        browser_open_consumed_at=now,
        viewer_session_token="viewer-token",
        viewer_session_expires_at=now + timedelta(minutes=30),
        viewer_cookie_name="ainrf_terminal_viewer",
    )

    class FakeWebSocket:
        def __init__(self) -> None:
            self.app = app
            self.cookies = {"ainrf_terminal_viewer": "viewer-token"}
            self.client_state = WebSocketState.CONNECTED
            self.accepted = False
            self.closed_code: int | None = None
            self.sent_text: list[str] = []
            self._received_once = False

        async def accept(self) -> None:
            self.accepted = True

        async def receive(self) -> dict[str, str | None]:
            if not self._received_once:
                self._received_once = True
                return {"type": "websocket.disconnect", "text": None, "bytes": None}
            raise AssertionError("browser receive should stop after disconnect")

        async def send_text(self, message: str) -> None:
            self.sent_text.append(message)

        async def send_bytes(self, message: bytes) -> None:
            raise AssertionError(f"unexpected binary message: {message!r}")

        async def close(self, code: int = 1000) -> None:
            self.client_state = WebSocketState.DISCONNECTED
            self.closed_code = code

    class FakeUpstream:
        def __init__(self) -> None:
            self.sent: list[str | bytes] = []
            self._messages = iter(["upstream-ready"])

        async def send(self, message: str | bytes) -> None:
            self.sent.append(message)

        def __aiter__(self) -> "FakeUpstream":
            return self

        async def __anext__(self) -> str:
            try:
                return next(self._messages)
            except StopIteration as exc:
                raise StopAsyncIteration from exc

    upstream = FakeUpstream()

    class FakeConnect:
        def __init__(self, upstream_conn: FakeUpstream) -> None:
            self.upstream_conn = upstream_conn

        async def __aenter__(self) -> FakeUpstream:
            return self.upstream_conn

        async def __aexit__(self, exc_type, exc, tb) -> bool:
            return False

    monkeypatch.setattr(terminal_routes.websockets, "connect", lambda *args, **kwargs: FakeConnect(upstream))

    websocket = FakeWebSocket()

    await terminal_routes.proxy_terminal_websocket("term-1", websocket)  # type: ignore[arg-type]

    assert websocket.accepted is True
    assert websocket.sent_text == ["upstream-ready"]
    assert websocket.closed_code == 1000
    assert upstream.sent == []


@pytest.mark.anyio
async def test_terminal_websocket_proxy_rejects_wrong_session_id(tmp_path: Path) -> None:
    from ainrf.api.routes import terminal as terminal_routes
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

    now = utc_now()
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )
    app.state.terminal_session = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=now,
        started_at=now,
        terminal_url="http://testserver/terminal/session/term-1/open?token=open-token",
        browser_open_token="open-token",
        browser_open_expires_at=now + timedelta(minutes=5),
        browser_open_consumed_at=now,
        viewer_session_token="viewer-token",
        viewer_session_expires_at=now + timedelta(minutes=30),
        viewer_cookie_name="ainrf_terminal_viewer",
    )

    class FakeWebSocket:
        def __init__(self) -> None:
            self.app = app
            self.cookies = {"ainrf_terminal_viewer": "viewer-token"}
            self.client_state = WebSocketState.CONNECTED
            self.accepted = False
            self.closed_code: int | None = None

        async def accept(self) -> None:
            self.accepted = True

        async def receive(self) -> dict[str, str | None]:
            raise AssertionError("websocket should be closed before receiving")

        async def send_text(self, message: str) -> None:
            raise AssertionError(f"unexpected text message: {message!r}")

        async def send_bytes(self, message: bytes) -> None:
            raise AssertionError(f"unexpected binary message: {message!r}")

        async def close(self, code: int = 1000) -> None:
            self.client_state = WebSocketState.DISCONNECTED
            self.closed_code = code

    websocket = FakeWebSocket()

    await terminal_routes.proxy_terminal_websocket("wrong-id", websocket)  # type: ignore[arg-type]

    assert websocket.accepted is False
    assert websocket.closed_code == 4404


@pytest.mark.anyio
async def test_terminal_session_delete_stops_active_session_and_clears_browser_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

    running = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=utc_now(),
        started_at=utc_now(),
        terminal_url="http://testserver/terminal/session/term-1/open?token=open-token",
        pid=4321,
        browser_open_token="open-token",
        browser_open_expires_at=utc_now() + timedelta(minutes=5),
        browser_open_consumed_at=utc_now(),
        viewer_session_token="viewer-token",
        viewer_session_expires_at=utc_now() + timedelta(minutes=30),
        viewer_cookie_name="ainrf_terminal_viewer",
    )
    stopped = TerminalSessionRecord(
        session_id=None,
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.IDLE,
        closed_at=utc_now(),
        browser_open_token=None,
        browser_open_expires_at=None,
        browser_open_consumed_at=None,
        viewer_session_token=None,
        viewer_session_expires_at=None,
        viewer_cookie_name="ainrf_terminal_viewer",
    )
    captured: dict[str, object] = {}

    def fake_stop_ttyd_session(session: TerminalSessionRecord) -> TerminalSessionRecord:
        captured["session"] = session
        return stopped

    monkeypatch.setattr("ainrf.api.routes.terminal.stop_ttyd_session", fake_stop_ttyd_session)

    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )
    app.state.terminal_session = running

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.delete("/terminal/session", headers={"X-API-Key": "secret-key"})

    assert response.status_code == 200
    assert captured == {"session": running}
    assert app.state.terminal_session == stopped
    assert response.json()["status"] == "idle"
