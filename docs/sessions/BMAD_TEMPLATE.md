# BMAD Session Document

**B**aseline - **M**ilestone - **A**gent Dispatch - **D**ocumentation

---

## 📋 SESSION METADATA

| Field | Value |
|-------|-------|
| **Session ID** | `{{SESSION_ID}}` |
| **Date** | `{{YYYY-MM-DD}}` |
| **Project** | `{{PROJECT_NAME}}` |
| **Branch** | `{{GIT_BRANCH}}` |
| **Session Goal** | `{{ONE_LINE_GOAL}}` |
| **Status** | 🔄 IN PROGRESS / ✅ COMPLETE / ❌ FAILED |
| **Duration** | `{{X}}` hours |
| **Lead Agent** | `{{AGENT_NAME}}` |

---

## [B] BASELINE - Current State Snapshot

> **Purpose**: Document the exact state of the project BEFORE any work begins
> **When to fill**: Phase 2 (after context gathering)
> **Fill time**: 10-20 minutes

### 📸 Project State

**Date**: {{DATE}}
**Branch**: {{BRANCH}}
**Last Commit**: {{COMMIT_SHA}} - "{{COMMIT_MESSAGE}}"

---

### 🏗️ Architecture Overview

**Backend**:
- Framework: {{e.g., FastAPI, Django, Express}}
- Language: {{e.g., Python 3.11, TypeScript}}
- Database: {{e.g., PostgreSQL, MongoDB, None yet}}
- Key Libraries: {{list main dependencies}}

**Frontend**:
- Framework: {{e.g., Next.js 15, React, Vue}}
- Language: {{e.g., TypeScript, JavaScript}}
- UI Library: {{e.g., TailwindCSS, shadcn/ui}}
- Key Libraries: {{list main dependencies}}

**Infrastructure**:
- Hosting: {{e.g., Vercel, Cloud Run, local only}}
- CI/CD: {{e.g., GitHub Actions, None}}
- Monitoring: {{e.g., Vertex AI, None}}

---

### ✅ Current Capabilities

What the system can do TODAY:

1. {{CAPABILITY_1}} - {{brief description}}
2. {{CAPABILITY_2}} - {{brief description}}
3. {{CAPABILITY_3}} - {{brief description}}
...

**Key Files**:
- `{{file_path}}` - {{purpose}}
- `{{file_path}}` - {{purpose}}

---

### 🐛 Known Issues / Technical Debt

Issues we're aware of but not fixing in this session:

- **[ISSUE-001]**: {{Description}} - {{Impact: High/Medium/Low}}
- **[ISSUE-002]**: {{Description}} - {{Impact: High/Medium/Low}}
- **[ISSUE-003]**: {{Description}} - {{Impact: High/Medium/Low}}

---

### 📊 Baseline Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **Lines of Code** | {{LOC}} | From `cloc` or manual count |
| **Test Coverage** | {{X}}% | From test runner |
| **Monthly Cost** | ${{COST}} | Infrastructure + API costs |
| **Performance** | {{X}}ms avg response | If applicable |
| **Build Time** | {{X}}s | Frontend/backend |

---

### 🗂️ File Structure (Relevant Paths)

```
project-root/
├── app/                    # {{description}}
│   ├── agent.py           # {{purpose}}
│   └── config.py          # {{purpose}}
├── nextjs/                # {{description}}
│   └── src/
│       ├── app/           # {{purpose}}
│       └── components/    # {{purpose}}
├── docs/                  # {{description}}
└── tests/                 # {{description}}
```

---

### 🔍 Dependencies Snapshot

**Python** (from `pyproject.toml` or `requirements.txt`):
```
google-adk==X.X.X
fastapi==X.X.X
{{other key deps}}
```

**JavaScript** (from `package.json`):
```
next==X.X.X
react==X.X.X
{{other key deps}}
```

---

### ❓ Open Questions (Start of Session)

Questions we have BEFORE starting work:

