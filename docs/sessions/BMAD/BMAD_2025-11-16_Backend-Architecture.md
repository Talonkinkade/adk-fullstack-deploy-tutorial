# BMAD Session: [Session Name]
**Date:** YYYY-MM-DD
**Duration:** [Actual time spent]
**Primary Agent:** [Claude-Code / Aider / Windsurf / Cline]
**Status:** [In Progress / Completed / Blocked]
**Session ID:** [Unique identifier]

---

## 📋 QUICK REFERENCE

| Attribute | Value |
|-----------|-------|
| **Project** | LearnQwest Education Platform |
| **Tech Stack** | Next.js 15, Python ADK, Vertex AI, PostgreSQL |
| **Context** | 60 learning objectives (Ions), TEKS alignment, Texas schools |
| **Budget** | $200/month operational |
| **Deadline** | 2025-11-18 (Nov 18) |
| **Team** | Solo developer, no DBA |

---

## B - BASELINE (Current State Snapshot)

### Repository State
- **Branch:** [Branch name, e.g., `main` or `feature/backend-architecture`]
- **Last Commit:** [Commit hash + message, e.g., `abc1234 - docs: update README`]
- **Git Status:**
  ```bash
  # Modified Files
  [List files with git status output]

  # Untracked Files
  [List untracked files]
  ```
- **Current Test Status:**
  - Unit Tests: [X passed / Y total]
  - Integration Tests: [X passed / Y total]
  - Test Coverage: [X%]

### Current Functionality
> Describe what exists NOW, before this session begins. Be specific.

**Example for Backend Architecture Decision:**
- No backend database implemented yet (greenfield)
- Frontend exists but mocked data only
- No persistent storage for:
  - Learning objectives (60 Ions)
  - Student progress tracking
  - TEKS standard mappings
- API routes exist but return static JSON

**Your Session:**
[Fill in current state for YOUR session]

---

### Current Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Build Time | [X seconds] | `npm run build` |
| Test Coverage | [X%] | `npm test -- --coverage` |
| Bundle Size (Frontend) | [X MB] | `.next/` output |
| Backend Response Time | [X ms] | Average API latency |
| Database Size | [X MB / N/A] | Current data volume |
| Monthly Cost | $[X] | Current infrastructure |

**Example:**
| Metric | Value | Notes |
|--------|-------|-------|
| Build Time | 45s | Next.js build |
| Test Coverage | 0% | No backend tests yet |
| Bundle Size | 2.1 MB | Frontend only |
| Backend Response Time | N/A | No backend yet |
| Database Size | N/A | No database yet |
| Monthly Cost | $0 | Local dev only |

---

### Known Issues (Before This Session)
- [ ] Issue 1: [Description, e.g., "No persistent storage - data lost on refresh"]
- [ ] Issue 2: [Description]
- [ ] Issue 3: [Description]

**Example:**
- [ ] No persistent storage for learning objectives
- [ ] API endpoints return mock data
- [ ] No student progress tracking
- [ ] TEKS alignment data is hardcoded

---

### Files to Modify/Create

```bash
# Expected file changes for this session
# Mark [MODIFY] for existing files, [CREATE] for new files

[MODIFY] app/config.py
[CREATE] app/database/schema.py
[CREATE] app/database/migrations/001_initial_schema.sql
[MODIFY] nextjs/src/app/api/goals/route.ts
[CREATE] tests/test_database.py
```

**Your Session:**
```bash
[Fill in files you expect to change]
```

---

## M - MILESTONE (Success Criteria)

### Goal
> Single-sentence description of what "done" looks like for THIS session.

**Example:**
> Choose backend architecture (PostgreSQL vs Neo4j vs JSON), generate schema draft, and document decision rationale with cost/performance analysis.

**Your Session:**
[Fill in your goal]

---

### Success Criteria (Measurable)

Mark each criterion as you complete it:

1. ✅ **Criterion 1:** [Specific, testable criterion]
   - **How to verify:** [Test command or observation]
   - **Example:** Database choice documented with cost comparison table
   - **Status:** [PASS / FAIL / IN PROGRESS]

