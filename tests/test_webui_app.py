from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import gradio as gr

from ainrf.api.schemas import (
    ApiStatus,
    ArtifactItemResponse,
    HealthResponse,
    TaskActionResponse,
    TaskArtifactsResponse,
    TaskCreateResponse,
    TaskDetailResponse,
    TaskListResponse,
    TaskSummaryResponse,
)
from ainrf.artifacts import GateType, HumanGateStatus
from ainrf.events import TaskEvent, TaskEventCategory
from ainrf.state import TaskMode, TaskStage
from ainrf.webui.app import (
    apply_container_profile_and_render,
    approve_run_and_render,
    build_task_create_request,
    connect_session,
    create_webui,
    normalize_project_slug,
    refresh_selected_run,
    render_project_list_summary,
    render_run_detail,
    reject_run_and_render,
    save_container_profile_and_render,
    save_project_from_form,
    select_container_profile_and_render,
    submit_project_run,
)
from ainrf.webui.client import ApiAuthenticationError
from ainrf.webui.models import ConnectionSession, ProjectRunRecord, WebUiConfig
from ainrf.webui.store import JsonProjectStore


class FakeClient:
    def __init__(
        self,
        *,
        health: HealthResponse | None = None,
        task_list: TaskListResponse | None = None,
        create_response: TaskCreateResponse | None = None,
        task_detail: TaskDetailResponse | None = None,
        action_response: TaskActionResponse | None = None,
        events: list[TaskEvent] | None = None,
        task_artifacts: list[ArtifactItemResponse] | None = None,
        error: Exception | None = None,
    ) -> None:
        self._health = health
        self._task_list = task_list
        self._create_response = create_response
        self._task_detail = task_detail
        self._action_response = action_response
        self._events = events or []
        self._task_artifacts = task_artifacts or []
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

    def create_task(self, payload: object) -> TaskCreateResponse:
        _ = payload
        if self._error is not None:
            raise self._error
        assert self._create_response is not None
        return self._create_response

    def get_task(self, task_id: str) -> TaskDetailResponse:
        _ = task_id
        if self._error is not None:
            raise self._error
        assert self._task_detail is not None
        return self._task_detail

    def approve_task(self, task_id: str) -> TaskActionResponse:
        _ = task_id
        if self._error is not None:
            raise self._error
        assert self._action_response is not None
        return self._action_response

    def reject_task(self, task_id: str, feedback: str | None) -> TaskActionResponse:
        _ = (task_id, feedback)
        if self._error is not None:
            raise self._error
        assert self._action_response is not None
        return self._action_response

    def list_task_events(self, task_id: str, **kwargs: object) -> list[TaskEvent]:
        _unused = (task_id, kwargs)
        if self._error is not None:
            raise self._error
        return list(self._events)

    def list_task_artifacts(self, task_id: str) -> TaskArtifactsResponse:
        _ = task_id
        if self._error is not None:
            raise self._error
        return TaskArtifactsResponse(task_id="t-001", items=list(self._task_artifacts))


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


def build_task_detail(task_id: str, status: TaskStage) -> TaskDetailResponse:
    now = datetime(2026, 3, 16, tzinfo=UTC)
    return TaskDetailResponse.model_validate(
        {
            "task_id": task_id,
            "mode": TaskMode.DEEP_REPRODUCTION.value,
            "status": status.value,
            "created_at": now,
            "updated_at": now,
            "current_stage": status.value,
            "termination_reason": None,
            "budget_limit": {"gpu_hours": 1.0, "api_cost_usd": 2.0, "wall_clock_hours": 3.0},
            "budget_used": {"gpu_hours": 0.1, "api_cost_usd": 0.2, "wall_clock_hours": 0.3},
            "gates": [],
            "active_gate": {
                "gate_id": "g-001",
                "gate_type": GateType.INTAKE.value,
                "status": HumanGateStatus.WAITING.value,
                "summary": "Review intake",
                "payload": {"paper_count": 1},
                "deadline_at": now,
                "resolved_at": None,
                "reminder_sent_at": None,
                "feedback": None,
                "auto_approved": False,
            }
            if status is TaskStage.GATE_WAITING
            else None,
            "artifact_summary": {"counts": {"human_gate": 1}, "total": 1},
            "config": {},
        }
    )


