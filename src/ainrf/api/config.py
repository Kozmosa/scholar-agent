from __future__ import annotations

import json
import os
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, cast

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
    terminal_host: str = "127.0.0.1"
    terminal_port: int = 7681
    terminal_command: tuple[str, ...] = ("/bin/sh",)
    code_server_host: str = "127.0.0.1"
    code_server_port: int = 18080
    code_server_workspace_dir: Path | None = None

    @classmethod
    def from_env(cls, state_root: Path | None = None) -> ApiConfig:
        resolved_state_root = state_root or default_state_root()
        env_hashes = os.environ.get("AINRF_API_KEY_HASHES")
        api_key_hashes = _parse_api_key_hashes(env_hashes) if env_hashes else frozenset()

        payload: object | None = None
        config_path = resolved_state_root / "config.json"
        if config_path.exists():
            payload = json.loads(config_path.read_text(encoding="utf-8"))

        if not api_key_hashes:
            api_key_hashes = cls._parse_config_hashes(payload)

        if not api_key_hashes:
            raise ValueError("AINRF API key hashes are not configured")

        try:
            container_config = ContainerConfig.from_env()
        except ValueError:
            container_config = cls._parse_container_config(payload)

        return cls(
            api_key_hashes=api_key_hashes,
            state_root=resolved_state_root,
            container_config=container_config,
            code_server_workspace_dir=Path(container_config.project_dir) if container_config else None,
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

    @staticmethod
    def _parse_container_config(payload: object) -> ContainerConfig | None:
        if not isinstance(payload, dict):
            return None
        normalized_payload = cast(dict[str, object], payload)
        raw_profiles = normalized_payload.get("container_profiles")
        if not isinstance(raw_profiles, dict):
            return None
        profiles = cast(dict[str, object], raw_profiles)
        default_profile = normalized_payload.get("default_container_profile")
        if not isinstance(default_profile, str) or not default_profile:
            return None
        raw_profile = profiles.get(default_profile)
        if not isinstance(raw_profile, dict):
            return None
        profile = cast(dict[str, object], raw_profile)
        host = profile.get("host")
        user = profile.get("user")
        if not isinstance(host, str) or not host or not isinstance(user, str) or not user:
            return None
        port = profile.get("port", 22)
        if not isinstance(port, int):
            return None
        ssh_key_path = profile.get("ssh_key_path")
        ssh_password = profile.get("ssh_password")
        project_dir = profile.get("project_dir", "/workspace/projects")
        connect_timeout = profile.get("connect_timeout", 30)
        command_timeout = profile.get("command_timeout", 3600)
        if not isinstance(project_dir, str):
            return None
        if not isinstance(connect_timeout, int) or not isinstance(command_timeout, int):
            return None
        return ContainerConfig(
            host=host,
            port=port,
            user=user,
            ssh_key_path=ssh_key_path if isinstance(ssh_key_path, str) else None,
            ssh_password=ssh_password if isinstance(ssh_password, str) and ssh_password else None,
            connect_timeout=connect_timeout,
            command_timeout=command_timeout,
            project_dir=project_dir,
        )

    def verify_api_key(self, value: str | None) -> bool:
        if value is None:
            return False
        return hash_api_key(value) in self.api_key_hashes

    def as_public_health_payload(self) -> dict[str, Any]:
        return {
            "state_root": str(self.state_root),
            "container_configured": self.container_config is not None,
        }
