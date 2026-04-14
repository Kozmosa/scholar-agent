from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from ainrf.api.config import ApiConfig
from ainrf.api.middleware import build_api_key_middleware
from ainrf.api.routes.code import router as code_router
from ainrf.api.routes.health import router as health_router
from ainrf.api.routes.terminal import router as terminal_router
from ainrf.code_server import CodeServerSupervisor


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    config = app.state.api_config
    supervisor = CodeServerSupervisor(
        host=config.code_server_host,
        port=config.code_server_port,
        workspace_dir=config.code_server_workspace_dir,
        state_root=config.state_root,
    )
    app.state.code_server_supervisor = supervisor
    supervisor.start()
    try:
        yield
    finally:
        supervisor.stop()


def create_app(config: ApiConfig | None = None) -> FastAPI:
    api_config = config or ApiConfig.from_env()
    app = FastAPI(title="AINRF API", version="0.1.0", lifespan=lifespan)
    app.state.api_config = api_config
    app.middleware("http")(build_api_key_middleware(api_config))
    app.include_router(health_router)
    app.include_router(terminal_router)
    app.include_router(code_router)
    app.include_router(health_router, prefix="/v1")
    app.include_router(terminal_router, prefix="/v1")
    app.include_router(code_router, prefix="/v1")
    return app
