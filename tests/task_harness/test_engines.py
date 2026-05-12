from __future__ import annotations

import asyncio

import pytest

from ainrf.task_harness.engines.base import EngineContext
from ainrf.task_harness.engines import ClaudeCodeEngine, CodexAppServerEngine, NotSupportedError, get_engine
from ainrf.task_harness.models import ResearchAgentProfileSnapshot, TaskConfigurationMode, TaskConfigurationSnapshot


def _make_context() -> EngineContext:
    return EngineContext(
        task_id="t-1",
        working_directory="/tmp",
        rendered_prompt="hello",
        agent_profile=ResearchAgentProfileSnapshot(
            profile_id="p-1",
            label="Test",
            system_prompt=None,
            skills=[],
            skills_prompt=None,
            settings_json=None,
            settings_artifact_path=None,
        ),
        task_config=TaskConfigurationSnapshot(
            mode=TaskConfigurationMode.RAW_PROMPT,
            template_id=None,
            template_vars={},
            raw_prompt="hello",
            rendered_task_input="hello",
        ),
    )


def test_get_engine_unknown():
    with pytest.raises(ValueError, match="Unknown execution engine"):
        get_engine("unknown")


def test_claude_code_engine_not_supported():
    engine = ClaudeCodeEngine()
    with pytest.raises(NotSupportedError):
        asyncio.run(engine.pause("t-1"))
    with pytest.raises(NotSupportedError):
        asyncio.run(engine.resume(_make_context(), lambda _event: None))
    with pytest.raises(NotSupportedError):
        asyncio.run(engine.send_prompt("t-1", "hello"))


def test_get_engine_codex_app_server():
    engine = get_engine("codex-app-server")
    assert isinstance(engine, CodexAppServerEngine)
