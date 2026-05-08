from __future__ import annotations

import asyncio

from ainrf.task_harness.engines import AgentSdkEngine


def test_agent_sdk_engine_init():
    engine = AgentSdkEngine()
    assert engine._sessions == {}


def test_agent_sdk_engine_send_prompt_no_session():
    engine = AgentSdkEngine()
    # No active session, should handle silently
    asyncio.run(engine.send_prompt("t-1", "hello"))
