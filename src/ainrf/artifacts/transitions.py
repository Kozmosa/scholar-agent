from __future__ import annotations

from collections.abc import Mapping, Set

from ainrf.artifacts.errors import InvalidTransitionError
from ainrf.artifacts.models import ArtifactType

TransitionMap = Mapping[ArtifactType, Mapping[str, Set[str]]]


TRANSITIONS: TransitionMap = {
    ArtifactType.PAPER_CARD: {
        "captured": {"structured"},
        "structured": set(),
    },
    ArtifactType.REPRODUCTION_TASK: {
        "proposed": {"active", "blocked", "completed"},
        "active": {"blocked", "completed"},
        "blocked": set(),
        "completed": set(),
    },
    ArtifactType.EXPERIMENT_RUN: {
        "pending": {"running", "cancelled"},
        "running": {"completed", "failed", "env_failure", "cancelled"},
        "completed": set(),
        "failed": set(),
        "env_failure": set(),
        "cancelled": set(),
    },
    ArtifactType.HUMAN_GATE: {
        "waiting": {"approved", "rejected", "cancelled"},
        "approved": set(),
        "rejected": set(),
        "cancelled": set(),
    },
}


def get_allowed_transitions(artifact_type: ArtifactType, current_status: str) -> set[str]:
    return set(TRANSITIONS.get(artifact_type, {}).get(current_status, set()))


def assert_transition_allowed(
    artifact_type: ArtifactType,
    current_status: str,
    next_status: str,
) -> None:
    allowed = get_allowed_transitions(artifact_type, current_status)
    if next_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid transition for {artifact_type.value}: {current_status!r} -> {next_status!r}"
        )
