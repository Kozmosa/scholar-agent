from __future__ import annotations

import asyncio
from pathlib import Path
from typing import cast

from ainrf.agents import AgentAdapter
from ainrf.agents.base import AgentExecutionError
from ainrf.artifacts import (
    ArtifactType,
    EvidenceRecord,
    EvidenceType,
    ExperimentRun,
    ExplorationGraph,
    QualityAssessment,
)
from ainrf.engine.engine import EngineContext, TaskEngine
from ainrf.engine.models import AtomicTaskSpec, TaskExecutionResult, TaskPlanResult
from ainrf.events import JsonlTaskEventStore, TaskEventService
from ainrf.gates import HumanGateManager, WebhookDispatcher
from ainrf.parsing import ParseFailure, ParseFailureType, ParseMetadata, ParseRequest, ParseResult
from ainrf.runtime import WebhookSecretStore
from ainrf.state import JsonStateStore, TaskCheckpoint, TaskMode, TaskRecord, TaskStage


class NoopWebhookDispatcher(WebhookDispatcher):
    async def send(self, *, url: str, secret: str | None, payload: object) -> None:
        _ = url, secret, payload
        return None


class FakeParser:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    async def parse_pdf(self, request: ParseRequest) -> ParseResult | ParseFailure:
        if self.fail:
            return ParseFailure(
                failure_type=ParseFailureType.INVALID_STRUCTURE,
                message="bad pdf",
                retryable=False,
            )
        return ParseResult(
            markdown="# Paper",
            metadata=ParseMetadata(title="Attention Is All You Need", abstract="Abstract"),
        )


class FakeAdapter(AgentAdapter):
    def __init__(self, *, budget_gpu: float = 0.5) -> None:
        self.plan_contexts: list[dict[str, object]] = []
        self.bootstrap_calls = 0
        self.budget_gpu = budget_gpu

    async def bootstrap(self, container: object) -> None:
        _ = container
        self.bootstrap_calls += 1

    async def health_check(self, container: object) -> bool:
        _ = container
        return True

    async def plan_reproduction(
        self,
        *,
        container: object,
        prompt: str,
        context: dict[str, object],
    ) -> TaskPlanResult:
        _ = container, prompt
        self.plan_contexts.append(context)
        if context.get("task_mode") == TaskMode.RESEARCH_DISCOVERY.value:
            paper_card = cast(dict[str, object], context["paper_card"])
            return TaskPlanResult(
                summary="Planned literature exploration",
                milestones=["Clarify", "Explore", "Report"],
                estimated_steps=4,
                strategy="research-discovery",
                target_paper_id=str(paper_card["artifact_id"]),
                success_criteria=["graph and claims generated"],
                steps=[
                    AtomicTaskSpec(
                        step_id="m1-step-1",
                        kind="clarify_research_goal",
                        title="Clarify goal",
                        payload={"domain_context": "llm systems"},
                    ),
                    AtomicTaskSpec(
                        step_id="m1-step-2",
                        kind="update_knowledge_graph",
                        title="Update graph",
                        payload={},
                    ),
                    AtomicTaskSpec(
                        step_id="m1-step-3",
                        kind="check_termination",
                        title="Check termination",
                        payload={},
                    ),
                    AtomicTaskSpec(
                        step_id="m1-step-4",
                        kind="generate_discovery_report",
                        title="Generate report",
                        payload={"output_path": "reports/discovery/discovery-report.md"},
                    ),
                ],
            )
        paper_card = cast(dict[str, object], context["paper_card"])
        return TaskPlanResult(
            summary="Planned deep reproduction",
            milestones=["Implement", "Validate"],
            estimated_steps=2,
            strategy="implement-from-paper",
            target_paper_id=str(paper_card["artifact_id"]),
            success_criteria=["step done"],
            steps=[
                AtomicTaskSpec(
                    step_id="step-1",
                    kind="implement_module",
                    title="Implement core",
                    payload={"module": "core"},
                ),
                AtomicTaskSpec(
                    step_id="step-2",
                    kind="summarize_execution",
                    title="Summarize",
                    payload={"path": "reports/reproduction/summary.md"},
                ),
            ],
        )

    async def execute_step(
        self,
        *,
        container: object,
        step: AtomicTaskSpec,
        context: dict[str, object],
    ) -> TaskExecutionResult:
        _ = container, context
        if step.kind == "update_knowledge_graph":
            return TaskExecutionResult(
                status="succeeded",
                summary="Updated discovery graph",
                resource_usage={"gpu_hours": self.budget_gpu, "api_cost_usd": 1.0, "wall_clock_hours": 0.1},
                step_updates={
                    "knowledge_graph_update": {
                        "claims": [
                            {
                                "statement": "Adapter-based transfer remains stable under low budget.",
                                "confidence": 0.73,
                            }
                        ]
                    }
                },
            )
        if step.kind == "check_termination":
            return TaskExecutionResult(
                status="succeeded",
                summary="Termination condition reached",
                resource_usage={"gpu_hours": 0.0, "api_cost_usd": 0.0, "wall_clock_hours": 0.0},
                step_updates={
                    "termination": {
                        "should_terminate": True,
                        "reason": "diminishing_returns",
                    }
                },
            )
        return TaskExecutionResult(
            status="succeeded",
            summary=f"Executed {step.kind}",
            resource_usage={"gpu_hours": self.budget_gpu, "api_cost_usd": 1.0, "wall_clock_hours": 0.1},
        )


