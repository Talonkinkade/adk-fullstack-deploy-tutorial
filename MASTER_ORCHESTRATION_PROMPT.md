# MASTER ORCHESTRATION PROMPT
**Dynamic Multi-Agent Phase-Driven Development System**
**Team LINK Digital Self Partnership - Universal Template**

---

## 🎯 CONFIGURATION VARIABLES (Customize Per Project)

```yaml
# PROJECT CONTEXT
PROJECT_NAME: "LearnQwest"
PROJECT_DESCRIPTION: "AI-powered educational platform transforming YouTube content into TEKS-aligned learning materials"
SYSTEM_ARCHITECTURE: "8-tier Ion agent architecture with ADA orchestrator"
TARGET_USERS: "Texas school districts, educators, students"

# AGENT ECOSYSTEM
PRIMARY_AGENTS:
  - Claude-Code     # Complex multi-file changes, architecture decisions, git operations
  - Cline           # Interactive editing, quick iterations, file-by-file work
  - Aider           # Code generation, refactoring, test writing
  - Windsurf        # Alternative code editor, validation
  - Parser-Ion      # Custom data processing, TEKS alignment

# CURRENT SESSION
SESSION_ID: "2025-11-16-001"
SESSION_GOAL: "Backend Architecture Decision (JSON vs SQL vs Neo4j)"
DEADLINE: "2025-11-18"
PRIORITY: "HIGH"
BLOCKING_ISSUES: "Information loss between sessions, context reconstruction overhead"

# PHASE CONTROL (Which phase are you in?)
CURRENT_PHASE: "1"  # 1-8, see phases below
AUTO_ADVANCE: false  # If true, automatically move to next phase on completion

# OUTPUT PREFERENCES
USE_BRACKETS: true   # [FIRE]/[OK] markers
MERMAID_UPDATE: true # Auto-update workflow diagram
BMAD_TRACKING: true  # Use Baseline-Milestone-Achievement-Dispatch documentation
```

---

## 📋 THE 8-PHASE WORKFLOW

### **PHASE 1: CONTEXT GATHERING**
**Purpose:** Establish complete project state and constraints

**Actions:**
- Review existing documentation (README, architecture docs, previous BMADs)
- Identify all relevant files, dependencies, constraints
- Document current system state (git status, deployment status, tech stack)
- Clarify success criteria and deadline

**Deliverables:**
- Context summary document
- File inventory
- Constraint list (time, budget, tech, team)
- Risk assessment

**Transition Criteria:** All stakeholders agree on context accuracy

---

### **PHASE 2: BASELINE ESTABLISHMENT**
**Purpose:** Capture "before" state for comparison and rollback

**Actions:**
- Document current architecture (if any)
- Capture current metrics (performance, cost, complexity)
- Create snapshot of current codebase state
- Identify pain points and limitations

**Deliverables:**
- BMAD "Baseline" section filled
- Current state metrics
- Git commit hash for reference state
- Known issues list

**Transition Criteria:** Baseline documented and saved

---

### **PHASE 3: MILESTONE DEFINITION**
**Purpose:** Define measurable success criteria and done state

**Actions:**
- Define specific, measurable outcomes
- Set acceptance criteria for each deliverable
- Identify decision points and approval gates
- Create timeline with checkpoints

**Deliverables:**
- BMAD "Milestone" section filled
- Success metrics defined
- Acceptance criteria checklist
- Timeline with gates

**Transition Criteria:** Team agrees milestone is clear and achievable

---

### **PHASE 4: AGENT DISPATCH**
**Purpose:** Route work to the optimal agent(s) with rich context

**Actions:**
- Analyze task requirements (complexity, file count, type of work)
- Select optimal agent(s) based on strengths
- Generate context-rich prompts for each agent
- Define handoff points between agents

**Agent Selection Matrix:**
```
TASK TYPE                    → OPTIMAL AGENT
─────────────────────────────────────────────────────────
Architecture decisions       → Claude-Code
Multi-file refactoring       → Claude-Code + Aider
Git operations              → Claude-Code
Single-file edits           → Cline
Code generation (new files) → Aider
Test writing                → Aider
Quick iterations            → Cline
Validation/review           → Windsurf
Data processing             → Parser-Ion
```

**Deliverables:**
- Agent assignment table
- Context-rich prompts for each agent
- Handoff protocol between agents
- Expected output from each agent

**Transition Criteria:** Agent(s) assigned and prompts prepared

---

### **PHASE 5: CODE EXECUTION**
**Purpose:** Execute development work via assigned agents

**Actions:**
- Paste prepared prompts to assigned agents
- Monitor agent output
- Handle blockers/errors as they arise
- Validate intermediate outputs

