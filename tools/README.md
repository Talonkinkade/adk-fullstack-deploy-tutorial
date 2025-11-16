# LearnQwest Tools

**Team LINK Development Utilities**

## 🔧 Available Tools

### `workflow_updater.py`
Programmatically manage the LearnQwest living workflow diagram.

**Features:**
- Add new agents to any tier
- Create connections between nodes
- Update agent status (Planned → Development → Deployed)
- Add new subgraphs for functional areas
- Automatic changelog management
- Search and count agents

**Usage:**
```python
from workflow_updater import WorkflowUpdater

updater = WorkflowUpdater("../LEARNQWEST_WORKFLOW.mmd")

# Add a new agent
updater.add_agent(
    agent_id="Ion-CustomAgent",
    agent_name="Custom Agent",
    description="Does something awesome",
    tier="Tier4_Generation",
    status="Development"
)

# Connect agents
updater.add_connection(
    from_node="Ion-CustomAgent",
    to_node="LessonPlanGen",
    label="provides data"
)

# Update status
updater.update_agent_status("Ion-CustomAgent", "Deployed")

# Save changes
updater.save()
```

**Quick Commands:**
```bash
# Make executable
chmod +x workflow_updater.py

# Run interactive mode
python workflow_updater.py

# Import in your scripts
python -c "from workflow_updater import WorkflowUpdater; updater = WorkflowUpdater(); print(f'Total agents: {updater.get_agent_count()}')"
```

---

## 📊 Future Tools (Planned)

- `agent_generator.py` - Template generator for new Ion agents
- `tier_analyzer.py` - Dependency and bottleneck analysis
- `deployment_validator.py` - Pre-deployment checks across all tiers
- `metric_collector.py` - Gather analytics from Tier 8 agents
- `teks_validator.py` - Validate content against TEKS standards

---

## 🚀 Contributing New Tools

When adding new tools to this directory:

1. Follow Python best practices (type hints, docstrings)
2. Include usage examples in docstring
3. Update this README
4. Add entry to workflow diagram if it's an agent-facing tool
5. Use Team LINK naming conventions

**Example Tool Template:**
```python
#!/usr/bin/env python3
"""
Tool Name - Brief Description
Team LINK - Digital Self Partnership Tool
"""

from pathlib import Path
from typing import List

class YourTool:
    """Main tool class."""

    def __init__(self):
        pass

    def run(self):
        """Execute main functionality."""
        pass

def main():
    """CLI entry point."""
    tool = YourTool()
    tool.run()

if __name__ == "__main__":
    main()
```

---

[OK] Tools ready for Team LINK! 🔧
