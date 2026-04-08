---
name: mode2-reproduction-aris
description: "Mode 2 (ARIS): Bounded Reproduction Task using Auto-claude-code-research-in-sleep (ARIS) skills. Parses target paper via MinerU, implements core method, runs experiments via /run-experiment, monitors via /monitor-experiment, analyzes via /analyze-results, generates claims via /result-to-claim, iterates via /auto-review-loop. Produces REPRODUCTION_OUTCOME.md and QualityAssessment."
argument-hint: [paper-path] --scope [core-only|full-suite] --target [table-name] --budget [hours] --compact [true|false]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply, mcp__chat__*
---

# Mode 2 (ARIS): Bounded Reproduction Task

Execute a bounded reproduction task using ARIS skills for: **$ARGUMENTS**

## Overview

Mode 2 ARIS leverages ARIS experiment execution and analysis skills for paper reproduction. It chains deployment → monitoring → analysis → claim generation → iterative review.

```
Phase 1: Paper intake → Phase 2: Implementation → Phase 3: Run experiments → Phase 4: Monitor & collect → Phase 5: Analyze results → Phase 6: Result-to-claim → Phase 7: Auto-review-loop → Phase 8: QualityAssessment → Phase 9: Outcome report
```

## Constants

- **SCOPE = core-only** — Default scope. Override via `--scope full-suite`.
- **MAX_GPU_HOURS = 4** — Default GPU budget. Override via `--budget N`.
- **MAX_ITERATIONS = 3** — Maximum fix iterations for significant deviation.
- **MINERU_API = http://localhost:8000/parse** — MinerU PDF parsing endpoint.
- **ACCEPTABLE_DEVIATION = 5%** — Relative deviation threshold.
- **AUTO_PROCEED = true** — Auto-proceed at checkpoints.
- **COMPACT = false** — Compact summary when true.
- **HUMAN_CHECKPOINT = false** — Pause at each review round when true.
- **REVIEWER_MODEL = gpt-5.4** — Model for Codex MCP.

> Override: `/mode2-reproduction-aris papers/target.pdf --scope full-suite --target Table3 --budget 8 --human-checkpoint true`

## Input Contract

Parse `$ARGUMENTS` for:

| Parameter | Flag | Required | Description |
|-----------|------|----------|-------------|
| Paper | first arg | Yes | Target paper PDF path |
| Scope | --scope | No | `core-only` (default) or `full-suite` |
| Target | --target | No | Specific table/figure to reproduce |
| Budget | --budget | No | Override MAX_GPU_HOURS |
| Compact | --compact | No | Override COMPACT |
| Human checkpoint | --human-checkpoint | No | Override HUMAN_CHECKPOINT |

## Task Lifecycle

### Phase 1: Intake & Paper Analysis

1. **Create reproduction task record**:
   ```markdown
   # Reproduction Task Record (ARIS)

   **Task ID**: reproduction-aris-[timestamp]
   **Target Paper**: [PDF path]
   **Scope**: [core-only/full-suite]
   **Target Results**: [table/figure or "all"]
   **Budget**: [N] GPU hours
   **Status**: intake
   ```

2. **Parse paper via MinerU**:
   - Call MinerU API: `POST /parse` with PDF file
   - Store parsed Markdown in `workspace/papers/[paper-id].md`

3. **Generate PaperCard**:
   ```markdown
   # PaperCard: [paper-id] — Reproduction Target

   ## Method Description
   [Architecture, loss function, training procedure]

   ## Experimental Setup
   - Dataset: [name, size, splits]
   - Hyperparameters: [lr, batch, epochs]
   - Hardware: [GPU type, training time]
   - Evaluation: [metrics, baselines]

   ## Target Results
   [Table with paper's reported values]

   ## Reproduction Challenges
   [Ambiguities, missing details]
   ```

4. **HumanGate: Intake Confirmation**
   - Present: paper summary, target results, planned scope
   - If approved → proceed

### Phase 2: Implementation

Implement from scratch (no existing code):

```
workspace/
├── src/
│   ├── model.py
│   ├── loss.py
│   ├── train.py
│   └── eval.py
├── configs/
│   └── paper.yaml
├── README.md
└── requirements.txt
```

Implementation strategy:
- Core architecture first → loss/training → evaluation
- For `core-only`: focus on main method
- For `full-suite`: all components

### Phase 3: Run Experiments

Invoke `/run-experiment`:

```
/run-experiment "reproduce [paper-id] --config configs/paper.yaml --scope [core-only/full-suite]"
```

**What this does:**
- Detect environment (local/remote GPU from CLAUDE.md)
- Pre-flight GPU check
- Sync code (rsync or git)
- Deploy via SSH + screen (remote) or background (local)
- Verify launch

For each experiment:
- Each gets own screen session + GPU binding
- `tee` to save logs

### Phase 4: Monitor & Collect

Invoke `/monitor-experiment`:

```
/monitor-experiment [server-alias or screen-name]
```

**What this does:**
- Check running screens
- Collect output (hardcopy or logs)
- Pull W&B metrics if configured
- Summarize progress

Collect:
- Training loss curves (converging?)
- Eval metrics at checkpoints
- GPU memory, learning rate
- Run status (running/finished/crashed)

### Phase 5: Analyze Results

Invoke `/analyze-results`:

```
/analyze-results "workspace/results/"
```

**What this does:**
- Locate JSON/CSV result files
- Build comparison table
- Statistical analysis (mean ± std, trends)
- Generate insights

