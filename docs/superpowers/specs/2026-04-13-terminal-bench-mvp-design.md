# Terminal Bench MVP Design

## Context

Cleanup-first realignment has now removed the retired orchestrator / task / WebUI-v1 product center from the main code path. The surviving runtime surface is intentionally minimal:

- `ainrf serve`
- `ainrf container add`
- `GET /health`
- `GET /v1/health`
- health-only frontend shell

The next step should not restore task-centric dashboard logic. The user explicitly chose to start the new realignment from a **web terminal bench**, with these priorities:

1. **Fastest usable path first**
2. **Local-first target first**

In this context, “local-first” means the first terminal target is the daemon’s current host/container environment. The initial goal is therefore not a general terminal platform, but a minimal, controlled browser terminal that opens a shell in the daemon runtime environment and proves the terminal-bench direction end-to-end.

## Goal

Add a minimal **Terminal Bench MVP** on top of the cleaned runtime and health shell so the user can:

- open a browser terminal
- connect to the daemon host/container shell
- view terminal session state
- stop the session cleanly

This is a terminal-first starting point for the future workbench, not the final terminal workbench design.

## Non-goals

This MVP does **not** try to implement:

- multi-target terminal routing
- project-aware routing or project binding
- multi-session management
- pane/layout management
- persistent workspace/session replay
- recipe/template injection
- task orchestration
- terminal I/O logging or transcript storage
- a sandboxed execution environment

## Recommended approach

Use **AINRF as the control plane** and **ttyd as the terminal provider**.

### Why ttyd

The first requirement is a working browser terminal with the smallest possible implementation and operational risk. Compared with alternatives:

- **ttyd** already solves browser terminal serving, read/write policy, authentication hooks, reverse-proxy friendliness, and TLS/origin controls in a compact package.
- **Zellij** is promising as a future session/workspace layer, but current browser integration and product embedding certainty are not strong enough for the first implementation slice.
- A custom PTY/WebSocket bridge in AINRF would create unnecessary complexity, security burden, and terminal-protocol scope too early.

Therefore the MVP should use ttyd now, while keeping the AINRF-side provider boundary thin enough to replace ttyd later if the project decides to adopt a richer session provider such as Zellij.

## Product boundary

### What AINRF does

AINRF owns the **terminal session control plane**:

- create a terminal session
- read current terminal session state
- stop the current terminal session
- launch and supervise the ttyd process
- store minimal session metadata
- return controlled access information to the frontend

AINRF does **not** implement terminal transport itself.

### What ttyd does

ttyd is only the terminal provider for this MVP. It serves a browser-accessible shell session that AINRF creates and controls.

### What the frontend does

The frontend acts as:

- launcher
- status view
- container for the browser terminal view

It does not implement terminal protocol logic.

## Security and runtime boundaries

The MVP should be safe by being **narrow**, not by pretending to solve every terminal security problem.

### 1. Single target

The first implementation supports exactly one target kind:

- `daemon-host`

That means the terminal opens into the daemon’s current host/container environment only.

### 2. Single active session

Only one active terminal session may exist at a time.

This avoids:

- session routing complexity
- multi-user/session concurrency issues
- multiple provider lifecycles
- premature session registry design

### 3. Backend-controlled startup

The browser must not choose:

- the shell command
- the provider port
- the bind address
- the target environment

Those decisions belong to AINRF only.

### 4. Controlled exposure

The ttyd process should be treated as an internal provider. It should not be exposed as a general public service endpoint with independent lifecycle or product identity.

### 5. Explicit trust boundary

This is **not** a sandbox. It is controlled browser access to a real shell in a trusted environment. The design should make that clear in both implementation and UI wording.

### 6. Minimal observability only

For this MVP, AINRF should record:

- session creation time
- started/stopped/failed state
- target kind
- provider type
- failure detail

It should **not** record full terminal I/O logs yet.

## Core object model

The MVP needs only one main object.

### `TerminalSession`

Suggested fields:

- `session_id`
- `provider` — initially `ttyd`
- `target_kind` — initially `daemon-host`
- `status` — `idle | starting | running | stopping | failed`
- `created_at`
- `started_at`
- `closed_at`
- `terminal_url` or `terminal_path`
- `detail`
- internal-only process metadata such as `pid`

