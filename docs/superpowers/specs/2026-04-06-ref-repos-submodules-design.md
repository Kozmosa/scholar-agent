# Ref-repos Submodules Migration Design

**Date:** 2026-04-06  
**Status:** Approved  
**Scope:** Convert ref-repos directory from tracked files to git submodules

## Objective

Migrate `ref-repos/EvoMaster` and `ref-repos/MagiClaw` from regular tracked directories to git submodules to:
- Prevent repository bloat (currently 34MB combined)
- Ensure consistent reference versions across development platforms
- Maintain read-only reference access for research purposes

## Requirements

- **Update frequency:** Occasional (monthly or less)
- **Version tracking:** Follow default branches (master/main)
- **Access pattern:** Read-only reference material
- **Multi-platform:** Consistent versions across all developer machines

## Architecture

### Current State
```
ref-repos/
├── EvoMaster/    # 29MB, tracked as regular files
└── MagiClaw/     # 4.8MB, tracked as regular files
```

### Target State
```
scholar-agent/
├── .gitmodules          # submodule configuration
├── ref-repos/
│   ├── EvoMaster/      # submodule (commit reference only)
│   └── MagiClaw/       # submodule (commit reference only)
```

### .gitmodules Configuration

```ini
[submodule "ref-repos/EvoMaster"]
    path = ref-repos/EvoMaster
    url = https://github.com/sjtu-sai-agents/EvoMaster.git

[submodule "ref-repos/MagiClaw"]
    path = ref-repos/MagiClaw
    url = https://github.com/sjtu-sai-agents/MagiClaw.git
```

## Implementation Plan

1. **Unstage current ref-repos files** (already staged in git)
2. **Remove ref-repos from git tracking** (preserve local files)
3. **Add git submodules** pointing to original repositories
4. **Commit configuration** to preserve submodule references

## Usage Patterns

### Initial Clone (for new developers)
```bash
git clone --recursive https://github.com/user/scholar-agent.git
# OR
git clone https://github.com/user/scholar-agent.git
git submodule update --init --recursive
```

### Update Reference Repositories
```bash
git submodule update --remote ref-repos/EvoMaster
git submodule update --remote ref-repos/MagiClaw
git add .gitmodules ref-repos/
git commit -m "chore: update reference repos to latest"
```

## Trade-offs

**Chosen: Git Submodules**
- ✅ Minimal storage overhead (commit references only)
- ✅ Consistent versions across platforms
- ✅ Standard Git feature, no dependencies
- ⚠️ Requires `--recursive` flag or extra initialization step

**Rejected Alternatives:**
- Git Subtree: Would embed full history, causing repository bloat
- Plain directories: No version consistency across platforms

## Success Criteria

- [ ] `.gitmodules` file created with both submodules configured
- [ ] `ref-repos/` directories properly initialized as submodules
- [ ] Repository size reduced by ~34MB
- [ ] New clone with `--recursive` fetches all submodules
- [ ] Existing developers can update with `git submodule update --init`