2. ✅ **Criterion 2:** [Specific, testable criterion]
   - **How to verify:** [Test command or observation]
   - **Example:** Schema draft created and validates against sample data
   - **Status:** [PASS / FAIL / IN PROGRESS]

3. ✅ **Criterion 3:** [Specific, testable criterion]
   - **How to verify:** [Test command or observation]
   - **Example:** Implementation roadmap fits 2-day deadline
   - **Status:** [PASS / FAIL / IN PROGRESS]

---

### Acceptance Tests

**Before marking this session COMPLETE, these tests must pass:**

- [ ] **Test 1:** [Specific test case]
  - **Command:** `[How to run this test]`
  - **Expected Result:** [What "pass" looks like]

- [ ] **Test 2:** [Specific test case]
  - **Command:** `[How to run this test]`
  - **Expected Result:** [What "pass" looks like]

- [ ] **Test 3:** [Specific test case]
  - **Command:** `[How to run this test]`
  - **Expected Result:** [What "pass" looks like]

**Example:**
- [ ] **Schema Migration:** Database tables created successfully
  - **Command:** `python -m app.database.migrate`
  - **Expected Result:** All tables exist, no errors

- [ ] **Sample Data:** Seed data loads without errors
  - **Command:** `python -m app.database.seed`
  - **Expected Result:** 60 Ions inserted, TEKS mappings present

---

### In Scope (What WILL be done this session)

- [x] [Task 1]
- [x] [Task 2]
- [x] [Task 3]

**Example:**
- [x] Evaluate 3 backend options (PostgreSQL, Neo4j, JSON)
- [x] Create cost/performance comparison table
- [x] Generate schema draft for chosen option
- [x] Document decision rationale

---

### Out of Scope (Deferred to Phase 2)

> List what you're explicitly NOT doing in this session. This prevents scope creep.

- [ ] [Deferred task 1] - **Reason:** [Why deferred]
- [ ] [Deferred task 2] - **Reason:** [Why deferred]

**Example:**
- [ ] Full ORM implementation - **Reason:** Schema design first, code later
- [ ] API endpoint refactoring - **Reason:** Focus on architecture decision only
- [ ] Authentication/authorization - **Reason:** Backend architecture is prerequisite

---

### Definition of Done

**Check ALL boxes before closing this session:**

- [ ] ✅ Code written and reviewed
- [ ] ✅ Tests passing (unit + integration)
- [ ] ✅ Documentation updated (README, API docs, etc.)
- [ ] ✅ BMAD session completed (all sections filled)
- [ ] ✅ Mermaid diagram updated with this session
- [ ] ✅ Changes committed to git with clear messages
- [ ] ✅ No regressions (existing tests still pass)
- [ ] ✅ Success criteria met (see above)

---

## A - ARCHITECTURE DECISIONS

### Decision Summary Table

| Decision | Options Considered | Choice | Rationale | Trade-offs | Impact | Date |
|----------|-------------------|--------|-----------|------------|--------|------|
| [Decision 1] | [Option A, B, C] | [Chosen] | [Why this choice] | [Pros/Cons] | [Scope of change] | YYYY-MM-DD |
| [Decision 2] | [Option A, B, C] | [Chosen] | [Why this choice] | [Pros/Cons] | [Scope of change] | YYYY-MM-DD |

**Example:**
| Decision | Options Considered | Choice | Rationale | Trade-offs | Impact | Date |
|----------|-------------------|--------|-----------|------------|--------|------|
| Backend Database | JSON files, PostgreSQL, Neo4j | **PostgreSQL** | Cost ($50-100/mo vs Neo4j $300+), <20ms latency, team familiarity with SQL | Limited graph queries compared to Neo4j, but good enough for MVP | Core infrastructure decision | 2025-11-16 |
| ORM Framework | SQLAlchemy, Django ORM, Raw SQL | **SQLAlchemy** | Type safety, migration support, works with FastAPI | Slightly slower than raw SQL, learning curve | Backend data layer | 2025-11-16 |

---

### Decision Deep-Dive

For each major decision, provide full analysis:

---

#### Decision 1: [Decision Name, e.g., "Backend Database Choice"]

**Problem Statement:**
> What problem does this decision solve?

