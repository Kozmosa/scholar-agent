from __future__ import annotations

from collections import Counter
from collections.abc import Callable

import gradio as gr

from ainrf.api.schemas import ApiStatus, TaskSummaryResponse
from ainrf.state import TaskStage
from ainrf.webui.client import (
    AinrfApiClient,
    ApiAuthenticationError,
    ApiConnectionError,
    ApiProtocolError,
)
from ainrf.webui.models import ConnectionSession, TaskStageSummary, WebUiConfig

ApiClientFactory = Callable[[str, str], AinrfApiClient]

_APP_CSS = """
.app-shell {
  background:
    radial-gradient(circle at top left, rgba(45, 212, 191, 0.12), transparent 32%),
    linear-gradient(180deg, #f6fbfa 0%, #eef4f2 100%);
}
.status-card {
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 14px;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.88);
}
.status-ok {
  border-left: 4px solid #0f766e;
}
.status-warn {
  border-left: 4px solid #b45309;
}
.status-error {
  border-left: 4px solid #b91c1c;
}
"""


def create_webui(
    config: WebUiConfig,
    *,
    client_factory: ApiClientFactory | None = None,
) -> gr.Blocks:
    factory = client_factory or (lambda base_url, api_key: AinrfApiClient(base_url, api_key))
    initial_session = ConnectionSession(api_base_url=config.api_base_url)

    with gr.Blocks(
        title="AINRF WebUI",
        css=_APP_CSS,
        fill_width=True,
        elem_classes=["app-shell"],
    ) as demo:
        session_state = gr.State(initial_session)

        gr.Markdown(
            """
            # AINRF WebUI
            API-first project workbench for AINRF. W1 provides the connection layer and
            three-page shell only; Project persistence, run creation, and live event views arrive later.
            """
        )
        with gr.Row(equal_height=True):
            api_base_url = gr.Textbox(label="API Base URL", value=config.api_base_url, scale=3)
            api_key = gr.Textbox(label="API Key", type="password", scale=2)
            connect = gr.Button("Connect / Retry", variant="primary", min_width=180)

        status_banner = gr.Markdown(value=render_connection_banner(initial_session))
        health_panel = gr.Markdown(value=render_health_panel(initial_session))

        with gr.Tab("Project List"):
            project_list_summary = gr.Markdown(value=render_project_list_summary(initial_session))
            task_counts = gr.Dataframe(
                headers=["Stage", "Count"],
                datatype=["str", "number"],
                row_count=0,
                column_count=2,
                interactive=False,
                value=task_counts_rows(initial_session),
                label="Task Stage Counts",
            )

        with gr.Tab("Project Detail"):
            project_detail = gr.Markdown(value=render_project_detail_placeholder(initial_session))

        with gr.Tab("Run Detail"):
            run_detail = gr.Markdown(value=render_run_detail_placeholder(initial_session))

        connect.click(
            fn=lambda api_url, key, current_session: connect_session(
                api_url,
                key,
                current_session,
                client_factory=factory,
            ),
            inputs=[api_base_url, api_key, session_state],
            outputs=[
                session_state,
                status_banner,
                health_panel,
                project_list_summary,
                task_counts,
                project_detail,
                run_detail,
            ],
        )

    return demo


def launch_webui(config: WebUiConfig) -> None:
    demo = create_webui(config)
    demo.launch(server_name=config.host, server_port=config.port, show_error=True, inbrowser=False)


def connect_session(
    api_base_url: str,
    api_key: str,
    session: ConnectionSession,
    *,
    client_factory: ApiClientFactory | None = None,
) -> tuple[ConnectionSession, str, str, str, list[list[object]], str, str]:
    normalized_url = api_base_url.strip().rstrip("/")
    next_session = ConnectionSession(api_base_url=normalized_url, api_key=api_key)
    factory = client_factory or (lambda base_url, key: AinrfApiClient(base_url, key))
    client = factory(normalized_url, api_key)

    try:
        health = client.get_health()
        next_session.reachable = True
        next_session.health_status = health.status
        next_session.state_root = health.state_root
        next_session.container_configured = health.container_configured
        next_session.container_detail = health.detail
    except ApiConnectionError as exc:
        next_session.last_error = str(exc)
        return render_session(next_session)
    except ApiProtocolError as exc:
        next_session.last_error = str(exc)
        return render_session(next_session)

    try:
        task_list = client.list_tasks()
    except ApiAuthenticationError as exc:
        next_session.last_error = str(exc)
        return render_session(next_session)
    except (ApiConnectionError, ApiProtocolError) as exc:
        next_session.last_error = str(exc)
        return render_session(next_session)

    next_session.authenticated = True
    next_session.task_summaries = summarize_task_stages(task_list.items)
    next_session.total_tasks = len(task_list.items)
    next_session.last_error = None
    return render_session(next_session)


