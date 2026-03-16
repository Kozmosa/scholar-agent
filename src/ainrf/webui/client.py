from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

import httpx

from ainrf.api.schemas import (
    HealthResponse,
    TaskCreateRequest,
    TaskCreateResponse,
    TaskActionResponse,
    TaskDetailResponse,
    TaskListResponse,
)
from ainrf.events import TaskEvent, TaskEventCategory
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

    def create_task(self, payload: TaskCreateRequest) -> TaskCreateResponse:
        response = self._request(
            "POST",
            "/tasks",
            expected_statuses={201},
            json=payload.model_dump(mode="json", exclude_none=True),
        )
        return self._validate_model(response, TaskCreateResponse)

    def approve_task(self, task_id: str) -> TaskActionResponse:
        response = self._request("POST", f"/tasks/{task_id}/approve", expected_statuses={200})
        return self._validate_model(response, TaskActionResponse)

    def reject_task(self, task_id: str, feedback: str | None) -> TaskActionResponse:
        payload = {"feedback": feedback} if feedback is not None else {}
        response = self._request(
            "POST",
            f"/tasks/{task_id}/reject",
            expected_statuses={200},
            json=payload,
        )
        return self._validate_model(response, TaskActionResponse)

    def list_task_events(
        self,
        task_id: str,
        *,
        after_id: int | None = None,
        categories: set[TaskEventCategory] | None = None,
        read_timeout_seconds: float = 0.2,
    ) -> list[TaskEvent]:
        params: dict[str, str] | None = None
        if categories:
            params = {"types": ",".join(sorted(category.value for category in categories))}
        headers = self._headers()
        if after_id is not None:
            headers["Last-Event-ID"] = str(after_id)

        current: dict[str, str] = {}
        events: list[TaskEvent] = []
        timeout = httpx.Timeout(self.timeout_seconds, read=read_timeout_seconds)
        try:
            with httpx.Client(
                base_url=self.base_url.rstrip("/"),
                headers=headers,
                timeout=timeout,
                transport=self.transport,
            ) as client:
                with client.stream("GET", f"/tasks/{task_id}/events", params=params) as response:
                    if response.status_code == 401:
                        raise ApiAuthenticationError("Unauthorized")
                    if response.status_code != 200:
                        raise ApiProtocolError(
                            f"Unexpected response status {response.status_code} for GET /tasks/{task_id}/events"
                        )
                    try:
                        for line in response.iter_lines():
                            if line.startswith(":"):
                                continue
                            if line == "":
                                event = self._build_task_event_from_sse(current)
                                if event is not None:
                                    events.append(event)
                                current = {}
                                continue
                            key, _, value = line.partition(":")
                            if not _:
                                continue
                            current[key] = value.lstrip()
                    except httpx.ReadTimeout:
                        pass
        except httpx.HTTPError as exc:
            raise ApiConnectionError(f"Failed to reach AINRF API at {self.base_url}: {exc}") from exc

        trailing_event = self._build_task_event_from_sse(current)
        if trailing_event is not None:
            events.append(trailing_event)
        return events

    def _request(
        self,
        method: str,
        path: str,
        *,
        authenticate: bool = True,
        expected_statuses: set[int],
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
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
                response = client.request(method, path, params=params, json=json)
        except httpx.HTTPError as exc:
            raise ApiConnectionError(f"Failed to reach AINRF API at {self.base_url}: {exc}") from exc
        if response.status_code == 401:
            raise ApiAuthenticationError("Unauthorized")
        if response.status_code not in expected_statuses:
            raise ApiProtocolError(
                f"Unexpected response status {response.status_code} for {method} {path}"
            )
        return response

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

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

    @staticmethod
    def _build_task_event_from_sse(payload: dict[str, str]) -> TaskEvent | None:
        data = payload.get("data")
        if data is None:
            return None
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ApiProtocolError(f"AINRF API returned invalid SSE payload: {exc}") from exc
        try:
            return TaskEvent.model_validate(parsed)
        except Exception as exc:
            raise ApiProtocolError(f"AINRF API returned invalid event payload: {exc}") from exc
