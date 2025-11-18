# ADA PRODUCTION LAUNCH GUIDE

**TeamLink Master Control System - Quick Start & User Manual**

---

## 🎯 WHAT YOU HAVE

You now have a **complete AI agent orchestration system** that eliminates information loss and coordinates complex multi-agent workflows.

**The 4 Core Artifacts**:

1. **MASTER_ORCHESTRATION_PROMPT.md** (685 lines)
   - Universal 8-phase workflow logic
   - Dynamic crew formation algorithms
   - Agent dispatch protocols
   - Location: `docs/ada-system/MASTER_ORCHESTRATION_PROMPT.md`

2. **WORKFLOW_MERMAID_TEMPLATE.mmd** (Interactive diagram)
   - Visual flowchart of all 8 phases
   - Appendable session history
   - Clickable links to BMAD files
   - Location: `docs/workflows/WORKFLOW_MERMAID_TEMPLATE.mmd`

3. **BMAD_TEMPLATE.md** (Session document structure)
   - Baseline → Milestone → Agent Dispatch → Documentation
   - Zero-information-loss design
   - Full traceability for every session
   - Location: `docs/sessions/BMAD_TEMPLATE.md`

4. **ada_orchestrator.py** (Python backend)
   - Crew formation engine
   - Agent task management
   - Prompt generation
   - Progress tracking
   - Location: `app/ada_orchestrator.py`

---

## 🔥 WHY THIS SOLVES YOUR PROBLEM

| Problem | ADA Solution | Proof |
|---------|--------------|-------|
| **Information loss between sessions** | BMAD captures EVERYTHING during work | Template enforces "fill as you go" |
| **Context reconstruction overhead** | Baseline + Milestone = exact state snapshot | 2-minute session pickup, not 2 hours |
| **Agent prompt ambiguity** | Phase 4 generates context-rich prompts | Agent Dispatch section shows examples |
| **Decision rationale disappears** | Architecture Decisions table in BMAD | Audit trail + reference for future |
| **Mermaid diagram gets stale** | Phase 8 appends every session to workflow | History section shows session → session |

---

## ⚡ 5-MINUTE SETUP

### Step 1: Verify File Structure

```bash
cd /home/user/adk-fullstack-deploy-tutorial

# Check that all ADA files exist
ls -la docs/ada-system/
# Should see: MASTER_ORCHESTRATION_PROMPT.md, PRODUCTION_LAUNCH_GUIDE.md

ls -la docs/workflows/
# Should see: WORKFLOW_MERMAID_TEMPLATE.mmd

ls -la docs/sessions/
# Should see: BMAD_TEMPLATE.md

ls -la app/
# Should see: ada_orchestrator.py
```

### Step 2: Install Python Dependencies (if needed)

```bash
# The orchestrator uses standard library only, but verify Python version
python3 --version
# Should be Python 3.10+

# If you want to test the orchestrator:
python3 app/ada_orchestrator.py
```

### Step 3: View the Mermaid Workflow

Open `docs/workflows/WORKFLOW_MERMAID_TEMPLATE.mmd` and paste into:

**Option A**: [Mermaid Live Editor](https://mermaid.live) (instant preview)

**Option B**: VSCode with Mermaid extension (local preview)

**Option C**: GitHub/GitLab markdown renderer (auto-renders)

### Step 4: Create Your First BMAD Session File

```bash
# Copy the template for your first session
cp docs/sessions/BMAD_TEMPLATE.md \
   docs/sessions/BMAD/2025-11-18_Your-First-Session.md

# Open and start filling it out
```

---

## 🚀 QUICK-START EXECUTION

### Scenario: You Need to Make a Backend Architecture Decision

**Situation**:
- Deadline: Nov 18
- Decision: PostgreSQL vs Neo4j vs JSON files
- Deliverables: Architecture doc + schema + ORM models
- Time: 2-3 hours

---

### **PHASE 1-3: ADA PLANNING** (15 minutes)

#### Open your BMAD file

```bash
# Create session file
cp docs/sessions/BMAD_TEMPLATE.md \
   docs/sessions/BMAD/2025-11-18_Backend-Architecture.md
```

#### Fill out [B] BASELINE section (10 min)

```markdown
## [B] BASELINE - Current State Snapshot

**Date**: 2025-11-18
**Branch**: main
**Last Commit**: 2068420 - "cleanup"

### Architecture Overview

**Backend**:
- Framework: FastAPI (via Google ADK)
- Language: Python 3.11
- Database: NONE YET (this is what we're deciding)
- Key Libraries: google-adk, vertexai

**Frontend**:
- Framework: Next.js 15
- Language: TypeScript
- UI Library: TailwindCSS + shadcn/ui

**Infrastructure**:
- Hosting: Local dev (targeting Vercel + Vertex AI)

### Current Capabilities

1. Goal-planning LLM agent (basic ADK setup)
2. Next.js chat UI with SSE streaming
3. Local development environment working

### Known Issues

- [ISSUE-001] No database chosen yet - blocking data persistence - HIGH
- [ISSUE-002] No authentication system - MEDIUM

### Baseline Metrics

| Metric | Value |
|--------|-------|
| Lines of Code | ~2000 |
| Test Coverage | 0% (no tests yet) |
| Monthly Cost | $0 (local only) |
```

#### Fill out [M] MILESTONE section (5 min)

```markdown
## [M] MILESTONE - Success Criteria

**Session Goal**: Choose backend architecture and generate schema by Nov 18 deadline

**Why this matters**: Need to start building data models for LearnQwest 60-Ion system

### Success Criteria (ALL must pass)

1. ✅ **[CRITERIA-1]**: Backend architecture chosen (PostgreSQL, Neo4j, or JSON)
   - **Verification**: Decision document exists with clear rationale
   - **Owner**: Claude-Code

2. ✅ **[CRITERIA-2]**: Cost analysis completed showing monthly infrastructure costs
   - **Verification**: Cost comparison table shows all 3 options
   - **Owner**: Claude-Code

3. ✅ **[CRITERIA-3]**: Database schema generated for chosen architecture
   - **Verification**: Schema file passes validation
   - **Owner**: Aider

4. ✅ **[CRITERIA-4]**: ORM models implemented in Python
   - **Verification**: Models pass type-checking (mypy)
   - **Owner**: Aider

5. ✅ **[CRITERIA-5]**: Integration tests written and passing
   - **Verification**: pytest runs successfully
   - **Owner**: Windsurf

### Deliverables Checklist

- [ ] **Architecture Decision Document**
  - File(s): `docs/architecture/backend-decision.md`
  - Format: Markdown with comparison table
  - Acceptance: All 3 options compared on cost, performance, scalability

- [ ] **Cost Analysis**
  - File(s): `docs/architecture/cost-analysis.md`
  - Format: Markdown with pricing tables
  - Acceptance: Monthly costs for each option (low, medium, high scale)

- [ ] **Database Schema**
  - File(s): `app/models/schema.sql` (or equivalent)
  - Format: SQL DDL or equivalent
  - Acceptance: Matches requirements, includes all entities

- [ ] **ORM Models**
  - File(s): `app/models/user.py`, `app/models/course.py`, etc.
  - Format: Python classes
  - Acceptance: Pass mypy type-checking

- [ ] **Integration Tests**
  - File(s): `tests/integration/test_models.py`
  - Format: pytest test suite
  - Acceptance: 100% model coverage, all tests pass

### Time Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| **Deadline** | 2025-11-18 23:59 | Need to start Phase 2 (Ion implementation) |
| **Estimated Duration** | 2.5 hours | Based on sequential crew of 3 agents |
| **Priority** | HIGH | Blocking all other data-related work |
| **Phase** | 24hr | Must complete today |
```

---

### **PHASE 4: AGENT DISPATCH** (5 minutes)

Now you paste your BMAD Baseline + Milestone into Claude-Code and ask it to form the crew:

#### Prompt for Claude-Code:

```
I'm using the ADA (Autonomous Development Architect) orchestration system.

My BMAD file is at: docs/sessions/BMAD/2025-11-18_Backend-Architecture.md

I've completed Phase 1-3 (Context, Baseline, Milestone). Now I need Phase 4: Agent Dispatch.

Please read my BMAD file, analyze the task complexity, and form an appropriate crew.

Then generate specific agent prompts for each crew member following the format in:
docs/ada-system/MASTER_ORCHESTRATION_PROMPT.md (Phase 4 section)

My Baseline summary:
- Current backend: FastAPI with no database
- Need to choose: PostgreSQL vs Neo4j vs JSON files
- Constraints: Cost-conscious, deadline Nov 18

My Milestone:
- Choose architecture with full rationale
- Generate schema + ORM models
- Write integration tests
- All deliverables by end of today

Please form the crew and generate the agent prompts.
```

**Claude-Code will respond with**:

1. Crew analysis (Sequential Crew recommended)
2. Agent roster (Claude-Code → Aider → Windsurf)
3. Individual prompts for each agent
4. Updated BMAD [A] section

---

### **PHASE 5: CODE EXECUTION** (2-3 hours)

#### Agent 1: Claude-Code (Architecture Decision)

Copy the generated prompt for Claude-Code and execute it. Claude-Code will:

1. Compare PostgreSQL, Neo4j, JSON options
2. Analyze costs ($50-100/mo vs $300/mo vs $0)
3. Evaluate performance (latency, scalability)
4. Recommend winner with rationale
5. Create files:
   - `docs/architecture/backend-decision.md`
   - `docs/architecture/cost-analysis.md`
6. Update BMAD with handoff notes

**Handoff to Agent 2**:
```markdown
## [A] AGENT DISPATCH - Claude-Code COMPLETE ✅

**Status**: ✅ COMPLETE
**Duration**: 45 minutes

**Deliverables**:
- docs/architecture/backend-decision.md
- docs/architecture/cost-analysis.md

**Decision**: PostgreSQL chosen

**Rationale**:
- Cost: $50-100/month (vs Neo4j $300+)
- Performance: <20ms latency for typical queries
- Familiarity: Team knows SQL, faster development
- Scalability: Sufficient for 100K+ users

**Handoff to Aider**:
- Task: Generate PostgreSQL schema + SQLAlchemy ORM models
- Input: See docs/architecture/backend-decision.md for entity list
- Expected entities: User, Course, TEKS, Progress, Assessment
- Output: app/models/*.py
```

---

#### Agent 2: Aider (Code Generation)

Copy the generated prompt for Aider and run it. Aider will:

1. Read the architecture decision
2. Generate PostgreSQL schema (SQL DDL)
3. Create SQLAlchemy ORM models:
   - `app/models/user.py`
   - `app/models/course.py`
   - `app/models/teks.py`
   - `app/models/progress.py`
   - `app/models/assessment.py`
4. Ensure models pass type-checking (`mypy app/models/`)
5. Update BMAD with handoff notes

**Handoff to Agent 3**:
```markdown
## [A] AGENT DISPATCH - Aider COMPLETE ✅

**Status**: ✅ COMPLETE
**Duration**: 60 minutes

**Deliverables**:
- app/models/schema.sql (PostgreSQL DDL)
- app/models/user.py (User + Profile models)
- app/models/course.py (Course + Module models)
- app/models/teks.py (TEKS standard models)
- app/models/progress.py (StudentProgress model)
- app/models/assessment.py (Assessment + Question models)

**Type-checking**: ✅ PASS (mypy reports 0 errors)

**Handoff to Windsurf**:
- Task: Write integration tests for all models
- Input: All files in app/models/*.py
- Expected: 100% coverage of model methods
- Output: tests/integration/test_models.py
```

---

#### Agent 3: Windsurf (Validation)

Copy the generated prompt for Windsurf and run it. Windsurf will:

1. Read all ORM models
2. Write integration tests:
   - Test CRUD operations
   - Test relationships (foreign keys, joins)
   - Test constraints (unique, not null)
   - Test edge cases (empty strings, large values)
3. Run tests: `pytest tests/integration/test_models.py`
4. Ensure 100% coverage
5. Update BMAD with validation report

**Completion**:
```markdown
## [A] AGENT DISPATCH - Windsurf COMPLETE ✅

**Status**: ✅ COMPLETE
**Duration**: 30 minutes

**Deliverables**:
- tests/integration/test_models.py (45 test cases)

**Test Results**:
- Unit Tests: 45/45 ✅
- Coverage: 100% of model methods ✅
- Linting: ✅ PASS
- Type-checking: ✅ PASS

**VALIDATION STATUS**: ✅ ALL CRITERIA MET

Crew execution complete! 🎉
```

---

### **PHASE 6: VALIDATION** (15 minutes)

Run final checks:

```bash
# Type-checking
mypy app/models/

# Linting
ruff check app/models/

# Tests
pytest tests/integration/test_models.py -v

# Verify deliverables exist
ls -la docs/architecture/backend-decision.md
ls -la docs/architecture/cost-analysis.md
ls -la app/models/schema.sql
ls -la app/models/*.py
ls -la tests/integration/test_models.py
```

**All pass? Proceed to Phase 7!**

---

### **PHASE 7: ACHIEVEMENT DOCUMENTATION** (10 minutes)

Fill out [D] DOCUMENTATION section in BMAD:

```markdown
## [D] DOCUMENTATION - Achievement & Decisions

**Final Status**: ✅ SUCCESS
**Completion Date**: 2025-11-18 18:30
**Total Duration**: 2 hours 15 minutes

### What Was Accomplished

1. ✅ **Backend Architecture Chosen**
   - Description: PostgreSQL selected after comparing 3 options
   - Impact: Unblocks all data model work for Phase 2
   - Files: docs/architecture/backend-decision.md

2. ✅ **Database Schema Designed**
   - Description: Full SQL schema for 5 core entities
   - Impact: Ready for database provisioning
   - Files: app/models/schema.sql

3. ✅ **ORM Models Implemented**
   - Description: SQLAlchemy models for all entities
   - Impact: Backend can now persist data
   - Files: app/models/*.py (5 files)

4. ✅ **Integration Tests Created**
   - Description: 45 test cases covering all CRUD operations
   - Impact: Confident in model correctness
   - Files: tests/integration/test_models.py

### Architecture Decisions

| Decision ID | Decision | Alternatives | Rationale | Impact |
|-------------|----------|-------------|-----------|--------|
| **AD-001** | PostgreSQL for backend | Neo4j ($300/mo), JSON files ($0) | Lower cost ($50-100/mo), faster dev, team familiarity | Need to provision PostgreSQL instance |
| **AD-002** | SQLAlchemy ORM | Raw SQL, Prisma | Python-native, type-safe, ADK compatible | Adds dependency |

### Lessons Learned

- 💡 Cost analysis was crucial - Neo4j would have blown budget
- 💡 Sequential crew worked perfectly - each agent built on previous
- 💡 BMAD handoffs prevented context loss

### Future Work

- [ ] **Provision PostgreSQL database** - Priority: HIGH - Reason: Need for Phase 2
- [ ] **Add database migrations** - Priority: MEDIUM - Reason: Schema evolution
- [ ] **Implement authentication** - Priority: HIGH - Reason: User system needs auth
```

---

### **PHASE 8: MERMAID UPDATE** (5 minutes)

Open `docs/workflows/WORKFLOW_MERMAID_TEMPLATE.mmd` and add your session to the history:

Find the "Session History" section and add:

```mermaid
S002[Session 002: Backend Architecture<br/>2025-11-18<br/>✅ COMPLETE]

click S002 "docs/sessions/BMAD/2025-11-18_Backend-Architecture.md" "View Session 002 BMAD"
```

Link it to previous session:

```mermaid
S001 -->|Enables| S002
```

Commit the updated Mermaid file.

---

### **GIT OPERATIONS** (5 minutes)

```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
feat: Backend architecture decision and PostgreSQL implementation

Session: 2025-11-18_Backend-Architecture
Status: ✅ COMPLETE
Duration: 2h 15m

Deliverables:
- PostgreSQL chosen over Neo4j and JSON (cost + performance)
- Database schema designed (5 entities)
- SQLAlchemy ORM models implemented
- Integration test suite (45 tests, 100% coverage)

Architecture Decision:
- PostgreSQL: $50-100/mo, <20ms latency, team familiarity
- Rejected Neo4j: $300+/mo too expensive
- Rejected JSON: No query performance or relational support

Files:
- docs/architecture/backend-decision.md
- docs/architecture/cost-analysis.md
- app/models/schema.sql
- app/models/*.py (5 ORM models)
- tests/integration/test_models.py

Tests: ✅ 45/45 passing
Type-check: ✅ PASS
Linting: ✅ PASS

BMAD: docs/sessions/BMAD/2025-11-18_Backend-Architecture.md
EOF
)"

# Push to remote
git push -u origin claude/teamlink-master-control-01NF7pKugYq3eybZ3C1FhtFo
```

---

## 🎉 SESSION COMPLETE!

**Result**:
- Zero information loss ✅
- Full decision audit trail ✅
- All deliverables created ✅
- Tests passing ✅
- Mermaid updated ✅
- Git committed ✅

**Next session pickup time**: 2 minutes (just read the BMAD file)

---

## 💡 PRO TIPS FOR YOUR WORKFLOW

### Tip 1: Use BMAD as Your Single Source of Truth

**Don't**:
- Try to remember what you decided 3 days ago
- Re-run analyses you already did
- Search through chat logs for context

**Do**:
- Open the BMAD file first thing
- Read [B] Baseline to see where you left off
- Check [D] Documentation for past decisions
- Use "Architecture Decisions" table as reference

---

### Tip 2: Fill BMAD As You Go, Not After

**Don't**:
- Wait until the end of the session to document
- Try to remember what happened 2 hours ago
- Batch all documentation at once

**Do**:
- Update [A] Agent Dispatch after each agent completes
- Add decisions to Architecture Decisions table immediately
- Write handoff notes BEFORE moving to next agent

**Why**: Real-time updates = zero information loss

---

### Tip 3: Use Sequential Crews for Learning

**Don't**:
- Start with parallel crews (complex coordination)
- Try dynamic spawning on first session

**Do**:
- Start with sequential crews (simple handoffs)
- Master the BMAD workflow first
- Graduate to parallel/dynamic after 3-5 sessions

**Why**: Learn to walk before you run

---

### Tip 4: Timebox Your Agents

**Don't**:
- Let agents run indefinitely
- Forget to check progress

**Do**:
- Set realistic time budgets in AgentTask
- Check BMAD every 30 minutes
- Stop agents if they exceed budget by 50%

**Why**: Prevents runaway sessions

---

### Tip 5: Review Validation Reports

**Don't**:
- Skip Phase 6 validation
- Assume tests pass without checking

**Do**:
- Run ALL validation checks (tests, linting, type-checking)
- Read test output carefully
- Fix issues before Phase 7

**Why**: Catch problems before they compound

---

### Tip 6: Use Mermaid as Your Timeline

**Don't**:
- Forget to update Mermaid after sessions
- Let the diagram go stale

**Do**:
- Update Mermaid in Phase 8 EVERY session
- Link sessions together (shows dependencies)
- Use it to visualize your project journey

**Why**: Visual timeline prevents big-picture blindness

---

### Tip 7: Reference Past BMADs

**Don't**:
- Start from scratch each session
- Forget what you learned before

**Do**:
- Link related sessions in [D] Documentation
- Copy baseline from previous session (if similar)
- Review past "Lessons Learned" sections

**Why**: Compound knowledge, not restart knowledge

---

## 🔧 TROUBLESHOOTING

### Problem: "BMAD file is too long, overwhelming"

**Solution**:
- Use collapsible sections (`<details>` tags) for appendices
- Keep main sections concise (Baseline: 1 page, Milestone: 1 page)
- Move detailed logs to separate files, link from BMAD

---

### Problem: "Agent went off-track, not following prompt"

**Solution**:
- Check if prompt includes ALL necessary context
- Ensure success criteria are specific and testable
- Add more constraints ("DO NOT do X, only do Y")
- Try a different agent (swap Aider for Claude-Code)

---

### Problem: "Tests failing in Phase 6"

**Solution**:
- DO NOT mark session as complete
- Create new agent task: "Fix failing tests"
- Add to crew roster
- Run validation again
- Only complete session when ALL tests pass

---

### Problem: "Lost track of what I was doing mid-session"

**Solution**:
- Open BMAD file
- Read [M] Milestone (what you're trying to achieve)
- Read [A] Agent Dispatch (where you are in the workflow)
- Check last completed agent's handoff notes
- Continue from there

---

### Problem: "Don't know which agent to use for task"

**Reference**:

| Task Type | Recommended Agent |
|-----------|------------------|
| Planning, architecture, decision-making | Claude-Code (Architect) |
| Code implementation, refactoring | Aider (Generator) |
| Testing, validation, quality checks | Windsurf (Validator) |
| Documentation, parsing, analysis | Parser-Ion (Parser) |
| Specialized/niche tasks | Cline (Specialist) |

---

### Problem: "Session taking too long, past deadline"

**Solution**:
1. Stop current work
2. Mark session as "⚠️ PARTIAL SUCCESS"
3. Document what WAS completed in [D] Documentation
4. Move incomplete items to "Future Work"
5. Commit partial progress
6. Create new session for remaining work

**Why**: Better to have documented partial progress than nothing

---

## 📚 REFERENCE: THE 8 PHASES AT A GLANCE

| Phase | Name | Duration | Agent | Output |
|-------|------|----------|-------|--------|
| 1 | Context Gathering | 5-15min | Claude-Code | Context summary |
| 2 | Baseline Establishment | 10-20min | Claude-Code | BMAD [B] section |
| 3 | Milestone Definition | 10-15min | Claude-Code | BMAD [M] section |
| 4 | Agent Dispatch | 5-10min | ADA | BMAD [A] section + prompts |
| 5 | Code Execution | 30min-8hr | Crew | Deliverables |
| 6 | Validation | 15-30min | Windsurf | Test reports |
| 7 | Achievement Documentation | 10-15min | Claude-Code | BMAD [D] section |
| 8 | Mermaid Update | 5-10min | Claude-Code | Updated diagram |

**Total overhead**: ~1 hour (for 3-hour session = 33% overhead, but saves 2 hours on next session)

---

## 🎯 SUCCESS METRICS

**You'll know ADA is working when**:

✅ You can pick up any session in 2 minutes by reading BMAD
✅ You never ask "Why did we decide X?" (it's in Architecture Decisions table)
✅ Your Mermaid diagram shows a clear timeline of progress
✅ New team members can onboard by reading 3 BMAD files
✅ You spend more time coding, less time "remembering what I was doing"

---

## 🚀 WHAT'S NEXT

**After mastering sequential crews, try**:

1. **Parallel Crews**: Backend + Frontend simultaneously
2. **Dynamic Task Forces**: Emergency bug fixes with spawning
3. **Multi-Session Epics**: Link 5-10 BMADs for large features
4. **Automated BMAD Generation**: Python script to generate BMAD from git commits

**Advanced topics** (future guides):

- Integrating ADA with CI/CD pipelines
- Using ada_orchestrator.py to automate crew formation
- Building custom agent roles for your domain
- Mermaid diagram auto-updates via git hooks

---

## 📞 SUPPORT

**If you get stuck**:

1. Read `MASTER_ORCHESTRATION_PROMPT.md` (comprehensive reference)
2. Check `BMAD_TEMPLATE.md` for section guidelines
3. Review past BMAD files in `docs/sessions/BMAD/`
4. Open GitHub issue: [Your repo issues page]

---

## 🏁 FINAL CHECKLIST

Before starting your first session, verify:

- [ ] All 4 core files exist (Master Prompt, Mermaid, BMAD Template, orchestrator.py)
- [ ] Mermaid diagram renders in Mermaid Live Editor
- [ ] Python orchestrator runs without errors
- [ ] Git branch is set up correctly
- [ ] You've read this guide's "Quick-Start Execution" section

**You're ready to launch!** 🚀

---

**Version**: 1.0.0
**Last Updated**: 2025-11-18
**Maintained by**: TeamLink Master Control System

---

**"Iron sharpens iron, and one agent sharpens another."** ⚔️💎
