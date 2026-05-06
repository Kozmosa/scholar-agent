"""Skill registry sync service: manages git workspace and syncs skills to load directory."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from ainrf.skills.json_generator import generate_skill_json, parse_skill_md_frontmatter
from ainrf.skills.registry_models import SkillRegistryConfig, SkillRegistryStatus


class DirtyWorktreeError(Exception):
    """Raised when the git workspace has uncommitted changes."""

    def __init__(self, files: list[str]) -> None:
        self.files = files
        super().__init__(f"Git worktree is dirty: {', '.join(files)}")


class SkillRegistrySyncService:
    """Manages git clone/pull and one-way sync to the skills load directory."""

    def __init__(
        self,
        registry: SkillRegistryConfig,
        workspace_dir: Path,
        load_dir: Path,
    ) -> None:
        self.registry = registry
        self.workspace_dir = workspace_dir
        self.load_dir = load_dir
        self.git_workspace = workspace_dir / f"{registry.registry_id}-git-sync"

    def is_installed(self) -> bool:
        """Check if any skills from this registry are present in the load directory."""
        if not self.load_dir.exists():
            return False
        for subdir in self.load_dir.iterdir():
            if subdir.is_dir() and (subdir / "SKILL.md").exists():
                return True
        return False

    def install(self) -> SkillRegistryStatus:
        """First-time install: clone repo and sync all skills."""
        if self.git_workspace.exists():
            shutil.rmtree(self.git_workspace)

        result = subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                self.registry.git_ref,
                self.registry.git_url,
                str(self.git_workspace),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"git clone failed: {result.stderr}")

        self._sync_all()
        return self._build_status()

    def check_update(self) -> SkillRegistryStatus:
        """Check if remote has newer commits. Does not modify anything."""
        if not self.git_workspace.exists():
            return self._build_status()

        remote_commit = self._git_ls_remote()
        local_commit = self._git_rev_parse()
        is_dirty = self._git_is_dirty()

        status = self._build_status()
        status.remote_commit = remote_commit
        status.local_commit = local_commit
        status.has_update = remote_commit is not None and remote_commit != local_commit
        status.is_dirty = is_dirty
        return status

    def update(self, force: bool = False) -> SkillRegistryStatus:
        """Pull latest and sync. Raises DirtyWorktreeError if dirty and not forced."""
        if not self.git_workspace.exists():
            raise RuntimeError("Registry not installed. Call install() first.")

        status = self.check_update()
        if status.is_dirty and not force:
            dirty_files = self._git_dirty_files()
            raise DirtyWorktreeError(dirty_files)

        if status.is_dirty and force:
            self._git_run(["reset", "--hard", "HEAD"])

        pull_result = self._git_run(["pull", "origin", self.registry.git_ref])
        if pull_result.returncode != 0:
            raise RuntimeError(f"git pull failed: {pull_result.stderr}")

        self._sync_all()
        return self._build_status()

    def _sync_all(self) -> None:
        """Sync all skills from git workspace to load directory."""
        source_root = self.git_workspace / self.registry.source_skills_path
        if not source_root.exists():
            raise RuntimeError(f"Source skills path not found: {source_root}")

        self.load_dir.mkdir(parents=True, exist_ok=True)
        core_set = set(self.registry.core_skill_ids)

        for skill_name in self._find_skill_dirs(source_root):
            source = source_root / skill_name
            is_core = skill_name in core_set
            self._sync_skill_dir(source, self.load_dir, is_core)

    def _find_skill_dirs(self, root: Path) -> list[str]:
        """Find all subdirectories under root that contain SKILL.md."""
        result: list[str] = []
        if not root.exists():
            return result
        for subdir in sorted(root.iterdir()):
            if subdir.is_dir() and (subdir / "SKILL.md").is_file():
                result.append(subdir.name)
        return result

    def _sync_skill_dir(self, source: Path, dest_root: Path, is_core: bool) -> None:
        """Sync a single skill: generate skill.json and copy SKILL.md."""
        skill_name = source.name
        dest = dest_root / skill_name
        dest.mkdir(parents=True, exist_ok=True)

        skill_md_path = source / "SKILL.md"
        skill_md_content = skill_md_path.read_text(encoding="utf-8")
        frontmatter = parse_skill_md_frontmatter(skill_md_content)

        skill_json = generate_skill_json(skill_name, frontmatter, is_core)
        (dest / "skill.json").write_text(
            json.dumps(skill_json, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        shutil.copy2(skill_md_path, dest / "SKILL.md")

    def _build_status(self) -> SkillRegistryStatus:
        """Build current status from filesystem."""
        installed_count = 0
        if self.load_dir.exists():
            installed_count = sum(
                1 for d in self.load_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
            )

        return SkillRegistryStatus(
            registry_id=self.registry.registry_id,
            installed=self.is_installed(),
            installed_count=installed_count,
        )

    def _git_run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.git_workspace), *args],
            capture_output=True,
            text=True,
        )

    def _git_ls_remote(self) -> str | None:
        result = subprocess.run(
            ["git", "ls-remote", self.registry.git_url, self.registry.git_ref],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or not result.stdout:
            return None
        # Output format: "<commit>\t<ref>\n"
        return result.stdout.split()[0] if result.stdout.split() else None

    def _git_rev_parse(self) -> str | None:
        result = self._git_run(["rev-parse", "HEAD"])
        return result.stdout.strip() if result.returncode == 0 else None

    def _git_is_dirty(self) -> bool:
        result = self._git_run(["status", "--porcelain"])
        return result.returncode == 0 and bool(result.stdout.strip())

    def _git_dirty_files(self) -> list[str]:
        result = self._git_run(["status", "--porcelain"])
        if result.returncode != 0:
            return []
        return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