1. ❓ {{QUESTION_1}} - Why this matters: {{REASON}}
2. ❓ {{QUESTION_2}} - Why this matters: {{REASON}}
3. ❓ {{QUESTION_3}} - Why this matters: {{REASON}}

---

## [M] MILESTONE - Success Criteria

> **Purpose**: Define what "done" looks like for THIS session
> **When to fill**: Phase 3 (after baseline)
> **Fill time**: 10-15 minutes

### 🎯 Session Goal Statement

**In one sentence**: {{GOAL}}

**Why this matters**: {{BUSINESS_VALUE or TECHNICAL_REASON}}

---

### ✅ Success Criteria (ALL must pass)

Each criterion should be testable/verifiable:

1. ✅ **[CRITERIA-1]**: {{Description}}
   - **Verification**: {{How to check this passes}}
   - **Owner**: {{Agent responsible}}

2. ✅ **[CRITERIA-2]**: {{Description}}
   - **Verification**: {{How to check this passes}}
   - **Owner**: {{Agent responsible}}

3. ✅ **[CRITERIA-3]**: {{Description}}
   - **Verification**: {{How to check this passes}}
   - **Owner**: {{Agent responsible}}

---

### 📦 Deliverables Checklist

Concrete outputs from this session:

- [ ] **{{DELIVERABLE_1}}**
  - File(s): `{{path/to/file}}`
  - Format: {{e.g., Python module, JSON schema, Markdown doc}}
  - Acceptance: {{What makes this "done"}}

- [ ] **{{DELIVERABLE_2}}**
  - File(s): `{{path/to/file}}`
  - Format: {{format}}
  - Acceptance: {{criteria}}

- [ ] **{{DELIVERABLE_3}}**
  - File(s): `{{path/to/file}}`
  - Format: {{format}}
  - Acceptance: {{criteria}}

---

### ⏰ Time Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| **Deadline** | {{YYYY-MM-DD HH:MM}} | {{Why this deadline exists}} |
| **Estimated Duration** | {{X}} hours | Based on complexity analysis |
| **Priority** | HIGH / MEDIUM / LOW | {{Why this priority}} |
| **Phase** | 24hr / Phase 2 / Future | When this must be done |

---

### 🚨 Rollback Plan

**If we fail to meet milestone**:

1. **Condition**: If {{FAILURE_SCENARIO}}
2. **Action**: Then {{ROLLBACK_STEPS}}
3. **Fallback**: Use {{ALTERNATIVE_APPROACH}}

**Branch strategy**:
- Work branch: `{{WORK_BRANCH}}`
- Merge to: `{{BASE_BRANCH}}` only if milestone met
- Discard if: {{CONDITIONS_FOR_DISCARD}}

---

### 🔗 Dependencies & Blockers

**This session depends on**:
- {{DEPENDENCY_1}} - Status: ✅ Ready / ⏳ Waiting / ❌ Blocked
- {{DEPENDENCY_2}} - Status: ✅ Ready / ⏳ Waiting / ❌ Blocked

**This session may be blocked by**:
- {{BLOCKER_1}} - Mitigation: {{HOW_TO_HANDLE}}
- {{BLOCKER_2}} - Mitigation: {{HOW_TO_HANDLE}}

---

## [A] AGENT DISPATCH - Crew Formation

> **Purpose**: Document which agents are working on what
> **When to fill**: Phase 4 (after milestone defined)
> **Fill time**: 5-10 minutes + updated throughout Phase 5

### 🤖 Crew Configuration

**Crew Type**: Solo / Sequential / Parallel / Dynamic Task Force

**Coordination Mode**: Sequential / Parallel

**Total Agents**: {{N}}

**Estimated Crew Runtime**: {{X}} hours

---

### 👥 Agent Roster & Task Assignments

---

#### **Agent 1: {{AGENT_NAME}}** ({{ROLE}})

**Status**: ⏳ PENDING / 🔄 IN PROGRESS / ✅ COMPLETE / ❌ FAILED

