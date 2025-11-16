# 🤖 Agent Platform - Autonomous Multi-Agent System

A production-ready autonomous agent platform for lifelong productivity, learning, health, finance, and personal development. Built on event-driven architecture with a universal context graph.

## 🌟 Overview

This platform enables you to build and orchestrate autonomous agents that:
- Communicate via events (pub/sub pattern)
- Share knowledge through a universal Neo4j context graph
- Self-monitor and improve over time
- Discover and compose dynamically
- Operate 24/7 without manual intervention

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Platform                        │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │  Event Bus  │  │   Registry   │  │ Context Graph  │ │
│  │   (Redis)   │  │  (Neo4j)     │  │    (Neo4j)     │ │
│  └──────┬──────┘  └──────┬───────┘  └────────┬───────┘ │
│         │                 │                   │          │
│  ┌──────┴─────────────────┴───────────────────┴──────┐  │
│  │              Platform Core Services                 │  │
│  └──────┬────────────┬────────────┬───────────────────┘  │
│         │            │            │                       │
│  ┌──────┴──┐  ┌─────┴────┐  ┌────┴──────┐               │
│  │ Agent 1 │  │ Agent 2  │  │ Agent N   │               │
│  │(Journal)│  │(Context) │  │(Analytics)│               │
│  └─────────┘  └──────────┘  └───────────┘               │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Core Components

1. **Event Bus** (Redis Streams)
   - Publish/subscribe messaging
   - Pattern-based routing (`task.*`, `agent.started`)
   - Priority queues (critical, high, normal, low)
   - Event replay for agent initialization

2. **Agent Registry** (Neo4j)
   - Dynamic agent discovery
   - Capability-based lookup
   - Health monitoring
   - Team composition (assemble agents for complex tasks)

3. **Context Service** (Neo4j)
   - Universal knowledge graph
   - Temporal queries (what happened when)
   - Causal queries (what led to what)
   - Cross-domain insights

4. **Base Agent SDK**
   - Lifecycle management (setup, start, stop)
   - Event pub/sub integration
   - Context graph access
   - Performance monitoring

## 🚀 Quick Start

### Prerequisites

- Python 3.10-3.12
- Docker & Docker Compose (for Redis + Neo4j)
- uv (or pip)

### Installation

1. **Install dependencies:**

```bash
uv pip install -e .
```

2. **Start infrastructure services:**

```bash
docker-compose up -d
```

This starts:
- Redis on `localhost:6379`
- Neo4j on `localhost:7687` (browser: `http://localhost:7474`)

3. **Run the example:**

```bash
python examples/basic_platform_usage.py
```

### Environment Variables

Create a `.env` file (or set environment variables):

```bash
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 📖 Building Your First Agent

```python
from app.agent_platform.core import BaseAgent
from app.agent_platform.models import AgentCapability, BaseEvent

class MyAgent(BaseAgent):
    """My custom agent."""

    def __init__(self, config=None):
        super().__init__(
            name="my_agent",
            description="Does amazing things",
            config=config or {},
        )

    async def setup(self):
        """Setup hook - called before agent starts."""
        # Subscribe to events
        await self.subscribe("user.input", self._handle_user_input)

    async def process_event(self, event: BaseEvent):
        """Main event processing logic."""
        if event.event_type == "user.input":
            await self._handle_user_input(event)

    async def _handle_user_input(self, event: BaseEvent):
        """Handle user input events."""
        user_message = event.data.get("message", "")

        # Do something with the message
        response = f"Processed: {user_message}"

        # Store in context graph
        await self.update_context(
            node_type="entity",
            properties={"user_message": user_message, "response": response}
        )

        # Publish response event
        await self.publish_event(
            "agent.response",
            {"response": response}
        )

    def get_capabilities(self):
        """Declare what this agent can do."""
        return [
            AgentCapability(
                name="process_user_input",
                description="Processes user messages",
            )
        ]
```

**Register and run:**

```python
from app.agent_platform import get_platform

