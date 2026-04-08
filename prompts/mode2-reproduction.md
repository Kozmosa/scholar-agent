---
name: mode2-reproduction
description: "Mode 2: Bounded Reproduction Task. Parses target paper via MinerU, implements core method, runs experiments, compares results with paper claims, generates QualityAssessment and reproduction outcome report."
argument-hint: [paper-path] --scope [core-only|full-suite] --target [table-name] --budget [hours]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill, mcp__chat__*
---

# Mode 2: Bounded Reproduction Task

Execute a bounded reproduction task for: **$ARGUMENTS**

## Overview

Mode 2 is a **bounded reproduction baseline** — not a guarantee of high-precision paper reproduction, but a trackable implementation/experimentation task with clear milestones and structured output.

```
Paper intake → Implementation → Experiments → Result comparison → Quality assessment → Outcome report
```

## Constants

- **SCOPE = core-only** — Default scope. Override via `--scope full-suite`.
- **MAX_GPU_HOURS = 4** — Default GPU budget. Override via `--budget N`.
- **MAX_ITERATIONS = 3** — Maximum fix iterations for significant deviation (>5%).
- **MINERU_API = http://localhost:8000/parse** — MinerU PDF parsing endpoint.
- **ACCEPTABLE_DEVIATION = 5%** — Relative deviation threshold for "close enough".
- **AUTO_PROCEED = true** — If user doesn't respond at checkpoint, auto-proceed.
- **COMPACT = false** — When true, generate compact summary files for session recovery.

> Override: `/mode2-reproduction papers/target.pdf --scope full-suite --target Table3 --budget 8`

## Input Contract

Parse `$ARGUMENTS` for:

| Parameter | Flag | Required | Description |
|-----------|------|----------|-------------|
| Paper | first arg | Yes | Target paper PDF path |
| Scope | --scope | No | `core-only` (default) or `full-suite` |
| Target | --target | No | Specific table/figure to reproduce (e.g., `Table2`) |
| Budget | --budget | No | Override MAX_GPU_HOURS |
| Baseline check | --baseline | No | Run quick baseline validation first |

## Task Lifecycle

### Phase 1: Intake & Paper Analysis

1. **Create reproduction task record**:
   ```markdown
   # Reproduction Task Record

   **Task ID**: reproduction-[timestamp]
   **Target Paper**: [PDF path]
   **Scope**: [core-only/full-suite]
   **Target Results**: [table/figure or "all"]
   **Budget**: [N] GPU hours
   **Status**: intake
   **Created**: [timestamp]
   ```

2. **Parse paper via MinerU**:
   - Call MinerU API: `POST /parse` with PDF file
   - Store parsed Markdown in `workspace/papers/[paper-id].md`
   - Extract: method description, experimental setup, target tables

3. **Generate PaperCard with reproduction focus**:
   ```markdown
   # PaperCard: [paper-id] — Reproduction Target

   **Title**: [title]
   **Authors**: [authors]
   **Year/Venue**: [year, venue]

   ## Method Description
   [Detailed extraction: architecture, loss function, training procedure]

   ## Experimental Setup
   - Dataset: [dataset name, size, splits]
   - Hyperparameters: [learning rate, batch size, epochs, etc.]
   - Hardware: [reported GPU type, training time]
   - Evaluation: [metrics, baselines]

   ## Target Results
   [Table extraction with paper's reported values]

   ## Implementation Notes
   [Key technical details from paper: equations, diagrams, code snippets if available]

   ## Reproduction Challenges
   [Identified ambiguities, missing details, potential issues]
   ```

4. **HumanGate: Intake Confirmation**
   - Present: paper summary, extracted method, target results, planned scope
   - Ask: "Is this the correct target? Should I adjust scope or focus on specific components?"
   - If approved → proceed; if adjustments → refine and re-present

### Phase 2: Implementation

Implement the paper's method from scratch (no existing code):

1. **Project structure**:
   ```
   workspace/
   ├── src/
   │   ├── model.py       # Core architecture
   │   ├── loss.py        # Loss functions
   │   ├── train.py       # Training loop
   │   └── eval.py        # Evaluation script
   ├── configs/
   │   └── paper.yaml     # Hyperparameters from paper
   ├── README.md          # Implementation notes
   └── requirements.txt   # Dependencies
   ```

2. **Implementation strategy**:
   - Start with core architecture (model.py)
   - Add loss functions and training logic
   - Build evaluation pipeline
   - For `core-only`: focus on main method, skip auxiliary experiments
   - For `full-suite`: implement all components mentioned

3. **Baseline sanity check**:
   - Run minimal training (1-2 epochs, small subset)
   - Verify: loss decreases, metrics compute correctly
   - If baseline fails → debug before full experiments

### Phase 3: Experiments

Execute reproduction experiments:

1. **Configuration alignment**:
   - Match paper's hyperparameters exactly (from PaperCard)
   - Use same dataset splits, preprocessing, evaluation metrics

2. **Run reproduction**:
   ```bash
   # Core experiment
   python src/train.py --config configs/paper.yaml --scope [core-only/full-suite]

   # For specific target
   python src/train.py --config configs/paper.yaml --target [Table2]
   ```

