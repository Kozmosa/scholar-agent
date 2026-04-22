from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from anyio import to_thread
from fastapi import FastAPI

from ainrf.api.config import ApiConfig
from ainrf.api.middleware import build_api_key_middleware
from ainrf.api.routes.code import router as code_router
from ainrf.api.routes.environments import router as environments_router
from ainrf.api.routes.health import router as health_router
from ainrf.api.routes.projects import router as projects_router
from ainrf.api.routes.terminal import router as terminal_router
from ainrf.code_server import CodeServerSupervisor
from ainrf.environments import InMemoryEnvironmentService
from ainrf.terminal.pty import stop_terminal_session


def _run_sync_in_lifespan(callback: Callable[[], None]) -> Awaitable[None]:
    return to_thread.run_sync(callback)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    environment_service = app.state.environment_service
    manager = CodeServerSupervisor(
        state_root=app.state.api_config.state_root,
        environment_service=environment_service,
        local_host=app.state.api_config.code_server_host,
        local_port=app.state.api_config.code_server_port,
    )
    app.state.code_server_manager = manager
    app.state.code_server_supervisor = manager
    try:
        yield
    finally:
        terminal_runtime = getattr(app.state, "terminal_runtime", None)
        if terminal_runtime is not None:
            await _run_sync_in_lifespan(lambda: stop_terminal_session(terminal_runtime))
        await manager.stop()


def create_app(config: ApiConfig | None = None) -> FastAPI:
    api_config = config or ApiConfig.from_env()
    app = FastAPI(title="AINRF API", version="0.1.0", lifespan=lifespan)
    app.state.api_config = api_config
    app.state.environment_service = InMemoryEnvironmentService()
    app.middleware("http")(build_api_key_middleware(api_config))
    app.include_router(health_router)
    app.include_router(environments_router)
    app.include_router(projects_router)
    app.include_router(terminal_router)
    app.include_router(code_router)
    app.include_router(health_router, prefix="/v1")
    app.include_router(environments_router, prefix="/v1")
    app.include_router(projects_router, prefix="/v1")
    app.include_router(terminal_router, prefix="/v1")
    app.include_router(code_router, prefix="/v1")
    return app
