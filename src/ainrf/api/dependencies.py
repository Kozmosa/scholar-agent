from __future__ import annotations

from fastapi import Request

from ainrf.api.config import ApiConfig
from ainrf.state import JsonStateStore


def get_api_config(request: Request) -> ApiConfig:
    return request.app.state.api_config


def get_state_store(request: Request) -> JsonStateStore:
    return request.app.state.state_store