def make_task(tmp_path: Path, *, mode: TaskMode = TaskMode.DEEP_REPRODUCTION, yolo: bool = False) -> TaskRecord:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"%PDF-1.4")
    return TaskRecord(
        task_id="t-001",
        mode=mode,
        status=TaskStage.PLANNING,
        checkpoint=TaskCheckpoint(current_stage=TaskStage.PLANNING),
        config={
            "papers": [{"title": "Paper", "pdf_path": str(pdf_path), "role": "target"}],
            "container": {
                "host": "gpu-server-01",
                "port": 22,
                "user": "researcher",
                "ssh_key_path": "/tmp/id",
                "project_dir": "/workspace/project",
            },
            "webhook_url": "https://example.com/hooks/ainrf",
            "yolo": yolo,
        },
    )


def make_engine(
    tmp_path: Path,
    *,
    adapter: FakeAdapter | None = None,
    parser: FakeParser | None = None,
) -> tuple[TaskEngine, JsonStateStore, HumanGateManager]:
    store = JsonStateStore(tmp_path)
    event_service = TaskEventService(JsonlTaskEventStore(tmp_path))
    gate_manager = HumanGateManager(
        store=store,
        event_service=event_service,
        webhook_dispatcher=NoopWebhookDispatcher(),
        secret_registry=WebhookSecretStore(tmp_path),
        gate_timeout_seconds=3600,
    )
    engine = TaskEngine(
        EngineContext(
            state_store=store,
            event_service=event_service,
            gate_manager=gate_manager,
            parser=parser or FakeParser(),
            agent_adapter=adapter or FakeAdapter(),
            runtime_root=tmp_path,
        )
    )
    return engine, store, gate_manager


def test_run_once_ingests_and_creates_plan_gate(tmp_path: Path) -> None:
    engine, store, _gate_manager = make_engine(tmp_path)
    task = make_task(tmp_path)
    store.save_task(task)

    ran = asyncio.run(engine.run_once())

    updated = store.load_task("t-001")
    assert ran is True
    assert updated is not None
    assert updated.status is TaskStage.GATE_WAITING
    assert store.query_artifacts(ArtifactType.PAPER_CARD)
    assert store.query_artifacts(ArtifactType.REPRODUCTION_TASK)


def test_run_once_executes_after_plan_gate_approval(tmp_path: Path) -> None:
    adapter = FakeAdapter()
    engine, store, gate_manager = make_engine(tmp_path, adapter=adapter)
    task = make_task(tmp_path)
    store.save_task(task)
    asyncio.run(engine.run_once())
    waiting = store.load_task("t-001")
    assert waiting is not None
    approved_task, _gate = asyncio.run(
        gate_manager.resolve_current_gate(task=waiting, approved=True, feedback=None)
    )

    store.save_task(approved_task)
    asyncio.run(engine.run_once())
    asyncio.run(engine.run_once())

    completed = store.load_task("t-001")
    assert completed is not None
    assert completed.status is TaskStage.COMPLETED
    events = JsonlTaskEventStore(tmp_path).list_events("t-001")
    assert "task.progress" in [event.event for event in events]
    assert "task.completed" in [event.event for event in events]