**Example:**
> LearnQwest needs persistent storage for 60 learning objectives (Ions), student progress tracking, and TEKS alignment queries. Must support relational queries, fit $200/mo budget, and deploy in 2 days.

**Your Session:**
[Fill in your problem statement]

---

**Options Evaluated:**

##### Option A: [Name, e.g., "JSON Files on Disk"]
- **Pros:**
  - [Pro 1, e.g., "Zero cost"]
  - [Pro 2, e.g., "No setup required"]
  - [Pro 3, e.g., "Simple deployment"]

- **Cons:**
  - [Con 1, e.g., "No relational queries"]
  - [Con 2, e.g., "Poor concurrency"]
  - [Con 3, e.g., "No transactions"]

- **Cost Estimate:**
  - Setup: $[X]
  - Monthly: $[X]
  - **Total Year 1:** $[X]

- **Performance Estimate:**
  - Read latency: [X ms]
  - Write latency: [X ms]
  - Concurrent users: [X]

- **Complexity:** [Low / Medium / High]

- **Risk Assessment:**
  - [Risk 1]
  - [Risk 2]

---

##### Option B: [Name, e.g., "PostgreSQL (Cloud SQL)"]
- **Pros:**
  - [Pro 1]
  - [Pro 2]

- **Cons:**
  - [Con 1]
  - [Con 2]

- **Cost Estimate:**
  - Setup: $[X]
  - Monthly: $[X]
  - **Total Year 1:** $[X]

- **Performance Estimate:**
  - Read latency: [X ms]
  - Write latency: [X ms]
  - Concurrent users: [X]

- **Complexity:** [Low / Medium / High]

- **Risk Assessment:**
  - [Risk 1]
  - [Risk 2]

---

##### Option C: [Name, e.g., "Neo4j Graph Database"]
- **Pros:**
  - [Pro 1]
  - [Pro 2]

- **Cons:**
  - [Con 1]
  - [Con 2]

- **Cost Estimate:**
  - Setup: $[X]
  - Monthly: $[X]
  - **Total Year 1:** $[X]

- **Performance Estimate:**
  - Read latency: [X ms]
  - Write latency: [X ms]
  - Concurrent users: [X]

- **Complexity:** [Low / Medium / High]

- **Risk Assessment:**
  - [Risk 1]
  - [Risk 2]

---

**Winner:** [Chosen Option]

**Rationale:**
> Detailed explanation of WHY this choice was made. Include data, metrics, and reasoning.

**Example:**
> PostgreSQL was chosen because:
> 1. **Cost:** $50-100/month (Cloud SQL db-f1-micro) vs Neo4j $300+/month
> 2. **Performance:** <20ms query latency for expected load (100 students)
> 3. **Team Familiarity:** Team knows SQL, no Neo4j experience
> 4. **Timeline:** Can deploy in 2 days with SQLAlchemy migrations
> 5. **Relational Fit:** 70% of queries are relational (student→progress→ions), not graph traversals
> 6. **Vendor Lock-in:** PostgreSQL is portable (can move to AWS RDS, self-hosted, etc.)

**Your Session:**
[Fill in your rationale]

---

**Reversibility:**
> Can we change this decision later? How hard would it be?

**Example:**
> **Reversibility: Medium**
> - Switching to Neo4j later: Would require rewriting ORM models and queries. Estimated 40-60 hours.
> - Mitigation: Keep data access layer abstracted behind repository pattern.
> - We can revisit if graph query needs become critical (e.g., complex prerequisite chains).

**Your Session:**
[Fill in reversibility analysis]

---

**Phase 2 Considerations:**
> What future work does this decision enable or constrain?

**Example:**
> - **Enables:** Full-text search (PostgreSQL has built-in support)
> - **Enables:** Geospatial queries for school district boundaries
> - **Constrains:** Complex graph queries (would need to add Neo4j as secondary store or use recursive CTEs)
> - **Next Steps:** Implement caching layer (Redis) if query latency exceeds 50ms

**Your Session:**
[Fill in Phase 2 implications]

---

## D - DOCUMENTATION (Implementation Details)

### Agent Dispatch

#### Phase 4: Agent Assignment