platform = await get_platform()
agent = MyAgent()
await platform.register_agent(agent)
```

## 🔌 Pre-Built Agents

### 1. Context Loader Agent
Loads context from files, APIs, and databases.

```python
from app.agent_platform.agents.context_loader import ContextLoaderAgent

agent = ContextLoaderAgent(config={
    "auto_sync": True,
    "context_sources": [
        {"type": "file", "path": "./data/projects.json"},
        {"type": "file", "path": "./knowledge_base/*.md"},
    ],
})
```

### 2. Developer Journal Agent
Daily prompts, learning logs, and knowledge capture.

```python
from app.agent_platform.agents.developer_journal import DeveloperJournalAgent

agent = DeveloperJournalAgent(config={
    "prompt_time": "09:00",  # Daily prompt at 9 AM
    "auto_summarize": True,
})

# Create an entry
await agent.create_entry(
    title="Today's Learning",
    content="Learned about event-driven architecture",
    tags=["learning", "architecture"],
    learnings=["Event-driven design", "Pub/Sub patterns"],
)

# Search entries
entries = await agent.search_entries(query="architecture", limit=10)

# Generate weekly summary
summary = await agent.generate_weekly_summary()
```

### 3. Performance Analytics Agent
Monitor agent performance and detect bottlenecks.

```python
from app.agent_platform.agents.performance_analytics import PerformanceAnalyticsAgent

agent = PerformanceAnalyticsAgent()

# Record metrics
await agent.record_metric(
    agent_name="my_agent",
    metric_name="response_time_ms",
    metric_value=45.2,
)

# Analyze performance
report = await agent.analyze_agent_performance("my_agent")

# Detect bottlenecks
bottlenecks = await agent.detect_bottlenecks()

# Generate platform-wide report
report = await agent.generate_performance_report()
```

## 🧠 Working with Context Graph

The context graph enables agents to share knowledge and discover insights.

### Create Nodes

```python
# Create a project node
project_id = await agent.update_context(
    node_type="project",
    properties={
        "name": "Agent Platform",
        "status": "in_progress",
        "priority": "high",
    }
)
```

### Create Relationships

```python
# Link a task to the project
await agent.create_relationship(
    from_node=task_id,
    to_node=project_id,
    rel_type="part_of",
    properties={"created_at": "2025-01-15"}
)
```

### Query the Graph

```python
# Find all tasks in a project
results = await agent.query_context(
    """
    MATCH (task)-[:part_of]->(project {name: $project_name})
    RETURN task
    """,
    {"project_name": "Agent Platform"}
)
```

### Temporal Queries

```python
from datetime import datetime, timedelta

# What did I work on this week?
results = await context_service.temporal_query(
    start_time=datetime.now() - timedelta(days=7),
    end_time=datetime.now(),
    node_types=["task", "journal_entry"]
)
```

### Causal Chains

```python
# What led to this insight?
causal_chain = await context_service.causal_chain(
    node_id=insight_id,
    max_depth=5
)
```

## 📊 Event System

Agents communicate via typed events.

### Publishing Events

```python
await agent.publish_event(
    event_type="task.completed",
    data={"task_id": "123", "duration_seconds": 300},
    priority=EventPriority.HIGH,
    correlation_id="workflow_456"  # Track related events
)
```

### Subscribing to Events

```python
# Exact match
await agent.subscribe("task.completed", handler)

# Wildcard patterns
await agent.subscribe("task.*", handler)  # All task events
await agent.subscribe("*.completed", handler)  # All completion events
await agent.subscribe("*", handler)  # All events
```

### Event Types

Pre-defined event types:
- `agent.registered`, `agent.started`, `agent.stopped`, `agent.error`
- `task.created`, `task.started`, `task.completed`, `task.failed`
- `context.updated`, `context.query`
- `data.collected`, `insight.generated`, `pattern.detected`
- `user.input`, `user.notification`
- `performance.metric`, `anomaly.detected`

## 🎯 Advanced Features

### Agent Discovery

```python
# Find agents by capability
agents = await registry.find_agents_by_capability("process_user_input")

# Find agents by tag
agents = await registry.find_agents_by_tag("ml")