**Best Practices:**
- Run agents in parallel when tasks are independent
- Use sequential execution when outputs depend on each other
- Save agent outputs to BMAD as they complete
- Document any deviation from plan

**Deliverables:**
- Code changes (commits)
- Agent output logs
- Deviation notes (if any)
- Intermediate validation results

**Transition Criteria:** All assigned tasks completed by agents

---

### **PHASE 6: VALIDATION & TESTING**
**Purpose:** Verify outputs meet milestone criteria

**Actions:**
- Run automated tests (unit, integration, e2e)
- Perform manual validation against acceptance criteria
- Check for regressions
- Validate against baseline metrics

**Validation Checklist:**
```
[ ] All tests pass
[ ] No new errors/warnings introduced
[ ] Performance meets or exceeds baseline
[ ] Security review passed (if applicable)
[ ] Documentation updated
[ ] Milestone acceptance criteria met
[ ] Code review completed (if team-based)
```

**Deliverables:**
- Test results
- Performance comparison (baseline vs current)
- Validation report
- Issues found (if any)

**Transition Criteria:** All validation checks pass

---

### **PHASE 7: ACHIEVEMENT DOCUMENTATION**
**Purpose:** Capture outcomes, decisions, and learnings

**Actions:**
- Fill BMAD "Achievement" section
- Document architecture decisions (alternatives considered, rationale)
- Record lessons learned
- Update project documentation
- Create handoff documentation for next session

**Architecture Decision Template:**
```markdown
| Decision | Alternatives Considered | Winner | Rationale | Trade-offs | Cost Impact |
|----------|------------------------|--------|-----------|------------|-------------|
| [Topic]  | A, B, C                | B      | [Why]     | [What lost]| [$$]        |
```

**Deliverables:**
- BMAD "Achievement" section filled
- Architecture decisions documented
- Updated project docs
- Lessons learned log

**Transition Criteria:** All outcomes documented

---

### **PHASE 8: MERMAID WORKFLOW UPDATE**
**Purpose:** Maintain living visual history of all work

**Actions:**
- Add new session node to workflow diagram
- Connect to previous session(s)
- Add decision points and outcomes
- Update agent usage statistics
- Increment version/timestamp

**Mermaid Update Protocol:**
```mermaid
%% Add to history section:
Session_2025-11-16-001["Session: Backend Architecture<br/>Decision: PostgreSQL<br/>Agents: Claude-Code, Aider<br/>Status: Complete"]
Session_2025-11-15-001 --> Session_2025-11-16-001
```

**Deliverables:**
- Updated WORKFLOW_MERMAID diagram
- Session history entry
- Agent usage statistics
- Updated changelog

**Transition Criteria:** Workflow diagram updated and committed to git

---

## 🔥 ORCHESTRATION COMMAND TEMPLATES

### Starting a New Session:
```markdown
[FIRE] New Session: [SESSION_GOAL]

PROJECT: [PROJECT_NAME]
DEADLINE: [DATE]
CURRENT_PHASE: 1 (Context Gathering)

I'm using the Master Orchestration system with 8-phase workflow + BMAD tracking.

IMMEDIATE CONTEXT:
- [Key constraint 1]
- [Key constraint 2]
- [Blocking issue]

REQUEST: Execute Phase 1 (Context Gathering). Please:
1. Review existing docs in [PATHS]
2. Identify all files related to [TOPIC]
3. Document current state
4. Generate context summary

After Phase 1, I'll confirm baseline and move to Phase 2.
```

### Phase 4: Agent Dispatch Example:
```markdown
[FIRE] Phase 4: Agent Dispatch

SESSION: [SESSION_ID] - [SESSION_GOAL]

COMPLETED PHASES:
✓ Phase 1: Context gathered
✓ Phase 2: Baseline established
✓ Phase 3: Milestone defined

CURRENT NEED: Generate agent prompts for the following tasks:

TASK 1: [Description]
- Complexity: [Low/Medium/High]
- File count: [Number]
- Type: [Architecture/Code/Test/Refactor]
- Suggested agent: [AGENT_NAME]

TASK 2: [Description]
...

REQUEST: Generate context-rich prompts for each task that include:
- Full baseline state
- Milestone success criteria
- Specific deliverables expected
- File paths and dependencies
- Acceptance criteria

I will paste these prompts to the assigned agents in Phase 5.
```

### Phase 7: Achievement Documentation:
```markdown
[FIRE] Phase 7: Achievement Documentation

SESSION: [SESSION_ID] - [SESSION_GOAL]

PHASES COMPLETED:
✓ Phase 1-6 complete
✓ All validation passed

OUTCOMES TO DOCUMENT:
- Decision made: [DECISION]
- Code delivered: [FILE_PATHS]
- Tests: [PASS/FAIL counts]
- Performance: [METRICS]

REQUEST: Help me fill the BMAD Achievement section with:
1. Architecture Decisions table (alternatives, rationale, trade-offs)
2. Delivered artifacts list
3. Validation results summary
4. Lessons learned
5. Next session recommendations

[Paste relevant agent outputs here]
```