def test_run_once_replans_with_reject_feedback(tmp_path: Path) -> None:
    adapter = FakeAdapter()
    engine, store, gate_manager = make_engine(tmp_path, adapter=adapter)
    store.save_task(make_task(tmp_path))
    asyncio.run(engine.run_once())
    waiting = store.load_task("t-001")
    assert waiting is not None
    rejected_task, _gate = asyncio.run(
        gate_manager.resolve_current_gate(task=waiting, approved=False, feedback="tighten scope")
    )
    store.save_task(rejected_task)

    asyncio.run(engine.run_once())

    assert adapter.plan_contexts[-1]["latest_feedback"] == "tighten scope"


def test_run_once_executes_research_discovery_mode(tmp_path: Path) -> None:
    engine, store, _gate_manager = make_engine(tmp_path)
    store.save_task(make_task(tmp_path, mode=TaskMode.RESEARCH_DISCOVERY, yolo=True))

    asyncio.run(engine.run_once())
    for _ in range(5):
        task = store.load_task("t-001")
        assert task is not None
        if task.status is TaskStage.COMPLETED:
            break
        asyncio.run(engine.run_once())

    task = store.load_task("t-001")
    assert task is not None
    assert task.status is TaskStage.COMPLETED
    assert task.termination_reason == "diminishing_returns"

    exploration_graphs = store.query_artifacts(ArtifactType.EXPLORATION_GRAPH)
    assert len(exploration_graphs) == 1
    graph = exploration_graphs[0]
    assert isinstance(graph, ExplorationGraph)
    assert graph.max_depth == 3
    assert graph.max_breadth == 3

    claims = store.query_artifacts(ArtifactType.CLAIM)
    assert claims


def test_run_once_completes_when_budget_exhausted(tmp_path: Path) -> None:
    adapter = FakeAdapter(budget_gpu=2.0)
    engine, store, gate_manager = make_engine(tmp_path, adapter=adapter)
    task = make_task(tmp_path, yolo=True)
    task = task.model_copy(
        update={
            "budget_limit": task.budget_limit.model_copy(update={"gpu_hours": 1.0, "api_cost_usd": 10.0, "wall_clock_hours": 10.0})
        }
    )
    store.save_task(task)
    asyncio.run(engine.run_once())
    waiting = store.load_task("t-001")
    assert waiting is not None
    assert waiting.status is TaskStage.EXECUTING

    asyncio.run(engine.run_once())

    completed = store.load_task("t-001")
    assert completed is not None
    assert completed.status is TaskStage.COMPLETED
    assert completed.termination_reason == "budget_exhausted"


def test_run_once_retryable_execution_error_rotates_pending_queue(tmp_path: Path) -> None:
    class RetryOnceAdapter(FakeAdapter):
        def __init__(self) -> None:
            super().__init__()
            self.failed_steps: set[str] = set()

        async def execute_step(
            self,
            *,
            container: object,
            step: AtomicTaskSpec,
            context: dict[str, object],
        ) -> TaskExecutionResult:
            _ = container, context
            if step.kind == "implement_module" and step.step_id not in self.failed_steps:
                self.failed_steps.add(step.step_id)
                raise AgentExecutionError("temporary timeout", retryable=True)
            return await super().execute_step(container=container, step=step, context=context)

    adapter = RetryOnceAdapter()
    engine, store, _gate_manager = make_engine(tmp_path, adapter=adapter)
    task = make_task(tmp_path, yolo=True)
    store.save_task(task)

    asyncio.run(engine.run_once())
    queued = store.load_task("t-001")
    assert queued is not None
    assert queued.status is TaskStage.EXECUTING

    asyncio.run(engine.run_once())
    retried = store.load_task("t-001")
    assert retried is not None
    assert retried.status is TaskStage.EXECUTING
    assert len(retried.checkpoint.pending_queue) == 2
    assert retried.checkpoint.pending_queue[0].step == "summarize_execution"
    assert retried.checkpoint.pending_queue[1].step == "implement_module"
    assert retried.checkpoint.pending_queue[1].details.get("retry_count") == 1

    asyncio.run(engine.run_once())
    asyncio.run(engine.run_once())

    completed = store.load_task("t-001")
    assert completed is not None
    assert completed.status is TaskStage.COMPLETED


