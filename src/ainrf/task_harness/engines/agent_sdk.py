from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher
from claude_agent_sdk import (
    AssistantMessage,
    ResultMessage,
    SystemMessage,
    UserMessage,
    StreamEvent,
    RateLimitEvent,
    TextBlock,
    ThinkingBlock,
    ToolUseBlock,
    ToolResultBlock,
)

from .base import EngineContext, EngineEvent, ExecutionEngine
from ainrf.task_harness.session_state import SessionCheckpoint, SessionStateStore


@dataclass
class AgentSession:
    task_id: str
    abort_event: asyncio.Event = field(default_factory=asyncio.Event)
    should_pause_after_turn: bool = False
    pending_prompts: deque[str] = field(default_factory=deque)
    session_id: str | None = None
    turn_count: int = 0
    total_cost_usd: float = 0.0
    had_error: bool = False


class AgentSdkEngine(ExecutionEngine):
    def __init__(self) -> None:
        self._sessions: dict[str, AgentSession] = {}
        self._lock = asyncio.Lock()

    async def start(self, context: EngineContext, emit) -> None:
        async with self._lock:
            session = self._sessions.get(context.task_id)
            if session is None:
                session = AgentSession(task_id=context.task_id)
                self._sessions[context.task_id] = session

        # Load checkpoint if available
        if context.session_state_path:
            state_root = Path(context.session_state_path).parent.parent
            store = SessionStateStore(state_root)
            checkpoint = store.load(context.task_id)
            if checkpoint:
                session.session_id = checkpoint.session_id
                session.turn_count = checkpoint.turn_count
                session.total_cost_usd = checkpoint.total_cost_usd
                if checkpoint.pending_prompts:
                    session.pending_prompts.extend(checkpoint.pending_prompts)

        # Determine prompt for this turn
        if session.pending_prompts:
            prompt = session.pending_prompts.popleft()
        else:
            prompt = context.rendered_prompt

        options = ClaudeAgentOptions(
            model=context.agent_profile.model or "claude-sonnet-4-5",
            system_prompt=context.agent_profile.system_prompt,
            permission_mode=context.agent_profile.permission_mode or "acceptEdits",
            cwd=context.working_directory,
            resume=session.session_id,
            max_turns=context.agent_profile.max_turns,
            max_budget_usd=context.agent_profile.max_budget_usd,
            mcp_servers=context.agent_profile.mcp_servers or {},
            allowed_tools=context.agent_profile.skills or [],
            disallowed_tools=context.agent_profile.disallowed_tools or [],
            hooks={
                "PostToolUse": [HookMatcher(hooks=[self._post_tool_use_hook(emit)])],
                "Notification": [HookMatcher(hooks=[self._notification_hook(emit)])],
            },
            include_partial_messages=True,
        )

        try:
            async for sdk_msg in query(prompt=prompt, options=options):
                if session.abort_event.is_set():
                    break

                events = self._convert_sdk_message(sdk_msg, session)
                for event in events:
                    await emit(event)

            if session.had_error:
                raise RuntimeError("Agent SDK session completed with errors")

            if session.should_pause_after_turn:
                await emit(
                    EngineEvent(
                        event_type="system",
                        payload={"subtype": "task_paused", "task_id": context.task_id},
                    )
                )
            elif not session.abort_event.is_set():
                await emit(
                    EngineEvent(
                        event_type="system",
                        payload={"subtype": "task_completed", "task_id": context.task_id},
                    )
                )
        except Exception as exc:
            await emit(
                EngineEvent(
                    event_type="error",
                    payload={"message": str(exc), "task_id": context.task_id},
                )
            )
            await emit(
                EngineEvent(
                    event_type="system",
                    payload={"subtype": "task_failed", "task_id": context.task_id},
                )
            )
        finally:
            await self._save_checkpoint(context, session)

    async def pause(self, task_id: str) -> None:
        async with self._lock:
            session = self._sessions.get(task_id)
            if session is not None:
                session.should_pause_after_turn = True

    async def resume(self, context: EngineContext, emit) -> None:
        await self.start(context, emit)

    async def send_prompt(self, task_id: str, prompt: str) -> None:
        async with self._lock:
            session = self._sessions.get(task_id)
            if session is not None:
                session.pending_prompts.append(prompt)

    async def abort(self, task_id: str) -> None:
        async with self._lock:
            session = self._sessions.get(task_id)
            if session is not None:
                session.abort_event.set()

    def _convert_sdk_message(self, sdk_msg, session: AgentSession) -> list[EngineEvent]:
        events: list[EngineEvent] = []

        if isinstance(sdk_msg, AssistantMessage):
            for block in sdk_msg.content:
                if isinstance(block, TextBlock):
                    events.append(
                        EngineEvent(
                            event_type="message",
                            payload={"role": "assistant", "content": block.text},
                        )
                    )
                elif isinstance(block, ThinkingBlock):
                    events.append(
                        EngineEvent(
                            event_type="thinking",
                            payload={"content": block.thinking},
                        )
                    )
                elif isinstance(block, ToolUseBlock):
                    events.append(
                        EngineEvent(
                            event_type="tool_call",
                            payload={
                                "id": block.id,
                                "name": block.name,
                                "arguments": block.input,
                            },
                        )
                    )
                elif isinstance(block, ToolResultBlock):
                    events.append(
                        EngineEvent(
                            event_type="tool_result",
                            payload={
                                "tool_use_id": block.tool_use_id,
                                "content": block.content,
                                "is_error": block.is_error,
                            },
                        )
                    )
            return events

        if isinstance(sdk_msg, UserMessage):
            content = sdk_msg.content
            if isinstance(content, list):
                # Serialize list content to string for simplicity
                content = "\n".join(
                    item.get("text", str(item)) if isinstance(item, dict) else str(item)
                    for item in content
                )
            events.append(
                EngineEvent(
                    event_type="message",
                    payload={"role": "user", "content": content},
                )
            )
            return events

        if isinstance(sdk_msg, SystemMessage):
            if sdk_msg.subtype == "init":
                events.append(
                    EngineEvent(
                        event_type="system",
                        payload={
                            "subtype": "task_started",
                            "session_id": sdk_msg.data.get("session_id"),
                        },
                    )
                )
            else:
                events.append(
                    EngineEvent(
                        event_type="system",
                        payload={"subtype": sdk_msg.subtype, "data": sdk_msg.data},
                    )
                )
            return events

        if isinstance(sdk_msg, ResultMessage):
            session.session_id = sdk_msg.session_id
            session.turn_count += sdk_msg.num_turns or 0
            session.total_cost_usd += sdk_msg.total_cost_usd or 0.0

            if sdk_msg.is_error:
                session.had_error = True
                events.append(
                    EngineEvent(
                        event_type="system",
                        payload={
                            "subtype": "task_failed",
                            "session_id": sdk_msg.session_id,
                            "num_turns": sdk_msg.num_turns,
                            "total_cost_usd": sdk_msg.total_cost_usd,
                            "errors": sdk_msg.errors,
                        },
                    )
                )
            else:
                events.append(
                    EngineEvent(
                        event_type="system",
                        payload={
                            "subtype": "task_completed",
                            "session_id": sdk_msg.session_id,
                            "num_turns": sdk_msg.num_turns,
                            "total_cost_usd": sdk_msg.total_cost_usd,
                        },
                    )
                )
            return events

        if isinstance(sdk_msg, StreamEvent):
            event_type = sdk_msg.event.get("type")
            if event_type == "content_block_delta":
                delta = sdk_msg.event.get("delta", {})
                text = delta.get("text")
                if text:
                    events.append(
                        EngineEvent(
                            event_type="message",
                            payload={"role": "assistant", "content": text, "streaming": True},
                        )
                    )
            return events

        if isinstance(sdk_msg, RateLimitEvent):
            events.append(
                EngineEvent(
                    event_type="system",
                    payload={
                        "subtype": "rate_limit",
                        "rate_limit_info": sdk_msg.rate_limit_info,
                    },
                )
            )
            return events

        return events

    def _post_tool_use_hook(self, emit):
        async def hook(input_data, tool_use_id, context):
            await emit(
                EngineEvent(
                    event_type="tool_result",
                    payload={
                        "tool_name": input_data.get("tool_name"),
                        "tool_input": input_data.get("tool_input"),
                        "tool_response": input_data.get("tool_response"),
                        "tool_use_id": tool_use_id,
                    },
                )
            )
            return {}

        return hook

    def _notification_hook(self, emit):
        async def hook(input_data, tool_use_id, context):
            await emit(
                EngineEvent(
                    event_type="system",
                    payload={
                        "subtype": "notification",
                        "message": input_data.get("message"),
                        "title": input_data.get("title"),
                        "notification_type": input_data.get("notification_type"),
                    },
                )
            )
            return {}

        return hook

    async def _save_checkpoint(self, context: EngineContext, session: AgentSession) -> None:
        if context.session_state_path:
            store = SessionStateStore(Path(context.session_state_path).parent.parent)
        else:
            store = SessionStateStore(Path(context.working_directory) / ".ainrf")
        checkpoint = SessionCheckpoint(
            task_id=session.task_id,
            session_id=session.session_id,
            cwd=context.working_directory,
            created_at=datetime.now().isoformat(),
            turn_count=session.turn_count,
            total_cost_usd=session.total_cost_usd,
            pending_prompts=list(session.pending_prompts),
        )
        store.save(checkpoint)