3. **Collect results**:
   - Save metrics to `results/reproduction_[timestamp].json`
   - Log training curves, intermediate checkpoints

4. **Deviation handling**:
   - If deviation > ACCEPTABLE_DEVIATION → enter fix loop (max 3 iterations)
   - Fix strategies: hyperparameter tuning, architecture refinement, data processing adjustment
   - Document each fix attempt in `FIX_LOG.md`

### Phase 4: Result Comparison

Compare reproduction results with paper claims:

1. **Per-table comparison**:
   ```markdown
   # Result Comparison: [Table Name]

   | Metric | Paper Value | Reproduction Value | Deviation | Status |
   |--------|-------------|-------------------|-----------|--------|
   | [M1] | [V1] | [V2] | [+X%] | ✓ close |
   | [M2] | [V3] | [V4] | [+Y%] | ⚠ significant |
   ```

2. **Deviation analysis** (for significant deviations > 5%):
   ```markdown
   # Deviation Analysis: [metric]

   ## Hypothesis
   [What might cause the deviation]

   ## Evidence
   [Evidence from implementation or logs]

   ## Attempted Fixes
   1. [Fix 1]: [result]
   2. [Fix 2]: [result]

   ## Conclusion
   [Likely root cause: paper ambiguity / implementation bug / hardware difference]
   ```

3. **EvidenceRecord for each claim**:
   ```markdown
   # EvidenceRecord: [paper claim]

   **Claim**: [exact claim from paper]
   **Evidence Type**: reproduction_result
   **Strength**: [strong/moderate/weak/failed]
   **Details**: [reproduction outcome]
   **Deviation**: [X%]
   ```

### Phase 5: Quality Assessment

Generate structured assessment of the paper:

```markdown
# QualityAssessment: [paper-id]

## Overall Rating

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Contribution quality | [high/moderate/low] | [Is it a genuine advance or incremental?] |
| Reproducibility | [easy/moderate/hard/failed] | [Could we reproduce from paper alone?] |
| Scientific rigor | [strong/moderate/weak] | [Experimental design quality] |

## Reproducibility Details

### What Worked
- [Clear instructions that reproduced well]

### What Was Ambiguous
- [Missing details that required guessing]

### What Failed
- [Components that couldn't be reproduced]

## Deviation Summary

| Table | Overall Status | Key Deviations |
|-------|---------------|----------------|
| [T1] | [✓/⚠/✗] | [list] |

## Recommendations for Authors

[List specific improvements that would help reproducibility]
```

### Phase 6: Outcome Report

Generate `REPRODUCTION_OUTCOME.md`:

```markdown
# Reproduction Outcome Report

**Task**: reproduction-[id]
**Target Paper**: [title]
**Scope**: [core-only/full-suite]
**Duration**: [actual hours]
**Status**: completed / failed / partial / budget-exhausted

## Implementation Summary
- Code: `workspace/src/`
- Config: `workspace/configs/paper.yaml`
- README: `workspace/README.md`

## Result Comparison
[Per-table comparison summary]

## QualityAssessment
[Rating summary from Phase 5]

## Key Findings
1. [Finding 1 — what we learned about the method]
2. [Finding 2 — reproducibility issues]
3. [Finding 3 — surprising results]

## Deviation Analysis
[List significant deviations and root causes]

## EvidenceRecords
[List EvidenceRecord files generated]

## Next Steps
- [ ] If successful: Use as baseline for new experiments
- [ ] If partial: Identify missing components for full reproduction
- [ ] If failed: Document paper issues, consider alternative approaches
```

## State Persistence

Write `TASK_STATE.json` after each phase:

```json
{
  "taskId": "reproduction-...",
  "phase": "experiments",
  "scope": "core-only",
  "iterationsUsed": 1,
  "budgetUsed": 2.0,
  "maxDeviation": "3.2%",
  "status": "in_progress",
  "timestamp": "2026-04-07T14:00:00"
}
```

**On context compaction**: Read `TASK_STATE.json`, PaperCard, and latest results to resume.

## Dashboard Requirements

Task must expose to dashboard:
- Current phase and status
- Milestone/checkpoint timeline
- Result artifacts (tables, figures)
- Resource usage (GPU hours consumed)
- Deviation status (summary per target table)

## Key Rules

- **Parse via MinerU**: Always use MinerU API for PDF → Markdown
- **Implement from scratch**: No reliance on existing code (unless user provides)
- **Boundaries are hard**: Stop at budget/iteration limit
- **Document everything**: Every experiment, every deviation, every fix attempt
- **Failures are valid**: A failed reproduction with documented analysis is a complete task
- **QualityAssessment is mandatory**: Even for failed reproductions, generate assessment
- **EvidenceRecords for claims**: Track evidence strength for each paper claim

## Non-Goals (Explicit)

- NOT guarantee stable high-precision reproduction
- NOT complete full experiment suite automatically
- NOT automatic bias attribution with scientific certainty
- NOT full QualityAssessment semantics from blueprint (baseline only)