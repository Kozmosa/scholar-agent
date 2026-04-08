---
name: mode1-discovery-aris
description: "Mode 1 (ARIS): Bounded Discovery Task using Auto-claude-code-research-in-sleep (ARIS) skills. Orchestrates research-lit → idea-creator → novelty-check → research-review → research-refine-pipeline within bounded constraints. Produces IDEA_REPORT.md, FINAL_PROPOSAL.md, and EXPERIMENT_PLAN.md."
argument-hint: [topic-description] --seed [pdf-path] --depth [N] --budget [hours] --compact [true|false]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply, mcp__chat__*
---

# Mode 1 (ARIS): Bounded Discovery Task

Execute a bounded discovery task using ARIS skills for: **$ARGUMENTS**

## Overview

Mode 1 ARIS leverages the `/idea-discovery` pipeline from the ARIS plugin, adapted to the scholar-agent bounded discovery baseline. It chains multiple ARIS skills into an automated workflow with checkpoints and termination conditions.

```
Phase 0.5: Ref paper summary → Phase 1: research-lit → Phase 2: idea-creator → Phase 3: novelty-check → Phase 4: research-review → Phase 4.5: research-refine-pipeline → Phase 5: Final report
```

## Constants

- **MAX_DEPTH = 3** — Maximum recursion depth for reference expansion.
- **MAX_HOURS = 4** — Default time budget. Override via `--budget N`.
- **PILOT_MAX_HOURS = 2** — Skip pilot experiments > 2 hours per GPU.
- **PILOT_TIMEOUT_HOURS = 3** — Hard timeout for running pilots.
- **MAX_PILOT_IDEAS = 3** — Run pilots for at most 3 top ideas.
- **AUTO_PROCEED = true** — Auto-proceed if user doesn't respond at checkpoint.
- **REVIEWER_MODEL = gpt-5.4** — Model for Codex MCP reviews.
- **ARXIV_DOWNLOAD = false** — Only fetch metadata by default.
- **COMPACT = false** — Generate compact summary when true.

> Override: `/mode1-discovery-aris "topic" --depth 5 --budget 8 --seed papers/ref.pdf --compact true`

## Input Contract

Parse `$ARGUMENTS` for:

| Parameter | Flag | Required | Description |
|-----------|------|----------|-------------|
| Topic | first arg | Yes | Research direction/question |
| Seed PDF | --seed | Yes (at least one) | Reference paper PDF path |
| Ref paper | --ref-paper | No | Reference paper URL or local path for idea generation context |
| Focus hints | --focus | No | Directions to prioritize |
| Ignore hints | --ignore | No | Sub-areas to skip |
| Depth limit | --depth | No | Override MAX_DEPTH |
| Budget | --budget | No | Override MAX_HOURS |
| Compact | --compact | No | Override COMPACT |

## Task Lifecycle

### Phase 0.5: Reference Paper Summary (optional)

**If `--ref-paper` is provided**, summarize the reference paper first:

1. **If arXiv URL**: Invoke `/arxiv "ARXIV_ID"` to fetch PDF, read first 5 pages
2. **If local PDF**: Read directly (first 5 pages)
3. **If other URL**: Fetch via WebFetch

Generate `REF_PAPER_SUMMARY.md`:
```markdown
# Reference Paper Summary

**Title**: [title]
**Authors**: [authors]
**Venue**: [venue, year]

## What They Did
[2-3 sentences: core method and contribution]

## Key Results
[Main quantitative findings]

## Limitations & Open Questions
[What the paper didn't solve, acknowledged weaknesses]

## Potential Improvement Directions
[Based on limitations, what could be improved?]
```

**Checkpoint**: Present summary, then proceed to Phase 1.

### Phase 1: Literature Survey

Invoke `/research-lit`:

```
/research-lit "$TOPIC" --sources local,web --arxiv-download $ARXIV_DOWNLOAD
```

**What this does:**
- Search arXiv, Semantic Scholar, Google Scholar
- Build landscape: sub-directions, approaches, open problems
- Identify structural gaps and recurring limitations
- Output `LITERATURE_LANDSCAPE.md`

**Checkpoint**: Present landscape summary. Ask user to confirm scope or adjust.

### Phase 2: Idea Generation + Filtering + Pilots

Invoke `/idea-creator`:

```
/idea-creator "$TOPIC"
```

