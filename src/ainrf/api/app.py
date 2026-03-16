from __future__ import annotations

from fastapi import FastAPI

from ainrf.api.config import ApiConfig
from ainrf.api.middleware import build_api_key_middleware
from ainrf.api.routes.health import router as health_router
from ainrf.api.routes.tasks import router as tasks_router
from ainrf.state import JsonStateStore


def create_app(config: ApiConfig | None = None) -> FastAPI:
    api_config = config or ApiConfig.from_env()
    app = FastAPI(title="AINRF API", version="0.1.0")
    app.state.api_config = api_config
    app.state.state_store = JsonStateStore(api_config.state_root)
    app.middleware("http")(build_api_key_middleware(api_config))
    app.include_router(health_router)
    app.include_router(tasks_router)
    return app