def test_create_webui_returns_blocks(tmp_path: Path) -> None:
    demo = create_webui(WebUiConfig(state_root=tmp_path))

    assert isinstance(demo, gr.Blocks)


def test_connect_session_updates_local_run_bindings(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    session = ConnectionSession(selected_project_slug="vision-stack")
    save_project_from_form(
        session,
        store,
        name="Vision Stack",
        slug="vision-stack",
        description="",
        container_host="gpu-01",
        container_port=22,
        container_user="researcher",
        container_ssh_key_path="",
        container_project_dir="/workspace/projects/vision-stack",
        budget_gpu_hours=12.0,
        budget_api_cost_usd=6.0,
        budget_wall_clock_hours=24.0,
        webhook_url="",
        yolo=False,
        mode_one_domain_context="",
        mode_one_max_depth=3,
        mode_one_focus_directions="",
        mode_one_ignore_directions="",
        mode_two_scope="core-only",
        mode_two_target_tables="",
        mode_two_baseline_first=True,
    )
    store.save_project_run(
        build_run_binding(
            task_id="t-001",
            project_slug="vision-stack",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.SUBMITTED,
        )
    )
    health = HealthResponse(
        status=ApiStatus.OK,
        state_root=".ainrf",
        container_configured=False,
        container_health=None,
        detail=None,
    )
    task_list = TaskListResponse(
        items=[build_task_summary("t-001", TaskMode.DEEP_REPRODUCTION, TaskStage.PLANNING)]
    )

    next_session = connect_session(
        "http://ainrf.local",
        "secret",
        session,
        store=store,
        client_factory=lambda base_url, api_key: FakeClient(health=health, task_list=task_list),
    )

    assert next_session.authenticated is True
    binding = store.load_project_run("t-001")
    assert binding is not None
    assert binding.last_known_status is TaskStage.PLANNING


def test_save_project_from_form_persists_defaults(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    session = ConnectionSession()

    next_session, feedback = save_project_from_form(
        session,
        store,
        name="Vision Stack",
        slug="",
        description="Project for experiments",
        container_host="gpu-01",
        container_port=22,
        container_user="researcher",
        container_ssh_key_path="/tmp/id_rsa",
        container_project_dir="/workspace/projects/vision-stack",
        budget_gpu_hours=12.0,
        budget_api_cost_usd=6.0,
        budget_wall_clock_hours=24.0,
        webhook_url="https://example.com/hook",
        yolo=True,
        mode_one_domain_context="multimodal",
        mode_one_max_depth=4,
        mode_one_focus_directions="clip, llama",
        mode_one_ignore_directions="speech",
        mode_two_scope="full-suite",
        mode_two_target_tables="Table 1, Table 2",
        mode_two_baseline_first=False,
    )

    project = store.load_project("vision-stack")
    assert next_session.selected_project_slug == "vision-stack"
    assert "Saved Project" in feedback
    assert project is not None
    assert project.defaults.mode_1.focus_directions == ["clip", "llama"]
    assert project.defaults.mode_2.scope.value == "full-suite"


def test_build_task_create_request_uses_project_defaults_and_mode_specific_inputs(
    tmp_path: Path,
) -> None:
    store = JsonProjectStore(tmp_path)
    session = ConnectionSession()
    save_project_from_form(
        session,
        store,
        name="Vision Stack",
        slug="vision-stack",
        description="",
        container_host="gpu-01",
        container_port=22,
        container_user="researcher",
        container_ssh_key_path="",
        container_project_dir="/workspace/projects/vision-stack",
        budget_gpu_hours=12.0,
        budget_api_cost_usd=6.0,
        budget_wall_clock_hours=24.0,
        webhook_url="https://example.com/hook",
        yolo=False,
        mode_one_domain_context="multimodal",
        mode_one_max_depth=4,
        mode_one_focus_directions="clip",
        mode_one_ignore_directions="speech",
        mode_two_scope="core-only",
        mode_two_target_tables="Table 1",
        mode_two_baseline_first=True,
    )
    project = store.load_project("vision-stack")
    assert project is not None

    request = build_task_create_request(
        project=project,
        mode=TaskMode.RESEARCH_DISCOVERY.value,
        run_container_host="",
        run_container_port=None,
        run_container_user="",
        run_container_ssh_key_path="",
        run_container_project_dir="",
        run_budget_gpu_hours=None,
        run_budget_api_cost_usd=None,
        run_budget_wall_clock_hours=None,
        run_webhook_url="",
        run_webhook_secret="runtime-secret",
        run_yolo=False,
        mode_one_seed_rows=[["Seed Paper", "https://example.com/paper.pdf", ""]],
        run_mode_one_domain_context="",
        run_mode_one_max_depth=None,
        run_mode_one_focus_directions="adapter",
        run_mode_one_ignore_directions="",
        mode_two_title="",
        mode_two_pdf_url="",
        mode_two_pdf_path="",
        run_mode_two_scope="core-only",
        run_mode_two_target_tables="",
        run_mode_two_baseline_first=True,
    )

    assert request.container.host == "gpu-01"
    assert request.config.mode_1 is not None
    assert request.config.mode_1.focus_directions == ["adapter"]
    assert request.webhook_secret == "runtime-secret"


def test_submit_project_run_creates_binding_and_keeps_secret_out_of_store(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    session = ConnectionSession(
        api_base_url="http://ainrf.local",
        api_key="secret",
        reachable=True,
        authenticated=True,
    )
    next_session, _ = save_project_from_form(
        session,
        store,
        name="Vision Stack",
        slug="vision-stack",
        description="",
        container_host="gpu-01",
        container_port=22,
        container_user="researcher",
        container_ssh_key_path="",
        container_project_dir="/workspace/projects/vision-stack",
        budget_gpu_hours=12.0,
        budget_api_cost_usd=6.0,
        budget_wall_clock_hours=24.0,
        webhook_url="https://example.com/hook",
        yolo=False,
        mode_one_domain_context="multimodal",
        mode_one_max_depth=4,
        mode_one_focus_directions="clip",
        mode_one_ignore_directions="speech",
        mode_two_scope="core-only",
        mode_two_target_tables="Table 1",
        mode_two_baseline_first=True,
    )
    health = HealthResponse(
        status=ApiStatus.OK,
        state_root=".ainrf",
        container_configured=False,
        container_health=None,
        detail=None,
    )
    task_list = TaskListResponse(
        items=[build_task_summary("t-900", TaskMode.DEEP_REPRODUCTION, TaskStage.GATE_WAITING)]
    )

    updated_session, feedback = submit_project_run(
        next_session,
        store,
        client_factory=lambda base_url, api_key: FakeClient(
            health=health,
            task_list=task_list,
            create_response=TaskCreateResponse(task_id="t-900", status=TaskStage.GATE_WAITING),
            task_detail=build_task_detail("t-900", TaskStage.GATE_WAITING),
        ),
        mode=TaskMode.DEEP_REPRODUCTION.value,
        run_container_host="",
        run_container_port=None,
        run_container_user="",
        run_container_ssh_key_path="",
        run_container_project_dir="",
        run_budget_gpu_hours=None,
        run_budget_api_cost_usd=None,
        run_budget_wall_clock_hours=None,
        run_webhook_url="",
        run_webhook_secret="runtime-secret",
        run_yolo=False,
        mode_one_seed_rows=[],
        run_mode_one_domain_context="",
        run_mode_one_max_depth=None,
        run_mode_one_focus_directions="",
        run_mode_one_ignore_directions="",
        mode_two_title="Target Paper",
        mode_two_pdf_url="https://example.com/target.pdf",
        mode_two_pdf_path="",
        run_mode_two_scope="core-only",
        run_mode_two_target_tables="Table 1",
        run_mode_two_baseline_first=True,
    )

    binding = store.load_project_run("t-900")
    assert updated_session.selected_run_task_id == "t-900"
    assert "Created Run" in feedback
    assert binding is not None
    assert binding.project_slug == "vision-stack"
    assert "runtime-secret" not in (store.project_runs_dir / "t-900.json").read_text(
        encoding="utf-8"
    )


def test_render_project_list_summary_mentions_local_projects_when_disconnected(
    tmp_path: Path,
) -> None:
    store = JsonProjectStore(tmp_path)
    session = ConnectionSession()

    summary = render_project_list_summary(session, store)

    assert "Local projects" in summary


def test_normalize_project_slug_uses_name_when_blank() -> None:
    assert normalize_project_slug("", "Vision Stack") == "vision-stack"


def test_save_container_profile_and_apply_to_forms(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)

    _, save_feedback = save_container_profile_and_render(
        store,
        profile_name="gpu-main",
        host="gpu-01",
        port=2222,
        user="researcher",
        ssh_key_path="/tmp/id_rsa",
        ssh_password="secret",
        project_dir="/workspace/projects/vision-stack",
    )
    selected = select_container_profile_and_render(store, "gpu-main")
    applied = apply_container_profile_and_render(
        store,
        profile_name="gpu-main",
        current_project_host="",
        current_project_port=22,
        current_project_user="",
        current_project_ssh_key_path="",
        current_project_dir="",
        current_run_host="",
        current_run_port=22,
        current_run_user="",
        current_run_ssh_key_path="",
        current_run_dir="",
    )

    assert "Saved container profile" in save_feedback
    assert selected[0] == "gpu-main"
    assert selected[1] == "gpu-01"
    assert selected[5] == "secret"
    assert applied[0] == "gpu-01"
    assert applied[1] == 2222
    assert applied[5] == "gpu-01"
    assert "Applied container profile" in applied[-1]


def test_submit_project_run_requires_authenticated_session(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    session = ConnectionSession(selected_project_slug="vision-stack")

    _, feedback = submit_project_run(
        session,
        store,
        client_factory=lambda base_url, api_key: FakeClient(
            error=ApiAuthenticationError("Unauthorized")
        ),
        mode=TaskMode.DEEP_REPRODUCTION.value,
        run_container_host="",
        run_container_port=None,
        run_container_user="",
        run_container_ssh_key_path="",
        run_container_project_dir="",
        run_budget_gpu_hours=None,
        run_budget_api_cost_usd=None,
        run_budget_wall_clock_hours=None,
        run_webhook_url="",
        run_webhook_secret="",
        run_yolo=False,
        mode_one_seed_rows=[],
        run_mode_one_domain_context="",
        run_mode_one_max_depth=None,
        run_mode_one_focus_directions="",
        run_mode_one_ignore_directions="",
        mode_two_title="Target Paper",
        mode_two_pdf_url="https://example.com/target.pdf",
        mode_two_pdf_path="",
        run_mode_two_scope="core-only",
        run_mode_two_target_tables="",
        run_mode_two_baseline_first=True,
    )

    assert "Connect to the API" in feedback


def test_refresh_selected_run_loads_detail_and_timeline(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    session = ConnectionSession(
        api_base_url="http://ainrf.local",
        api_key="secret",
        reachable=True,
        authenticated=True,
    )
    next_session, _ = save_project_from_form(
        session,
        store,
        name="Vision Stack",
        slug="vision-stack",
        description="",
        container_host="gpu-01",
        container_port=22,
        container_user="researcher",
        container_ssh_key_path="",
        container_project_dir="/workspace/projects/vision-stack",
        budget_gpu_hours=12.0,
        budget_api_cost_usd=6.0,
        budget_wall_clock_hours=24.0,
        webhook_url="https://example.com/hook",
        yolo=False,
        mode_one_domain_context="multimodal",
        mode_one_max_depth=4,
        mode_one_focus_directions="clip",
        mode_one_ignore_directions="speech",
        mode_two_scope="core-only",
        mode_two_target_tables="Table 1",
        mode_two_baseline_first=True,
    )
    store.save_project_run(
        build_run_binding(
            task_id="t-001",
            project_slug="vision-stack",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
        )
    )
    next_session.selected_run_task_id = "t-001"

    updated = refresh_selected_run(
        next_session,
        store,
        client_factory=lambda base_url, api_key: FakeClient(
            task_detail=build_task_detail("t-001", TaskStage.GATE_WAITING),
            task_artifacts=[
                ArtifactItemResponse.model_validate(
                    {
                        "artifact_id": "eg-001",
                        "artifact_type": "ExplorationGraph",
                        "source_task_id": "t-001",
                        "summary": "graph",
                        "status": None,
                        "payload": {
                            "seed_paper_ids": ["pc-001"],
                            "visited_paper_ids": ["pc-001", "pc-002"],
                            "queued_paper_ids": ["pc-003"],
                            "current_depth": 1,
                            "no_new_claim_rounds": 2,
                            "reference_scores": {
                                "pc-002": 0.82,
                                "pc-003": 0.75,
                            },
                            "prune_reasons": {
                                "pc-004": "below_top_k",
                            },
                            "termination_reason": None,
                        },
                    }
                ),
                ArtifactItemResponse.model_validate(
                    {
                        "artifact_id": "cl-001",
                        "artifact_type": "Claim",
                        "source_task_id": "t-001",
                        "summary": "claim",
                        "status": None,
                        "payload": {
                            "statement": "Adapter families can be mixed.",
                            "confidence": 0.73,
                        },
                    }
                ),
            ],
            events=[
                TaskEvent.model_validate(
                    {
                        "event_id": 1,
                        "task_id": "t-001",
                        "category": TaskEventCategory.GATE.value,
                        "event": "gate.waiting",
                        "timestamp": "2026-03-16T00:00:00Z",
                        "payload": {"gate_id": "g-001"},
                    }
                )
            ],
        ),
    )

    assert updated.selected_run_detail is not None
    assert len(updated.selected_run_artifacts) == 2
    assert updated.selected_run_detail.active_gate is not None
    assert updated.run_event_mode == "sse"
    assert len(updated.run_timeline_items) == 1
    rendered = render_run_detail(updated, store)
    assert "Mode 1 Outputs" in rendered
    assert "no_new_rounds=2" in rendered
    assert "pc-002:0.82" in rendered
    assert "pc-004:below_top_k" in rendered
    assert "Event Timeline" in rendered


def test_approve_run_and_render_updates_run_status(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    session = ConnectionSession(
        api_base_url="http://ainrf.local",
        api_key="secret",
        reachable=True,
        authenticated=True,
        selected_project_slug="vision-stack",
        selected_run_task_id="t-001",
        selected_run_detail=build_task_detail("t-001", TaskStage.GATE_WAITING),
    )
    next_session, _ = save_project_from_form(
        session,
        store,
        name="Vision Stack",
        slug="vision-stack",
        description="",
        container_host="gpu-01",
        container_port=22,
        container_user="researcher",
        container_ssh_key_path="",
        container_project_dir="/workspace/projects/vision-stack",
        budget_gpu_hours=12.0,
        budget_api_cost_usd=6.0,
        budget_wall_clock_hours=24.0,
        webhook_url="",
        yolo=False,
        mode_one_domain_context="",
        mode_one_max_depth=3,
        mode_one_focus_directions="",
        mode_one_ignore_directions="",
        mode_two_scope="core-only",
        mode_two_target_tables="",
        mode_two_baseline_first=True,
    )
    next_session.selected_run_task_id = "t-001"
    next_session.selected_run_detail = build_task_detail("t-001", TaskStage.GATE_WAITING)
    store.save_project_run(
        build_run_binding(
            task_id="t-001",
            project_slug="vision-stack",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
        )
    )
    health = HealthResponse(
        status=ApiStatus.OK,
        state_root=".ainrf",
        container_configured=False,
        container_health=None,
        detail=None,
    )
    task_list = TaskListResponse(
        items=[build_task_summary("t-001", TaskMode.DEEP_REPRODUCTION, TaskStage.PLANNING)]
    )

    updated = approve_run_and_render(
        next_session,
        store,
        client_factory=lambda base_url, api_key: FakeClient(
            health=health,
            task_list=task_list,
            task_detail=build_task_detail("t-001", TaskStage.PLANNING),
            action_response=TaskActionResponse(
                task_id="t-001", status=TaskStage.PLANNING, detail="approved"
            ),
        ),
    )

    next_session = updated[0]
    assert next_session.selected_run_detail is not None
    assert next_session.selected_run_detail.status is TaskStage.PLANNING
    binding = store.load_project_run("t-001")
    assert binding is not None
    assert binding.last_known_status is TaskStage.PLANNING


def test_reject_run_and_render_updates_feedback_message(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    session = ConnectionSession(
        api_base_url="http://ainrf.local",
        api_key="secret",
        reachable=True,
        authenticated=True,
        selected_project_slug="vision-stack",
        selected_run_task_id="t-001",
        selected_run_detail=build_task_detail("t-001", TaskStage.GATE_WAITING),
    )
    next_session, _ = save_project_from_form(
        session,
        store,
        name="Vision Stack",
        slug="vision-stack",
        description="",
        container_host="gpu-01",
        container_port=22,
        container_user="researcher",
        container_ssh_key_path="",
        container_project_dir="/workspace/projects/vision-stack",
        budget_gpu_hours=12.0,
        budget_api_cost_usd=6.0,
        budget_wall_clock_hours=24.0,
        webhook_url="",
        yolo=False,
        mode_one_domain_context="",
        mode_one_max_depth=3,
        mode_one_focus_directions="",
        mode_one_ignore_directions="",
        mode_two_scope="core-only",
        mode_two_target_tables="",
        mode_two_baseline_first=True,
    )
    next_session.selected_run_task_id = "t-001"
    next_session.selected_run_detail = build_task_detail("t-001", TaskStage.GATE_WAITING)
    store.save_project_run(
        build_run_binding(
            task_id="t-001",
            project_slug="vision-stack",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
        )
    )
    health = HealthResponse(
        status=ApiStatus.OK,
        state_root=".ainrf",
        container_configured=False,
        container_health=None,
        detail=None,
    )
    task_list = TaskListResponse(
        items=[build_task_summary("t-001", TaskMode.DEEP_REPRODUCTION, TaskStage.CANCELLED)]
    )

    updated = reject_run_and_render(
        next_session,
        store,
        "not in scope",
        client_factory=lambda base_url, api_key: FakeClient(
            health=health,
            task_list=task_list,
            task_detail=TaskDetailResponse.model_validate(
                build_task_detail("t-001", TaskStage.CANCELLED).model_dump(mode="json")
            ),
            action_response=TaskActionResponse(
                task_id="t-001", status=TaskStage.CANCELLED, detail="rejected"
            ),
        ),
    )

    next_session = updated[0]
    assert next_session.selected_run_detail is not None
    assert next_session.selected_run_detail.status is TaskStage.CANCELLED


def build_run_binding(
    task_id: str,
    project_slug: str,
    mode: TaskMode,
    status: TaskStage,
) -> ProjectRunRecord:
    return ProjectRunRecord(
        task_id=task_id,
        project_slug=project_slug,
        mode=mode,
        paper_titles=["Paper"],
        last_known_status=status,
        last_known_stage=status,
    )