| Agent | Task | Input | Output | Duration |
|-------|------|-------|--------|----------|
| [Agent Name] | [Task description] | [What agent receives] | [What agent produces] | [Time spent] |

**Example:**
| Agent | Task | Input | Output | Duration |
|-------|------|-------|--------|----------|
| Claude-Code | Context analysis + architecture comparison | User request + project context | Decision table + rationale | 30 min |
| Aider | PostgreSQL schema generation | Architecture decision + requirements | SQLAlchemy models + migrations | 1.5 hrs |
| Windsurf | Test schema + validate migration | Schema files + seed data | Test results + validation report | 30 min |
| Claude-Code | BMAD documentation + Mermaid update | All session artifacts | Complete BMAD + updated workflow | 20 min |

---

#### Agent Prompts (Full Text)

**Claude-Code Prompt (Phase 1: Context Gathering):**
```markdown
[Paste the EXACT prompt used for Claude-Code here]

Example:
---
# Claude-Code Session: Backend Architecture Decision

## Your Role
You are analyzing backend database options for LearnQwest.

## Context
- Project: Educational platform with 60 learning objectives (Ions)
- Users: Texas school districts, ~100-500 students per district
- Queries: Student progress tracking, TEKS alignment lookups, prerequisite chains
- Budget: $200/month total infrastructure
- Timeline: Nov 18 deadline (2 days)
- Team: Solo developer, no DBA

## Task
Evaluate 3 options: JSON files, PostgreSQL, Neo4j

## Output Format
1. Cost comparison table (setup + monthly + year 1)
2. Performance estimates (latency, concurrent users)
3. Recommendation with detailed rationale
4. Risk assessment for each option

## Handoff
Pass recommendation to Aider for schema generation
---
```

**Your Session:**
```markdown
[Fill in your Claude-Code prompt]
```

---

**Aider Prompt (Phase 5: Code Generation):**
```markdown
[Paste the EXACT prompt used for Aider here]

Example:
---
# Aider Task: Generate PostgreSQL Schema

## Context
Project: LearnQwest
Decision: PostgreSQL with SQLAlchemy ORM
Files: Create `app/database/schema.py`, `app/database/migrations/001_initial.sql`

## Requirements
Tables needed:
- `ions` (60 learning objectives)
  - id (UUID primary key)
  - title (text)
  - description (text)
  - teks_standard (text, foreign key to `teks` table)
  - created_at, updated_at (timestamps)

- `students`
  - id (UUID primary key)
  - name (text)
  - school_district (text)
  - grade_level (integer)
  - created_at, updated_at

- `student_progress`
  - id (UUID primary key)
  - student_id (foreign key to `students`)
  - ion_id (foreign key to `ions`)
  - status (enum: 'not_started', 'in_progress', 'completed')
  - score (integer, nullable)
  - started_at, completed_at (timestamps, nullable)

- `teks_standards`
  - id (UUID primary key)
  - code (text, unique, e.g., "5.3A")
  - description (text)
  - grade_level (integer)

## Implementation Instructions
1. Use SQLAlchemy ORM with declarative base
2. Add indexes for common queries:
   - `student_progress(student_id, ion_id)` (composite)
   - `ions(teks_standard)`
   - `teks_standards(grade_level)`
3. Include `created_at`, `updated_at` timestamps on all tables
4. Use UUIDs for all primary keys
5. Add foreign key constraints with `ON DELETE CASCADE` where appropriate

## Testing
Generate seed data:
- 60 Ions (full set)
- 10 sample students
- 100 progress records

## Commit Message Format
"feat: add PostgreSQL schema with SQLAlchemy models"
---
```

**Your Session:**
```markdown
[Fill in your Aider prompt]
```

---

**Windsurf Prompt (Phase 6: Validation):**
```markdown
[Paste the EXACT prompt used for Windsurf here]
```

---

### Implementation Summary

#### Files Changed

```bash
# List all files modified/created with line count changes

# Modified
app/config.py                          (+45, -12)
nextjs/src/app/api/goals/route.ts      (+67, -23)

# Created
app/database/__init__.py               (+5, -0)
app/database/schema.py                 (+234, -0)
app/database/migrations/001_initial.sql (+156, -0)
tests/test_database.py                 (+89, -0)
docs/sessions/BMAD/BMAD_2025-11-16.md  (+500, -0)

# Total
+1051 lines added, -35 lines removed
```

