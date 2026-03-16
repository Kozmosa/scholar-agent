from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from ainrf.api.schemas import HealthResponse, TaskDetailResponse, TaskListResponse
from ainrf.state import TaskStage


class ApiClientError(RuntimeError):
    """Base error for WebUI API client failures."""


class ApiConnectionError(ApiClientError):
    """Raised when the API cannot be reached."""


class ApiAuthenticationError(ApiClientError):
    """Raised when the API rejects the provided API key."""


class ApiProtocolError(ApiClientError):
    """Raised when the API responds with an unexpected payload or status."""


@dataclass(slots=True)
class AinrfApiClient:
    base_url: str
    api_key: str | None = None
    timeout_seconds: float = 5.0
    transport: httpx.BaseTransport | None = None

    def get_health(self) -> HealthResponse:
        response = self._request("GET", "/health", authenticate=False, expected_statuses={200, 503})
        return self._validate_model(response, HealthResponse)

    def list_tasks(self, status: TaskStage | None = None) -> TaskListResponse:
        params: dict[str, str] | None = None
        if status is not None:
            params = {"status": status.value}
        response = self._request("GET", "/tasks", params=params, expected_statuses={200})
        return self._validate_model(response, TaskListResponse)

    def get_task(self, task_id: str) -> TaskDetailResponse:
        response = self._request("GET", f"/tasks/{task_id}", expected_statuses={200})
        return self._validate_model(response, TaskDetailResponse)

    def _request(
        self,
        method: str,
        path: str,
        *,
        authenticate: bool = True,
        expected_statuses: set[int],
        params: dict[str, str] | None = None,
    ) -> httpx.Response:
        headers: dict[str, str] = {}
        if authenticate and self.api_key:
            headers["X-API-Key"] = self.api_key
        try:
            with httpx.Client(
                base_url=self.base_url.rstrip("/"),
                headers=headers,
                timeout=self.timeout_seconds,
                transport=self.transport,
            ) as client:
                response = client.request(method, path, params=params)
        except httpx.HTTPError as exc:
            raise ApiConnectionError(f"Failed to reach AINRF API at {self.base_url}: {exc}") from exc
        if response.status_code == 401:
            raise ApiAuthenticationError("Unauthorized")
        if response.status_code not in expected_statuses:
            raise ApiProtocolError(
                f"Unexpected response status {response.status_code} for {method} {path}"
            )
        return response

    @staticmethod
    def _validate_model(response: httpx.Response, model_type: type[Any]) -> Any:
        try:
            payload = response.json()
        except ValueError as exc:
            raise ApiProtocolError("AINRF API returned invalid JSON") from exc
        try:
            return model_type.model_validate(payload)
        except Exception as exc:
            raise ApiProtocolError(f"AINRF API returned invalid payload: {exc}") from exc
