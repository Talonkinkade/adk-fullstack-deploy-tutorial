# 🚀 Agent Platform Quick Start

Get the autonomous agent platform running in 5 minutes!

## Step 1: Start Infrastructure (2 minutes)

```bash
# Start Redis + Neo4j
docker-compose up -d

# Verify services are healthy
docker-compose ps
```

You should see:
- ✅ `agent-platform-redis` - running on port 6379
- ✅ `agent-platform-neo4j` - running on ports 7474, 7687

## Step 2: Install Dependencies (1 minute)

```bash
# Install Python dependencies
uv pip install -e .

# Or with pip
pip install -e .
```

## Step 3: Run the Example (1 minute)

```bash
python examples/basic_platform_usage.py
```

You should see:
```
🚀 Starting Agent Platform Example
✅ Platform initialized!
✅ Context Loader Agent registered
✅ Developer Journal Agent registered
✅ Performance Analytics Agent registered
✅ Journal entry created: <entry_id>
📊 Platform Performance Report
...
```

## Step 4: Explore Neo4j (1 minute)

1. Open http://localhost:7474 in your browser
2. Login with:
   - Username: `neo4j`
   - Password: `password`
3. Run a query:

```cypher
MATCH (n) RETURN n LIMIT 50
```

You'll see your journal entries, agents, and context nodes!

## What Just Happened?

The example:
1. ✅ Initialized the platform with Redis + Neo4j
2. ✅ Registered 3 autonomous agents
3. ✅ Created a journal entry with learnings
4. ✅ Stored data in the context graph
5. ✅ Linked journal entry to skill nodes
6. ✅ Generated a performance report
7. ✅ Detected any bottlenecks

## Next Steps

### 1. Build Your Own Agent

Create `app/agent_platform/agents/my_agent/agent.py`:

```python
from app.agent_platform.core import BaseAgent
from app.agent_platform.models import BaseEvent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="my_agent",
            description="My custom agent",
        )

    async def setup(self):
        await self.subscribe("user.input", self._handle_input)

    async def process_event(self, event: BaseEvent):
        # Your logic here
        pass

    async def _handle_input(self, event: BaseEvent):
        message = event.data.get("message")
        await self.publish_event("agent.response", {"reply": f"Got: {message}"})
```

Register it:
```python
from app.agent_platform import get_platform
from app.agent_platform.agents.my_agent import MyAgent

platform = await get_platform()
await platform.register_agent(MyAgent())
```

### 2. Query the Context Graph

```python
# Find all journal entries
results = await agent.query_context("""
    MATCH (e:JournalEntry)
    RETURN e
    ORDER BY e.timestamp DESC
    LIMIT 10
""")

# Find what you learned this week
results = await agent.query_context("""
    MATCH (entry:JournalEntry)-[:RELATED_TO]->(skill:Skill)
    WHERE entry.timestamp > datetime() - duration({days: 7})
    RETURN skill.name, count(entry) as mentions
    ORDER BY mentions DESC
""")
```

### 3. Add More Agents

Priority agents to build:
- **Scheduling Agent** - Calendar + reminders
- **Health Agent** - Daily logs, habit tracking
- **Finance Agent** - Budget, subscriptions
- **Learning Path Agent** - Adaptive skill development

See `AGENT_PLATFORM_README.md` for 20+ agent ideas!

## Troubleshooting

### Services won't start

```bash
# Check if ports are in use
lsof -i :6379  # Redis
lsof -i :7687  # Neo4j

# Restart services
docker-compose down
docker-compose up -d
```

### Import errors

```bash
# Reinstall dependencies
uv pip install -e . --force-reinstall
```

### Neo4j connection fails

```bash
# Check Neo4j logs
docker-compose logs neo4j

# Wait for Neo4j to fully start (takes ~30s)
docker-compose up -d neo4j
sleep 30
```

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         Your Agents                      │
│  (Developer Journal, Context Loader...)  │
└───────────────┬──────────────────────────┘
                │
    ┌───────────┴───────────┐
    │   Agent Platform      │
    │  ┌─────────────────┐  │
    │  │   Event Bus     │  │  ← Redis
    │  │   (Pub/Sub)     │  │
    │  └─────────────────┘  │
    │  ┌─────────────────┐  │
    │  │ Context Graph   │  │  ← Neo4j
    │  │  (Knowledge)    │  │
    │  └─────────────────┘  │
    │  ┌─────────────────┐  │
    │  │  Agent Registry │  │  ← Discovery
    │  │  (Discovery)    │  │
    │  └─────────────────┘  │
    └─────────────────────────┘
```

## Key Concepts

1. **Agents** - Autonomous workers that process events
2. **Events** - Messages that agents publish/subscribe to
3. **Context Graph** - Shared knowledge stored in Neo4j
4. **Registry** - Where agents register and discover each other

## Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Reset data (⚠️ deletes all context)
docker-compose down -v

# Run specific agent
python -c "
import asyncio
from app.agent_platform import get_platform
from app.agent_platform.agents.developer_journal import DeveloperJournalAgent

async def main():
    platform = await get_platform()
    await platform.register_agent(DeveloperJournalAgent())
    await asyncio.sleep(3600)  # Run for 1 hour

asyncio.run(main())
"
```

## Resources

- Full docs: `AGENT_PLATFORM_README.md`
- Example code: `examples/basic_platform_usage.py`
- Neo4j browser: http://localhost:7474
- Redis CLI: `docker exec -it agent-platform-redis redis-cli`

Happy building! 🎉