**Task Description**:
{{What this agent is doing - 2-3 sentences}}

**Input**:
- Files: `{{input_file_1}}`, `{{input_file_2}}`
- Context: {{From previous agent or baseline}}

**Output**:
- Files: `{{output_file_1}}`, `{{output_file_2}}`
- Format: {{Description}}

**Success Criteria**:
- ✅ {{CRITERION_1}}
- ✅ {{CRITERION_2}}

**Time Budget**: {{X}} minutes

**Started**: {{YYYY-MM-DD HH:MM}} or N/A
**Completed**: {{YYYY-MM-DD HH:MM}} or N/A
**Actual Duration**: {{X}} minutes or N/A

**Handoff Instructions** (if sequential crew):
```markdown
For next agent ({{NEXT_AGENT}}):
- Context: {{What they need to know}}
- Files produced: {{List}}
- Key decisions made: {{Summary}}
- Next steps: {{What to do}}
```

---

#### **Agent 2: {{AGENT_NAME}}** ({{ROLE}})

**Status**: ⏳ PENDING / 🔄 IN PROGRESS / ✅ COMPLETE / ❌ FAILED

**Task Description**:
{{What this agent is doing}}

**Input**:
- Files: `{{input_file_1}}`
- Context: {{From Agent 1 handoff}}

**Output**:
- Files: `{{output_file_1}}`
- Format: {{Description}}

**Success Criteria**:
- ✅ {{CRITERION_1}}
- ✅ {{CRITERION_2}}

**Time Budget**: {{X}} minutes

**Started**: {{YYYY-MM-DD HH:MM}} or N/A
**Completed**: {{YYYY-MM-DD HH:MM}} or N/A
**Actual Duration**: {{X}} minutes or N/A

**Handoff Instructions**:
```markdown
For next agent ({{NEXT_AGENT}}):
- Context: {{Summary}}
- Files produced: {{List}}
- Key decisions: {{Summary}}
```

---

#### **Agent N: {{AGENT_NAME}}** ({{ROLE}})

_[Add more agent sections as needed]_

---

### 🔄 Dynamic Spawns (if applicable)

**Spawned Agents** (created during execution):

1. **{{SPECIALIST_NAME}}** (spawned by {{PARENT_AGENT}})
   - **Reason**: {{Why spawned}}
   - **Task**: {{What they did}}
   - **Output**: {{What they produced}}
   - **Status**: ✅ COMPLETE

---

### 📊 Crew Progress Tracker

| Agent | Role | Status | Start | End | Duration | Output |
|-------|------|--------|-------|-----|----------|--------|
| {{AGENT_1}} | {{ROLE}} | ✅ | {{TIME}} | {{TIME}} | {{X}}m | {{FILES}} |
| {{AGENT_2}} | {{ROLE}} | 🔄 | {{TIME}} | - | - | - |
| {{AGENT_3}} | {{ROLE}} | ⏳ | - | - | - | - |

---

## [D] DOCUMENTATION - Achievement & Decisions

> **Purpose**: Record what was accomplished and why
> **When to fill**: Phase 7 (after validation passes)
> **Fill time**: 10-15 minutes

### 🎉 Session Outcome

**Final Status**: ✅ SUCCESS / ⚠️ PARTIAL SUCCESS / ❌ FAILED

**Completion Date**: {{YYYY-MM-DD HH:MM}}

**Total Duration**: {{X}} hours {{Y}} minutes

---

### ✅ What Was Accomplished

**Milestone Met?**: YES / NO / PARTIALLY

**Achievements**:

1. ✅ **{{ACHIEVEMENT_1}}**
   - Description: {{What was done}}
   - Impact: {{Why this matters}}
   - Files: `{{file_paths}}`

2. ✅ **{{ACHIEVEMENT_2}}**
   - Description: {{What was done}}
   - Impact: {{Why this matters}}
   - Files: `{{file_paths}}`

