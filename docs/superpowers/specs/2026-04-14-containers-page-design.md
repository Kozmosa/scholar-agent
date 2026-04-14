# Containers Page Design

**Date:** 2026-04-14  
**Status:** Approved  
**Scope:** Replace the `/containers` placeholder with a real execution-environment management surface for the WebUI

## Objective

Turn `/containers` into the primary management page for execution environments.

In this project, a "container" does **not** mean a Docker container. It means an execution environment anchored by an SSH target plus environment metadata and probed runtime capabilities, such as Python toolchains, CUDA / GPU availability, and Claude-related readiness.

The page should let users:
- maintain a reusable user-level environment library,
- attach those environments to the current project through project-level references and overrides,
- inspect cached manual detection results,
- launch related runtime flows from the same place.

## Product Decisions Confirmed

- `/containers` is a **full management page**, not a read-only monitor.
- The core object is an **execution environment**, not a Docker container.
- The page's first priority is **environment inventory management**.
- Data is split into:
  - **configuration** entered by the user,
  - **detection snapshots** produced only by manual probing.
- Environment editing supports **two modes**:
  - structured form mode,
  - advanced ssh-config-style text mode.
- Persistence is **layered**:
  - user-level environment registry,
  - project-level references and runtime overrides.
- The default page layout is a **card grid**.
- Each card shows a **mixed summary** of config, capability badges, and current detection status.
- Detection is **manual only**. No automatic probing on save or page load.
- Initial detection scope covers:
  - SSH / basic connectivity,
  - Python toolchains,
  - AI / training capabilities,
  - Claude-related readiness.
- Project-level overrides are limited to **runtime-related fields**, not global connection identity.
- Environment detail tabs are:
  - `Overview`,
  - `Config`,
  - `Detection`,
  - `Project Overrides`.
- User-level environments **cannot be deleted while referenced by any project**.
- Environment identity uses:
  - internal stable `id`,
  - user-facing unique `alias`.
- Supported page actions include:
  - create,
  - edit,
  - delete with reference guard,
  - manual detect,
  - set as current project default environment,
  - open related terminal / workspace flows.

## Recommended Architecture

Use an **environment registry + project reference layer** design.

### Why this approach

This best matches the required product model:
- reusable user-level environment assets,
- project-specific runtime context,
- explicit separation between configuration and observed state,
- clean future integration with Terminal and Workspaces.

### Rejected alternatives

#### Project-first model
Would make current-project operations shorter, but weakens the user-level environment library and would likely require rework once environments need to be shared across projects.

#### Text-config-first model
Fits the ssh-config mental model well, but would make the page feel like a configuration-file frontend instead of a capability-aware management surface.

## Information Architecture

### Top-level page structure
`/containers` should contain:
- a top action bar,
- filter / search controls,
- a card grid of environments,
- a detail surface opened from a selected card.

### Card grid
Each environment card should display, within one screenful:
- display name,
- alias,
- host summary,
- default work directory summary,
- last detection status,
- last detection timestamp when available,
- capability badges for key tools and runtime readiness,
- whether the current project references the environment,
- whether it is the current project's default environment.

Primary card actions:
- `Detect`,
- `Edit`,
- `Set as project default`,
- `Open in terminal`,
- `Open in workspace`.

### Detail surface
The detail surface is organized into four tabs:

#### Overview
High-level identity, connection summary, latest detection summary, project usage summary, and fast actions.

#### Config
Editable user-level configuration shown in both form mode and advanced text mode.

#### Detection
Latest manual detection snapshot, including detailed results, warnings, and failures.

#### Project Overrides
Current-project reference state, default-environment toggle, and allowed runtime overrides.

## Core Data Model

The feature is built around four conceptual layers.

### 1. Environment Registry Entry
A user-level execution environment record.

Contains:
- stable identity,
- connection configuration,
- runtime defaults,
- descriptive metadata.

Key rule:
- `id` is for stable internal references,
- `alias` is the required unique user-facing identifier.

### 2. Detection Snapshot
A manual probe result stored separately from configuration.

Contains:
- detection time,
- success / partial / failure state,
- capability findings,
- warnings and errors.

Key rule:
- probing never mutates the configuration object directly.

### 3. Project Environment Reference
A project-level link to a user-level environment.

Contains:
- referenced environment ID,
- current-project default flag,
- limited runtime overrides.

Key rule:
- project-level data references an environment instead of duplicating it.

### 4. Action Surface
Operational affordances exposed through UI and API.

Includes:
- creation,
- editing,
- deletion with guardrails,
- manual detection,
- current-project default selection,
- entrypoints into related terminal / workspace flows.

## Configuration Schema

### Identity fields
- `id`
- `alias`
- `display_name`
- `description`
- `tags`

### SSH connection fields
- `host`
- `port`
- `user`
- `auth_kind`
- `identity_file` or equivalent auth reference
- `proxy_jump` (optional)
- `proxy_command` (optional)
- `ssh_options` for advanced mode extensions

### Runtime default fields
- `default_workdir`
- `preferred_python`
- `preferred_env_manager`
- `preferred_runtime_notes`

### Metadata fields
- `created_at`
- `updated_at`

## Detection Snapshot Schema

### Detection status
- `environment_id`
- `detected_at`
- `status` (`success` / `partial` / `failed`)
- `summary`
- `errors`
- `warnings`