def test_run_once_retryable_execution_error_exhaustion_fails(tmp_path: Path) -> None:
    class AlwaysRetryableErrorAdapter(FakeAdapter):
        async def plan_reproduction(
            self,
            *,
            container: object,
            prompt: str,
            context: dict[str, object],
        ) -> TaskPlanResult:
            _ = container, prompt, context
            return TaskPlanResult(
                summary="Single-step plan",
                milestones=["Implement"],
                estimated_steps=1,
                strategy="implement-from-paper",
                target_paper_id="pc-001",
                success_criteria=["step done"],
                steps=[
                    AtomicTaskSpec(
                        step_id="step-1",
                        kind="implement_module",
                        title="Implement core",
                        payload={"module": "core"},
                    )
                ],
            )

        async def execute_step(
            self,
            *,
            container: object,
            step: AtomicTaskSpec,
            context: dict[str, object],
        ) -> TaskExecutionResult:
            _ = container, step, context
            raise AgentExecutionError("still flaky", retryable=True)

    adapter = AlwaysRetryableErrorAdapter()
    engine, store, _gate_manager = make_engine(tmp_path, adapter=adapter)
    task = make_task(tmp_path, yolo=True)
    store.save_task(task)

    asyncio.run(engine.run_once())
    for _ in range(4):
        asyncio.run(engine.run_once())

    failed = store.load_task("t-001")
    assert failed is not None
    assert failed.status is TaskStage.FAILED
    assert failed.termination_reason == "agent_execution_retry_exhausted"


def test_run_once_produces_experiment_runs_and_quality_assessment(tmp_path: Path) -> None:
    class P8StyleAdapter(FakeAdapter):
        async def plan_reproduction(
            self,
            *,
            container: object,
            prompt: str,
            context: dict[str, object],
        ) -> TaskPlanResult:
            _ = container, prompt, context
            return TaskPlanResult(
                summary="P8 style plan",
                milestones=["Baseline", "Full"],
                estimated_steps=2,
                strategy="implement-from-paper",
                target_paper_id="pc-001",
                success_criteria=["baseline done", "full done"],
                steps=[
                    AtomicTaskSpec(
                        step_id="step-baseline",
                        kind="run_baseline",
                        title="Run baseline",
                    ),
                    AtomicTaskSpec(
                        step_id="step-full",
                        kind="run_full_experiment",
                        title="Run full experiment",
                    ),
                ],
            )

        async def execute_step(
            self,
            *,
            container: object,
            step: AtomicTaskSpec,
            context: dict[str, object],
        ) -> TaskExecutionResult:
            _ = container, context
            return TaskExecutionResult(
                status="succeeded",
                summary=f"Finished {step.kind}",
                step_updates={"metrics": {"accuracy": 0.9}},
                resource_usage={"gpu_hours": 0.2, "api_cost_usd": 1.0, "wall_clock_hours": 0.1},
            )

    adapter = P8StyleAdapter()
    engine, store, _gate_manager = make_engine(tmp_path, adapter=adapter)
    store.save_task(make_task(tmp_path, yolo=True))

    asyncio.run(engine.run_once())
    asyncio.run(engine.run_once())
    asyncio.run(engine.run_once())

    completed = store.load_task("t-001")
    assert completed is not None
    assert completed.status is TaskStage.COMPLETED

    runs = store.query_artifacts(ArtifactType.EXPERIMENT_RUN)
    assert len(runs) == 2
    assert all(isinstance(item, ExperimentRun) for item in runs)
    assert {run.run_type for run in runs if isinstance(run, ExperimentRun)} == {
        "baseline",
        "full_reproduction",
    }

    assessments = store.query_artifacts(ArtifactType.QUALITY_ASSESSMENT)
    assert len(assessments) == 1
    assert isinstance(assessments[0], QualityAssessment)
    assert assessments[0].source_task_id == "t-001"