3. ✅ **{{ACHIEVEMENT_3}}**
   - Description: {{What was done}}
   - Impact: {{Why this matters}}
   - Files: `{{file_paths}}`

---

### 🏗️ Architecture Decisions

**Key decisions made during this session**:

| Decision ID | Decision | Alternatives Considered | Rationale | Impact | Risk |
|-------------|----------|------------------------|-----------|--------|------|
| **AD-001** | {{DECISION}} | {{ALT_1}}, {{ALT_2}}, {{ALT_3}} | {{WHY_CHOSEN}} | {{WHAT_CHANGES}} | {{POTENTIAL_ISSUES}} |
| **AD-002** | {{DECISION}} | {{ALTERNATIVES}} | {{RATIONALE}} | {{IMPACT}} | {{RISK}} |
| **AD-003** | {{DECISION}} | {{ALTERNATIVES}} | {{RATIONALE}} | {{IMPACT}} | {{RISK}} |

**Example**:
| Decision ID | Decision | Alternatives Considered | Rationale | Impact | Risk |
|-------------|----------|------------------------|-----------|--------|------|
| **AD-001** | Use PostgreSQL for backend | Neo4j, MongoDB, JSON files | Lower cost ($50-100/mo vs $300), faster dev time, team familiarity | Database schema created, ORM models implemented | Migration later if graph features needed |

---

### 📝 Technical Details

**Code Changes**:
- {{X}} files modified
- {{Y}} files created
- {{Z}} lines added
- {{W}} lines deleted

**Tests**:
- Unit tests: {{PASS}}/{{TOTAL}} ✅
- Integration tests: {{PASS}}/{{TOTAL}} ✅
- E2E tests: {{PASS}}/{{TOTAL}} ✅
- Test coverage: {{X}}% ({{INCREASE}} from baseline)

**Linting & Type-Checking**:
- Linter: ✅ PASS / ❌ FAIL ({{errors}} errors)
- Type-checker: ✅ PASS / ❌ FAIL ({{errors}} errors)

---

### 💡 Lessons Learned

**What worked well**:
- 💡 {{INSIGHT_1}}
- 💡 {{INSIGHT_2}}
- 💡 {{INSIGHT_3}}

**What could be improved**:
- 🔧 {{IMPROVEMENT_1}}
- 🔧 {{IMPROVEMENT_2}}

**Surprises / Unexpected findings**:
- ⚡ {{SURPRISE_1}}
- ⚡ {{SURPRISE_2}}

---

### 🔮 Future Work / Phase 2 Items

**Not completed in this session (deferred)**:

- [ ] **{{TODO_1}}** - Priority: {{HIGH/MEDIUM/LOW}} - Reason deferred: {{WHY}}
- [ ] **{{TODO_2}}** - Priority: {{HIGH/MEDIUM/LOW}} - Reason deferred: {{WHY}}
- [ ] **{{TODO_3}}** - Priority: {{HIGH/MEDIUM/LOW}} - Reason deferred: {{WHY}}

**New work identified during session**:

- [ ] **{{NEW_TODO_1}}** - Priority: {{PRIORITY}} - Why needed: {{REASON}}
- [ ] **{{NEW_TODO_2}}** - Priority: {{PRIORITY}} - Why needed: {{REASON}}

**Recommended next session**:
- **Topic**: {{NEXT_SESSION_TOPIC}}
- **Why**: {{RATIONALE}}
- **Dependencies**: {{WHAT_MUST_BE_DONE_FIRST}}

---

### 🔗 Related Sessions

**This session built upon**:
- [Session {{ID}}]({{PATH_TO_BMAD}}) - {{TITLE}}

**This session enables**:
- [Session {{ID}}]({{PATH_TO_BMAD}}) - {{TITLE}} (planned/future)

**Related documentation**:
- [{{DOC_TITLE}}]({{PATH}})
- [{{DOC_TITLE}}]({{PATH}})

