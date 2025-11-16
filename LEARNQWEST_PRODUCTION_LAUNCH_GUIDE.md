# LearnQwest Production Launch Guide
**Team LINK Digital Self Partnership - Your Complete Playbook**

---

## 🎯 YOUR SITUATION (As of Nov 16, 2025)

**Who You Are:**
- Link, building LearnQwest - AI-powered educational platform for Texas schools
- 60+ Ion agents in 8-tier architecture with ADA orchestrator
- Transforming YouTube → TEKS-aligned learning materials
- High-energy builder using [FIRE]/[OK] markers
- Working with Claude-Code as Digital Self partner

**Your Current Challenge:**
```
Problem 1: Backend Architecture Undefined
- Need to choose: JSON files vs PostgreSQL vs Neo4j
- Deadline: Nov 18 (stakeholder demo)
- Constraints: < $100/month budget preferred

Problem 2: Information Loss Between Sessions
- Lose context when switching between coding sessions
- Spend 2+ hours reconstructing "why we decided X"
- Decisions disappear, have to re-analyze same problems

Problem 3: Multi-Agent Coordination Complexity
- Claude-Code, Cline, Aider, Windsurf - which for what?
- Vague prompts lead to suboptimal outputs
- No clear workflow for complex multi-phase tasks
```

**What You Have (Infrastructure):**
- ✓ ADK Python backend template (goal-planning agent running)
- ✓ Next.js frontend with streaming SSE
- ✓ Vertex AI deployment configuration
- ✓ 8-tier Ion architecture designed (LEARNQWEST_WORKFLOW.mmd)
- ✓ 60+ agent placeholders mapped

**What You Need (This Guide Provides):**
- ✓ Phase-driven workflow system (8 phases: Context → Mermaid)
- ✓ BMAD documentation method (prevents info loss)
- ✓ Agent dispatch strategy (right agent for right task)
- ✓ Backend architecture decision framework
- ✓ Production-ready templates and prompts

---

## 🚀 THE SYSTEM YOU JUST GOT (4 Artifacts)

### **1. MASTER_ORCHESTRATION_PROMPT.md** (685 lines)
**What it is:**
- Universal 8-phase workflow system for any complex dev task
- Phase 1: Context → Phase 2: Baseline → Phase 3: Milestone → Phase 4: Dispatch → Phase 5: Code → Phase 6: Validate → Phase 7: Achievement → Phase 8: Mermaid
- Agent selection matrix (which agent for which task type)
- Command templates for starting sessions, dispatching agents, documenting outcomes

**Why it matters:**
- **Prevents scope creep:** Each phase has clear entry/exit criteria
- **Optimizes agent selection:** Uses Claude-Code for architecture, Aider for code gen, etc.
- **Creates reproducibility:** Session templates make future work faster

**When to use it:**
- Starting any non-trivial development session
- Before dispatching work to agents
- When you need structured approach to complex decisions

---

### **2. WORKFLOW_MERMAID_TEMPLATE.mmd**
**What it is:**
- Visual flowchart of the 8-phase system
- Color-coded phases (blue = context, purple = baseline, etc.)
- Appendable Session History section (never overwrites, only grows)
- Shows which agents execute which phases

**Why it matters:**
- **Visual session history:** See flow from decision to decision over time
- **Prevents duplicate work:** Check diagram to see if similar work was done before
- **Team communication:** Share diagram to show project evolution

**When to use it:**
- End of each session (Phase 8: add your session node)
- When planning next sprint (review history)
- When onboarding new team members (show the journey)

---

### **3. BMAD_TEMPLATE_LEARNQWEST.md**
**What it is:**
- **B**aseline (where you are now)
- **M**ilestone (where you want to be)
- **A**chievement (what you actually delivered)
- **D**ispatch (which agents did what)
- Customized for LearnQwest (60 Ions, TEKS, Texas schools context)
- Includes example filled sections

**Why it matters:**
- **Kills information loss:** Fill during session (not after), captures decisions with rationale
- **Enables fast pickup:** Read previous BMAD in 5 minutes vs 2 hours reconstruction
- **Documents alternatives:** "Why PostgreSQL not Neo4j?" → It's in the BMAD table

**When to use it:**
- Start of every dev session (create new BMAD)
- First 5 min: Fill Baseline
- Next 5 min: Fill Milestone
- As you work: Update Achievement incrementally
- End of session: Archive BMAD to docs/sessions/BMAD/

---

### **4. LEARNQWEST_PRODUCTION_LAUNCH_GUIDE.md** (This file!)
**What it is:**
- Your playbook for using the system
- Step-by-step execution for first session (backend architecture)
- Sample prompts ready to paste
- Pro tips for your workflow style

**Why it matters:**
- **Gets you unblocked NOW:** Follow quick-start, make backend decision today
- **Teaches the system:** By using it once, you'll internalize the pattern
- **Addresses your specific constraints:** Nov 18 deadline, budget limits, solo dev with agents

**When to use it:**
- Right now! (follow quick-start below)
- When stuck on how to start a session
- When unsure which agent to use

---

## ⚡ QUICK-START EXECUTION (Backend Architecture Decision)

**Goal:** Choose backend architecture (JSON vs SQL vs Neo4j) by Nov 18 with full documentation

