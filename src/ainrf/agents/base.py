from __future__ import annotations

from abc import ABC, abstractmethod

from ainrf.engine.models import AtomicTaskSpec, TaskExecutionResult, TaskPlanResult
from ainrf.execution import ContainerConfig


class AgentAdapterError(RuntimeError):
    pass


class AgentExecutionError(AgentAdapterError):
    def __init__(self, message: str, *, retryable: bool) -> None:
        super().__init__(message)
        self.retryable = retryable


class AgentAdapter(ABC):
    @abstractmethod
    async def bootstrap(self, container: ContainerConfig) -> None: ...

    @abstractmethod
    async def health_check(self, container: ContainerConfig) -> bool: ...

    @abstractmethod
    async def plan_reproduction(
        self,
        *,
        container: ContainerConfig,
        prompt: str,
        context: dict[str, object],
    ) -> TaskPlanResult: ...

    @abstractmethod
    async def execute_step(
        self,
        *,
        container: ContainerConfig,
        step: AtomicTaskSpec,
        context: dict[str, object],
    ) -> TaskExecutionResult: ...