**What this does:**
- If `REF_PAPER_SUMMARY.md` exists, ideas build on/improve the reference paper
- Brainstorm 8-12 concrete ideas via GPT-5.4 xhigh
- Filter by feasibility, compute cost, quick novelty search
- Deep validate top ideas (full novelty check + devil's advocate)
- Run parallel pilot experiments (top 2-3 ideas) if GPU available
- Rank by empirical signal
- Output `IDEA_REPORT.md`

**Checkpoint**: Present ranked ideas. Ask user to select or regenerate.

### Phase 3: Deep Novelty Verification

For each top idea (positive pilot signal), invoke `/novelty-check`:

```
/novelty-check "[top idea 1 description]"
/novelty-check "[top idea 2 description]"
```

**What this does:**
- Multi-source literature search (arXiv, Scholar, Semantic Scholar)
- Cross-verify with GPT-5.4 xhigh
- Check concurrent work (last 3-6 months)
- Identify closest existing work and differentiation

Update `IDEA_REPORT.md` with novelty results. Eliminate ideas already published.

### Phase 4: External Critical Review

For surviving top idea(s), invoke `/research-review`:

```
/research-review "[top idea with hypothesis + pilot results]"
```

**What this does:**
- GPT-5.4 xhigh acts as senior reviewer (NeurIPS/ICML level)
- Scores idea, identifies weaknesses, suggests improvements
- Provides feedback on experimental design

Update `IDEA_REPORT.md` with reviewer feedback.

### Phase 4.5: Method Refinement + Experiment Planning

Invoke `/research-refine-pipeline`:

```
/research-refine-pipeline "[top idea + pilot results + reviewer feedback]"
```

**What this does:**
- Freeze Problem Anchor to prevent scope drift
- Iterative method refinement via GPT-5.4 (up to 5 rounds, score ≥ 9)
- Generate claim-driven experiment roadmap
- Output: `refine-logs/FINAL_PROPOSAL.md`, `refine-logs/EXPERIMENT_PLAN.md`, `refine-logs/EXPERIMENT_TRACKER.md`

**Checkpoint**: Present refined proposal summary. Ask user to approve or adjust.

### Phase 5: Final Report

Generate `DISCOVERY_OUTCOME.md`:

```markdown
# Discovery Outcome Report (ARIS)

**Task**: discovery-aris-[id]
**Topic**: $TOPIC
**Pipeline**: research-lit → idea-creator → novelty-check → research-review → research-refine-pipeline
**Status**: completed

## Executive Summary
[Best idea, key evidence, next step]

## Literature Landscape
[from Phase 1]

## Ranked Ideas
[from Phase 2, updated with Phase 3-4]

### 🏆 Idea 1: [title] — RECOMMENDED
- Pilot: POSITIVE (+X%)
- Novelty: CONFIRMED (closest: [paper])
- Reviewer score: X/10
- Next step: /run-experiment → /auto-review-loop

## Refined Proposal
- Proposal: `refine-logs/FINAL_PROPOSAL.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Tracker: `refine-logs/EXPERIMENT_TRACKER.md`

## Next Steps
- [ ] /run-experiment to deploy experiments
- [ ] /auto-review-loop to iterate until submission-ready
- [ ] Or /research-pipeline for full end-to-end flow
```

### Phase 5.5: Compact Summary (when COMPACT = true)

Write `IDEA_CANDIDATES.md` — lean summary of top 3-5 ideas:

```markdown
# Idea Candidates

| # | Idea | Pilot Signal | Novelty | Reviewer Score | Status |
|---|------|-------------|---------|---------------|--------|
| 1 | [title] | +X% | Confirmed | X/10 | RECOMMENDED |
| 2 | [title] | +Y% | Confirmed | X/10 | BACKUP |

## Active Idea: #1 — [title]
- Hypothesis: [one sentence]
- Key evidence: [pilot result]
- Next step: /experiment-bridge
```

## State Persistence

Write `TASK_STATE.json` after each phase:

```json
{
  "taskId": "discovery-aris-...",
  "phase": "idea_creator",
  "topIdeas": ["idea1", "idea2"],
  "budgetUsed": 1.5,
  "status": "in_progress",
  "timestamp": "2026-04-07T12:00:00"
}
```

**On context compaction**: Read `TASK_STATE.json` + `IDEA_CANDIDATES.md` (if COMPACT) or `IDEA_REPORT.md` to resume.

## Dashboard Requirements

Task must expose:
- Current phase and status
- Milestone/checkpoint timeline
- Recent artifacts (IDEA_REPORT.md snippets, EXPERIMENT_PLAN.md)
- Resource usage (budget consumed)

## Key Rules

- **Use ARIS skills**: Invoke `/research-lit`, `/idea-creator`, `/novelty-check`, `/research-review`, `/research-refine-pipeline`
- **Boundaries are hard**: Stop at budget limit, skip pilots > PILOT_MAX_HOURS
- **Checkpoints between phases**: Summarize before moving on
- **Kill ideas early**: Better to kill 10 bad ideas in Phase 3 than implement one
- **Empirical signal > theoretical appeal**: Positive pilot outranks "sounds great"
- **Document everything**: Dead ends are valuable for future reference
- **Large file handling**: If Write fails, use Bash (`cat << 'EOF' > file`)
- **Feishu optional**: If `~/.claude/feishu.json` exists, send checkpoint/pipeline_done

## Composing with Workflow 2 (ARIS)

After this pipeline produces a validated top idea:

```
/mode1-discovery-aris "topic"    ← you are here
/run-experiment                  ← deploy from EXPERIMENT_PLAN.md
/auto-review-loop "top idea"     ← iterate until submission-ready

Or use /research-pipeline for full end-to-end.
```

## Non-Goals (Explicit)

- NOT complete autonomous literature graph
- NOT guarantee high-quality idea validation
- NOT automatic paper reproduction (that's Mode 2)
- NOT full ExplorationGraph semantics from blueprint