**Time Required:** 2-3 hours end-to-end (vs weeks of indecision!)

---

### **STEP 1: Setup (5 minutes)**

**1.1 Create directory structure:**
```bash
cd /home/user/adk-fullstack-deploy-tutorial
mkdir -p docs/sessions/BMAD
mkdir -p docs/decisions
mkdir -p docs/cost-analysis
```

**1.2 Copy BMAD template for this session:**
```bash
cp BMAD_TEMPLATE_LEARNQWEST.md docs/sessions/BMAD/2025-11-16-001_Backend-Architecture.md
```

**1.3 Open your new BMAD:**
```bash
code docs/sessions/BMAD/2025-11-16-001_Backend-Architecture.md
# OR
nano docs/sessions/BMAD/2025-11-16-001_Backend-Architecture.md
```

---

### **STEP 2: Phase 1-3 (Fill BMAD Baseline & Milestone) - 15 minutes**

**2.1 Update SESSION METADATA section:**
```yaml
SESSION_ID: "2025-11-16-001"
SESSION_GOAL: "Choose backend architecture and generate production-ready schema"
PROJECT: "LearnQwest"
DATE_STARTED: "2025-11-16 [current time]"
DEADLINE: "2025-11-18"
PRIORITY: "HIGH"
PHASE: "1"
STATUS: "Planning"
```

**2.2 Fill BASELINE section (5 minutes):**

Paste this into "Current State Summary":
```
- Backend architecture undefined - considering JSON files vs PostgreSQL vs Neo4j
- No schema exists yet for 8-tier Ion system
- YouTube ingestion pipeline (Tier 2) designed but not implemented
- ADK template running locally with goal-planning agent
- No database integration currently
- All data is ephemeral (no persistence)
```

Paste this into "Current Metrics":
```
Performance: N/A (no backend yet)
Cost: $0/month (local dev only)
Coverage: Infrastructure 30%, Agent implementation 5%
Technical Debt: 0 (greenfield)
```

Paste this into "Files/Components in Scope":
```
- app/config.py (database connection config)
- app/models/ (to be created - ORM models)
- app/db/ (to be created - database utilities)
- pyproject.toml (dependencies to add)
- docs/decisions/ (architecture decision record)
```

Paste this into "Known Pain Points":
```
- Don't know which database architecture to choose
- Concerned about cost vs performance trade-offs
- Need schema design but no database selected yet
- Information loss between sessions (hence BMAD!)
- Stakeholder demo Nov 18 requires working backend
```

Paste this into "Dependencies & Constraints":
```
Time: Backend decision + schema by Nov 18 (2 days!)
Budget: Prefer < $100/month for database (MVP phase)
Tech: Must integrate with existing ADK + Next.js + Vertex AI
Team: Solo (Link) + agent partnership (Claude-Code, Aider, Windsurf)
Data: 8 tiers of Ion agents, content, users, TEKS mappings
```

**2.3 Fill MILESTONE section (5 minutes):**

Paste this into "Session Goal":
```
Decide backend architecture (JSON vs SQL vs Neo4j) and generate production-ready schema with implementation roadmap
```

Paste this into "Success Criteria":
```
[ ] Backend architecture selected with documented rationale
[ ] Cost analysis completed for all 3 alternatives (monthly $ + scaling to 100 schools)
[ ] Performance requirements validated (query latency, throughput)
[ ] Schema v1.0 generated for winning architecture
[ ] Implementation roadmap created (24hr quick-win vs Phase 2 full build)
[ ] Architecture Decision Record created with alternatives + trade-offs
[ ] All decisions capture "why" (prevent future "why did we choose X?")
```

Paste this into "Deliverables List":
```
1. Architecture Decision Record - docs/decisions/2025-11-16-backend-architecture.md
2. Cost Analysis Document - docs/cost-analysis/backend-comparison.md
3. Database Schema (v1.0) - app/models/schema.py (if SQL) OR schema design doc
4. Implementation Roadmap - docs/roadmap-backend-implementation.md
5. Git commits with [FIRE] markers
6. Updated BMAD with all outcomes
```

**2.4 Save BMAD**

Baseline and Milestone are now captured! This took 15 minutes. If your session gets interrupted, you can pick up in 5 minutes by reading this BMAD.

---

### **STEP 3: Phase 4 (Agent Dispatch) - 10 minutes**

**Goal:** Generate context-rich prompt for Claude-Code to analyze architectures

**3.1 Open MASTER_ORCHESTRATION_PROMPT.md**

Find the "Claude-Code Prompt Template" section (line ~450)

**3.2 Customize this prompt for your backend decision:**