**Your Session:**
```bash
[Fill in your file changes]
```

---

#### New APIs

**List any new API endpoints, their contracts, and examples:**

**Endpoint:** `POST /api/v1/goals`
```typescript
// Request
{
  userId: string;          // UUID of student
  goalText: string;        // Natural language goal
  deadline?: string;       // ISO 8601 date
}

// Response (200 OK)
{
  goalId: string;          // UUID of created goal
  planSteps: string[];     // Array of plan steps
  estimatedDuration: number; // Minutes
  relatedIons: {           // Matching learning objectives
    ionId: string;
    title: string;
    relevanceScore: number; // 0-1
  }[];
}

// Error Response (400)
{
  error: string;
  details?: string;
}
```

**Example Request:**
```bash
curl -X POST http://localhost:3000/api/v1/goals \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "goalText": "Learn multiplication tables",
    "deadline": "2025-12-01T00:00:00Z"
  }'
```

**Your Session:**
[Fill in your APIs]

---

#### New Components (Frontend)

**Component:** `GoalPlanningForm`
```typescript
// Props
interface GoalPlanningFormProps {
  onSubmit: (goal: Goal) => void;
  initialValue?: string;
  userId: string;
}

// Usage
<GoalPlanningForm
  userId={currentUser.id}
  onSubmit={(goal) => console.log('Goal created:', goal)}
  initialValue="Learn fractions"
/>
```

**Your Session:**
[Fill in your components]

---

#### Database Changes

**Migration:** `001_initial_schema.sql`
```sql
-- Full SQL migration script

CREATE TABLE ions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT,
  teks_standard TEXT REFERENCES teks_standards(code),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE students (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  school_district TEXT,
  grade_level INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_ions_teks ON ions(teks_standard);
CREATE INDEX idx_students_grade ON students(grade_level);
```

**Your Session:**
[Fill in your migrations]

---

### Validation Results

#### Test Execution

```bash
# Paste full test output

$ npm test
PASS  tests/database.test.ts
  ✓ Schema migration creates all tables (123ms)
  ✓ Seed data inserts 60 Ions (89ms)
  ✓ Foreign keys enforce constraints (45ms)
  ✓ Indexes improve query performance (67ms)

$ pytest tests/test_database.py
============================= test session starts ==============================
collected 12 items

tests/test_database.py ............                                      [100%]

============================== 12 passed in 2.34s ==============================
```

**Your Session:**
[Fill in your test results]

---

#### Milestone Verification

> Go back to your Success Criteria in the Milestone section and verify each one.

- [x] ✅ **Criterion 1:** Database choice documented with cost comparison
  - **Evidence:** Architecture Decisions table completed with 3 options evaluated
  - **Status:** PASS

- [x] ✅ **Criterion 2:** Schema draft created and validates
  - **Evidence:** `001_initial_schema.sql` migrates successfully, all tables created
  - **Status:** PASS

- [x] ✅ **Criterion 3:** Implementation roadmap fits 2-day deadline
  - **Evidence:** Roadmap shows 16 hours of work, fits within deadline
  - **Status:** PASS

---

#### Quality Metrics

| Metric | Baseline | Current | Change | Status |
|--------|----------|---------|--------|--------|
| Test Coverage | 0% | 87% | +87% | ✅ IMPROVED |
| Build Time | 45s | 47s | +2s | ⚠️ ACCEPTABLE |
| Bundle Size | 2.1 MB | 2.3 MB | +0.2 MB | ⚠️ ACCEPTABLE |
| Linting Errors | 0 | 0 | 0 | ✅ PASS |
| Type Errors | 0 | 0 | 0 | ✅ PASS |
| Security Scan | N/A | 0 vulnerabilities | - | ✅ PASS |

**Your Session:**
[Fill in your metrics]

---

### Lessons Learned

#### What Worked Well
- [Success 1]
- [Success 2]
- [Success 3]

**Example:**
- Using BMAD framework prevented information loss between sessions
- Agent dispatch with specific prompts eliminated back-and-forth questions
- PostgreSQL decision was data-driven (cost/perf metrics), not emotional