This object should remain intentionally small. It must describe one active terminal session cleanly without pretending to model future multi-workspace behavior.

## API design

The MVP should expose exactly three endpoints.

### `GET /terminal/session`

Purpose:

- return the current terminal session state for page load / refresh

Behavior:

- if no session exists, return an `idle` representation
- if a session exists, return the session object

### `POST /terminal/session`

Purpose:

- create a terminal session

Behavior:

- if no session exists, start ttyd and persist the new session
- if a running session already exists, return that same session instead of creating another one

### `DELETE /terminal/session`

Purpose:

- stop the current session

Behavior:

- terminate the ttyd process
- update session state
- invalidate the frontend access path

## Provider boundary

Even though ttyd is the initial provider, AINRF should keep a thin internal provider boundary. Conceptually, the provider side only needs behavior equivalent to:

- start session
- inspect session
- stop session

This is enough to preserve a future path toward a richer provider (for example, a Zellij-backed session provider) without overengineering this MVP.

## Frontend design

The frontend should remain minimal and coherent with the current cleaned shell.

### Placement

For fastest delivery, reuse the existing shell rather than introducing a large new information architecture.

Recommended first cut:

- keep the current frontend shell
- extend the current page with a **Terminal Bench panel**

This is faster than introducing a broader route structure immediately.

### Required UI elements

1. **Terminal session status card**
   - session status
   - target kind
   - provider
   - created/started time if available
   - failure detail if present

2. **Start terminal button**
   - visible when idle or failed

3. **Stop terminal button**
   - visible when running

4. **Embedded terminal view container**
   - visible when running

### Frontend state model

The frontend only needs to handle:

- `idle`
- `starting`
- `running`
- `stopping`
- `failed`

## User interaction flow

### Happy path

1. User opens the frontend shell
2. Frontend calls `GET /terminal/session`
3. If state is idle, user sees “Start terminal”
4. User clicks start
5. Frontend calls `POST /terminal/session`
6. AINRF starts ttyd and records the session
7. Frontend receives session info
8. Frontend renders the terminal container
9. User runs shell commands directly in the browser terminal
10. User clicks stop
11. Frontend calls `DELETE /terminal/session`
12. AINRF terminates ttyd and returns to idle state

### Failure path

At minimum, the design must handle:

- ttyd missing or launch failure
- port allocation conflict
- stored session exists but ttyd process died
- terminal URL/path returned but terminal is unreachable
- stop requested after provider already exited

The UI should show these as explicit failed states rather than pretending the session is still running.

## Validation plan

This MVP is not complete until both automated verification and real smoke validation exist.

### Backend/API validation

Tests should cover:

- `GET /terminal/session` returns idle initially
- `POST /terminal/session` creates a session successfully
- repeated `POST /terminal/session` returns the existing running session
- `DELETE /terminal/session` stops the session
- provider launch failures are surfaced clearly

### Provider lifecycle validation

Tests should verify:

- ttyd process starts
- stored session metadata matches the process state
- stop actually terminates the process
- dead provider processes are recognized and surfaced as invalid/failed state

### Frontend validation

Frontend checks should verify:

- idle → starting → running transitions
- failed state rendering
- running state renders the terminal container
- stop returns the page to idle

### Real smoke validation

A real manual smoke is required:

- start the daemon
- open frontend
- start terminal session
- run simple commands such as:
  - `pwd`
  - `whoami`
  - `claude --version` (or equivalent existence check available in environment)
- stop the session
- start again to confirm repeatability

## MVP completion criteria

This slice is complete only if:

- the user can open a browser terminal into the daemon host/container shell
- the session can be started, viewed, and stopped
- the frontend remains honest about system state
- AINRF remains a thin control plane rather than reintroducing orchestrator complexity
- automated tests and real smoke validation both pass

## Follow-on path after this MVP

If this MVP works, the next design discussion can choose among later expansions such as:

- multiple targets
- project-aware session binding
- session registry/history
- recipe/template launch flows
- richer provider replacement or augmentation using Zellij

Those should be treated as later design steps, not bundled into the first terminal-bench implementation slice.
