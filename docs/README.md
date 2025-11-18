# Documentation Directory

This directory contains the **ADA (Autonomous Development Architect)** orchestration system and session documentation.

---

## 📁 Directory Structure

```
docs/
├── README.md                          # This file
├── ada-system/                        # Core ADA system files
│   ├── MASTER_ORCHESTRATION_PROMPT.md # The brain of ADA (685 lines)
│   └── PRODUCTION_LAUNCH_GUIDE.md     # User manual & quick-start
├── workflows/                         # Visual workflow diagrams
│   └── WORKFLOW_MERMAID_TEMPLATE.mmd  # Interactive Mermaid diagram
└── sessions/                          # Session documentation
    ├── BMAD_TEMPLATE.md               # Template for new sessions
    └── BMAD/                          # Completed BMAD session files
        └── 2025-11-18_ADA-System-Bootstrap.md  # Session 001
```

---

## 🎯 What is ADA?

**ADA (Autonomous Development Architect)** is an AI agent orchestration system that enables intelligent crew formation and zero-information-loss workflows.

**Key Features**:
- **8-Phase Workflow**: Context → Baseline → Milestone → Dispatch → Execution → Validation → Documentation → Mermaid
- **BMAD Sessions**: Structured documentation (Baseline-Milestone-Agent-Dispatch-Documentation)
- **Crew Management**: Solo, Sequential, Parallel, and Dynamic Task Force modes
- **Visual Tracking**: Mermaid diagrams show session timeline and dependencies
- **Python Backend**: Programmatic crew formation and progress tracking

---

## 🚀 Quick Start

### For New Users

1. **Read the Launch Guide** (5 minutes)
   ```bash
   cat docs/ada-system/PRODUCTION_LAUNCH_GUIDE.md
   ```

2. **Copy the BMAD Template** for your session
   ```bash
   cp docs/sessions/BMAD_TEMPLATE.md \
      docs/sessions/BMAD/2025-11-18_Your-Session-Name.md
   ```

3. **Fill out Baseline and Milestone** (20 minutes)
   - [B] Baseline: Document current project state
   - [M] Milestone: Define success criteria

4. **Ask ADA to form a crew** (Claude-Code, Aider, Windsurf, etc.)

5. **Execute agents** → **Validate** → **Document** → **Update Mermaid**

---

## 📚 Key Files Explained

### `MASTER_ORCHESTRATION_PROMPT.md`

The comprehensive guide to ADA's 8-phase workflow. Read this to understand:
- How to analyze task complexity
- When to use which crew type
- How to generate agent prompts
- Dynamic spawning protocols
- Examples of crews in action

**When to read**: Before starting your first ADA session

---

### `PRODUCTION_LAUNCH_GUIDE.md`

Your practical playbook for using ADA. Includes:
- 5-minute setup instructions
- Step-by-step execution walkthrough
- Troubleshooting guide
- Pro tips for your workflow
- Real-world example (backend architecture decision)

**When to read**: When you want to start using ADA right now

---

### `BMAD_TEMPLATE.md`

The template for documenting every ADA session. Contains:
- **[B] Baseline**: Current state snapshot
- **[M] Milestone**: Success criteria & deliverables
- **[A] Agent Dispatch**: Crew formation & task assignments
- **[D] Documentation**: Achievements, decisions, lessons learned

**When to use**: Copy this for EVERY new session

---

### `WORKFLOW_MERMAID_TEMPLATE.mmd`

Interactive Mermaid diagram showing:
- The 8-phase workflow
- Crew formation decision tree
- Agent roster
- Crew type examples
- **Appendable session history** (grows over time)

**When to update**: Phase 8 of every session (append your session to history)

