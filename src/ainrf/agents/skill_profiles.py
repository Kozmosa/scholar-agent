from __future__ import annotations

from dataclasses import dataclass

from ainrf.engine.models import AtomicTaskSpec


@dataclass(frozen=True, slots=True)
class StepSkillProfile:
    skill_name: str
    objective: str
    output_key: str
    guidance: tuple[str, ...]

    def to_payload(
        self,
        *,
        step: AtomicTaskSpec,
        context: dict[str, object],
    ) -> dict[str, object]:
        return {
            "skill_name": self.skill_name,
            "objective": self.objective,
            "output_key": self.output_key,
            "guidance": list(self.guidance),
            "step_kind": step.kind,
            "step_title": step.title,
            "step_payload": step.payload,
            "task_context": context,
        }


_STEP_SKILL_PROFILES: dict[str, StepSkillProfile] = {
    "clarify_research_goal": StepSkillProfile(
        skill_name="idea-discovery",
        objective="Clarify the research objective, focus directions, and ignored directions before literature expansion.",
        output_key="problem_profile",
        guidance=(
            "Condense the user's research goal into a short scope statement.",
            "Return focus_directions and ignore_directions as short lists.",
            "Prefer actionable clarification over generic background exposition.",
        ),
    ),
    "extract_references": StepSkillProfile(
        skill_name="research-lit",
        objective="Identify candidate references relevant to the research question and rank signal quality.",
        output_key="reference_candidates",
        guidance=(
            "Prefer papers tightly coupled to the target problem, not broad surveys unless foundational.",
            "Include lightweight ranking signals such as novelty, method difference, and citation_count when available.",
            "Return compact candidate entries that are easy to persist into the exploration queue.",
        ),
    ),
    "prioritize_references": StepSkillProfile(
        skill_name="research-lit",
        objective="Rank extracted references for the next exploration round.",
        output_key="ranked_references",
        guidance=(
            "Prioritize by relevance to the research goal, expected novelty signal, and methodological diversity.",
            "Assign explicit rank values starting at 1.",
            "Keep the top of the list concise and execution-oriented.",
        ),
    ),
    "explore_paper": StepSkillProfile(
        skill_name="research-lit",
        objective="Extract claims, follow-up references, and exploration queue updates from a single paper.",
        output_key="exploration",
        guidance=(
            "Return visited_paper_ids, queued_paper_ids, current_depth, and new_claims.",
            "Prefer claims backed by evidence or quantitative observations over vague narratives.",
            "Keep follow-up references tightly scoped to the current paper's main method cluster.",
        ),
    ),
    "update_knowledge_graph": StepSkillProfile(
        skill_name="idea-discovery",
        objective="Synthesize newly explored evidence into graph-ready claim and relation updates.",
        output_key="knowledge_graph_update",
        guidance=(
            "Emit graph-ready claims or relations, not prose-only summaries.",
            "Prefer concise claim statements with confidence scores where possible.",
            "Group updates around the active method cluster.",
        ),
    ),
    "summarize_method_cluster": StepSkillProfile(
        skill_name="research-lit",
        objective="Summarize the current method cluster, evaluation norms, and open tensions.",
        output_key="method_cluster",
        guidance=(
            "Summaries should focus on consensus, disagreement, and experiment conventions.",
            "Include the cluster name in the output.",
            "Keep the summary short enough to be shown directly in the run detail UI.",
        ),
    ),
    "evaluate_user_idea": StepSkillProfile(
        skill_name="research-review",
        objective="Assess feasibility, risks, and minimal validation path for the user's proposed idea.",
        output_key="idea_evaluation",
        guidance=(
            "Return feasibility, major risks, and a minimal validation path when possible.",
            "Use critique grounded in related work rather than generic optimism.",
            "Call out disqualifying assumptions explicitly.",
        ),
    ),
    "propose_idea_directions": StepSkillProfile(
        skill_name="idea-discovery",
        objective="Generate a few concrete idea directions emerging from the current exploration state.",
        output_key="idea_candidates",
        guidance=(
            "Return a short ranked list of candidate ideas with rationale.",
            "Prefer ideas that connect gaps or tensions found in the explored papers.",
            "Avoid generic future work statements.",
        ),
    ),
    "analyze_method": StepSkillProfile(
        skill_name="research-review",
        objective="Extract the core method, implementation-critical details, and high-risk assumptions from the target paper.",
        output_key="method_analysis",
        guidance=(
            "Focus on architecture, losses, training assumptions, and target tables.",
            "Call out underspecified details that may block reproduction.",
            "Prefer implementer-facing analysis over paper summary prose.",
        ),
    ),
    "plan_implementation": StepSkillProfile(
        skill_name="run-experiment",
        objective="Turn the target reproduction scope into an execution plan with build and experiment milestones.",
        output_key="implementation_plan",
        guidance=(
            "Sequence implementation, baseline validation, and full experiment runs.",
            "Call out missing dependencies or environment assumptions.",
            "Keep milestones concrete enough for direct execution.",
        ),
    ),
    "run_baseline": StepSkillProfile(
        skill_name="run-experiment",
        objective="Run a cheap baseline reproduction and report metrics plus run metadata.",
        output_key="metrics",
        guidance=(
            "Return metrics in a machine-readable mapping.",
            "Mention the smallest configuration that still validates pipeline correctness.",
            "If execution is partial, expose what completed and what remains blocked.",
        ),
    ),
    "diagnose_deviation": StepSkillProfile(
        skill_name="analyze-results",
        objective="Diagnose why reproduced metrics deviate from expected values and suggest the minimum fixes.",
        output_key="diagnosis",
        guidance=(
            "Return a concise diagnosis summary and actionable fix list.",
            "Ground the diagnosis in the actual metric deltas when available.",
            "Prioritize cheap, high-signal fixes first.",
        ),
    ),
    "run_full_experiment": StepSkillProfile(
        skill_name="run-experiment",
        objective="Execute the full reproduction configuration and report final metrics.",
        output_key="metrics",
        guidance=(
            "Return final metrics in a machine-readable mapping.",
            "Capture whether the run is full-suite or narrowed scope.",
            "Surface incomplete sub-runs instead of hiding them.",
        ),
    ),
    "compare_tables": StepSkillProfile(
        skill_name="analyze-results",
        objective="Compare reproduced results against target paper tables and quantify deviation.",
        output_key="table_comparisons",
        guidance=(
            "Return one comparison entry per target table or metric.",
            "Include paper_value, reproduced_value, and deviation_percent when possible.",
            "Make the result directly usable as evidence.",
        ),
    ),
    "generate_quality_assessment": StepSkillProfile(
        skill_name="research-review",
        objective="Critically assess research contribution, reproducibility, and scientific rigor from the current evidence.",
        output_key="quality_assessment",
        guidance=(
            "Return machine-readable scores or score-like fields for core assessment dimensions.",
            "Ground the assessment in completed runs and deviation evidence.",
            "Prefer concrete criticism over vague praise.",
        ),
    ),
}


def get_step_skill_profile(step_kind: str) -> StepSkillProfile | None:
    return _STEP_SKILL_PROFILES.get(step_kind)


def build_step_skill_payload(
    step: AtomicTaskSpec,
    context: dict[str, object],
) -> dict[str, object] | None:
    profile = get_step_skill_profile(step.kind)
    if profile is None:
        return None
    return profile.to_payload(step=step, context=context)
