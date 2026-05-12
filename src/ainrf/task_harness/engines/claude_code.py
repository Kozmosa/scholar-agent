from __future__ import annotations

import asyncio

from .base import EngineContext, EngineEvent, ExecutionEngine, NotSupportedError


class ClaudeCodeEngine(ExecutionEngine):
    async def start(self, context: EngineContext, emit) -> None:
        command = [
            "claude",
            "-p",
            "--no-session-persistence",
            "--permission-mode",
            "bypassPermissions",
        ]
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=context.working_directory,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdin = process.stdin
        stdout = process.stdout
        stderr = process.stderr
        if stdin is None or stdout is None or stderr is None:
            raise RuntimeError("Claude Code engine failed to attach stdio pipes")

        # Write the prompt to stdin
        if context.rendered_prompt:
            stdin.write(context.rendered_prompt.encode())
            await stdin.drain()
            stdin.close()

        await emit(EngineEvent(event_type="system", payload={"subtype": "task_started"}))

        async def read_stream(stream, kind):
            while True:
                line = await stream.readline()
                if not line:
                    break
                role = "assistant" if kind == "stdout" else "system"
                await emit(
                    EngineEvent(
                        event_type="message",
                        payload={"role": role, "content": line.decode("utf-8", errors="replace")},
                    )
                )

        await asyncio.gather(
            read_stream(stdout, "stdout"),
            read_stream(stderr, "stderr"),
        )
        await process.wait()

        status = "succeeded" if process.returncode == 0 else "failed"
        await emit(EngineEvent(event_type="system", payload={"subtype": f"task_{status}"}))
        await emit(EngineEvent(event_type="status", payload={"status": status}))

    async def pause(self, task_id: str) -> None:
        raise NotSupportedError("ClaudeCodeEngine does not support pause")

    async def resume(self, context: EngineContext, emit) -> None:
        raise NotSupportedError("ClaudeCodeEngine does not support resume")

    async def send_prompt(self, task_id: str, prompt: str) -> None:
        raise NotSupportedError("ClaudeCodeEngine does not support send_prompt")

    async def abort(self, task_id: str) -> None:
        # Process abort is handled by service layer (via _running_processes reference)
        pass
