from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ainrf.skills.registry_models import SkillRegistryConfig
from ainrf.skills.registry_sync import (
    DirtyWorktreeError,
    SkillRegistrySyncService,
)


class TestSkillRegistrySyncService:
    @pytest.fixture
    def registry(self):
        return SkillRegistryConfig(
            registry_id="test-registry",
            display_name="Test Registry",
            git_url="https://example.com/test.git",
            git_ref="main",
            source_skills_path="skills",
            core_skill_ids=["core-skill"],
        )

    @pytest.fixture
    def service(self, tmp_path: Path, registry):
        return SkillRegistrySyncService(
            registry=registry,
            workspace_dir=tmp_path,
            load_dir=tmp_path / "skills",
        )

    def test_git_workspace_path(self, service: SkillRegistrySyncService, tmp_path: Path):
        assert service.git_workspace == tmp_path / "test-registry-git-sync"

    def test_find_skill_dirs_finds_direct_children(
        self, service: SkillRegistrySyncService, tmp_path: Path
    ):
        skills_root = tmp_path / "skills"
        (skills_root / "skill-a").mkdir(parents=True)
        (skills_root / "skill-a" / "SKILL.md").write_text("# Skill A")
        (skills_root / "skill-b").mkdir(parents=True)
        (skills_root / "skill-b" / "SKILL.md").write_text("# Skill B")
        (skills_root / "not-a-skill.txt").write_text("nope")

        dirs = list(service._find_skill_dirs(skills_root))
        assert sorted(dirs) == ["skill-a", "skill-b"]

    def test_find_skill_dirs_skips_dirs_without_skill_md(
        self, service: SkillRegistrySyncService, tmp_path: Path
    ):
        skills_root = tmp_path / "skills"
        (skills_root / "empty-dir").mkdir(parents=True)
        (skills_root / "valid").mkdir(parents=True)
        (skills_root / "valid" / "SKILL.md").write_text("# Valid")

        dirs = list(service._find_skill_dirs(skills_root))
        assert dirs == ["valid"]

    def test_sync_skill_generates_skill_json(
        self, service: SkillRegistrySyncService, tmp_path: Path
    ):
        source = tmp_path / "source" / "my-skill"
        source.mkdir(parents=True)
        source.joinpath("SKILL.md").write_text(
            "---\nname: my-skill\ndescription: A test skill\n---\n\n# My Skill"
        )

        service._sync_skill_dir(source, tmp_path / "skills", is_core=False)

        skill_json_path = tmp_path / "skills" / "my-skill" / "skill.json"
        assert skill_json_path.exists()
        data = json.loads(skill_json_path.read_text())
        assert data["skill_id"] == "my-skill"
        assert data["inject_mode"] == "disabled"

    def test_sync_skill_core_uses_auto(self, service: SkillRegistrySyncService, tmp_path: Path):
        source = tmp_path / "source" / "core-skill"
        source.mkdir(parents=True)
        source.joinpath("SKILL.md").write_text("---\nname: core-skill\n---\n\n# Core")

        service._sync_skill_dir(source, tmp_path / "skills", is_core=True)

        data = json.loads((tmp_path / "skills" / "core-skill" / "skill.json").read_text())
        assert data["inject_mode"] == "auto"

    def test_sync_skill_copies_skill_md(self, service: SkillRegistrySyncService, tmp_path: Path):
        source = tmp_path / "source" / "my-skill"
        source.mkdir(parents=True)
        source.joinpath("SKILL.md").write_text("# Content")

        service._sync_skill_dir(source, tmp_path / "skills", is_core=False)

        md_path = tmp_path / "skills" / "my-skill" / "SKILL.md"
        assert md_path.exists()
        assert md_path.read_text() == "# Content"

    def test_is_installed_checks_load_dir(self, service: SkillRegistrySyncService, tmp_path: Path):
        assert not service.is_installed()

        (tmp_path / "skills" / "some-skill").mkdir(parents=True)
        (tmp_path / "skills" / "some-skill" / "SKILL.md").write_text("# X")

        assert service.is_installed()

    @patch("ainrf.skills.registry_sync.subprocess.run")
    def test_check_update_detects_available_update(
        self, mock_run, service: SkillRegistrySyncService, tmp_path: Path
    ):
        service.git_workspace.mkdir(parents=True)
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="abc123\trefs/heads/main\n"),
            MagicMock(returncode=0, stdout="def456\n"),
            MagicMock(returncode=0, stdout=""),
        ]

        status = service.check_update()

        assert status.has_update is True
        assert status.remote_commit == "abc123"
        assert status.local_commit == "def456"
        assert status.is_dirty is False

    @patch("ainrf.skills.registry_sync.subprocess.run")
    def test_check_update_detects_dirty(
        self, mock_run, service: SkillRegistrySyncService, tmp_path: Path
    ):
        service.git_workspace.mkdir(parents=True)
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="abc123\trefs/heads/main\n"),
            MagicMock(returncode=0, stdout="abc123\n"),
            MagicMock(returncode=0, stdout="M  skills/test/SKILL.md\n"),
        ]

        status = service.check_update()

        assert status.has_update is False
        assert status.is_dirty is True

    @patch("ainrf.skills.registry_sync.subprocess.run")
    def test_update_raises_when_dirty_and_not_forced(
        self, mock_run, service: SkillRegistrySyncService, tmp_path: Path
    ):
        service.git_workspace.mkdir(parents=True)
        (tmp_path / "skills" / "x").mkdir(parents=True)
        (tmp_path / "skills" / "x" / "SKILL.md").write_text("# X")

        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="remote\trefs/heads/main\n"),
            MagicMock(returncode=0, stdout="local\n"),
            MagicMock(returncode=0, stdout="M  file\n"),
            MagicMock(returncode=0, stdout="M  file\n"),
        ]

        with pytest.raises(DirtyWorktreeError):
            service.update(force=False)