def summarize_task_stages(items: list[TaskSummaryResponse]) -> tuple[TaskStageSummary, ...]:
    counts = Counter(item.status for item in items)
    return tuple(TaskStageSummary(stage=stage, count=counts.get(stage, 0)) for stage in TaskStage)


def render_session(
    session: ConnectionSession,
) -> tuple[ConnectionSession, str, str, str, list[list[object]], str, str]:
    return (
        session,
        render_connection_banner(session),
        render_health_panel(session),
        render_project_list_summary(session),
        task_counts_rows(session),
        render_project_detail_placeholder(session),
        render_run_detail_placeholder(session),
    )


def render_connection_banner(session: ConnectionSession) -> str:
    if not session.reachable:
        detail = session.last_error or "Enter an API base URL and API key, then connect."
        return _status_card("Connection not established", detail, "status-error")
    if not session.authenticated:
        detail = session.last_error or "API is reachable, but the provided API key was rejected."
        return _status_card("API reachable, authentication failed", detail, "status-warn")
    if session.health_status is ApiStatus.DEGRADED:
        detail = session.container_detail or "API is reachable but container health is degraded."
        return _status_card("Connected with degraded backend health", detail, "status-warn")
    return _status_card(
        "Connected",
        f"Authenticated against {session.api_base_url}.",
        "status-ok",
    )


def render_health_panel(session: ConnectionSession) -> str:
    if not session.reachable:
        return (
            "## Health\n"
            "No backend health data yet. Connect to an AINRF API to inspect reachability and container health."
        )
    health_label = session.health_status.value if session.health_status is not None else "unknown"
    container_mode = "configured" if session.container_configured else "not configured"
    detail = session.container_detail or "No additional health detail."
    return (
        "## Health\n"
        f"- API base URL: `{session.api_base_url}`\n"
        f"- Health status: `{health_label}`\n"
        f"- State root: `{session.state_root or 'unknown'}`\n"
        f"- Container probe: `{container_mode}`\n"
        f"- Detail: {detail}"
    )


def render_project_list_summary(session: ConnectionSession) -> str:
    if not session.authenticated:
        return (
            "## Project List\n"
            "W1 does not persist Project records yet. Once connected, this view shows task-stage aggregates "
            "as the first project-level health signal."
        )
    return (
        "## Project List\n"
        f"- Authenticated to `{session.api_base_url}`\n"
        f"- Total tasks discovered: `{session.total_tasks}`\n"
        "- W2 will add Project persistence, defaults, and project-scoped task grouping."
    )


def render_project_detail_placeholder(session: ConnectionSession) -> str:
    if not session.authenticated:
        return (
            "## Project Detail\n"
            "No project selected. Connect to the API first; W2 will add local Project defaults and selection."
        )
    return (
        "## Project Detail\n"
        "No project selected. W1 fixes the shell only. W2 will populate this page with project defaults, "
        "run listings, and project-scoped actions."
    )


def render_run_detail_placeholder(session: ConnectionSession) -> str:
    if not session.authenticated:
        return (
            "## Run Detail\n"
            "No run selected. W1 does not yet expose run browsing or live task detail."
        )
    return (
        "## Run Detail\n"
        "No run selected. W3 will connect this page to task detail, gate actions, and event timeline views."
    )


def task_counts_rows(session: ConnectionSession) -> list[list[object]]:
    return [[summary.stage.value, summary.count] for summary in session.task_summaries]


def _status_card(title: str, detail: str, css_class: str) -> str:
    return (
        f"<div class='status-card {css_class}'>"
        f"<strong>{title}</strong><br/>{detail}"
        "</div>"
    )