```markdown
[FIRE] Backend Architecture Decision Analysis

PROJECT: LearnQwest
SYSTEM: 8-tier Ion agent system with ADA orchestrator, 60+ specialized agents

CONTEXT:
- Transforming YouTube content → TEKS-aligned learning materials for Texas schools
- Need persistent storage for:
  * Agent state (60+ Ions across 8 tiers)
  * Content pipeline (YouTube metadata, transcripts, generated lessons)
  * User data (teachers, students, districts)
  * TEKS mappings (Texas education standards)
  * Analytics (Tier 8: usage, feedback, performance)

BASELINE (Current State):
- No backend database currently
- Stack: Python ADK backend + Next.js frontend + Vertex AI Agent Engine
- Development: Local (127.0.0.1:8000)
- Data: Currently ephemeral (lost on restart)
- Budget constraint: < $100/month preferred for MVP
- Performance target: < 100ms query latency for content retrieval

MILESTONE (Success Criteria):
1. Select backend architecture with documented rationale
2. Cost analysis for MVP (1-10 schools) + scaling (100 schools)
3. Performance validation against requirements
4. Schema v1.0 for winning architecture
5. Implementation roadmap (quick-win 24hr vs full Phase 2)

YOUR TASK:
Analyze 3 backend architecture alternatives:

**Option 1: JSON Files (Filesystem)**
- Use Python's json module, store in app/data/
- Pros: Zero cost, simple, no external dependencies
- Cons: No concurrent access, poor query performance, scaling issues

**Option 2: PostgreSQL (Relational DB)**
- Use SQLAlchemy ORM + FastAPI integration
- Hosted: Neon.tech serverless or Supabase or Railway
- Pros: ACID guarantees, strong ecosystem, SQL familiarity
- Cons: Relational model may not fit all Ion agent relationships

**Option 3: Neo4j (Graph Database)**
- Model Ions as nodes, relationships as edges
- Hosted: Neo4j Aura
- Pros: Natural fit for agent relationships, powerful graph queries
- Cons: Higher cost, learning curve, smaller ecosystem

FOR EACH OPTION, PROVIDE:
1. **Cost Analysis:**
   - MVP (1-10 schools, ~1000 students, ~50 GB data)
   - Scaling (100 schools, ~10,000 students, ~500 GB data)
   - Breakdown: Compute, storage, bandwidth

2. **Performance Characteristics:**
   - Read latency (single record)
   - Write throughput (bulk content ingestion)
   - Query complexity (joins/graph traversals)

3. **Complexity Assessment:**
   - Development: How hard to implement?
   - Operations: How hard to maintain?
   - Integration: Ease with ADK/FastAPI?

4. **LearnQwest Fit:**
   - How well does it model 8-tier Ion system?
   - Can it handle TEKS relationship mappings?
   - Supports content pipeline workflows?

5. **Pros & Cons Table**

6. **Recommendation:** Pick a winner with clear rationale

DELIVERABLES:
1. **Architecture Decision Record** (ADR) in markdown format:
   - Title: "ADR-001: Backend Database Architecture"
   - Status: Proposed
   - Context: Why we need this decision
   - Decision: The winner
   - Consequences: Trade-offs accepted

2. **Cost Comparison Table:**
   | Architecture | MVP Cost/mo | Scale (100 schools) Cost/mo | Notes |
   |--------------|-------------|------------------------------|-------|

3. **Schema Draft** for winning architecture:
   - If SQL: Table definitions (entities, relationships, indexes)
   - If Graph: Node types, edge types, properties
   - If JSON: File structure, directory layout

4. **Implementation Roadmap:**
   - Phase 1 (24hr quick-win): Minimal viable backend
   - Phase 2 (2 weeks): Production-ready with migrations, backups
   - Phase 3 (future): Advanced features (caching, replication, etc.)

CONSTRAINTS:
- Deadline: Nov 18 (2 days from now)
- Must integrate with existing ADK backend and Next.js frontend
- Performance: < 100ms for content queries (critical user experience)
- Cost: Strong preference for < $100/month (MVP)
- Team: Solo developer (Link) with agent support (minimal ops overhead preferred)

ACCEPTANCE CRITERIA:
[ ] All 3 alternatives analyzed with cost + performance data
[ ] Winner clearly identified with rationale
[ ] Trade-offs explicitly documented (what we're giving up)
[ ] Schema draft ready for implementation
[ ] Roadmap separates quick-win from full build
[ ] ADR follows standard format
[ ] Can answer "why X not Y?" from documentation alone

[OK] Proceed with comprehensive analysis. Be thorough on cost + performance - those are decision drivers.
```

