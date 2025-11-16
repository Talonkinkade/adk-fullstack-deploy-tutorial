"""
Agent Platform - Autonomous, multi-agent system for lifelong productivity and growth.

This platform provides:
- Event-driven agent communication
- Universal context graph for shared knowledge
- Agent registry and discovery
- Performance monitoring and analytics
- Extensible agent framework

Quick Start:
-----------
```python
from app.agent_platform import get_platform
from app.agent_platform.agents.developer_journal import DeveloperJournalAgent

# Get platform instance
platform = await get_platform()

# Register agents
journal_agent = DeveloperJournalAgent()
await platform.register_agent(journal_agent)

# Platform is now running!
```
"""

from app.agent_platform.platform import (
    AgentPlatform,
    get_platform,
    shutdown_platform,
)

__all__ = [
    "AgentPlatform",
    "get_platform",
    "shutdown_platform",
]