---

#### What Didn't Work
- [Challenge 1]
- [Challenge 2]

**Example:**
- Initial schema forgot indexes, had to revise
- Underestimated time for test writing (2x longer than expected)

---

#### What We'd Do Differently
- [Improvement 1]
- [Improvement 2]

**Example:**
- Next time: Include index design in initial schema prompt
- Next time: Allocate 50% more time for testing phase

---

#### Reusable Patterns
> Patterns or approaches from this session that can be reused in future sessions.

- [Pattern 1: Description]
- [Pattern 2: Description]

**Example:**
- **Pattern:** "Cost-first architecture evaluation" - Always evaluate cost BEFORE feature complexity
- **Pattern:** "Schema-first database design" - Validate schema with sample data before writing ORM code
- **Pattern:** "Agent prompt templates" - Reuse prompt structure (Context → Task → Output → Handoff)

---

### Open Questions
- [ ] **Question 1:** [Question text]
  - **Blocked by:** [What's preventing answer]
  - **Impact:** [High / Medium / Low]
  - **Next step:** [Who/what will resolve this]

- [ ] **Question 2:** [Question text]

**Example:**
- [ ] **Question:** Should we add full-text search to Ions now or later?
  - **Blocked by:** Need to see actual user search queries first
  - **Impact:** Medium (nice-to-have, not critical for MVP)
  - **Next step:** Defer to Phase 2, revisit after 1 week of user testing

---

### Phase 2 Backlog
> Items explicitly deferred from this session.

- [ ] **Item 1:** [Description]
  - **Estimated effort:** [Hours/days]
  - **Priority:** [High / Medium / Low]
  - **Depends on:** [Prerequisites]

- [ ] **Item 2:** [Description]

**Example:**
- [ ] **Full ORM implementation:** Complete SQLAlchemy models with all relationships
  - **Estimated effort:** 8 hours
  - **Priority:** High
  - **Depends on:** Schema validated (✅ done in this session)

- [ ] **API endpoint refactoring:** Switch from mock data to real database queries
  - **Estimated effort:** 6 hours
  - **Priority:** High
  - **Depends on:** ORM models complete

- [ ] **Caching layer (Redis):** Add caching for frequently accessed Ions
  - **Estimated effort:** 4 hours
  - **Priority:** Low
  - **Depends on:** Performance testing shows need

---

## 📊 Session Metadata

**Start Time:** YYYY-MM-DD HH:MM
**End Time:** YYYY-MM-DD HH:MM
**Total Duration:** [X hours Y minutes]

**Agents Used:**
- Claude-Code: 60% (context, decisions, docs)
- Aider: 30% (code generation)
- Windsurf: 10% (validation)

**Git Commits:** [5]
```bash
abc1234 - docs: baseline capture for backend architecture
def5678 - docs: milestone definition
ghi9012 - feat: add PostgreSQL schema with SQLAlchemy models
jkl3456 - test: add database schema tests
mno7890 - docs: complete BMAD for backend architecture decision
```

**Lines Changed:** +1051, -35

**Outcome:** ✅ SUCCESS / ⚠️ PARTIAL / ❌ BLOCKED

**Next Session:** [Link to next BMAD file, e.g., `BMAD_2025-11-17_API-Implementation.md`] or "TBD"

---

## 📎 Appendix

### References
- [PostgreSQL Cloud SQL Pricing](https://cloud.google.com/sql/pricing)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [ADK Deployment Guide](../../ADK_DEPLOYMENT_GUIDE.md)

### Related Sessions
- None (first session)
- [Link to related BMAD file if applicable]

### Screenshots/Artifacts
> Save screenshots, diagrams, or other artifacts to `docs/sessions/BMAD/artifacts/YYYY-MM-DD_[name].png`

- `artifacts/2025-11-16_schema_diagram.png` - Database ER diagram
- `artifacts/2025-11-16_cost_comparison.png` - Cost analysis spreadsheet

---

**End of BMAD Session**

**Template Version:** 2.0
**Last Updated:** 2025-11-16
**Next Review:** After each session (update template based on learnings)