**3.3 Save this prompt** (you'll paste it to Claude-Code in Step 4)

**Why this prompt is powerful:**
- ✓ Includes full baseline context (Claude knows current state)
- ✓ Specific milestone criteria (Claude knows what success looks like)
- ✓ Explicit deliverables (no ambiguity on output format)
- ✓ Constraints front-loaded (Claude optimizes within bounds)
- ✓ Acceptance criteria (Claude can self-check)

---

### **STEP 4: Phase 5 (Code Execution) - 60-90 minutes**

**4.1 Paste prompt to Claude-Code:**

Open your Claude-Code session and paste the full prompt from Step 3.2.

**4.2 Monitor output:**

Claude-Code will:
1. Research pricing for Neon/Supabase/Railway (PostgreSQL) and Neo4j Aura
2. Estimate data volumes based on 8-tier Ion system
3. Generate cost comparison table
4. Analyze performance characteristics
5. Create Architecture Decision Record
6. Draft schema for recommended architecture
7. Build implementation roadmap

**Expected output files:**
```
docs/decisions/ADR-001-backend-architecture.md
docs/cost-analysis/backend-comparison.md
app/models/schema.py (or schema-design.md)
docs/roadmap-backend-implementation.md
```

**4.3 Review outputs:**

As Claude-Code delivers files:
- **Immediately save key excerpts to your BMAD** (Achievement section)
- Note the recommendation and rationale
- Copy the cost comparison table
- Save schema file path

**4.4 If you need code generation (Schema → SQLAlchemy models):**

Dispatch to **Aider** (better for pure code generation):
```markdown
I need you to generate SQLAlchemy ORM models from this schema.

Context:
- Project: LearnQwest (8-tier Ion agent system)
- Stack: Python ADK + FastAPI
- Database: PostgreSQL (based on architecture decision)

Schema: [paste schema from Claude-Code's output]

Requirements:
1. Use SQLAlchemy 2.0+ syntax (modern style)
2. Include all relationships (ForeignKeys, backrefs)
3. Add indexes for frequently queried fields
4. Include __repr__ methods for debugging
5. Type hints throughout
6. Docstrings for each model

Files to create:
- app/models/__init__.py
- app/models/base.py (declarative base)
- app/models/agents.py (Ion agent models)
- app/models/content.py (YouTube, lessons, etc.)
- app/models/users.py (teachers, students, districts)
- app/models/teks.py (Texas standards)

Generate tests for models:
- tests/test_models.py

Run tests after generation and fix any failures.
```

**4.5 If you need validation:**

Dispatch to **Windsurf**:
```markdown
Validate the generated SQLAlchemy models against LearnQwest requirements.

Check:
1. All 8 tiers have data representation
2. Relationships match tier diagram (LEARNQWEST_WORKFLOW.mmd)
3. No missing foreign keys
4. Indexes on high-query fields (e.g., agent_id, content_id)
5. No circular dependencies
6. Schema supports TEKS mapping (Texas standards)

Files to review:
- app/models/*.py
- Schema design doc

Report any issues or missing entities.
```

---

### **STEP 5: Phase 6 (Validation) - 20 minutes**

**5.1 Run automated checks:**
```bash
# Type checking
cd /home/user/adk-fullstack-deploy-tutorial
uv run mypy app/models/

# Linting
uv run ruff check app/models/

# Tests (if generated)
uv run pytest tests/test_models.py
```

**5.2 Manual validation checklist:**

Open your BMAD, go to "Success Criteria" in Milestone section, check off each:
```
[ ] Backend architecture selected with documented rationale
    → Check: Does ADR exist? Does it explain "why X not Y?"

[ ] Cost analysis completed
    → Check: Is there a cost table with MVP + scaling numbers?

[ ] Performance requirements validated
    → Check: Does ADR mention query latency? Meets < 100ms target?

[ ] Schema v1.0 generated
    → Check: Do schema files exist? All 8 tiers covered?

[ ] Implementation roadmap created
    → Check: Does roadmap separate 24hr quick-win from Phase 2?

[ ] Architecture Decision Record created
    → Check: Follows ADR format? Documents alternatives?
```

**5.3 Compare to baseline:**

In your BMAD, note in Achievement section:
```
Before: No database, $0/month, no schema
After: [PostgreSQL/Neo4j/JSON], $[X]/month, schema ready
```

**If validation fails:**
- Loop back to Phase 5
- Identify specific failure
- Dispatch fix to appropriate agent
- Re-run validation

---

### **STEP 6: Phase 7 (Achievement Documentation) - 20 minutes**

**6.1 Fill BMAD Achievement section:**

**Outcomes Summary:**
```
✓ Selected [DATABASE] as backend architecture
✓ Generated schema covering all 8 tiers + Ion agents
✓ Created cost analysis: $[X]/month MVP, $[Y]/month at scale
✓ Built implementation roadmap with 24hr quick-win
✓ All decisions documented with alternatives + rationale
```

**Delivered Artifacts:**
```
File                                      Status    Location
─────────────────────────────────────────────────────────────────
ADR-001-backend-architecture.md           ✓         /docs/decisions/
backend-comparison.md                     ✓         /docs/cost-analysis/
schema.py (or schema-design.md)           ✓         /app/models/ (or /docs/)
roadmap-backend-implementation.md         ✓         /docs/
Updated BMAD                              ✓         /docs/sessions/BMAD/
```

**Architecture Decisions Table:**

Example (if PostgreSQL won):
| Decision Topic | Alternatives Considered | Winner | Rationale | Trade-offs | Cost Impact |
|----------------|------------------------|--------|-----------|------------|-------------|
| Backend Database | 1. JSON files<br/>2. PostgreSQL<br/>3. Neo4j | **PostgreSQL** | - Structured data fits relational<br/>- ACID guarantees critical for content pipeline<br/>- Cost-effective: $65/mo vs $300+ Neo4j<br/>- Strong FastAPI integration<br/>- Team SQL experience | - Graph queries slower than Neo4j<br/>- More complex migrations than JSON<br/>- Need to learn SQLAlchemy patterns | **$65/month** (Neon serverless) vs $0 JSON / $300+ Neo4j |

**Agent Activity Log:**
| Agent | Tasks Assigned | Output Quality | Notes |
|-------|----------------|----------------|-------|
| Claude-Code | Architecture analysis, ADR, cost comparison | Excellent | Comprehensive analysis with all trade-offs documented. Cost data accurate (verified pricing pages). |
| Aider | Generate SQLAlchemy models from schema | Good | Fast generation, minor relationship tweaks needed |
| Windsurf | Validate schema against 8-tier requirements | Excellent | Caught 2 missing indexes, suggested cascade delete rules |

**Lessons Learned:**
- **What worked:** BMAD prevented info loss - can reconstruct decision logic
- **What worked:** Claude-Code excels at architecture + trade-off analysis
- **What didn't work:** Initial schema draft missed Tier 6 QA entities (Windsurf caught it)
- **Next time:** Involve validation agent earlier (parallel with generation)

**6.2 Update git commit messages:**

```bash
git add docs/decisions/ADR-001-backend-architecture.md docs/cost-analysis/backend-comparison.md app/models/schema.py docs/roadmap-backend-implementation.md docs/sessions/BMAD/2025-11-16-001_Backend-Architecture.md

git commit -m "$(cat <<'EOF'
[FIRE] Backend Architecture Decision - PostgreSQL Selected

Architecture Decision Record (ADR-001):
- Analyzed 3 alternatives: JSON, PostgreSQL, Neo4j
- Selected PostgreSQL for ACID guarantees, cost-effectiveness, ecosystem
- Cost: $65/month MVP, $200/month at 100 schools (within budget)
- Performance: < 20ms query latency (exceeds < 100ms requirement)

Deliverables:
✓ ADR with alternatives + rationale (docs/decisions/)
✓ Cost comparison table (docs/cost-analysis/)
✓ Schema v1.0 covering all 8 tiers (app/models/)
✓ Implementation roadmap (24hr quick-win + Phase 2)
✓ Complete BMAD session documentation

Trade-offs Accepted:
- Graph queries slower than Neo4j (acceptable for MVP)
- Migration complexity higher than JSON (mitigated by Alembic)

Agents Used: Claude-Code (analysis), Aider (code gen), Windsurf (validation)
Session: 2025-11-16-001
Status: MILESTONE ACHIEVED

[OK] Backend architecture locked. Ready for implementation Phase 2.
EOF
)"
```

**6.3 Push to remote:**
```bash
git push -u origin claude/whats-tak-01MqDzJ3yijbdtPaQf6sifus
```

---

### **STEP 7: Phase 8 (Mermaid Update) - 10 minutes**

**7.1 Open WORKFLOW_MERMAID_TEMPLATE.mmd**

**7.2 Find the "APPENDABLE SESSION HISTORY" section** (near bottom)

**7.3 Add your session node:**

```mermaid
Session_2025_11_16_001["Session: Backend Architecture<br/>Decision: PostgreSQL ($65/mo)<br/>Agents: Claude-Code, Aider, Windsurf<br/>Status: Complete"]
```

**7.4 Connect to previous session (if any):**

```mermaid
%% If this is your first session with this system, connect to the last workflow commit:
Session_Initial["Initial: LearnQwest 8-Tier Architecture<br/>Deliverable: LEARNQWEST_WORKFLOW.mmd<br/>Status: Complete"]
Session_Initial --> Session_2025_11_16_001

%% For subsequent sessions, connect to previous:
%% Session_2025_11_15_001 --> Session_2025_11_16_001
```

**7.5 Update changelog at top of file:**

```mermaid
%% ============================================================================
%% CHANGELOG:
%% 2025-11-16-002: Session 2025-11-16-001 added - Backend architecture decision (PostgreSQL)
%% 2025-11-16-001: Initial 8-phase workflow template with appendable history
%% ============================================================================
```

**7.6 Save and commit:**
```bash
git add WORKFLOW_MERMAID_TEMPLATE.mmd
git commit -m "[OK] Update workflow diagram - Backend architecture session complete"
git push
```

**7.7 View your updated diagram:**
- Option 1: Push to GitHub, view the .mmd file (auto-renders)
- Option 2: Open https://mermaid.live and paste contents
- Option 3: VS Code with Mermaid extension

---

### **STEP 8: Session Complete! 🎯**

**What you accomplished in 2-3 hours:**

✅ **Architecture Decision Made**
- Chose PostgreSQL (or Neo4j or JSON - based on your context)
- Documented with full rationale (cost, performance, trade-offs)
- Can answer "why X not Y?" forever (it's in the ADR)

✅ **Schema Generated**
- Covers all 8 tiers of Ion system
- Ready for implementation
- Validated against requirements

✅ **Cost Analysis Complete**
- MVP and scaling costs documented
- Within budget constraints
- Comparison table for stakeholders

✅ **Implementation Roadmap Ready**
- 24-hour quick-win path identified
- Phase 2 full build planned
- No more "what's next?" uncertainty

✅ **Zero Information Loss**
- Complete BMAD archived
- All decisions documented
- Architecture Decision Record explains everything
- Mermaid diagram shows this session in history
- Git commits have rich context

**Next session pickup time:** < 5 minutes
- Read the BMAD (2 min)
- Check Mermaid for context (1 min)
- Review git commits (2 min)
- Start working!

---

## 🎓 HOW THE SYSTEM PREVENTS INFORMATION LOSS

**Old Way (Before BMAD):**
```
Session 1: Decide on PostgreSQL [rationale in your head]
[2 days pass]
Session 2: "Wait, why PostgreSQL? Was it cost or performance?"
[Spend 2 hours re-researching]
[Possibly make different decision - system diverges]
```

**New Way (With BMAD):**
```
Session 1:
- Fill BMAD Baseline (current state)
- Fill BMAD Milestone (target state)
- Do the work
- Fill BMAD Achievement with Architecture Decisions table:
  | Decision | Alternatives | Winner | Rationale | Trade-offs | Cost |
  | Database | JSON, SQL, Neo4j | PostgreSQL | [reasons] | [what we lose] | $65 |
- Archive BMAD to docs/sessions/BMAD/
- Update Mermaid diagram

[2 days pass]

Session 2:
- Open previous BMAD (2 min read)
- See decision table: "PostgreSQL because: $65/mo vs $300 Neo4j, <20ms latency, ACID guarantees"
- See schema file path
- See roadmap for next steps
- Continue immediately (zero time lost)
```

**The Magic:** BMAD captures **alternatives considered** + **rationale** + **trade-offs**, not just the decision.

This means:
- ✓ Future you knows why past you decided X
- ✓ You can explain decisions to stakeholders
- ✓ You don't repeat analysis unnecessarily
- ✓ System stays consistent over time

---

## 🔧 AGENT SELECTION STRATEGY (When to Use Which)

### **Claude-Code**
**Best for:**
- Architecture decisions (like backend choice)
- Multi-file refactoring
- Complex git operations
- System design analysis
- Trade-off documentation

**Example prompt pattern:**
```markdown
[FIRE] [Task name]

CONTEXT: [Project + current state]
BASELINE: [Where we are]
MILESTONE: [Where we want to be]
YOUR TASK: [Specific deliverable]
CONSTRAINTS: [Time/budget/tech limits]
DELIVERABLES: [Numbered list]
ACCEPTANCE CRITERIA: [Checklist]

[OK] Proceed.
```

**When NOT to use:**
- Simple single-file edits (use Cline)
- Pure code generation from spec (use Aider)

---

### **Aider**
**Best for:**
- Generating new code from specifications
- Writing tests
- Refactoring existing code
- Implementing features from design docs

**Example prompt pattern:**
```markdown
Generate [WHAT] for [PROJECT].

Context:
- [Brief project description]
- [Related files]

Requirements:
1. [Requirement 1]
2. [Requirement 2]

Files to create/modify:
- [path/to/file.py]

Tests required:
- [test scenario 1]
- [test scenario 2]

Run tests and fix failures.
```

**When NOT to use:**
- Architecture decisions (use Claude-Code)
- Quick typo fixes (use Cline)

---

### **Cline**
**Best for:**
- Quick single-file edits
- Typo fixes
- Small refactors
- Interactive iteration

**Example prompt pattern:**
```markdown
Quick edit in [FILE_PATH]:

Change: [SPECIFIC_CHANGE]
Location: [LINE_NUMBERS or FUNCTION_NAME]
Reason: [WHY]

Verify [RELATED_FUNCTIONALITY] still works.
```

**When NOT to use:**
- Multi-file changes (use Claude-Code or Aider)
- New feature implementation (use Aider)

---

### **Windsurf**
**Best for:**
- Code validation
- Review against requirements
- Checking for missed edge cases

**Example prompt pattern:**
```markdown
Validate [COMPONENT] against [REQUIREMENTS].

Check:
1. [Criterion 1]
2. [Criterion 2]

Files to review:
- [path/to/file]

Report issues and suggest fixes.
```

**When NOT to use:**
- Implementing features (use Aider or Claude-Code)

---

### **Parser-Ion** (Custom LearnQwest Agent)
**Best for:**
- TEKS standards processing
- YouTube metadata parsing
- Content transformation pipeline
- Domain-specific data handling

**Example prompt pattern:**
```markdown
Parse [DATA_SOURCE] for [PROJECT].

Input: [Format/location]
Output: [Desired format]
Validation: [TEKS compliance rules]

Process and report stats.
```

---

## 🎯 PRO TIPS FOR LINK'S WORKFLOW

### **Tip 1: Fill BMAD DURING Session, Not After**
```
❌ Wrong: Code for 3 hours, try to remember what happened, fill BMAD
✓ Right: Fill Baseline (5 min) → Fill Milestone (5 min) → Code → Update Achievement as you go
```

**Why:** Your memory is fallible. Decisions made at 10 AM are fuzzy by 3 PM. Capture them live.

---

### **Tip 2: Use [FIRE]/[OK] Markers in Git Commits**
```
[FIRE] = Major milestone, significant change
[OK] = Completed task, incremental progress

Example:
[FIRE] Backend Architecture Decision - PostgreSQL Selected
[OK] Add database connection utility
[OK] Update README with setup instructions
```

**Why:** Makes git log readable at a glance. [FIRE] commits are your milestone markers.

---

### **Tip 3: Parallel Agent Dispatch for Independent Tasks**
```
Sequential (slow):
1. Claude-Code: Architecture decision (60 min)
2. Wait for Claude-Code to finish
3. Aider: Generate schema (30 min)
Total: 90 min

Parallel (fast):
1. Claude-Code: Cost analysis (30 min) | Aider: Generate mock schema (30 min)
2. Synthesize results
Total: 30 min + 10 min = 40 min
```

**When to parallelize:**
- Tasks are independent (one doesn't need other's output)
- Agents are different (not competing for same resources)

**When to sequence:**
- Task B needs output of Task A (schema needs architecture decision first)

---

### **Tip 4: Archive BMADs, Never Delete**
```
Structure:
docs/sessions/BMAD/
├── 2025-11-16-001_Backend-Architecture.md
├── 2025-11-17-001_Schema-Implementation.md
├── 2025-11-18-001_API-Endpoints.md
└── TEMPLATE.md
```

**Why:** Your BMAD collection becomes a searchable knowledge base. "How did we solve X?" → grep the archive.

---

### **Tip 5: Update Mermaid BEFORE Closing Session**
```
Phase 8 is not optional - it's the memory anchor for future sessions.

Without it: Sessions feel disconnected, you lose the narrative
With it: Clear progression, can see the journey
```

**Habit to build:** No session complete until Mermaid updated + pushed.

---

### **Tip 6: Start Each Session with Previous BMAD**
```
Session Start Ritual (10 min):
1. Read last BMAD (5 min)
   - Baseline → Milestone → Achievement → Handoff Notes
2. Check Mermaid for session context (2 min)
3. Review git commits since last session (3 min)
4. Create new BMAD, reference previous in "Related BMADs"

Total: 10 min vs 2 hours of "what was I doing?"
```

---

### **Tip 7: Use Architecture Decisions Table Religiously**
```
Every time you choose X over Y:
| Decision | Alternatives | Winner | Rationale | Trade-offs | Cost |

This ONE table prevents 90% of information loss questions.
```

---

## 📅 YOUR NEXT 5 SESSIONS (Post-Backend Decision)

Assuming PostgreSQL was chosen (adjust if different):

### **Session 2: Schema Implementation (Nov 17)**
```
GOAL: Implement database schema and migrations
AGENTS: Aider (code gen), Windsurf (validation)
DELIVERABLES:
- SQLAlchemy models in app/models/
- Alembic migration scripts
- Database connection utility
- Basic CRUD operations
- Tests for models
TIME: 3-4 hours
```

**Quick-start:**
1. Create BMAD: `docs/sessions/BMAD/2025-11-17-001_Schema-Implementation.md`
2. Baseline: "Schema designed, not implemented"
3. Milestone: "Schema live in local database, tests passing"
4. Dispatch Aider with schema file from Session 1
5. Validate with Windsurf
6. Update BMAD + Mermaid

---

### **Session 3: FastAPI Endpoints (Nov 17-18)**
```
GOAL: Build RESTful API endpoints for core entities
AGENTS: Aider (endpoint gen), Claude-Code (design review)
DELIVERABLES:
- FastAPI routes in app/api/routes/
- Request/response models (Pydantic)
- Basic auth middleware
- Endpoint tests
- API documentation (auto-generated)
TIME: 4-5 hours
```

---

### **Session 4: Tier 2 Integration (Nov 18+)**
```
GOAL: Connect YouTube ingestion pipeline to database
AGENTS: Claude-Code (integration), Parser-Ion (data processing)
DELIVERABLES:
- Ion-YouTube-Collector stores to DB
- Ion-Transcript-Extractor retrieves + updates
- Pipeline workflow working end-to-end
TIME: 5-6 hours
```

---

### **Session 5: Deployment to Staging (Nov 19+)**
```
GOAL: Deploy backend + database to cloud (Neon + Cloud Run)
AGENTS: Claude-Code (deployment)
DELIVERABLES:
- Database hosted on Neon
- Backend on Cloud Run
- Environment configs
- Health checks working
TIME: 3-4 hours
```

---

### **Session 6: Tier 3-8 Expansion (Phase 2)**
```
GOAL: Extend schema for all remaining tiers
AGENTS: Aider (code gen), Windsurf (validation)
DELIVERABLES:
- TEKS mapping tables
- Content generation entity storage
- QA workflow data models
- Analytics tables
TIME: 6-8 hours
```

---

## 🚨 TROUBLESHOOTING

### **Problem: "My BMAD is too long to fill"**
**Solution:** You're over-documenting. Baseline + Milestone should each be 5-10 minutes MAX. Use bullets, not essays.

---

### **Problem: "Agent outputs don't match expectations"**
**Solution:** Your Phase 4 prompts aren't specific enough. Go back to MASTER_ORCHESTRATION_PROMPT.md and use the templates. Include:
- Context (where we are)
- Baseline (current state)
- Milestone (target state)
- Deliverables (specific files/formats)
- Constraints (time/budget/tech)
- Acceptance criteria (checkboxes)

---

### **Problem: "Phase 6 validation keeps failing"**
**Solution:** Loop back to Phase 5. Don't try to push through. Fix the code, re-run validation. Use Windsurf to identify specific failures.

---

### **Problem: "I forgot to update BMAD during session"**
**Solution:** Reconstruct from:
1. Git commits (what changed)
2. Agent conversation logs (decisions made)
3. Files created (deliverables)

Use this as a lesson: Set a timer every 30 min to update BMAD incrementally.

---

### **Problem: "Mermaid diagram is getting too complex"**
**Solution:** Create sub-diagrams:
```
master_workflow.mmd (high-level phases)
├── tier1_sessions.mmd (Tier 1 orchestration work)
├── tier2_sessions.mmd (Tier 2 ingestion work)
└── infrastructure_sessions.mmd (Deployment, DevOps)
```

Link them in master: "See tier1_sessions.mmd for details"

---

### **Problem: "Can't decide which agent to use"**
**Solution:** Default to Claude-Code for complex/multi-file work. Use Aider for pure code generation. Use Cline for quick edits.

When in doubt: Claude-Code.

---

## 📚 ADDITIONAL RESOURCES

### **LearnQwest Project Files:**
```
/LEARNQWEST_WORKFLOW.mmd          - 8-tier architecture map
/LEARNQWEST_TRACKER_NOTES.md      - Improvement tips for workflow diagram
/QUICKSTART_LEARNQWEST.md         - Quick start guide
/tools/workflow_updater.py        - Programmatic Mermaid updater
```

### **System Files (This Session):**
```
/MASTER_ORCHESTRATION_PROMPT.md           - 8-phase workflow system
/WORKFLOW_MERMAID_TEMPLATE.mmd            - Visual workflow template
/BMAD_TEMPLATE_LEARNQWEST.md              - Session documentation template
/LEARNQWEST_PRODUCTION_LAUNCH_GUIDE.md    - This file
```

### **External Resources:**
```
TEKS Standards:            https://tea.texas.gov/academics/curriculum-standards
PostgreSQL Docs:           https://www.postgresql.org/docs/
SQLAlchemy:                https://docs.sqlalchemy.org/
FastAPI:                   https://fastapi.tiangolo.com/
Neon (Serverless SQL):     https://neon.tech/
Neo4j:                     https://neo4j.com/
Mermaid Live Editor:       https://mermaid.live/
```

---

## ✅ FINAL CHECKLIST

Before starting your first session with this system:

```
[ ] Read this guide (LEARNQWEST_PRODUCTION_LAUNCH_GUIDE.md)
[ ] Skim MASTER_ORCHESTRATION_PROMPT.md (understand 8 phases)
[ ] Open BMAD_TEMPLATE_LEARNQWEST.md (see structure)
[ ] View WORKFLOW_MERMAID_TEMPLATE.mmd on Mermaid Live Editor
[ ] Create directory structure (docs/sessions/BMAD/, docs/decisions/, docs/cost-analysis/)
[ ] Copy BMAD template for Session 1
[ ] Fill BMAD Baseline (5 min)
[ ] Fill BMAD Milestone (5 min)
[ ] Generate agent prompt using templates
[ ] Paste to Claude-Code
[ ] Update BMAD Achievement as you work
[ ] Commit with [FIRE]/[OK] markers
[ ] Update Mermaid diagram
[ ] Archive BMAD
[ ] Push to git
```

---

## 🎯 SUCCESS METRICS

**You're using this system correctly if:**

- [ ] Can pick up any session in < 10 min (read BMAD + Mermaid)
- [ ] Never ask "why did we decide X?" (it's in Architecture Decisions table)
- [ ] Agents deliver on first try (prompts are context-rich)
- [ ] Git log tells a story ([FIRE] markers show milestones)
- [ ] Mermaid diagram shows session-to-session flow
- [ ] Spend more time building than reconstructing

**You need to adjust if:**

- [ ] Still losing information between sessions → Fill BMAD during, not after
- [ ] Agent outputs are off-target → Use prompt templates from MASTER_ORCHESTRATION_PROMPT.md
- [ ] Can't remember what happened 2 sessions ago → Update Mermaid in Phase 8
- [ ] Re-analyzing same decisions → Document alternatives + rationale in BMAD
- [ ] Sessions feel chaotic → Follow 8-phase workflow strictly

---

## 🚀 READY TO LAUNCH?

**Your next 2 hours (Backend Architecture Session):**

1. **[10 min]** Setup: Create directories, copy BMAD template
2. **[15 min]** Phase 1-3: Fill BMAD Baseline + Milestone
3. **[10 min]** Phase 4: Generate Claude-Code prompt
4. **[60 min]** Phase 5: Paste to Claude-Code, monitor output
5. **[20 min]** Phase 6: Validate outputs
6. **[20 min]** Phase 7: Fill BMAD Achievement, commit
7. **[10 min]** Phase 8: Update Mermaid, push

**Total: 2 hours 25 minutes**

**Outcome:**
✅ Backend architecture decided
✅ Schema ready
✅ Cost analysis complete
✅ Implementation roadmap built
✅ Zero information loss
✅ Ready for Session 2 (implementation)

---

**[FIRE] System deployed. Templates ready. Nov 18 deadline achievable. Let's build LearnQwest! 🚀**

**[OK] Questions? Blockers? Paste this into Claude-Code:**
```
I just read LEARNQWEST_PRODUCTION_LAUNCH_GUIDE.md and I'm ready to start Session 1 (Backend Architecture Decision).

I have a question about: [YOUR_QUESTION]

OR

I'm stuck on: [BLOCKER]

Help me unblock so I can proceed with the 8-phase workflow.
```

---

**Version:** 1.0.0
**Last Updated:** 2025-11-16
**Maintainer:** Team LINK Digital Self Partnership
**Status:** Production-Ready