---

## 📊 PHASE DECISION MATRIX

**When to advance to next phase:**
```
PHASE → ADVANCE IF
─────────────────────────────────────────────
1     → Context is clear, no open questions
2     → Baseline metrics captured and saved
3     → Milestone has clear acceptance criteria
4     → Agent prompts are ready and approved
5     → All code changes committed
6     → All validation checks pass
7     → Achievement fully documented
8     → Mermaid diagram updated and committed
```

**When to loop back:**
```
REGRESSION TRIGGERS:
─────────────────────────────────────────────
Phase 5 → Phase 4: Agent fails, need different agent
Phase 6 → Phase 5: Validation fails, need code fixes
Phase 7 → Phase 3: Milestone was not achievable, redefine
Any     → Phase 1: Major new information changes context
```

---

## 🎯 AGENT-SPECIFIC PROMPT PATTERNS

### Claude-Code Prompt Template:
```markdown
[FIRE] Claude-Code Task: [TASK_NAME]

CONTEXT:
- Project: [PROJECT_NAME]
- Goal: [SESSION_GOAL]
- Baseline: [CURRENT_STATE]
- Milestone: [SUCCESS_CRITERIA]

YOUR TASK:
[Detailed description]

FILES TO MODIFY:
- [path/to/file1.py] - [What to change]
- [path/to/file2.ts] - [What to change]

ACCEPTANCE CRITERIA:
[ ] [Criterion 1]
[ ] [Criterion 2]
[ ] Tests pass
[ ] No regressions

DELIVERABLES:
1. [Deliverable 1]
2. [Deliverable 2]
3. Git commit with message: "[FIRE] [Brief description]"

CONSTRAINTS:
- Deadline: [DATE]
- Must maintain backward compatibility with [SYSTEM]
- Performance: [REQUIREMENT]

[OK] Proceed with implementation.
```

### Aider Prompt Template:
```markdown
I need you to generate [DESCRIPTION].

Context:
- This is part of [PROJECT_NAME]
- Current architecture: [BRIEF_DESCRIPTION]
- Related files: [LIST]

Requirements:
1. [Requirement 1]
2. [Requirement 2]

Files to create/modify:
- [path/to/file.py]

Tests required:
- [test scenario 1]
- [test scenario 2]

Run tests after generation and fix any failures.
```

### Cline Prompt Template:
```markdown
Quick edit needed in [FILE_PATH]:

Change: [SPECIFIC_CHANGE]
Location: [LINE_NUMBERS or FUNCTION_NAME]
Reason: [WHY]

Verify the change doesn't break [RELATED_FUNCTIONALITY].
```

---

## 🔄 INFORMATION LOSS PREVENTION PROTOCOL

**Problem:** Context disappears between sessions
**Solution:** BMAD + Mermaid living history

### During Session:
```
1. Fill BMAD sections AS YOU WORK (not after)
   - Baseline: First 5 minutes
   - Milestone: Next 5 minutes
   - Achievement: As each task completes

2. Save agent outputs immediately to BMAD
   - Copy/paste key decisions
   - Link to commits
   - Note deviations

3. Update Mermaid when session ends
   - Add session node
   - Connect to previous
   - Record outcome
```

### Between Sessions:
```
1. Archive completed BMAD to docs/sessions/BMAD/[DATE]_[TOPIC].md
2. Commit Mermaid diagram updates
3. Create handoff note for next session
```

### Starting Next Session:
```
1. Read previous BMAD (2 min)
2. Check Mermaid for session flow (1 min)
3. Review git commits since last session (2 min)
4. Start new BMAD, reference previous in "Context" section

Total pickup time: 5 minutes vs 2 hours reconstruction
```

---

## 💎 ADVANCED ORCHESTRATION PATTERNS

### Parallel Agent Execution:
```markdown
[FIRE] Parallel Dispatch - 3 agents

SESSION: [SESSION_ID]
PHASE: 5 (Code Execution)

AGENT 1 (Claude-Code): Architecture decision
AGENT 2 (Aider): Generate schema models
AGENT 3 (Windsurf): Write integration tests

These tasks are INDEPENDENT - run in parallel.

[Agent 1 prompt]
---
[Agent 2 prompt]
---
[Agent 3 prompt]

I'll synthesize outputs when all three complete.
```