def test_run_once_records_deviation_evidence_when_threshold_exceeded(tmp_path: Path) -> None:
    class DeviationAdapter(FakeAdapter):
        async def plan_reproduction(
            self,
            *,
            container: object,
            prompt: str,
            context: dict[str, object],
        ) -> TaskPlanResult:
            _ = container, prompt, context
            return TaskPlanResult(
                summary="Deviation plan",
                milestones=["Baseline"],
                estimated_steps=1,
                strategy="implement-from-paper",
                target_paper_id="pc-001",
                success_criteria=["detect deviation"],
                steps=[
                    AtomicTaskSpec(
                        step_id="step-baseline",
                        kind="run_baseline",
                        title="Run baseline",
                        payload={
                            "expected_metrics": {"accuracy": 0.95},
                            "deviation_threshold_percent": 5.0,
                        },
                    )
                ],
            )

        async def execute_step(
            self,
            *,
            container: object,
            step: AtomicTaskSpec,
            context: dict[str, object],
        ) -> TaskExecutionResult:
            _ = container, step, context
            return TaskExecutionResult(
                status="succeeded",
                summary="Baseline completed",
                step_updates={"metrics": {"accuracy": 0.80}},
                resource_usage={"gpu_hours": 0.1, "api_cost_usd": 0.5, "wall_clock_hours": 0.05},
            )

    adapter = DeviationAdapter()
    engine, store, _gate_manager = make_engine(tmp_path, adapter=adapter)
    store.save_task(make_task(tmp_path, yolo=True))

    asyncio.run(engine.run_once())
    asyncio.run(engine.run_once())

    evidence_items = store.query_artifacts(ArtifactType.EVIDENCE_RECORD)
    assert len(evidence_items) == 1
    evidence = evidence_items[0]
    assert isinstance(evidence, EvidenceRecord)
    assert evidence.evidence_type is EvidenceType.DEVIATION_ANALYSIS
    assert evidence.source_task_id == "t-001"

    events = JsonlTaskEventStore(tmp_path).list_events("t-001")
    event_names = [item.event for item in events]
    assert "deviation.detected" in event_names
    assert "diagnosis.completed" in event_names


def test_run_once_records_analysis_evidence_from_diagnose_and_compare_steps(tmp_path: Path) -> None:
    class AnalysisAdapter(FakeAdapter):
        async def plan_reproduction(
            self,
            *,
            container: object,
            prompt: str,
            context: dict[str, object],
        ) -> TaskPlanResult:
            _ = container, prompt, context
            return TaskPlanResult(
                summary="Analysis plan",
                milestones=["Diagnose", "Compare"],
                estimated_steps=2,
                strategy="implement-from-paper",
                target_paper_id="pc-001",
                success_criteria=["analysis done"],
                steps=[
                    AtomicTaskSpec(
                        step_id="step-diagnose",
                        kind="diagnose_deviation",
                        title="Diagnose deviation",
                    ),
                    AtomicTaskSpec(
                        step_id="step-compare",
                        kind="compare_tables",
                        title="Compare tables",
                    ),
                ],
            )

        async def execute_step(
            self,
            *,
            container: object,
            step: AtomicTaskSpec,
            context: dict[str, object],
        ) -> TaskExecutionResult:
            _ = container, context
            if step.kind == "diagnose_deviation":
                return TaskExecutionResult(
                    status="succeeded",
                    summary="Diagnosis completed",
                    step_updates={"diagnosis": {"summary": "Tokenizer mismatch"}},
                )
            return TaskExecutionResult(
                status="succeeded",
                summary="Comparison completed",
                step_updates={
                    "table_comparisons": [
                        {
                            "table_id": "table-1",
                            "metric": "accuracy",
                            "paper_value": 0.9,
                            "reproduced_value": 0.89,
                        }
                    ]
                },
            )

    adapter = AnalysisAdapter()
    engine, store, _gate_manager = make_engine(tmp_path, adapter=adapter)
    store.save_task(make_task(tmp_path, yolo=True))

    asyncio.run(engine.run_once())
    asyncio.run(engine.run_once())
    asyncio.run(engine.run_once())

    completed = store.load_task("t-001")
    assert completed is not None
    assert completed.status is TaskStage.COMPLETED

    evidence_items = [
        item
        for item in store.query_artifacts(ArtifactType.EVIDENCE_RECORD)
        if isinstance(item, EvidenceRecord)
    ]
    assert len(evidence_items) == 2
    assert all(item.evidence_type is EvidenceType.DEVIATION_ANALYSIS for item in evidence_items)
