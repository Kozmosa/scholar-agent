from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from datetime import UTC, datetime
import re
from typing import Any, TypeAlias
from typing import cast

import gradio as gr

from ainrf.api.schemas import (
    ApiStatus,
    ArtifactItemResponse,
    ModeTwoScope,
    TaskCreateRequest,
    TaskDetailResponse,
    TaskSummaryResponse,
)
from ainrf.artifacts import HumanGateStatus
from ainrf.events import TaskEvent
from ainrf.state import TaskMode, TaskStage
from ainrf.webui.client import (
    AinrfApiClient,
    ApiClientError,
    ApiAuthenticationError,
    ApiConnectionError,
    ApiProtocolError,
)
from ainrf.webui.models import (
    ContainerProfileRecord,
    ConnectionSession,
    ProjectDefaults,
    ProjectRecord,
    ProjectRunRecord,
    RunTimelineItem,
    TaskStageSummary,
    WebUiConfig,
)
from ainrf.webui.store import JsonProjectStore

ApiClientFactory = Callable[[str, str], AinrfApiClient]
ConnectionRenderResult: TypeAlias = tuple[Any, ...]
ProjectRenderResult: TypeAlias = tuple[Any, ...]
ProjectMutationRenderResult: TypeAlias = tuple[Any, ...]
RunSubmitRenderResult: TypeAlias = tuple[Any, ...]

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

_MODE_ONE_SEED_HEADERS = ["Title", "PDF URL", "PDF Path"]
_PROJECT_TABLE_HEADERS = ["Project", "Slug", "Runs", "Latest Status", "Updated At"]
_RUN_TABLE_HEADERS = ["Task ID", "Mode", "Status", "Stage", "Created At", "Papers"]
_TIMELINE_LIMIT = 12