### Basic connectivity and host info
- `ssh_ok`
- `hostname`
- `os_info`
- `arch`
- `workdir_exists`

### Python toolchain capabilities
- `python` with version and path
- `conda` with availability, version, and path
- `uv` with availability, version, and path
- `pixi` with availability, version, and path

### AI / training capabilities
- `torch` with availability and version
- `cuda` with availability and version
- `gpu_models`
- `gpu_count`

### Claude-related capabilities
- `claude_cli` with availability and version
- `anthropic_env` as `present` / `missing` / `unknown`

## Project Reference Schema

Each project-level reference should contain:
- `project_id` or equivalent project scope key,
- `environment_id`,
- `is_default`,
- `override_workdir`,
- `override_env_name`,
- `override_env_manager`,
- `override_runtime_notes`,
- `updated_at`.

Project overrides are limited to runtime context. They must **not** override:
- host,
- user,
- auth mode,
- identity file,
- other connection-identity fields.

## Interaction Design

### Create environment flow
- User clicks `Add environment`.
- Creation opens in **form mode** by default.
- User may switch to **advanced text mode**.
- User saves configuration without triggering detection.
- Success returns to the card grid and suggests running a manual first detection.

### Edit environment flow
- Existing environments can be edited in either form mode or text mode.
- `alias` may be changed but must remain unique.
- `id` never changes.
- Saving config does not automatically refresh detection results.
- Existing detection snapshots remain visible until the next manual detection run.

### Manual detection flow
- User clicks `Detect` from a card or the detail surface.
- The system runs a single manual probe.
- The latest detection snapshot is replaced or refreshed.
- UI updates card and detail views using the new snapshot.
- Failures are shown explicitly without corrupting saved config.

### Project reference flow
Users should be able to:
- attach an environment to the current project,
- set it as the current project's default environment,
- edit the allowed project-level runtime overrides.

### Terminal / workspace entry flow
The Containers page acts as the environment hub, but does not own terminal lifecycle or workspace runtime logic.

The page should provide entry actions that either:
- navigate into Terminal / Workspaces with environment context, or
- remain clearly marked as unavailable if the deeper integration is not implemented yet.

## API Boundary

### Environment registry APIs
- `GET /environments`
- `POST /environments`
- `GET /environments/:id`
- `PATCH /environments/:id`
- `DELETE /environments/:id`

### Detection APIs
- `POST /environments/:id/detect`
- `GET /environments/:id/detection`

Optional future extension:
- `GET /environments/:id/detections`

### Project reference APIs
- `GET /projects/:projectId/environment-refs`
- `POST /projects/:projectId/environment-refs`
- `PATCH /projects/:projectId/environment-refs/:environmentId`
- `DELETE /projects/:projectId/environment-refs/:environmentId`

Optional future extension:
- `POST /projects/:projectId/default-environment`

## Validation and Guardrails

Backend rules:
- `alias` must be globally unique.
- Environment deletion must fail while project references exist.
- Deletion failures must return structured information that identifies the projects still using the environment.
- Advanced text mode must parse into the canonical schema before saving.
- Detection failure must not invalidate or roll back saved configuration.

Frontend rules:
- form mode performs field-level validation,
- text mode reports parse or normalization failures clearly,
- configuration state and detection state are always displayed as separate concerns.

## Error Handling

### Save errors
- Show field-level errors in form mode.
- Show parse or block-level errors in text mode.
- Keep unsaved input intact when validation fails.

### Detection errors
- Persist the failed detection outcome as the latest snapshot.
- Show a short failure summary on the card.
- Show detailed errors and warnings in the Detection tab.

### Delete errors
- If an environment is still referenced, block deletion.
- Explain which projects still depend on it.
- Do not silently cascade-delete project references.

### Integration errors
- If opening terminal / workspace with environment context is not yet fully supported, present that clearly instead of implying success.

## Testing Strategy

### Frontend
Add tests for:
- new environment type contracts,
- API endpoint wrappers and mock responses,
- replacing `/containers` placeholder with a real page,
- card grid rendering,
- create flow,
- edit flow with form / text mode switching,
- manual detection result refresh,
- delete guard when an environment is still referenced,
- current-project default environment state changes.

### Backend
Add tests for:
- environment registry CRUD,
- alias uniqueness,
- project reference CRUD,
- deletion guard against active references,
- detection endpoint response structure.

If probing logic remains stubbed at first, keep the result schema fixed and test against that contract.

## Scope for the First Implementation Slice

### In scope
- replace `/containers` placeholder with a real page,
- card-grid overview,
- detail surface with the four tabs,
- create / edit flows with dual editing modes,
- user-level environment registry CRUD,
- project references and current-project default selection,
- manual detection and latest snapshot display,
- deletion guard for referenced environments.

### Out of scope for the first slice
- detection history timeline,
- batch detection,
- automatic background probing,
- complex SSH topology visualization,
- usage history or audit trails,
- heavy import / export workflows,
- deep terminal / workspace orchestration beyond entry actions.

## Success Criteria

The first version is successful when the WebUI treats execution environments as first-class assets:
- users can create and maintain reusable execution environments,
- projects can reference and customize them through limited runtime overrides,
- manual capability detection is visible and reliable,
- the page serves as the launch point for related runtime workflows without over-owning those flows.
