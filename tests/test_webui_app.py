from __future__ import annotations

from datetime import UTC, datetime

import gradio as gr

from ainrf.api.schemas import ApiStatus
from ainrf.state import TaskMode, TaskStage
from ainrf.webui.app import (
    connect_session,
    create_webui,
    render_connection_banner,
    render_project_detail_placeholder,
    render_project_list_summary,
    render_run_detail_placeholder,
    summarize_task_stages,
    task_counts_rows,
)
from ainrf.webui.client import (
    ApiAuthenticationError,
    ApiConnectionError,
)
from ainrf.webui.models import ConnectionSession, WebUiConfig
from ainrf.api.schemas import HealthResponse, TaskListResponse, TaskSummaryResponse


class FakeClient:
    def __init__(
        self,
        *,
        health: HealthResponse | None = None,
        task_list: TaskListResponse | None = None,
        error: Exception | None = None,
    ) -> None:
        self._health = health
        self._task_list = task_list
        self._error = error

    def get_health(self) -> HealthResponse:
        if self._error is not None:
            raise self._error
        assert self._health is not None
        return self._health

    def list_tasks(self, status: TaskStage | None = None) -> TaskListResponse:
        _ = status
        if self._error is not None:
            raise self._error
        assert self._task_list is not None
        return self._task_list


def build_task_summary(task_id: str, mode: TaskMode, status: TaskStage) -> TaskSummaryResponse:
    now = datetime(2026, 3, 16, tzinfo=UTC)
    return TaskSummaryResponse(
        task_id=task_id,
        mode=mode,
        status=status,
        created_at=now,
        updated_at=now,
        current_stage=status,
        termination_reason=None,
    )


def test_create_webui_returns_blocks() -> None:
    demo = create_webui(WebUiConfig())

    assert isinstance(demo, gr.Blocks)


def test_connect_session_handles_connection_error() -> None:
    session = ConnectionSession()

    rendered = connect_session(
        "http://ainrf.local",
        "secret",
        session,
        client_factory=lambda base_url, api_key: FakeClient(error=ApiConnectionError("unreachable")),
    )

    next_session = rendered[0]
    assert next_session.reachable is False
    assert "Connection not established" in rendered[1]


def test_connect_session_handles_auth_failure_after_health_probe() -> None:
    session = ConnectionSession()
    health = HealthResponse(
        status=ApiStatus.OK,
        state_root=".ainrf",
        container_configured=False,
        container_health=None,
        detail=None,
    )

    class AuthFailClient(FakeClient):
        def list_tasks(self, status: TaskStage | None = None) -> TaskListResponse:
            _ = status
            raise ApiAuthenticationError("Unauthorized")

    rendered = connect_session(
        "http://ainrf.local",
        "wrong",
        session,
        client_factory=lambda base_url, api_key: AuthFailClient(health=health),
    )

    next_session = rendered[0]
    assert next_session.reachable is True
    assert next_session.authenticated is False
    assert "authentication failed" in rendered[1]


def test_connect_session_renders_degraded_connected_state() -> None:
    health = HealthResponse(
        status=ApiStatus.DEGRADED,
        state_root=".ainrf",
        container_configured=True,
        container_health=None,
        detail="Container connectivity degraded",
    )
    task_list = TaskListResponse(
        items=[build_task_summary("t-001", TaskMode.DEEP_REPRODUCTION, TaskStage.PLANNING)]
    )

    rendered = connect_session(
        "http://ainrf.local/",
        "secret",
        ConnectionSession(),
        client_factory=lambda base_url, api_key: FakeClient(health=health, task_list=task_list),
    )

    next_session = rendered[0]
    assert next_session.reachable is True
    assert next_session.authenticated is True
    assert next_session.health_status is ApiStatus.DEGRADED
    assert next_session.api_base_url == "http://ainrf.local"
    assert rendered[4] == [[stage.value, 1 if stage is TaskStage.PLANNING else 0] for stage in TaskStage]


def test_task_stage_summary_helpers_cover_all_stages() -> None:
    summaries = summarize_task_stages(
        [
            build_task_summary("t-001", TaskMode.DEEP_REPRODUCTION, TaskStage.SUBMITTED),
            build_task_summary("t-002", TaskMode.LITERATURE_EXPLORATION, TaskStage.SUBMITTED),
        ]
    )

    rows = task_counts_rows(ConnectionSession(task_summaries=summaries))

    assert rows[0] == [TaskStage.SUBMITTED.value, 2]
    assert rows[-1] == [TaskStage.CANCELLED.value, 0]


def test_placeholder_renderers_switch_after_authentication() -> None:
    disconnected = ConnectionSession()
    connected = ConnectionSession(
        api_base_url="http://ainrf.local",
        reachable=True,
        authenticated=True,
        health_status=ApiStatus.OK,
        total_tasks=3,
    )

    assert "Project List" in render_project_list_summary(disconnected)
    assert "Total tasks discovered" in render_project_list_summary(connected)
    assert "W2 will populate" in render_project_detail_placeholder(connected)
    assert "W3 will connect" in render_run_detail_placeholder(connected)
    assert "Connected" in render_connection_banner(connected)
