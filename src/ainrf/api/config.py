from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
from typing import cast
import os

from ainrf.execution import ContainerConfig
from ainrf.state import default_state_root


def hash_api_key(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _parse_api_key_hashes(raw: str) -> frozenset[str]:
    hashes = {item.strip() for item in raw.split(",") if item.strip()}
    return frozenset(hashes)


@dataclass(slots=True)
class ApiConfig:
    api_key_hashes: frozenset[str]
    state_root: Path
    container_config: ContainerConfig | None = None
    gate_timeout_seconds: int = 3600
    gate_sweep_interval_seconds: int = 30
    webhook_timeout_seconds: float = 10.0

    @classmethod
    def from_env(cls, state_root: Path | None = None) -> ApiConfig:
        resolved_state_root = state_root or default_state_root()
        env_hashes = os.environ.get("AINRF_API_KEY_HASHES")
        api_key_hashes = _parse_api_key_hashes(env_hashes) if env_hashes else frozenset()

        if not api_key_hashes:
            config_path = resolved_state_root / "config.json"
            if config_path.exists():
                payload = json.loads(config_path.read_text(encoding="utf-8"))
                api_key_hashes = cls._parse_config_hashes(payload)

        if not api_key_hashes:
            raise ValueError("AINRF API key hashes are not configured")

        try:
            container_config = ContainerConfig.from_env()
        except ValueError:
            container_config = None

        gate_timeout_seconds = int(os.environ.get("AINRF_GATE_TIMEOUT_SECONDS", "3600"))
        gate_sweep_interval_seconds = int(os.environ.get("AINRF_GATE_SWEEP_INTERVAL_SECONDS", "30"))
        webhook_timeout_seconds = float(os.environ.get("AINRF_WEBHOOK_TIMEOUT_SECONDS", "10"))

        return cls(
            api_key_hashes=api_key_hashes,
            state_root=resolved_state_root,
            container_config=container_config,
            gate_timeout_seconds=gate_timeout_seconds,
            gate_sweep_interval_seconds=gate_sweep_interval_seconds,
            webhook_timeout_seconds=webhook_timeout_seconds,
        )

    @staticmethod
    def _parse_config_hashes(payload: object) -> frozenset[str]:
        if not isinstance(payload, dict):
            return frozenset()
        normalized_payload = cast(dict[str, object], payload)
        raw_hashes = normalized_payload.get("api_key_hashes")
        if not isinstance(raw_hashes, list):
            return frozenset()
        normalized = {item for item in raw_hashes if isinstance(item, str) and item}
        return frozenset(normalized)

    def verify_api_key(self, value: str | None) -> bool:
        if value is None:
            return False
        return hash_api_key(value) in self.api_key_hashes

    def as_public_health_payload(self) -> dict[str, Any]:
        return {
            "state_root": str(self.state_root),
            "container_configured": self.container_config is not None,
        }
