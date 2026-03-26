from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from ainrf.api.config import ApiConfig
from ainrf.api.middleware import build_api_key_middleware
from ainrf.events import JsonlTaskEventStore, TaskEventService
from ainrf.gates import HumanGateManager, WebhookDispatcher
from ainrf.api.routes.health import router as health_router
from ainrf.api.routes.tasks import router as tasks_router
from ainrf.runtime import WebhookSecretStore
from ainrf.state import JsonStateStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    sweep_task = asyncio.create_task(_gate_sweep_loop(app))
    try:
        yield
    finally:
        sweep_task.cancel()
        try:
            await sweep_task
        except asyncio.CancelledError:
            pass


async def _gate_sweep_loop(app: FastAPI) -> None:
    while True:
        await app.state.gate_manager.sweep_overdue_gates()
        await asyncio.sleep(app.state.api_config.gate_sweep_interval_seconds)


def create_app(config: ApiConfig | None = None) -> FastAPI:
    api_config = config or ApiConfig.from_env()
    app = FastAPI(title="AINRF API", version="0.1.0", lifespan=lifespan)
    state_store = JsonStateStore(api_config.state_root)
    event_store = JsonlTaskEventStore(api_config.state_root)
    app.state.api_config = api_config
    app.state.state_store = state_store
    app.state.event_service = TaskEventService(event_store)
    app.state.webhook_secret_store = WebhookSecretStore(api_config.state_root)
    app.state.gate_manager = HumanGateManager(
        store=state_store,
        event_service=app.state.event_service,
        webhook_dispatcher=WebhookDispatcher(timeout_seconds=api_config.webhook_timeout_seconds),
        secret_registry=app.state.webhook_secret_store,
        gate_timeout_seconds=api_config.gate_timeout_seconds,
    )
    app.middleware("http")(build_api_key_middleware(api_config))
    # Keep existing paths stable while exposing versioned aliases.
    app.include_router(health_router)
    app.include_router(tasks_router)
    app.include_router(health_router, prefix="/v1")
    app.include_router(tasks_router, prefix="/v1")
    return app