# Find agents providing specific context
agents = await registry.find_agents_by_context("health")
```

### Dynamic Team Composition

```python
# Assemble a team for a complex task
team = await registry.compose_team(
    required_capabilities=["data_analysis", "report_generation", "visualization"],
    preferred_tags=["data_science"]
)
```

### Performance Monitoring

Every agent automatically tracks:
- Events processed
- Average response time
- Error count
- Uptime
- Health score

```python
# Get agent metadata
metadata = await registry.get_agent(agent_id)
print(f"Events processed: {metadata.total_events_processed}")
print(f"Avg response time: {metadata.average_response_time_ms}ms")
print(f"Error rate: {metadata.error_count / metadata.total_events_processed}")
```

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Linting & Type Checking

```bash
make lint
```

### Viewing Logs

```bash
docker-compose logs -f agent-platform
```

### Neo4j Browser

Access at `http://localhost:7474` (user: `neo4j`, password: `password`)

Useful queries:
```cypher
// View all nodes
MATCH (n) RETURN n LIMIT 100

// View all agents
MATCH (a:Agent) RETURN a

// View context relationships
MATCH (a)-[r]->(b) RETURN a, r, b LIMIT 50
```

## 🚢 Deployment

### Docker Deployment

Build and run the entire platform:

```bash
docker-compose up -d
```

### Cloud Deployment

For production:
1. Use managed Redis (AWS ElastiCache, Redis Cloud)
2. Use managed Neo4j (Aura, EC2)
3. Deploy agents as services (Docker, Kubernetes)

Environment variables:
```bash
NEO4J_URI=bolt://your-neo4j.example.com:7687
REDIS_HOST=your-redis.example.com
```

## 🗺️ Roadmap: Additional Agents

See the original brainstorm for 20+ agent ideas. Priority agents to build next:

1. **Scheduling & Reminder Agent** - Calendar integration, smart reminders
2. **Health Monitoring Agent** - Daily logs, habit tracking, wellness insights
3. **Finance Tracker Agent** - Spending, subscriptions, investment tracking
4. **Automated Learning Path Agent** - Adaptive skill development
5. **Code Review & Refactor Agent** - Auto-linting, refactoring suggestions
6. **Cross-Domain Insight Engine** - Discover correlations across life domains
7. **Decision Journal Agent** - Track decisions and outcomes
8. **Serendipity Agent** - Introduce controlled randomness

## 📚 Resources

- [Neo4j Cypher Documentation](https://neo4j.com/docs/cypher-manual/)
- [Redis Streams](https://redis.io/docs/data-types/streams/)
- [Pydantic Models](https://docs.pydantic.dev/)
- [Google ADK](https://github.com/google/agent-development-kit)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Build your agent or enhancement
4. Add tests
5. Submit a pull request

## 📄 License

Apache-2.0 (unless noted otherwise in third-party files).

## 🎓 Example Use Cases

### Personal Operating System
```python
# Morning routine
await health_agent.log_sleep(hours=7.5, quality="good")
await journal_agent.send_daily_prompt()
await schedule_agent.get_today_agenda()
await finance_agent.check_subscriptions()
```

### Project Management
```python
# Start new project
await context_loader.load_context("file", "./project_spec.md")
await project_orchestrator.create_project("New Feature", priority="high")
await performance_analytics.track_progress()
```

### Continuous Learning
```python
# Learning workflow
await learning_path_agent.suggest_next_topic()
await resource_curator.find_tutorials(topic="distributed systems")
await journal_agent.log_learning(topic="consensus algorithms")
await skill_tracker.update_progress()
```

## 💡 Tips

1. **Start small**: Begin with 2-3 agents and expand
2. **Monitor performance**: Use the analytics agent to track health
3. **Use tags**: Tag agents and context nodes for easy discovery
4. **Event correlation**: Use `correlation_id` to track multi-step workflows
5. **Graph queries**: Learn Cypher for powerful context insights
6. **Health checks**: Implement custom health checks for your agents

---

**Built with Google ADK, Neo4j, Redis, and Python**

For questions or issues: See the main README or open an issue.