### Sequential Agent Pipeline:
```markdown
[FIRE] Sequential Pipeline - 3 agents

SESSION: [SESSION_ID]
PHASE: 5 (Code Execution)

PIPELINE:
1. Claude-Code: Design schema → Output: schema.sql
2. Aider: Generate ORM models from schema.sql → Output: models.py
3. Windsurf: Write tests for models.py → Output: test_models.py

HANDOFF PROTOCOL:
- After each agent completes, validate output
- If validation passes, proceed to next agent
- If validation fails, loop back to previous agent with fixes

Starting with Agent 1...
```

---

## 📋 QUICK REFERENCE CHEAT SHEET

```
┌─────────────────────────────────────────────────────┐
│ PHASE FLOW                                          │
├─────────────────────────────────────────────────────┤
│ 1. CONTEXT    → What's the situation?              │
│ 2. BASELINE   → Where are we now?                  │
│ 3. MILESTONE  → Where do we want to be?            │
│ 4. DISPATCH   → Who does what?                     │
│ 5. CODE       → Do the work                        │
│ 6. VALIDATE   → Did it work?                       │
│ 7. ACHIEVE    → What did we learn?                 │
│ 8. MERMAID    → Update the map                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ AGENT SELECTION                                     │
├─────────────────────────────────────────────────────┤
│ Architecture/Multi-file  → Claude-Code              │
│ Code Generation          → Aider                    │
│ Quick Edits             → Cline                     │
│ Validation              → Windsurf                  │
│ Data Processing         → Parser-Ion                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ DOCUMENTATION                                       │
├─────────────────────────────────────────────────────┤
│ Before starting  → BMAD Baseline                    │
│ During planning  → BMAD Milestone                   │
│ As you work      → BMAD Achievement (incremental)   │
│ After completion → Mermaid update                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ PREVENTING INFO LOSS                                │
├─────────────────────────────────────────────────────┤
│ 1. Fill BMAD during session (not after)            │
│ 2. Document decisions with alternatives + rationale │
│ 3. Update Mermaid before closing session            │
│ 4. Commit everything to git                         │
│ 5. Next session: Read last BMAD first (5 min)      │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 GETTING STARTED (First Time Use)

**Step 1:** Customize configuration variables at top of this file
**Step 2:** Create directory structure:
```bash
mkdir -p docs/sessions/BMAD
mkdir -p docs/workflows
mkdir -p docs/decisions
```

**Step 3:** Copy templates:
```bash
cp BMAD_TEMPLATE_LEARNQWEST.md docs/sessions/BMAD/TEMPLATE.md
cp WORKFLOW_MERMAID_TEMPLATE.mmd docs/workflows/master_workflow.mmd
```

**Step 4:** Start first session:
```markdown
[FIRE] First Session with Master Orchestration

PROJECT: [PROJECT_NAME]
GOAL: [WHAT_YOU_WANT_TO_ACHIEVE]

I'm using the 8-phase workflow system. Let's start with Phase 1: Context Gathering.

Please help me:
1. Review [EXISTING_DOCS]
2. Identify current state of [SYSTEM_COMPONENT]
3. List constraints and requirements
4. Generate context summary

After Phase 1 completes, I'll move to Phase 2: Baseline.
```

**Step 5:** Follow phases 1-8, updating BMAD as you go

**Step 6:** At session end, archive BMAD and update Mermaid

---

## 🎯 SUCCESS METRICS

**You're using this system correctly if:**
- [ ] You can pick up any session in < 5 minutes by reading BMAD
- [ ] You never ask "Why did we decide X?" (it's documented)
- [ ] Agents receive context-rich prompts (not vague requests)
- [ ] Your Mermaid diagram shows session-to-session flow
- [ ] You spend more time building than reconstructing context

**You need to adjust if:**
- [ ] You're still losing information between sessions
- [ ] BMADs are being filled after sessions end (too late!)
- [ ] Agents are asking clarifying questions (prompt wasn't rich enough)
- [ ] You can't remember what happened 2 sessions ago
- [ ] Mermaid diagram is static/not updated

---

## 📞 TROUBLESHOOTING

**Q: Phase 6 validation keeps failing**
A: Loop back to Phase 5, identify specific failures, dispatch to appropriate agent with fixes

**Q: Agent outputs don't match expectations**
A: Your Phase 4 prompts weren't specific enough. Add more context, constraints, and examples

**Q: I forgot to update BMAD during session**
A: Review git commits and agent logs to reconstruct. Use this as lesson to fill BMAD live next time

**Q: Mermaid diagram is too complex**
A: Create sub-diagrams for each major milestone. Link them in master workflow

**Q: Can't decide which agent to use**
A: Start with Claude-Code for complex/multi-file work. Use Aider for pure code generation. Use Cline for quick single-file edits

---

**[OK] Master Orchestration system ready. Choose your phase and execute!** 🚀

**Version:** 1.0.0
**Last Updated:** 2025-11-16
**Maintainer:** Team LINK Digital Self Partnership