Output structure:
```markdown
## Result Comparison

| Metric | Paper | Reproduction | Deviation | Status |
|--------|-------|--------------|-----------|--------|
| [M1] | [V1] | [V2] | [+X%] | ✓ close |
| [M2] | [V3] | [V4] | [+Y%] | ⚠ significant |
```

### Phase 6: Result-to-Claim Gate

Invoke `/result-to-claim`:

```
/result-to-claim "[paper-id] reproduction results"
```

**What this does:**
- Collect results from W&B or logs
- Codex judgment: claim_supported (yes/partial/no)
- Route based on verdict:
  - `no`: postmortem in findings.md, pivot
  - `partial`: update claim, design supplementary experiments
  - `yes`: record confirmed claim

For reproduction, the "claim" being tested is: **"Can the paper's method be reproduced and achieve reported results?"**

### Phase 7: Auto-Review-Loop (Iterative Improvement)

If deviation > ACCEPTABLE_DEVIATION or `/result-to-claim` returns `partial`:

Invoke `/auto-review-loop`:

```
/auto-review-loop "[paper-id] reproduction — compact: $COMPACT — human-checkpoint: $HUMAN_CHECKPOINT"
```

**What this does:**
- Review via Codex MCP (score 1-10)
- Parse assessment (score, verdict, action items)
- Implement fixes (code changes, run experiments, analysis)
- Wait for results
- Document round in `AUTO_REVIEW.md`
- Repeat up to MAX_ROUNDS

Fix strategies:
- Hyperparameter tuning
- Architecture refinement
- Data processing adjustment

State persistence: `REVIEW_STATE.json` for context compaction recovery.

### Phase 8: QualityAssessment

Generate structured assessment:

```markdown
# QualityAssessment: [paper-id]

## Overall Rating

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Contribution quality | [high/moderate/low] | [Genuine advance or incremental?] |
| Reproducibility | [easy/moderate/hard/failed] | [Could we reproduce from paper?] |
| Scientific rigor | [strong/moderate/weak] | [Experimental design quality] |

## Reproducibility Details

### What Worked
[Clear instructions that reproduced]

### What Was Ambiguous
[Missing details that required guessing]

### What Failed
[Components that couldn't be reproduced]

## Deviation Summary

| Table | Status | Key Deviations |
|-------|--------|----------------|

## Recommendations for Authors
[Specific improvements]
```

### Phase 9: Outcome Report

Generate `REPRODUCTION_OUTCOME.md`:

```markdown
# Reproduction Outcome Report (ARIS)

**Task**: reproduction-aris-[id]
**Target Paper**: [title]
**Pipeline**: intake → implementation → run-experiment → monitor → analyze → result-to-claim → auto-review-loop
**Status**: completed / partial / failed / budget-exhausted

## Implementation Summary
- Code: `workspace/src/`
- Config: `workspace/configs/paper.yaml`

## Result Comparison
[Per-table comparison]

## QualityAssessment
[Rating summary]

## Key Findings
1. [Method insight]
2. [Reproducibility issues]
3. [Surprising results]

## Deviation Analysis
[List deviations and root causes]

## Review Log
- Rounds: [N]
- Final score: [X/10]
- Outcome: [ready/partial/not ready]

## EvidenceRecords
[List EvidenceRecord files]

## Next Steps
- [ ] If successful: Use as baseline for new experiments
- [ ] If partial: Identify missing components
- [ ] If failed: Document paper issues
```

## State Persistence

Write `TASK_STATE.json` after each phase:

```json
{
  "taskId": "reproduction-aris-...",
  "phase": "monitor_experiment",
  "scope": "core-only",
  "iterationsUsed": 0,
  "budgetUsed": 1.5,
  "maxDeviation": "2.1%",
  "status": "in_progress",
  "timestamp": "2026-04-07T14:00:00"
}
```

**On context compaction**: Read `TASK_STATE.json` + `AUTO_REVIEW.md` (compact: `findings.md`) to resume.

## Dashboard Requirements

Task must expose:
- Current phase and status
- Milestone/checkpoint timeline
- Result artifacts (comparison tables, figures)
- Resource usage (GPU hours)
- Deviation status per target table

## Key Rules

- **Use ARIS skills**: `/run-experiment`, `/monitor-experiment`, `/analyze-results`, `/result-to-claim`, `/auto-review-loop`
- **Parse via MinerU**: Always use MinerU for PDF → Markdown
- **Implement from scratch**: No reliance on existing code
- **Boundaries are hard**: Stop at budget/iteration limit
- **Document everything**: Every experiment, deviation, fix attempt
- **Failures are valid**: Failed reproduction with documented analysis is complete
- **Large file handling**: If Write fails, use Bash (`cat << 'EOF' > file`)
- **W&B integration**: If `wandb: true` in CLAUDE.md, pull metrics for richer signal
- **Feishu optional**: If `~/.claude/feishu.json` exists, send notifications

## Composing with Other Workflows

After reproduction:

```
/mode2-reproduction-aris papers/target.pdf  ← you are here
/result-to-claim                             ← verify claims from results
/ablation-planner                            ← plan ablation studies (if needed)
/auto-review-loop                            ← iterate until submission-ready (for improvement)
/paper-writing                               ← write paper based on findings
```

## Non-Goals (Explicit)

- NOT guarantee stable high-precision reproduction
- NOT complete full experiment suite automatically
- NOT automatic bias attribution with scientific certainty
- NOT full QualityAssessment semantics from blueprint