def create_webui(
    config: WebUiConfig,
    *,
    client_factory: ApiClientFactory | None = None,
) -> gr.Blocks:
    factory = client_factory or (lambda base_url, api_key: AinrfApiClient(base_url, api_key))
    store = JsonProjectStore(config.state_root)
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
            API-first project workbench for AINRF. W2 adds local Project persistence and
            inline Run creation while keeping the API boundary unchanged.
            """
        )
        with gr.Row(equal_height=True):
            api_base_url = gr.Textbox(label="API Base URL", value=config.api_base_url, scale=3)
            api_key = gr.Textbox(label="API Key", type="password", scale=2)
            connect = gr.Button("Connect / Retry", variant="primary", min_width=180)

        status_banner = gr.Markdown(value=render_connection_banner(initial_session))
        health_panel = gr.Markdown(value=render_health_panel(initial_session))

        with gr.Row(equal_height=True):
            project_selector = gr.Dropdown(
                label="Active Project",
                choices=project_selector_choices(store),
                value=None,
                allow_custom_value=False,
                scale=3,
            )
            new_project = gr.Button("New Project", min_width=180)

        with gr.Tab("Project List"):
            project_list_summary = gr.Markdown(
                value=render_project_list_summary(initial_session, store)
            )
            project_table = gr.Dataframe(
                headers=_PROJECT_TABLE_HEADERS,
                datatype=["str", "str", "number", "str", "str"],
                column_count=5,
                interactive=False,
                value=project_table_rows(store),
                label="Local Projects",
            )

        with gr.Tab("Project Detail"):
            project_feedback = gr.Markdown(value="Ready to create or edit a local Project.")
            project_detail_summary = gr.Markdown(
                value=render_project_detail_summary(initial_session, store)
            )
            with gr.Row():
                project_name = gr.Textbox(label="Project Name")
                project_slug = gr.Textbox(label="Project Slug")
            project_description = gr.Textbox(label="Description", lines=3)
            gr.Markdown("### Container Profiles")
            container_profile_feedback = gr.Markdown(
                value="Container profiles are shared with CLI via `.ainrf/config.json`."
            )
            with gr.Row():
                container_profile_selector = gr.Dropdown(
                    label="Saved Container",
                    choices=container_profile_choices(store),
                    value=store.default_container_profile_name(),
                    allow_custom_value=False,
                    scale=3,
                )
                apply_container_profile_button = gr.Button("Apply to Project + Run", min_width=200)
            with gr.Row():
                container_profile_name = gr.Textbox(label="Profile Name")
                container_profile_host = gr.Textbox(label="Container Host")
                container_profile_port = gr.Number(label="Container Port", value=22, precision=0)
                container_profile_user = gr.Textbox(label="Container User")
            with gr.Row():
                container_profile_ssh_key_path = gr.Textbox(label="SSH Key Path")
                container_profile_ssh_password = gr.Textbox(label="SSH Password", type="password")
                container_profile_project_dir = gr.Textbox(label="Container Project Dir")
            container_profile_set_default = gr.Checkbox(
                label="Set as default container profile",
                value=False,
            )
            save_container_profile_button = gr.Button("Save Container Profile", variant="secondary")
            gr.Markdown("### Shared Defaults")
            with gr.Row():
                container_host = gr.Textbox(label="Container Host")
                container_port = gr.Number(label="Container Port", value=22, precision=0)
                container_user = gr.Textbox(label="Container User")
            with gr.Row():
                container_ssh_key_path = gr.Textbox(label="SSH Key Path")
                container_project_dir = gr.Textbox(label="Container Project Dir")
            with gr.Row():
                budget_gpu_hours = gr.Number(label="GPU Hours", value=None, precision=2)
                budget_api_cost_usd = gr.Number(label="API Cost USD", value=None, precision=2)
                budget_wall_clock_hours = gr.Number(
                    label="Wall Clock Hours", value=None, precision=2
                )
            with gr.Row():
                webhook_url = gr.Textbox(label="Default Webhook URL")
                default_yolo = gr.Checkbox(label="Default Yolo", value=False)
            gr.Markdown("### Mode 1 Template")
            mode_one_domain_context = gr.Textbox(label="Domain Context", lines=2)
            with gr.Row():
                mode_one_max_depth = gr.Number(label="Max Depth", value=3, precision=0)
                mode_one_focus_directions = gr.Textbox(label="Focus Directions", lines=2)
                mode_one_ignore_directions = gr.Textbox(label="Ignore Directions", lines=2)
            gr.Markdown("### Mode 2 Template")
            with gr.Row():
                mode_two_scope = gr.Dropdown(
                    label="Mode 2 Scope",
                    choices=[scope.value for scope in ModeTwoScope],
                    value=ModeTwoScope.CORE_ONLY.value,
                )
                mode_two_baseline_first = gr.Checkbox(label="Baseline First", value=True)
            mode_two_target_tables = gr.Textbox(label="Target Tables", lines=2)
            save_project_button = gr.Button("Save Project", variant="primary")

            gr.Markdown("### Runs")
            project_runs = gr.Dataframe(
                headers=_RUN_TABLE_HEADERS,
                datatype=["str", "str", "str", "str", "str", "str"],
                column_count=6,
                interactive=False,
                value=[],
                label="Runs in Active Project",
            )
            run_selector = gr.Dropdown(
                label="Active Run",
                choices=run_selector_choices(store, None),
                value=None,
                allow_custom_value=False,
            )
            run_feedback = gr.Markdown(value="Select a Project to create a Run.")
            with gr.Row():
                run_mode = gr.Radio(
                    label="Run Mode",
                    choices=[
                        ("Mode 2", TaskMode.DEEP_REPRODUCTION.value),
                        ("Mode 1", TaskMode.RESEARCH_DISCOVERY.value),
                    ],
                    value=TaskMode.DEEP_REPRODUCTION.value,
                )
                run_yolo = gr.Checkbox(label="Run Yolo", value=False)
            with gr.Row():
                run_container_host = gr.Textbox(label="Run Container Host")
                run_container_port = gr.Number(label="Run Container Port", value=22, precision=0)
                run_container_user = gr.Textbox(label="Run Container User")
            with gr.Row():
                run_container_ssh_key_path = gr.Textbox(label="Run SSH Key Path")
                run_container_project_dir = gr.Textbox(label="Run Container Project Dir")
            with gr.Row():
                run_budget_gpu_hours = gr.Number(label="Run GPU Hours", value=None, precision=2)
                run_budget_api_cost_usd = gr.Number(
                    label="Run API Cost USD", value=None, precision=2
                )
                run_budget_wall_clock_hours = gr.Number(
                    label="Run Wall Clock Hours", value=None, precision=2
                )
            with gr.Row():
                run_webhook_url = gr.Textbox(label="Run Webhook URL")
                run_webhook_secret = gr.Textbox(label="Run Webhook Secret", type="password")
            gr.Markdown("#### Mode 1 Papers")
            mode_one_seed_papers = gr.Dataframe(
                headers=_MODE_ONE_SEED_HEADERS,
                datatype=["str", "str", "str"],
                row_count=5,
                column_count=3,
                interactive=True,
                value=empty_seed_rows(),
                label="Seed Papers",
            )
            with gr.Row():
                run_mode_one_domain_context = gr.Textbox(label="Run Mode 1 Domain Context", lines=2)
                run_mode_one_max_depth = gr.Number(
                    label="Run Mode 1 Max Depth", value=3, precision=0
                )
            with gr.Row():
                run_mode_one_focus_directions = gr.Textbox(
                    label="Run Mode 1 Focus Directions", lines=2
                )
                run_mode_one_ignore_directions = gr.Textbox(
                    label="Run Mode 1 Ignore Directions", lines=2
                )
            gr.Markdown("#### Mode 2 Target")
            mode_two_title = gr.Textbox(label="Target Paper Title")
            with gr.Row():
                mode_two_pdf_url = gr.Textbox(label="Target PDF URL")
                mode_two_pdf_path = gr.Textbox(label="Target PDF Path")
            with gr.Row():
                run_mode_two_scope = gr.Dropdown(
                    label="Run Mode 2 Scope",
                    choices=[scope.value for scope in ModeTwoScope],
                    value=ModeTwoScope.CORE_ONLY.value,
                )
                run_mode_two_baseline_first = gr.Checkbox(
                    label="Run Mode 2 Baseline First", value=True
                )
            run_mode_two_target_tables = gr.Textbox(label="Run Mode 2 Target Tables", lines=2)
            submit_run_button = gr.Button("Create Run", variant="primary")

        with gr.Tab("Run Detail"):
            with gr.Row():
                refresh_run_button = gr.Button("Refresh Run Detail", variant="secondary")
                approve_run_button = gr.Button("Approve Gate", variant="primary")
                reject_run_button = gr.Button("Reject Gate", variant="stop")
            reject_feedback = gr.Textbox(label="Reject Feedback", lines=2)
            run_detail = gr.Markdown(value=render_run_detail(initial_session, store))

        connect_outputs = [
            session_state,
            status_banner,
            health_panel,
            project_selector,
            project_list_summary,
            project_table,
            project_feedback,
            project_detail_summary,
            project_runs,
            run_selector,
            run_feedback,
            run_detail,
        ]
        connect.click(
            fn=lambda api_url, key, current_session: connect_and_render(
                api_url,
                key,
                current_session,
                store,
                client_factory=factory,
            ),
            inputs=[api_base_url, api_key, session_state],
            outputs=connect_outputs,
        )

        selection_outputs = [
            session_state,
            project_feedback,
            project_detail_summary,
            project_name,
            project_slug,
            project_description,
            container_host,
            container_port,
            container_user,
            container_ssh_key_path,
            container_project_dir,
            budget_gpu_hours,
            budget_api_cost_usd,
            budget_wall_clock_hours,
            webhook_url,
            default_yolo,
            mode_one_domain_context,
            mode_one_max_depth,
            mode_one_focus_directions,
            mode_one_ignore_directions,
            mode_two_scope,
            mode_two_target_tables,
            mode_two_baseline_first,
            project_runs,
            run_selector,
            run_feedback,
            run_mode,
            run_container_host,
            run_container_port,
            run_container_user,
            run_container_ssh_key_path,
            run_container_project_dir,
            run_budget_gpu_hours,
            run_budget_api_cost_usd,
            run_budget_wall_clock_hours,
            run_webhook_url,
            run_webhook_secret,
            run_yolo,
            mode_one_seed_papers,
            run_mode_one_domain_context,
            run_mode_one_max_depth,
            run_mode_one_focus_directions,
            run_mode_one_ignore_directions,
            mode_two_title,
            mode_two_pdf_url,
            mode_two_pdf_path,
            run_mode_two_scope,
            run_mode_two_target_tables,
            run_mode_two_baseline_first,
            run_detail,
        ]
        project_selector.change(
            fn=lambda slug, current_session: select_project_and_render(
                current_session,
                store,
                slug,
                client_factory=factory,
            ),
            inputs=[project_selector, session_state],
            outputs=selection_outputs,
        )

        new_project.click(
            fn=lambda current_session: reset_project_and_render(current_session, store),
            inputs=[session_state],
            outputs=selection_outputs,
        )

        container_profile_selector.change(
            fn=lambda profile_name: select_container_profile_and_render(
                store,
                profile_name,
            ),
            inputs=[container_profile_selector],
            outputs=[
                container_profile_name,
                container_profile_host,
                container_profile_port,
                container_profile_user,
                container_profile_ssh_key_path,
                container_profile_ssh_password,
                container_profile_project_dir,
                container_profile_feedback,
            ],
        )

        save_container_profile_button.click(
            fn=lambda profile_name, host_value, port_value, user_value, ssh_key_value, ssh_password_value, project_dir_value, set_default_value: (
                save_container_profile_and_render(
                    store,
                    profile_name=profile_name,
                    host=host_value,
                    port=port_value,
                    user=user_value,
                    ssh_key_path=ssh_key_value,
                    ssh_password=ssh_password_value,
                    project_dir=project_dir_value,
                    set_default=set_default_value,
                )
            ),
            inputs=[
                container_profile_name,
                container_profile_host,
                container_profile_port,
                container_profile_user,
                container_profile_ssh_key_path,
                container_profile_ssh_password,
                container_profile_project_dir,
                container_profile_set_default,
            ],
            outputs=[container_profile_selector, container_profile_feedback],
        )

        apply_container_profile_button.click(
            fn=lambda profile_name, project_host, project_port, project_user, project_ssh_key, project_dir, run_host, run_port, run_user, run_ssh_key, run_dir: (
                apply_container_profile_and_render(
                    store,
                    profile_name=profile_name,
                    current_project_host=project_host,
                    current_project_port=project_port,
                    current_project_user=project_user,
                    current_project_ssh_key_path=project_ssh_key,
                    current_project_dir=project_dir,
                    current_run_host=run_host,
                    current_run_port=run_port,
                    current_run_user=run_user,
                    current_run_ssh_key_path=run_ssh_key,
                    current_run_dir=run_dir,
                )
            ),
            inputs=[
                container_profile_selector,
                container_host,
                container_port,
                container_user,
                container_ssh_key_path,
                container_project_dir,
                run_container_host,
                run_container_port,
                run_container_user,
                run_container_ssh_key_path,
                run_container_project_dir,
            ],
            outputs=[
                container_host,
                container_port,
                container_user,
                container_ssh_key_path,
                container_project_dir,
                run_container_host,
                run_container_port,
                run_container_user,
                run_container_ssh_key_path,
                run_container_project_dir,
                container_profile_feedback,
            ],
        )

        save_project_outputs = [
            session_state,
            project_selector,
            project_list_summary,
            project_table,
            *selection_outputs[1:],
        ]
        save_project_button.click(
            fn=lambda current_session, name, slug, description, host_value, port_value, user_value, ssh_key_value, project_dir_value, gpu_value, api_cost_value, wall_value, webhook_value, yolo_value, mode_one_domain_value, mode_one_depth_value, mode_one_focus_value, mode_one_ignore_value, mode_two_scope_value, mode_two_tables_value, mode_two_baseline_value: (
                save_project_and_render(
                    current_session,
                    store,
                    name=name,
                    slug=slug,
                    description=description,
                    container_host=host_value,
                    container_port=port_value,
                    container_user=user_value,
                    container_ssh_key_path=ssh_key_value,
                    container_project_dir=project_dir_value,
                    budget_gpu_hours=gpu_value,
                    budget_api_cost_usd=api_cost_value,
                    budget_wall_clock_hours=wall_value,
                    webhook_url=webhook_value,
                    yolo=yolo_value,
                    mode_one_domain_context=mode_one_domain_value,
                    mode_one_max_depth=mode_one_depth_value,
                    mode_one_focus_directions=mode_one_focus_value,
                    mode_one_ignore_directions=mode_one_ignore_value,
                    mode_two_scope=mode_two_scope_value,
                    mode_two_target_tables=mode_two_tables_value,
                    mode_two_baseline_first=mode_two_baseline_value,
                )
            ),
            inputs=[
                session_state,
                project_name,
                project_slug,
                project_description,
                container_host,
                container_port,
                container_user,
                container_ssh_key_path,
                container_project_dir,
                budget_gpu_hours,
                budget_api_cost_usd,
                budget_wall_clock_hours,
                webhook_url,
                default_yolo,
                mode_one_domain_context,
                mode_one_max_depth,
                mode_one_focus_directions,
                mode_one_ignore_directions,
                mode_two_scope,
                mode_two_target_tables,
                mode_two_baseline_first,
            ],
            outputs=save_project_outputs,
        )

        submit_run_button.click(
            fn=lambda current_session, selected_mode, run_host, run_port, run_user, run_ssh_key, run_project_dir, run_gpu, run_api_cost, run_wall, run_webhook, run_secret, run_yolo_value, seed_rows, run_mode_one_domain_value, run_mode_one_depth_value, run_mode_one_focus_value, run_mode_one_ignore_value, target_title, target_url, target_path, run_mode_two_scope_value, run_mode_two_tables_value, run_mode_two_baseline_value: (
                submit_run_and_render(
                    current_session,
                    store,
                    client_factory=factory,
                    mode=selected_mode,
                    run_container_host=run_host,
                    run_container_port=run_port,
                    run_container_user=run_user,
                    run_container_ssh_key_path=run_ssh_key,
                    run_container_project_dir=run_project_dir,
                    run_budget_gpu_hours=run_gpu,
                    run_budget_api_cost_usd=run_api_cost,
                    run_budget_wall_clock_hours=run_wall,
                    run_webhook_url=run_webhook,
                    run_webhook_secret=run_secret,
                    run_yolo=run_yolo_value,
                    mode_one_seed_rows=seed_rows,
                    run_mode_one_domain_context=run_mode_one_domain_value,
                    run_mode_one_max_depth=run_mode_one_depth_value,
                    run_mode_one_focus_directions=run_mode_one_focus_value,
                    run_mode_one_ignore_directions=run_mode_one_ignore_value,
                    mode_two_title=target_title,
                    mode_two_pdf_url=target_url,
                    mode_two_pdf_path=target_path,
                    run_mode_two_scope=run_mode_two_scope_value,
                    run_mode_two_target_tables=run_mode_two_tables_value,
                    run_mode_two_baseline_first=run_mode_two_baseline_value,
                )
            ),
            inputs=[
                session_state,
                run_mode,
                run_container_host,
                run_container_port,
                run_container_user,
                run_container_ssh_key_path,
                run_container_project_dir,
                run_budget_gpu_hours,
                run_budget_api_cost_usd,
                run_budget_wall_clock_hours,
                run_webhook_url,
                run_webhook_secret,
                run_yolo,
                mode_one_seed_papers,
                run_mode_one_domain_context,
                run_mode_one_max_depth,
                run_mode_one_focus_directions,
                run_mode_one_ignore_directions,
                mode_two_title,
                mode_two_pdf_url,
                mode_two_pdf_path,
                run_mode_two_scope,
                run_mode_two_target_tables,
                run_mode_two_baseline_first,
            ],
            outputs=[
                session_state,
                project_list_summary,
                project_table,
                project_runs,
                run_selector,
                run_feedback,
                run_detail,
            ],
        )

        run_selector.change(
            fn=lambda task_id, current_session: select_run_and_render(
                current_session,
                store,
                task_id,
                client_factory=factory,
            ),
            inputs=[run_selector, session_state],
            outputs=[session_state, run_selector, run_feedback, run_detail],
        )

        refresh_run_button.click(
            fn=lambda current_session: refresh_run_and_render(
                current_session,
                store,
                client_factory=factory,
            ),
            inputs=[session_state],
            outputs=[
                session_state,
                project_list_summary,
                project_table,
                project_runs,
                run_selector,
                run_feedback,
                run_detail,
            ],
        )

        approve_run_button.click(
            fn=lambda current_session: approve_run_and_render(
                current_session,
                store,
                client_factory=factory,
            ),
            inputs=[session_state],
            outputs=[
                session_state,
                project_list_summary,
                project_table,
                project_runs,
                run_selector,
                run_feedback,
                run_detail,
            ],
        )

        reject_run_button.click(
            fn=lambda current_session, feedback: reject_run_and_render(
                current_session,
                store,
                feedback,
                client_factory=factory,
            ),
            inputs=[session_state, reject_feedback],
            outputs=[
                session_state,
                project_list_summary,
                project_table,
                project_runs,
                run_selector,
                run_feedback,
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
    store: JsonProjectStore | None = None,
    client_factory: ApiClientFactory | None = None,
) -> ConnectionSession:
    normalized_url = api_base_url.strip().rstrip("/")
    next_session = ConnectionSession(
        api_base_url=normalized_url,
        api_key=api_key,
        selected_project_slug=session.selected_project_slug,
        selected_run_task_id=session.selected_run_task_id,
        selected_run_detail=session.selected_run_detail,
        run_timeline_items=session.run_timeline_items,
        last_event_id_by_task=dict(session.last_event_id_by_task),
        run_event_mode=session.run_event_mode,
        run_refresh_error=session.run_refresh_error,
    )
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
        return next_session
    except ApiProtocolError as exc:
        next_session.last_error = str(exc)
        return next_session

    try:
        task_list = client.list_tasks()
    except ApiAuthenticationError as exc:
        next_session.last_error = str(exc)
        return next_session
    except (ApiConnectionError, ApiProtocolError) as exc:
        next_session.last_error = str(exc)
        return next_session

    next_session.authenticated = True
    next_session.task_summaries = summarize_task_stages(task_list.items)
    next_session.total_tasks = len(task_list.items)
    next_session.last_error = None

    if store is not None:
        store.synchronize_task_summaries(task_list.items)
        projects = store.list_projects()
        if next_session.selected_project_slug is None and projects:
            next_session.selected_project_slug = projects[0].slug
        if (
            next_session.selected_project_slug
            and store.load_project(next_session.selected_project_slug) is None
        ):
            next_session.selected_project_slug = None
        if next_session.selected_project_slug:
            project_runs = store.list_project_runs(next_session.selected_project_slug)
            next_session.selected_run_task_id = project_runs[0].task_id if project_runs else None
        if next_session.selected_run_task_id is None:
            clear_run_observation(next_session)
    return next_session


def summarize_task_stages(items: list[TaskSummaryResponse]) -> tuple[TaskStageSummary, ...]:
    counts = Counter(item.status for item in items)
    return tuple(TaskStageSummary(stage=stage, count=counts.get(stage, 0)) for stage in TaskStage)


def connect_and_render(
    api_base_url: str,
    api_key: str,
    session: ConnectionSession,
    store: JsonProjectStore,
    *,
    client_factory: ApiClientFactory,
) -> ConnectionRenderResult:
    next_session = connect_session(
        api_base_url,
        api_key,
        session,
        store=store,
        client_factory=client_factory,
    )
    if next_session.authenticated and next_session.selected_run_task_id is not None:
        next_session = refresh_selected_run(next_session, store, client_factory=client_factory)
    feedback = "Connected to API." if next_session.authenticated else "Connection updated."
    return render_connection_outputs(next_session, store, project_feedback=feedback)


def clear_run_observation(session: ConnectionSession) -> ConnectionSession:
    session.selected_run_detail = None
    session.selected_run_artifacts = ()
    session.run_timeline_items = ()
    session.run_event_mode = None
    session.run_refresh_error = None
    return session


def refresh_selected_run(
    session: ConnectionSession,
    store: JsonProjectStore,
    *,
    client_factory: ApiClientFactory,
) -> ConnectionSession:
    task_id = session.selected_run_task_id
    if not session.authenticated or task_id is None:
        return clear_run_observation(session)

    client = client_factory(session.api_base_url, session.api_key)
    previous_detail = session.selected_run_detail
    if previous_detail is None or previous_detail.task_id != task_id:
        session.run_timeline_items = ()
        session.run_refresh_error = None

    try:
        detail = client.get_task(task_id)
    except ApiClientError as exc:
        session.selected_run_detail = None
        session.selected_run_artifacts = ()
        session.run_refresh_error = f"Failed to load run detail: {exc}"
        return session

    session.selected_run_detail = detail
    try:
        artifacts = client.list_task_artifacts(task_id)
        session.selected_run_artifacts = tuple(artifacts.items)
    except ApiClientError:
        # Keep detail visible even if artifact detail fetch fails.
        session.selected_run_artifacts = ()
    store.update_project_run_status(
        task_id,
        status=detail.status,
        stage=detail.current_stage,
        termination_reason=detail.termination_reason,
    )

    after_id = session.last_event_id_by_task.get(task_id)
    if previous_detail is None or previous_detail.task_id != task_id:
        after_id = None

    try:
        events = client.list_task_events(task_id, after_id=after_id)
        session.run_event_mode = "sse"
        session.run_refresh_error = None
        session.run_timeline_items = merge_timeline_items(
            session.run_timeline_items, events, reset=after_id is None
        )
        if events:
            session.last_event_id_by_task[task_id] = events[-1].event_id
    except ApiClientError as exc:
        session.run_event_mode = "polling"
        session.run_refresh_error = (
            "Event stream unavailable; keeping detail view in manual refresh fallback mode. "
            f"Cause: {exc}"
        )
    return session


def merge_timeline_items(
    existing: tuple[RunTimelineItem, ...],
    events: list[TaskEvent],
    *,
    reset: bool,
) -> tuple[RunTimelineItem, ...]:
    base = [] if reset else list(existing)
    seen_ids = {item.event_id for item in base}
    for event in events:
        if event.event_id in seen_ids:
            continue
        base.append(
            RunTimelineItem(
                event_id=event.event_id,
                event=event.event,
                category=event.category,
                created_at=event.timestamp,
                payload=event.payload,
            )
        )
        seen_ids.add(event.event_id)
    return tuple(base[-_TIMELINE_LIMIT:])


def select_project_and_render(
    session: ConnectionSession,
    store: JsonProjectStore,
    selected_slug: str | None,
    *,
    client_factory: ApiClientFactory,
) -> ProjectRenderResult:
    next_session = session
    next_session.selected_project_slug = selected_slug or None
    if next_session.selected_project_slug:
        runs = store.list_project_runs(next_session.selected_project_slug)
        next_session.selected_run_task_id = runs[0].task_id if runs else None
    else:
        next_session.selected_run_task_id = None
    clear_run_observation(next_session)
    if next_session.authenticated and next_session.selected_run_task_id is not None:
        next_session = refresh_selected_run(next_session, store, client_factory=client_factory)
    return render_project_outputs(
        next_session, store, project_feedback="Project selection updated."
    )


def reset_project_and_render(
    session: ConnectionSession,
    store: JsonProjectStore,
) -> ProjectRenderResult:
    next_session = session
    next_session.selected_project_slug = None
    next_session.selected_run_task_id = None
    clear_run_observation(next_session)
    return render_project_outputs(
        next_session, store, project_feedback="Creating a new local Project."
    )


def save_project_from_form(
    session: ConnectionSession,
    store: JsonProjectStore,
    *,
    name: str,
    slug: str,
    description: str,
    container_host: str,
    container_port: float | int | None,
    container_user: str,
    container_ssh_key_path: str,
    container_project_dir: str,
    budget_gpu_hours: float | None,
    budget_api_cost_usd: float | None,
    budget_wall_clock_hours: float | None,
    webhook_url: str,
    yolo: bool,
    mode_one_domain_context: str,
    mode_one_max_depth: float | int | None,
    mode_one_focus_directions: str,
    mode_one_ignore_directions: str,
    mode_two_scope: str,
    mode_two_target_tables: str,
    mode_two_baseline_first: bool,
) -> tuple[ConnectionSession, str]:
    normalized_name = name.strip()
    if not normalized_name:
        return session, "Project name is required."

    effective_slug = normalize_project_slug(slug, normalized_name)
    if not effective_slug:
        return session, "Project slug must contain letters or numbers."
    if session.selected_project_slug and session.selected_project_slug != effective_slug:
        return session, "Project slug is immutable after creation."

    existing = store.load_project(effective_slug)
    defaults = ProjectDefaults.model_validate(
        {
            "container_host": container_host.strip(),
            "container_port": coerce_int(container_port, 22),
            "container_user": container_user.strip(),
            "container_ssh_key_path": container_ssh_key_path.strip(),
            "container_project_dir": container_project_dir.strip(),
            "budget_gpu_hours": budget_gpu_hours,
            "budget_api_cost_usd": budget_api_cost_usd,
            "budget_wall_clock_hours": budget_wall_clock_hours,
            "webhook_url": webhook_url.strip(),
            "yolo": yolo,
            "mode_1": {
                "domain_context": mode_one_domain_context.strip(),
                "max_depth": coerce_int(mode_one_max_depth, 3),
                "focus_directions": split_text_list(mode_one_focus_directions),
                "ignore_directions": split_text_list(mode_one_ignore_directions),
            },
            "mode_2": {
                "scope": mode_two_scope,
                "target_tables": split_text_list(mode_two_target_tables),
                "baseline_first": mode_two_baseline_first,
            },
        }
    )
    created_at = existing.created_at if existing is not None else datetime.now(UTC)
    project = ProjectRecord(
        slug=effective_slug,
        name=normalized_name,
        description=description.strip(),
        defaults=defaults,
        created_at=created_at,
        updated_at=datetime.now(UTC),
    )
    store.save_project(project)

    next_session = session
    next_session.selected_project_slug = effective_slug
    runs = store.list_project_runs(effective_slug)
    next_session.selected_run_task_id = runs[0].task_id if runs else None
    clear_run_observation(next_session)
    return next_session, f"Saved Project `{effective_slug}`."


def save_project_and_render(
    session: ConnectionSession,
    store: JsonProjectStore,
    *,
    name: str,
    slug: str,
    description: str,
    container_host: str,
    container_port: float | int | None,
    container_user: str,
    container_ssh_key_path: str,
    container_project_dir: str,
    budget_gpu_hours: float | None,
    budget_api_cost_usd: float | None,
    budget_wall_clock_hours: float | None,
    webhook_url: str,
    yolo: bool,
    mode_one_domain_context: str,
    mode_one_max_depth: float | int | None,
    mode_one_focus_directions: str,
    mode_one_ignore_directions: str,
    mode_two_scope: str,
    mode_two_target_tables: str,
    mode_two_baseline_first: bool,
) -> ProjectMutationRenderResult:
    next_session, feedback = save_project_from_form(
        session,
        store,
        name=name,
        slug=slug,
        description=description,
        container_host=container_host,
        container_port=container_port,
        container_user=container_user,
        container_ssh_key_path=container_ssh_key_path,
        container_project_dir=container_project_dir,
        budget_gpu_hours=budget_gpu_hours,
        budget_api_cost_usd=budget_api_cost_usd,
        budget_wall_clock_hours=budget_wall_clock_hours,
        webhook_url=webhook_url,
        yolo=yolo,
        mode_one_domain_context=mode_one_domain_context,
        mode_one_max_depth=mode_one_max_depth,
        mode_one_focus_directions=mode_one_focus_directions,
        mode_one_ignore_directions=mode_one_ignore_directions,
        mode_two_scope=mode_two_scope,
        mode_two_target_tables=mode_two_target_tables,
        mode_two_baseline_first=mode_two_baseline_first,
    )
    return render_after_project_mutation(next_session, store, feedback)


def submit_project_run(
    session: ConnectionSession,
    store: JsonProjectStore,
    *,
    client_factory: ApiClientFactory,
    mode: str,
    run_container_host: str,
    run_container_port: float | int | None,
    run_container_user: str,
    run_container_ssh_key_path: str,
    run_container_project_dir: str,
    run_budget_gpu_hours: float | None,
    run_budget_api_cost_usd: float | None,
    run_budget_wall_clock_hours: float | None,
    run_webhook_url: str,
    run_webhook_secret: str,
    run_yolo: bool,
    mode_one_seed_rows: list[list[object]] | None,
    run_mode_one_domain_context: str,
    run_mode_one_max_depth: float | int | None,
    run_mode_one_focus_directions: str,
    run_mode_one_ignore_directions: str,
    mode_two_title: str,
    mode_two_pdf_url: str,
    mode_two_pdf_path: str,
    run_mode_two_scope: str,
    run_mode_two_target_tables: str,
    run_mode_two_baseline_first: bool,
) -> tuple[ConnectionSession, str]:
    if not session.authenticated:
        return session, "Connect to the API before creating a Run."
    if session.selected_project_slug is None:
        return session, "Select or create a Project before creating a Run."

    project = store.load_project(session.selected_project_slug)
    if project is None:
        return session, "Selected Project no longer exists."

    try:
        payload = build_task_create_request(
            project=project,
            mode=mode,
            run_container_host=run_container_host,
            run_container_port=run_container_port,
            run_container_user=run_container_user,
            run_container_ssh_key_path=run_container_ssh_key_path,
            run_container_project_dir=run_container_project_dir,
            run_budget_gpu_hours=run_budget_gpu_hours,
            run_budget_api_cost_usd=run_budget_api_cost_usd,
            run_budget_wall_clock_hours=run_budget_wall_clock_hours,
            run_webhook_url=run_webhook_url,
            run_webhook_secret=run_webhook_secret,
            run_yolo=run_yolo,
            mode_one_seed_rows=mode_one_seed_rows,
            run_mode_one_domain_context=run_mode_one_domain_context,
            run_mode_one_max_depth=run_mode_one_max_depth,
            run_mode_one_focus_directions=run_mode_one_focus_directions,
            run_mode_one_ignore_directions=run_mode_one_ignore_directions,
            mode_two_title=mode_two_title,
            mode_two_pdf_url=mode_two_pdf_url,
            mode_two_pdf_path=mode_two_pdf_path,
            run_mode_two_scope=run_mode_two_scope,
            run_mode_two_target_tables=run_mode_two_target_tables,
            run_mode_two_baseline_first=run_mode_two_baseline_first,
        )
    except ValueError as exc:
        return session, str(exc)

    client = client_factory(session.api_base_url, session.api_key)
    try:
        response = client.create_task(payload)
    except (ApiAuthenticationError, ApiConnectionError, ApiProtocolError) as exc:
        return session, f"Failed to create Run: {exc}"

    paper_titles = [paper.title for paper in payload.papers]
    binding = ProjectRunRecord(
        task_id=response.task_id,
        project_slug=project.slug,
        mode=payload.mode,
        paper_titles=paper_titles,
        last_known_status=response.status,
        last_known_stage=response.status,
    )
    store.save_project_run(binding)

    next_session = connect_session(
        session.api_base_url,
        session.api_key,
        session,
        store=store,
        client_factory=client_factory,
    )
    next_session.selected_project_slug = project.slug
    next_session.selected_run_task_id = response.task_id
    next_session = refresh_selected_run(next_session, store, client_factory=client_factory)
    return next_session, f"Created Run `{response.task_id}` for Project `{project.slug}`."


def submit_run_and_render(
    session: ConnectionSession,
    store: JsonProjectStore,
    *,
    client_factory: ApiClientFactory,
    mode: str,
    run_container_host: str,
    run_container_port: float | int | None,
    run_container_user: str,
    run_container_ssh_key_path: str,
    run_container_project_dir: str,
    run_budget_gpu_hours: float | None,
    run_budget_api_cost_usd: float | None,
    run_budget_wall_clock_hours: float | None,
    run_webhook_url: str,
    run_webhook_secret: str,
    run_yolo: bool,
    mode_one_seed_rows: list[list[object]] | None,
    run_mode_one_domain_context: str,
    run_mode_one_max_depth: float | int | None,
    run_mode_one_focus_directions: str,
    run_mode_one_ignore_directions: str,
    mode_two_title: str,
    mode_two_pdf_url: str,
    mode_two_pdf_path: str,
    run_mode_two_scope: str,
    run_mode_two_target_tables: str,
    run_mode_two_baseline_first: bool,
) -> RunSubmitRenderResult:
    next_session, feedback = submit_project_run(
        session,
        store,
        client_factory=client_factory,
        mode=mode,
        run_container_host=run_container_host,
        run_container_port=run_container_port,
        run_container_user=run_container_user,
        run_container_ssh_key_path=run_container_ssh_key_path,
        run_container_project_dir=run_container_project_dir,
        run_budget_gpu_hours=run_budget_gpu_hours,
        run_budget_api_cost_usd=run_budget_api_cost_usd,
        run_budget_wall_clock_hours=run_budget_wall_clock_hours,
        run_webhook_url=run_webhook_url,
        run_webhook_secret=run_webhook_secret,
        run_yolo=run_yolo,
        mode_one_seed_rows=mode_one_seed_rows,
        run_mode_one_domain_context=run_mode_one_domain_context,
        run_mode_one_max_depth=run_mode_one_max_depth,
        run_mode_one_focus_directions=run_mode_one_focus_directions,
        run_mode_one_ignore_directions=run_mode_one_ignore_directions,
        mode_two_title=mode_two_title,
        mode_two_pdf_url=mode_two_pdf_url,
        mode_two_pdf_path=mode_two_pdf_path,
        run_mode_two_scope=run_mode_two_scope,
        run_mode_two_target_tables=run_mode_two_target_tables,
        run_mode_two_baseline_first=run_mode_two_baseline_first,
    )
    return (
        next_session,
        render_project_list_summary(next_session, store),
        project_table_rows(store),
        project_runs_rows(store, next_session.selected_project_slug),
        gr.update(
            choices=run_selector_choices(store, next_session.selected_project_slug),
            value=next_session.selected_run_task_id,
        ),
        feedback,
        render_run_detail(next_session, store),
    )


def select_run_and_render(
    session: ConnectionSession,
    store: JsonProjectStore,
    task_id: str | None,
    *,
    client_factory: ApiClientFactory,
) -> tuple[ConnectionSession, object, str, str]:
    next_session = session
    next_session.selected_run_task_id = task_id or None
    clear_run_observation(next_session)
    if next_session.authenticated and next_session.selected_run_task_id is not None:
        next_session = refresh_selected_run(next_session, store, client_factory=client_factory)
    return (
        next_session,
        gr.update(
            choices=run_selector_choices(store, next_session.selected_project_slug),
            value=next_session.selected_run_task_id,
        ),
        render_run_feedback(next_session),
        render_run_detail(next_session, store),
    )


def refresh_run_and_render(
    session: ConnectionSession,
    store: JsonProjectStore,
    *,
    client_factory: ApiClientFactory,
) -> RunSubmitRenderResult:
    next_session = refresh_selected_run(session, store, client_factory=client_factory)
    return (
        next_session,
        render_project_list_summary(next_session, store),
        project_table_rows(store),
        project_runs_rows(store, next_session.selected_project_slug),
        gr.update(
            choices=run_selector_choices(store, next_session.selected_project_slug),
            value=next_session.selected_run_task_id,
        ),
        render_run_feedback(next_session),
        render_run_detail(next_session, store),
    )


def approve_run_and_render(
    session: ConnectionSession,
    store: JsonProjectStore,
    *,
    client_factory: ApiClientFactory,
) -> RunSubmitRenderResult:
    next_session = session
    task_id = next_session.selected_run_task_id
    if not next_session.authenticated or task_id is None:
        next_session.run_refresh_error = (
            "Connect to the API and select a Run before approving a gate."
        )
        return refresh_run_and_render(next_session, store, client_factory=client_factory)
    if not can_resolve_active_gate(next_session):
        next_session.run_refresh_error = "The selected Run does not have a waiting gate to approve."
        return refresh_run_and_render(next_session, store, client_factory=client_factory)

    client = client_factory(next_session.api_base_url, next_session.api_key)
    try:
        client.approve_task(task_id)
    except ApiClientError as exc:
        next_session.run_refresh_error = f"Failed to approve gate: {exc}"
        return refresh_run_and_render(next_session, store, client_factory=client_factory)
    next_session = connect_session(
        next_session.api_base_url,
        next_session.api_key,
        next_session,
        store=store,
        client_factory=client_factory,
    )
    next_session = refresh_selected_run(next_session, store, client_factory=client_factory)
    return refresh_run_and_render(next_session, store, client_factory=client_factory)


def reject_run_and_render(
    session: ConnectionSession,
    store: JsonProjectStore,
    feedback: str,
    *,
    client_factory: ApiClientFactory,
) -> RunSubmitRenderResult:
    next_session = session
    task_id = next_session.selected_run_task_id
    if not next_session.authenticated or task_id is None:
        next_session.run_refresh_error = (
            "Connect to the API and select a Run before rejecting a gate."
        )
        return refresh_run_and_render(next_session, store, client_factory=client_factory)
    if not can_resolve_active_gate(next_session):
        next_session.run_refresh_error = "The selected Run does not have a waiting gate to reject."
        return refresh_run_and_render(next_session, store, client_factory=client_factory)

    client = client_factory(next_session.api_base_url, next_session.api_key)
    try:
        client.reject_task(task_id, feedback.strip() or None)
    except ApiClientError as exc:
        next_session.run_refresh_error = f"Failed to reject gate: {exc}"
        return refresh_run_and_render(next_session, store, client_factory=client_factory)
    next_session = connect_session(
        next_session.api_base_url,
        next_session.api_key,
        next_session,
        store=store,
        client_factory=client_factory,
    )
    next_session = refresh_selected_run(next_session, store, client_factory=client_factory)
    return refresh_run_and_render(next_session, store, client_factory=client_factory)


def build_task_create_request(
    *,
    project: ProjectRecord,
    mode: str,
    run_container_host: str,
    run_container_port: float | int | None,
    run_container_user: str,
    run_container_ssh_key_path: str,
    run_container_project_dir: str,
    run_budget_gpu_hours: float | None,
    run_budget_api_cost_usd: float | None,
    run_budget_wall_clock_hours: float | None,
    run_webhook_url: str,
    run_webhook_secret: str,
    run_yolo: bool,
    mode_one_seed_rows: list[list[object]] | None,
    run_mode_one_domain_context: str,
    run_mode_one_max_depth: float | int | None,
    run_mode_one_focus_directions: str,
    run_mode_one_ignore_directions: str,
    mode_two_title: str,
    mode_two_pdf_url: str,
    mode_two_pdf_path: str,
    run_mode_two_scope: str,
    run_mode_two_target_tables: str,
    run_mode_two_baseline_first: bool,
) -> TaskCreateRequest:
    resolved_mode = TaskMode(mode)
    defaults = project.defaults

    container = {
        "host": prefer_text(run_container_host, defaults.container_host),
        "port": coerce_int(run_container_port, defaults.container_port),
        "user": prefer_text(run_container_user, defaults.container_user),
        "ssh_key_path": prefer_optional_text(
            run_container_ssh_key_path, defaults.container_ssh_key_path
        ),
        "project_dir": prefer_text(run_container_project_dir, defaults.container_project_dir),
    }
    budget = {
        "gpu_hours": coerce_optional_float(run_budget_gpu_hours, defaults.budget_gpu_hours),
        "api_cost_usd": coerce_optional_float(
            run_budget_api_cost_usd, defaults.budget_api_cost_usd
        ),
        "wall_clock_hours": coerce_optional_float(
            run_budget_wall_clock_hours,
            defaults.budget_wall_clock_hours,
        ),
    }
    payload: dict[str, object] = {
        "mode": resolved_mode.value,
        "container": container,
        "budget": budget,
        "yolo": run_yolo,
    }

    webhook_url = prefer_optional_text(run_webhook_url, defaults.webhook_url)
    if webhook_url:
        payload["webhook_url"] = webhook_url
    webhook_secret = run_webhook_secret.strip()
    if webhook_secret:
        payload["webhook_secret"] = webhook_secret

    if resolved_mode is TaskMode.RESEARCH_DISCOVERY:
        papers = build_mode_one_papers(mode_one_seed_rows or [])
        payload["papers"] = papers
        payload["config"] = {
            "mode_1": {
                "domain_context": prefer_optional_text(
                    run_mode_one_domain_context,
                    defaults.mode_1.domain_context,
                ),
                "max_depth": coerce_int(run_mode_one_max_depth, defaults.mode_1.max_depth),
                "focus_directions": prefer_text_list(
                    run_mode_one_focus_directions,
                    defaults.mode_1.focus_directions,
                ),
                "ignore_directions": prefer_text_list(
                    run_mode_one_ignore_directions,
                    defaults.mode_1.ignore_directions,
                ),
            }
        }
    else:
        papers = build_mode_two_papers(mode_two_title, mode_two_pdf_url, mode_two_pdf_path)
        payload["papers"] = papers
        payload["config"] = {
            "mode_2": {
                "scope": prefer_text(run_mode_two_scope, defaults.mode_2.scope.value),
                "target_tables": prefer_text_list(
                    run_mode_two_target_tables,
                    defaults.mode_2.target_tables,
                ),
                "baseline_first": run_mode_two_baseline_first,
            }
        }
    return TaskCreateRequest.model_validate(payload)


def render_connection_outputs(
    session: ConnectionSession,
    store: JsonProjectStore,
    *,
    project_feedback: str,
) -> ConnectionRenderResult:
    return (
        session,
        render_connection_banner(session),
        render_health_panel(session),
        gr.update(
            choices=project_selector_choices(store),
            value=session.selected_project_slug,
        ),
        render_project_list_summary(session, store),
        project_table_rows(store),
        project_feedback,
        render_project_detail_summary(session, store),
        project_runs_rows(store, session.selected_project_slug),
        gr.update(
            choices=run_selector_choices(store, session.selected_project_slug),
            value=session.selected_run_task_id,
        ),
        render_run_feedback(session),
        render_run_detail(session, store),
    )


def render_project_outputs(
    session: ConnectionSession,
    store: JsonProjectStore,
    *,
    project_feedback: str,
) -> ProjectRenderResult:
    project = selected_project(store, session)
    latest_run = selected_run(store, session)
    (
        project_name,
        project_slug,
        project_description,
        container_host,
        container_port,
        container_user,
        container_ssh_key_path,
        container_project_dir,
        budget_gpu_hours,
        budget_api_cost_usd,
        budget_wall_clock_hours,
        webhook_url,
        default_yolo,
        mode_one_domain_context,
        mode_one_max_depth,
        mode_one_focus_directions,
        mode_one_ignore_directions,
        mode_two_scope,
        mode_two_target_tables,
        mode_two_baseline_first,
    ) = project_form_values(project)
    (
        run_mode,
        run_container_host,
        run_container_port,
        run_container_user,
        run_container_ssh_key_path,
        run_container_project_dir,
        run_budget_gpu_hours,
        run_budget_api_cost_usd,
        run_budget_wall_clock_hours,
        run_webhook_url,
        run_webhook_secret,
        run_yolo,
        mode_one_seed_rows,
        run_mode_one_domain_context,
        run_mode_one_max_depth,
        run_mode_one_focus_directions,
        run_mode_one_ignore_directions,
        mode_two_title,
        mode_two_pdf_url,
        mode_two_pdf_path,
        run_mode_two_scope,
        run_mode_two_target_tables,
        run_mode_two_baseline_first,
    ) = run_form_values(project)
    return (
        session,
        project_feedback,
        render_project_detail_summary(session, store),
        project_name,
        project_slug,
        project_description,
        container_host,
        container_port,
        container_user,
        container_ssh_key_path,
        container_project_dir,
        budget_gpu_hours,
        budget_api_cost_usd,
        budget_wall_clock_hours,
        webhook_url,
        default_yolo,
        mode_one_domain_context,
        mode_one_max_depth,
        mode_one_focus_directions,
        mode_one_ignore_directions,
        mode_two_scope,
        mode_two_target_tables,
        mode_two_baseline_first,
        project_runs_rows(store, session.selected_project_slug),
        gr.update(
            choices=run_selector_choices(store, session.selected_project_slug),
            value=session.selected_run_task_id,
        ),
        render_run_feedback(session),
        run_mode,
        run_container_host,
        run_container_port,
        run_container_user,
        run_container_ssh_key_path,
        run_container_project_dir,
        run_budget_gpu_hours,
        run_budget_api_cost_usd,
        run_budget_wall_clock_hours,
        run_webhook_url,
        run_webhook_secret,
        run_yolo,
        mode_one_seed_rows,
        run_mode_one_domain_context,
        run_mode_one_max_depth,
        run_mode_one_focus_directions,
        run_mode_one_ignore_directions,
        mode_two_title,
        mode_two_pdf_url,
        mode_two_pdf_path,
        run_mode_two_scope,
        run_mode_two_target_tables,
        run_mode_two_baseline_first,
        render_run_detail(session, store if latest_run is not None else store),
    )


def render_after_project_mutation(
    session: ConnectionSession,
    store: JsonProjectStore,
    project_feedback: str,
) -> ProjectMutationRenderResult:
    project_outputs = render_project_outputs(session, store, project_feedback=project_feedback)
    return (
        project_outputs[0],
        gr.update(choices=project_selector_choices(store), value=session.selected_project_slug),
        render_project_list_summary(session, store),
        project_table_rows(store),
        *project_outputs[1:],
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


def render_project_list_summary(session: ConnectionSession, store: JsonProjectStore) -> str:
    project_count = len(store.list_projects())
    if not session.authenticated:
        return (
            "## Project List\n"
            f"- Local projects: `{project_count}`\n"
            "- Connect to the API to create runs and refresh run statuses."
        )
    return (
        "## Project List\n"
        f"- Authenticated to `{session.api_base_url}`\n"
        f"- Local projects: `{project_count}`\n"
        f"- API tasks discovered: `{session.total_tasks}`\n"
        "- History import is disabled: only WebUI-created runs are bound to Projects."
    )


def render_project_detail_summary(session: ConnectionSession, store: JsonProjectStore) -> str:
    project = selected_project(store, session)
    if project is None:
        return (
            "## Project Detail\n"
            "No Project selected. Create one locally or pick an existing Project from the selector."
        )
    run_count = len(store.list_project_runs(project.slug))
    return (
        "## Project Detail\n"
        f"- Project: `{project.name}` (`{project.slug}`)\n"
        f"- Description: {project.description or 'No description'}\n"
        f"- Local runs: `{run_count}`\n"
        f"- State root: `{store.webui_root}`"
    )


def render_run_feedback(session: ConnectionSession) -> str:
    if session.selected_project_slug is None:
        return "Select or create a Project before creating a Run."
    if not session.authenticated:
        return "Connect to the API before creating a Run."
    if session.selected_run_task_id is None:
        return "Project selected. Edit defaults or submit a new Run."
    if session.run_refresh_error:
        return session.run_refresh_error
    detail = session.selected_run_detail
    if detail is None:
        return "Run selected. Refresh Run Detail to load gate state and event timeline."
    if detail.active_gate is not None and detail.active_gate.status is HumanGateStatus.WAITING:
        return f"Waiting gate `{detail.active_gate.gate_type.value}` can be approved or rejected."
    mode = session.run_event_mode or "snapshot"
    return f"Run detail loaded in `{mode}` mode."


def render_run_detail(session: ConnectionSession, store: JsonProjectStore) -> str:
    run = selected_run(store, session)
    if run is None:
        return (
            "## Run Detail\n"
            "No bound Run selected yet. Select a local Run to load real task detail, gates, and events."
        )
    detail = session.selected_run_detail
    if detail is None or detail.task_id != run.task_id:
        return (
            "## Run Detail\n"
            f"- Task ID: `{run.task_id}`\n"
            f"- Project: `{run.project_slug}`\n"
            f"- Last known status: `{run.last_known_status.value}`\n"
            f"- Last known stage: `{run.last_known_stage.value}`\n"
            "- Live task detail not loaded yet. Use Refresh Run Detail after connecting to the API."
        )
    gate_section = render_active_gate(detail)
    artifact_section = render_artifact_summary(detail, session.selected_run_artifacts)
    timeline_section = render_timeline(session.run_timeline_items)
    observation_mode = session.run_event_mode or "snapshot"
    return (
        "## Run Detail\n"
        f"- Task ID: `{detail.task_id}`\n"
        f"- Project: `{run.project_slug}`\n"
        f"- Mode: `{detail.mode.value}`\n"
        f"- Status: `{detail.status.value}`\n"
        f"- Current stage: `{detail.current_stage.value}`\n"
        f"- Observation mode: `{observation_mode}`\n"
        f"- Created at: `{detail.created_at.isoformat(timespec='seconds')}`\n"
        f"- Updated at: `{detail.updated_at.isoformat(timespec='seconds')}`\n"
        f"- Termination reason: {detail.termination_reason or 'N/A'}\n"
        f"- Papers: {', '.join(run.paper_titles) if run.paper_titles else 'None'}\n"
        f"- Budget limit: GPU `{detail.budget_limit.gpu_hours}` / API `${detail.budget_limit.api_cost_usd}` / Wall `{detail.budget_limit.wall_clock_hours}`\n"
        f"- Budget used: GPU `{detail.budget_used.gpu_hours}` / API `${detail.budget_used.api_cost_usd}` / Wall `{detail.budget_used.wall_clock_hours}`\n"
        f"{gate_section}\n"
        f"{artifact_section}\n"
        f"{timeline_section}"
    )


def project_table_rows(store: JsonProjectStore) -> list[list[object]]:
    rows: list[list[object]] = []
    for project in store.list_projects():
        runs = store.list_project_runs(project.slug)
        latest = runs[0] if runs else None
        rows.append(
            [
                project.name,
                project.slug,
                len(runs),
                latest.last_known_status.value if latest is not None else "",
                project.updated_at.isoformat(timespec="seconds"),
            ]
        )
    return rows


def project_runs_rows(store: JsonProjectStore, project_slug: str | None) -> list[list[object]]:
    if not project_slug:
        return []
    rows: list[list[object]] = []
    for run in store.list_project_runs(project_slug):
        rows.append(
            [
                run.task_id,
                run.mode.value,
                run.last_known_status.value,
                run.last_known_stage.value,
                run.created_at.isoformat(timespec="seconds"),
                ", ".join(run.paper_titles),
            ]
        )
    return rows


def run_selector_choices(
    store: JsonProjectStore, project_slug: str | None
) -> list[tuple[str, str]]:
    if project_slug is None:
        return []
    return [
        (f"{run.task_id} · {run.last_known_status.value}", run.task_id)
        for run in store.list_project_runs(project_slug)
    ]


def container_profile_choices(store: JsonProjectStore) -> list[tuple[str, str]]:
    return [(name, name) for name in store.list_container_profiles()]


def project_selector_choices(store: JsonProjectStore) -> list[tuple[str, str]]:
    return [(project.name, project.slug) for project in store.list_projects()]


def select_container_profile_and_render(
    store: JsonProjectStore,
    profile_name: str | None,
) -> tuple[str, str, int, str, str, str, str, str]:
    if not profile_name:
        return "", "", 22, "", "", "", "", "Choose a saved container profile to preview or apply."
    profile = store.load_container_profile(profile_name)
    if profile is None:
        return "", "", 22, "", "", "", "", f"Container profile `{profile_name}` not found."
    return (
        profile_name,
        profile.host,
        profile.port,
        profile.user,
        profile.ssh_key_path,
        profile.ssh_password,
        profile.project_dir,
        f"Loaded container profile `{profile_name}`.",
    )


def save_container_profile_and_render(
    store: JsonProjectStore,
    *,
    profile_name: str,
    host: str,
    port: float | int | None,
    user: str,
    ssh_key_path: str,
    ssh_password: str,
    project_dir: str,
    set_default: bool,
) -> tuple[object, str]:
    normalized_name = profile_name.strip()
    if not normalized_name:
        return gr.update(
            choices=container_profile_choices(store), value=None
        ), "Container profile name is required."
    if not host.strip():
        return (
            gr.update(choices=container_profile_choices(store), value=normalized_name),
            "Container host is required.",
        )
    if not user.strip():
        return (
            gr.update(choices=container_profile_choices(store), value=normalized_name),
            "Container user is required.",
        )
    profile = ContainerProfileRecord(
        host=host.strip(),
        port=coerce_int(port, 22),
        user=user.strip(),
        ssh_key_path=ssh_key_path.strip(),
        ssh_password=ssh_password.strip(),
        project_dir=project_dir.strip(),
    )
    store.save_container_profile(normalized_name, profile, set_default=set_default)
    suffix = " and set as default" if set_default else ""
    return (
        gr.update(choices=container_profile_choices(store), value=normalized_name),
        f"Saved container profile `{normalized_name}`{suffix}.",
    )


def apply_container_profile_and_render(
    store: JsonProjectStore,
    *,
    profile_name: str | None,
    current_project_host: str,
    current_project_port: float | int | None,
    current_project_user: str,
    current_project_ssh_key_path: str,
    current_project_dir: str,
    current_run_host: str,
    current_run_port: float | int | None,
    current_run_user: str,
    current_run_ssh_key_path: str,
    current_run_dir: str,
) -> tuple[str, int, str, str, str, str, int, str, str, str, str]:
    if not profile_name:
        return (
            current_project_host,
            coerce_int(current_project_port, 22),
            current_project_user,
            current_project_ssh_key_path,
            current_project_dir,
            current_run_host,
            coerce_int(current_run_port, 22),
            current_run_user,
            current_run_ssh_key_path,
            current_run_dir,
            "Choose a container profile before applying.",
        )
    profile = store.load_container_profile(profile_name)
    if profile is None:
        return (
            current_project_host,
            coerce_int(current_project_port, 22),
            current_project_user,
            current_project_ssh_key_path,
            current_project_dir,
            current_run_host,
            coerce_int(current_run_port, 22),
            current_run_user,
            current_run_ssh_key_path,
            current_run_dir,
            f"Container profile `{profile_name}` not found.",
        )
    return (
        profile.host,
        profile.port,
        profile.user,
        profile.ssh_key_path,
        profile.project_dir,
        profile.host,
        profile.port,
        profile.user,
        profile.ssh_key_path,
        profile.project_dir,
        f"Applied container profile `{profile_name}` to Project and Run forms.",
    )


def selected_project(store: JsonProjectStore, session: ConnectionSession) -> ProjectRecord | None:
    if session.selected_project_slug is None:
        return None
    return store.load_project(session.selected_project_slug)


def selected_run(store: JsonProjectStore, session: ConnectionSession) -> ProjectRunRecord | None:
    if session.selected_run_task_id is None:
        return None
    return store.load_project_run(session.selected_run_task_id)


def can_resolve_active_gate(session: ConnectionSession) -> bool:
    detail = session.selected_run_detail
    return (
        detail is not None
        and detail.active_gate is not None
        and detail.active_gate.status is HumanGateStatus.WAITING
    )


def render_active_gate(detail: TaskDetailResponse) -> str:
    active_gate = detail.active_gate
    if active_gate is None:
        return "### Active Gate\n- No waiting gate."
    return (
        "### Active Gate\n"
        f"- Gate ID: `{active_gate.gate_id}`\n"
        f"- Type: `{active_gate.gate_type.value}`\n"
        f"- Status: `{active_gate.status.value}`\n"
        f"- Summary: {active_gate.summary}\n"
        f"- Deadline: {active_gate.deadline_at.isoformat(timespec='seconds') if active_gate.deadline_at else 'N/A'}\n"
        f"- Feedback: {active_gate.feedback or 'N/A'}\n"
        f"- Auto approved: `{active_gate.auto_approved}`"
    )


def render_artifact_summary(
    detail: TaskDetailResponse,
    artifacts: tuple[ArtifactItemResponse, ...],
) -> str:
    if not detail.artifact_summary.counts:
        return "### Artifact Summary\n- No artifacts recorded yet."
    rows = [
        f"- `{artifact_type}`: `{count}`"
        for artifact_type, count in sorted(detail.artifact_summary.counts.items())
    ]
    mode_one_rows = render_mode_one_artifacts(artifacts)
    if mode_one_rows:
        return "### Artifact Summary\n" + "\n".join(rows) + "\n" + mode_one_rows
    return "### Artifact Summary\n" + "\n".join(rows)


def render_mode_one_artifacts(artifacts: tuple[ArtifactItemResponse, ...]) -> str:
    if not artifacts:
        return ""
    graph_rows: list[str] = []
    claim_rows: list[str] = []
    for artifact in artifacts:
        payload = artifact.payload
        if artifact.artifact_type.value == "ExplorationGraph":
            seed_count = len(_string_list(payload.get("seed_paper_ids")))
            visited_count = len(_string_list(payload.get("visited_paper_ids")))
            queued_count = len(_string_list(payload.get("queued_paper_ids")))
            no_new_claim_rounds = _coerce_int(payload.get("no_new_claim_rounds"), default=0)
            reference_scores = _dict_payload(payload.get("reference_scores"))
            prune_reasons = _dict_payload(payload.get("prune_reasons"))
            score_pairs = [
                (paper_id, score)
                for paper_id, score in reference_scores.items()
                if isinstance(paper_id, str) and isinstance(score, int | float)
            ]
            score_pairs.sort(key=lambda item: item[0])
            score_summary = (
                ", ".join([f"{paper_id}:{float(score):.2f}" for paper_id, score in score_pairs[:6]])
                if score_pairs
                else "none"
            )
            prune_pairs = [
                (paper_id, reason)
                for paper_id, reason in prune_reasons.items()
                if isinstance(paper_id, str) and isinstance(reason, str)
            ]
            prune_pairs.sort(key=lambda item: item[0])
            prune_summary = (
                "; ".join([f"{paper_id}:{reason}" for paper_id, reason in prune_pairs[:6]])
                if prune_pairs
                else "none"
            )
            graph_rows.append(
                "- ExplorationGraph: "
                f"seed={seed_count}, visited={visited_count}, queued={queued_count}, "
                f"depth={payload.get('current_depth', 0)}, "
                f"no_new_rounds={no_new_claim_rounds}, "
                f"ref_scores=[{score_summary}], "
                f"prune_reasons=[{prune_summary}], "
                f"termination={payload.get('termination_reason') or 'N/A'}"
            )
        if artifact.artifact_type.value == "Claim":
            statement = str(payload.get("statement") or "")
            if not statement:
                continue
            confidence = payload.get("confidence")
            confidence_str = "N/A" if confidence is None else f"{float(confidence):.2f}"
            claim_rows.append(f"- Claim: {statement} (confidence={confidence_str})")
    if not graph_rows and not claim_rows:
        return ""
    rows = ["### Mode 1 Outputs", *graph_rows, *claim_rows[:5]]
    return "\n".join(rows)


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _dict_payload(value: object) -> dict[object, object]:
    if not isinstance(value, dict):
        return {}
    return cast(dict[object, object], value)


def _coerce_int(value: object, *, default: int) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return default


def render_timeline(items: tuple[RunTimelineItem, ...]) -> str:
    if not items:
        return "### Event Timeline\n- No events loaded yet."
    rows = [
        f"- `#{item.event_id}` `{item.event}` at `{item.created_at.isoformat(timespec='seconds')}` :: {summarize_payload(item.payload)}"
        for item in items
    ]
    return "### Event Timeline\n" + "\n".join(rows)


def summarize_payload(payload: dict[str, Any]) -> str:
    if not payload:
        return "no payload"
    parts = [f"{key}={value}" for key, value in list(payload.items())[:4]]
    return ", ".join(parts)


def project_form_values(
    project: ProjectRecord | None,
) -> tuple[
    str,
    str,
    str,
    str,
    int,
    str,
    str,
    str,
    float | None,
    float | None,
    float | None,
    str,
    bool,
    str,
    int,
    str,
    str,
    str,
    str,
    bool,
]:
    if project is None:
        defaults = ProjectDefaults()
        return (
            "",
            "",
            "",
            defaults.container_host,
            defaults.container_port,
            defaults.container_user,
            defaults.container_ssh_key_path,
            defaults.container_project_dir,
            defaults.budget_gpu_hours,
            defaults.budget_api_cost_usd,
            defaults.budget_wall_clock_hours,
            defaults.webhook_url,
            defaults.yolo,
            defaults.mode_1.domain_context,
            defaults.mode_1.max_depth,
            ", ".join(defaults.mode_1.focus_directions),
            ", ".join(defaults.mode_1.ignore_directions),
            defaults.mode_2.scope.value,
            ", ".join(defaults.mode_2.target_tables),
            defaults.mode_2.baseline_first,
        )
    defaults = project.defaults
    return (
        project.name,
        project.slug,
        project.description,
        defaults.container_host,
        defaults.container_port,
        defaults.container_user,
        defaults.container_ssh_key_path,
        defaults.container_project_dir,
        defaults.budget_gpu_hours,
        defaults.budget_api_cost_usd,
        defaults.budget_wall_clock_hours,
        defaults.webhook_url,
        defaults.yolo,
        defaults.mode_1.domain_context,
        defaults.mode_1.max_depth,
        ", ".join(defaults.mode_1.focus_directions),
        ", ".join(defaults.mode_1.ignore_directions),
        defaults.mode_2.scope.value,
        ", ".join(defaults.mode_2.target_tables),
        defaults.mode_2.baseline_first,
    )


def run_form_values(
    project: ProjectRecord | None,
) -> tuple[
    str,
    str,
    int,
    str,
    str,
    str,
    float | None,
    float | None,
    float | None,
    str,
    str,
    bool,
    list[list[str]],
    str,
    int,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    bool,
]:
    defaults = project.defaults if project is not None else ProjectDefaults()
    return (
        TaskMode.DEEP_REPRODUCTION.value,
        defaults.container_host,
        defaults.container_port,
        defaults.container_user,
        defaults.container_ssh_key_path,
        defaults.container_project_dir,
        defaults.budget_gpu_hours,
        defaults.budget_api_cost_usd,
        defaults.budget_wall_clock_hours,
        defaults.webhook_url,
        "",
        defaults.yolo,
        empty_seed_rows(),
        defaults.mode_1.domain_context,
        defaults.mode_1.max_depth,
        ", ".join(defaults.mode_1.focus_directions),
        ", ".join(defaults.mode_1.ignore_directions),
        "",
        "",
        "",
        defaults.mode_2.scope.value,
        ", ".join(defaults.mode_2.target_tables),
        defaults.mode_2.baseline_first,
    )


def empty_seed_rows() -> list[list[str]]:
    return [["", "", ""] for _ in range(5)]


def build_mode_one_papers(rows: list[list[object]]) -> list[dict[str, str]]:
    papers: list[dict[str, str]] = []
    for row in rows:
        if len(row) < 3:
            continue
        title = str(row[0]).strip()
        pdf_url = str(row[1]).strip()
        pdf_path = str(row[2]).strip()
        if not title and not pdf_url and not pdf_path:
            continue
        if not title:
            raise ValueError("Each Mode 1 seed paper requires a title.")
        if not pdf_url and not pdf_path:
            raise ValueError("Each Mode 1 seed paper requires pdf_url or pdf_path.")
        paper: dict[str, str] = {"title": title, "role": "seed"}
        if pdf_url:
            paper["pdf_url"] = pdf_url
        if pdf_path:
            paper["pdf_path"] = pdf_path
        papers.append(paper)
    if not papers:
        raise ValueError("Mode 1 requires at least one seed paper.")
    return papers


def build_mode_two_papers(title: str, pdf_url: str, pdf_path: str) -> list[dict[str, str]]:
    normalized_title = title.strip()
    normalized_url = pdf_url.strip()
    normalized_path = pdf_path.strip()
    if not normalized_title:
        raise ValueError("Mode 2 requires a target paper title.")
    if not normalized_url and not normalized_path:
        raise ValueError("Mode 2 requires pdf_url or pdf_path.")
    paper: dict[str, str] = {"title": normalized_title, "role": "target"}
    if normalized_url:
        paper["pdf_url"] = normalized_url
    if normalized_path:
        paper["pdf_path"] = normalized_path
    return [paper]


def normalize_project_slug(slug: str, name: str) -> str:
    candidate = slug.strip().lower() or name.strip().lower()
    candidate = re.sub(r"[^a-z0-9]+", "-", candidate)
    candidate = re.sub(r"-{2,}", "-", candidate).strip("-")
    return candidate


def split_text_list(value: str) -> list[str]:
    parts = re.split(r"[\n,]", value)
    return [item.strip() for item in parts if item.strip()]


def prefer_text(value: str, default: str) -> str:
    normalized = value.strip()
    return normalized or default


def prefer_optional_text(value: str, default: str) -> str | None:
    normalized = value.strip()
    fallback = default.strip()
    selected = normalized or fallback
    return selected or None


def prefer_text_list(value: str, default: list[str]) -> list[str]:
    parsed = split_text_list(value)
    return parsed or default


def coerce_int(value: float | int | None, default: int) -> int:
    if value is None:
        return default
    return int(value)


def coerce_optional_float(value: float | None, default: float | None) -> float | None:
    if value is None:
        return default
    return float(value)


def _status_card(title: str, detail: str, css_class: str) -> str:
    return f"<div class='status-card {css_class}'><strong>{title}</strong><br/>{detail}</div>"