**How to view**:
- Paste into [Mermaid Live Editor](https://mermaid.live)
- Or use VSCode Mermaid extension
- Or render in GitHub markdown

---

### `ada_orchestrator.py`

Python backend for ADA. Features:
- `ADAOrchestrator` class for crew management
- `AgentTask` dataclass for task tracking
- `Crew` dataclass for crew coordination
- Prompt generation helpers
- Progress tracking and status reports
- Factory functions for common crew patterns

**When to use**:
- Programmatically form crews
- Automate crew status tracking
- Generate agent prompts from code
- Build custom CLI tools

**How to run**:
```bash
python3 app/ada_orchestrator.py  # Runs example usage
```

---

## 🎓 Learning Path

### Level 1: First Session (Solo Agent)
- Copy BMAD template
- Fill out Baseline + Milestone
- Execute simple task with Claude-Code
- Document in [D] section
- Update Mermaid with your session

**Example**: Refactor a single file

---

### Level 2: Sequential Crew
- Plan task requiring 2-3 agents
- Form sequential crew (Agent A → B → C)
- Practice handoff notes between agents
- Validate with Windsurf

**Example**: Backend architecture decision → Schema generation → Integration tests

---

### Level 3: Parallel Crew
- Identify independent tasks
- Form parallel crew (Backend + Frontend simultaneously)
- Coordinate sync point for integration
- Validate combined output

**Example**: Build API endpoints + UI components in parallel

---

### Level 4: Dynamic Task Force
- Handle complex problem with unknown scope
- Enable dynamic spawning
- Spawn specialists as needed
- Coordinate emergency response

**Example**: Production bug fix with root cause analysis

---

## 📊 Session Archive

Completed BMAD sessions are stored in `docs/sessions/BMAD/`:

| Session | Date | Status | Topic | Duration |
|---------|------|--------|-------|----------|
| [001](sessions/BMAD/2025-11-18_ADA-System-Bootstrap.md) | 2025-11-18 | ✅ COMPLETE | ADA System Bootstrap | 2h |

Each session file contains:
- Complete project state snapshot (Baseline)
- Success criteria (Milestone)
- Agent assignments and execution log (Agent Dispatch)
- Architecture decisions and lessons learned (Documentation)

**To reference past sessions**: Open the BMAD file and read the [D] Documentation section

---

## 🔗 External Resources

- [Mermaid Live Editor](https://mermaid.live) - Preview Mermaid diagrams
- [Mermaid Documentation](https://mermaid.js.org/) - Learn Mermaid syntax
- [ADK Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-builder) - Google ADK reference

---

## 🤝 Contributing

When adding to the ADA system:

1. **New templates**: Add to `docs/sessions/`
2. **New workflows**: Add Mermaid diagrams to `docs/workflows/`
3. **Orchestrator updates**: Modify `app/ada_orchestrator.py`
4. **Documentation**: Update relevant files in `docs/ada-system/`

**Always**:
- Update this README if directory structure changes
- Add examples to demonstrate new features
- Document lessons learned in BMAD files

---

## 🎯 Goals of This System

1. **Zero Information Loss**: Everything captured in BMAD files
2. **2-Minute Session Pickup**: Read Baseline + Milestone, start working
3. **Full Traceability**: Architecture Decisions table shows all past choices
4. **Visual Timeline**: Mermaid shows project journey across sessions
5. **Intelligent Coordination**: Right agents for the right tasks
6. **Compound Knowledge**: Each session builds on previous learnings

---

## 🏁 Next Steps

**If you're new to ADA**:
1. Read `PRODUCTION_LAUNCH_GUIDE.md` (15 minutes)
2. Create your first BMAD file (copy template)
3. Try a simple solo-agent session
4. Update Mermaid with your session
5. Read Session 001 BMAD to see example

**If you're ready to build**:
1. Use ADA for your next feature/decision
2. Document everything in BMAD format
3. Share learnings in [D] Documentation section
4. Help improve the system based on your experience

---

**Welcome to the ADA ecosystem!** 🤖✨

**"Iron sharpens iron, and one agent sharpens another."** ⚔️💎

---

**Last Updated**: 2025-11-18
**Maintained by**: TeamLink Master Control System
