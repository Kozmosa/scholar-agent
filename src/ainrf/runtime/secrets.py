from __future__ import annotations

import json
from pathlib import Path


class WebhookSecretStore:
    def __init__(self, root_dir: Path) -> None:
        self._root_dir = root_dir

    @property
    def root_dir(self) -> Path:
        return self._root_dir

    @property
    def secrets_dir(self) -> Path:
        return self._root_dir / "runtime" / "webhook-secrets"

    def set(self, task_id: str, secret: str | None) -> None:
        path = self._secret_path(task_id)
        if not secret:
            if path.exists():
                path.unlink()
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"secret": secret}), encoding="utf-8")

    def get(self, task_id: str) -> str | None:
        path = self._secret_path(task_id)
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        secret = payload.get("secret")
        return secret if isinstance(secret, str) and secret else None

    def drop(self, task_id: str) -> None:
        path = self._secret_path(task_id)
        if path.exists():
            path.unlink()

    def _secret_path(self, task_id: str) -> Path:
        return self.secrets_dir / f"{task_id}.json"