---

### 📂 Artifact Locations

**BMAD File**: `docs/sessions/BMAD/{{YYYY-MM-DD}}_{{Session-Title}}.md` (this file)

**Deliverables**:
- `{{path/to/deliverable1}}`
- `{{path/to/deliverable2}}`
- `{{path/to/deliverable3}}`

**Test Files**:
- `{{path/to/test_file}}`

**Documentation**:
- `{{path/to/doc}}`

**Git Commit**: `{{COMMIT_SHA}}` on branch `{{BRANCH}}`

**Mermaid Workflow**: `docs/workflows/WORKFLOW_MERMAID_TEMPLATE.mmd` (updated with this session)

---

### 🤝 Handoff Notes

**For the next developer/session working on {{RELATED_TOPIC}}**:

**Context you need**:
- {{CONTEXT_1}}
- {{CONTEXT_2}}

**Key files to review**:
- `{{file_path}}` - {{Why important}}
- `{{file_path}}` - {{Why important}}

**Gotchas / Things to watch out for**:
- ⚠️ {{WARNING_1}}
- ⚠️ {{WARNING_2}}

**Recommended approach**:
{{ADVICE_FOR_NEXT_PERSON}}

---

### ❓ Open Questions (End of Session)

**Questions we still have AFTER completing this work**:

1. ❓ {{QUESTION_1}} - Why this matters: {{REASON}} - Needs investigation: {{YES/NO}}
2. ❓ {{QUESTION_2}} - Why this matters: {{REASON}} - Needs investigation: {{YES/NO}}

**Resolved questions** (from Baseline):
1. ✅ {{QUESTION_FROM_BASELINE}} - Answer: {{RESOLUTION}}

---

## 📊 SESSION METRICS

| Metric | Value | vs Baseline |
|--------|-------|-------------|
| **Duration** | {{X}}h {{Y}}m | {{COMPARE_TO_ESTIMATE}} |
| **Agents Used** | {{N}} | {{COMPARE_TO_PLAN}} |
| **Files Modified** | {{X}} | - |
| **Lines Changed** | {{+X}}/{{-Y}} | - |
| **Tests Added** | {{X}} | +{{INCREASE}} |
| **Cost (API calls)** | ${{COST}} | - |
| **Success Rate** | {{X}}/{{Y}} criteria met | {{PERCENTAGE}}% |

---

## 🔐 GIT OPERATIONS

**Branch**: `{{WORK_BRANCH}}`

**Commits**:
```bash
{{COMMIT_SHA_1}} - {{COMMIT_MESSAGE_1}}
{{COMMIT_SHA_2}} - {{COMMIT_MESSAGE_2}}
```

**Merge Status**:
- [ ] Ready to merge to `{{BASE_BRANCH}}`
- [ ] Needs review
- [ ] Conflicts to resolve
- [ ] Keep as feature branch

**PR Link** (if applicable): {{URL}}

---

## 📋 APPENDIX

### A. Full File Diff Summary

<details>
<summary>Click to expand file changes</summary>

```
{{OUTPUT_OF_git_diff_--stat}}
```

</details>

---

### B. Agent Prompts Used

<details>
<summary>Click to expand agent prompts</summary>

#### Agent 1: {{AGENT_NAME}}

```markdown
{{FULL_PROMPT_TEXT}}
```

#### Agent 2: {{AGENT_NAME}}

```markdown
{{FULL_PROMPT_TEXT}}
```

</details>

---

### C. Validation Report

<details>
<summary>Click to expand test results</summary>

```
{{FULL_TEST_OUTPUT}}
```

</details>

---

## 🏁 END OF BMAD

**Session Status**: ✅ COMPLETE

**Next Action**: {{WHAT_TO_DO_NEXT}}

**Archived**: {{YYYY-MM-DD}}

---

**Template Version**: 1.0.0
**Last Updated**: 2025-11-18
**Maintained by**: TeamLink Master Control System
