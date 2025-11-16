"""
Basic Agent Platform Usage Example

This example demonstrates how to:
1. Initialize the agent platform
2. Register multiple agents
3. Let agents communicate via events
4. Query the context graph
5. Monitor performance

Run with: python examples/basic_platform_usage.py
"""

import asyncio
import logging

from app.agent_platform import get_platform, shutdown_platform
from app.agent_platform.agents.context_loader.agent import ContextLoaderAgent
from app.agent_platform.agents.developer_journal.agent import DeveloperJournalAgent
from app.agent_platform.agents.performance_analytics.agent import (
    PerformanceAnalyticsAgent,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main() -> None:
    """Main example workflow."""

    logger.info("🚀 Starting Agent Platform Example")

    # -------------------------------------------------------------------------
    # Step 1: Initialize Platform
    # -------------------------------------------------------------------------
    logger.info("\n=== Step 1: Initialize Platform ===")

    platform = await get_platform()

    logger.info("✅ Platform initialized!")

    # Check platform health
    health = await platform.health_check()
    logger.info(f"Platform health: {health['platform']}")
    logger.info(f"Services: Neo4j={health['services']['neo4j']['status']}, "
                f"Redis={health['services']['redis']['status']}")

    # -------------------------------------------------------------------------
    # Step 2: Register Agents
    # -------------------------------------------------------------------------
    logger.info("\n=== Step 2: Register Agents ===")

    # Context Loader Agent
    context_loader = ContextLoaderAgent(
        config={
            "auto_sync": True,
            "context_sources": [
                # Example: Load from files
                # {"type": "file", "path": "./data/context.json"},
            ],
        }
    )
    await platform.register_agent(context_loader)
    logger.info("✅ Context Loader Agent registered")

    # Developer Journal Agent
    journal_agent = DeveloperJournalAgent(
        config={
            "prompt_time": "09:00",
            "auto_summarize": True,
        }
    )
    await platform.register_agent(journal_agent)
    logger.info("✅ Developer Journal Agent registered")

    # Performance Analytics Agent
    analytics_agent = PerformanceAnalyticsAgent(
        config={
            "analysis_interval_seconds": 300,  # 5 minutes
        }
    )
    await platform.register_agent(analytics_agent)
    logger.info("✅ Performance Analytics Agent registered")

    # -------------------------------------------------------------------------
    # Step 3: Create a Journal Entry
    # -------------------------------------------------------------------------
    logger.info("\n=== Step 3: Create a Journal Entry ===")

    entry_id = await journal_agent.create_entry(
        title="First Day with Agent Platform",
        content="""
        Today I set up the autonomous agent platform!

        Key learnings:
        - Event-driven architecture makes agents autonomous
        - Context graph enables cross-domain insights
        - Performance monitoring is built-in

        Challenges:
        - Understanding Neo4j query syntax
        - Configuring Redis streams

        Solutions:
        - Read Neo4j Cypher documentation
        - Used example queries from the platform
        """,
        category="learning",
        tags=["agent-platform", "neo4j", "redis"],
        learnings=[
            "Event-driven architecture",
            "Neo4j graph databases",
            "Redis streams",
        ],
    )

    logger.info(f"✅ Journal entry created: {entry_id}")

    # -------------------------------------------------------------------------
    # Step 4: Search Journal Entries
    # -------------------------------------------------------------------------
    logger.info("\n=== Step 4: Search Journal Entries ===")

    # Give some time for the entry to be stored
    await asyncio.sleep(1)

    entries = await journal_agent.search_entries(
        query="agent platform",
        category="learning",
        limit=5,
    )

    logger.info(f"Found {len(entries)} journal entries")

    # -------------------------------------------------------------------------
    # Step 5: Analyze Performance
    # -------------------------------------------------------------------------
    logger.info("\n=== Step 5: Analyze Performance ===")

    # Record some metrics
    await analytics_agent.record_metric(
        agent_name="developer_journal",
        metric_name="events_processed",
        metric_value=10,
        metric_unit="events",
    )

    # Generate performance report
    report = await analytics_agent.generate_performance_report()
    logger.info("\n" + report)

    # Detect bottlenecks
    bottlenecks = await analytics_agent.detect_bottlenecks()
    if bottlenecks:
        logger.warning(f"⚠️ Detected {len(bottlenecks)} bottlenecks")
        for bottleneck in bottlenecks:
            logger.warning(f"  - {bottleneck['agent']}: {bottleneck['type']}")
    else:
        logger.info("✅ No bottlenecks detected")

    # -------------------------------------------------------------------------
    # Step 6: Platform Statistics
    # -------------------------------------------------------------------------
    logger.info("\n=== Step 6: Platform Statistics ===")

    stats = await platform.get_platform_stats()
    logger.info(f"Total agents: {stats['total_agents']}")
    logger.info(f"Event bus stats: {stats.get('event_bus', {})}")
    logger.info(f"Registry stats: {stats.get('registry', {})}")

    # -------------------------------------------------------------------------
    # Step 7: Generate Weekly Summary
    # -------------------------------------------------------------------------
    logger.info("\n=== Step 7: Generate Weekly Summary ===")

    summary = await journal_agent.generate_weekly_summary()
    logger.info("\n" + summary)

    # -------------------------------------------------------------------------
    # Step 8: Keep Platform Running
    # -------------------------------------------------------------------------
    logger.info("\n=== Platform is Running ===")
    logger.info("Press Ctrl+C to stop")

    try:
        # Keep the platform running
        while platform.running:
            await asyncio.sleep(5)

            # Periodic health check (every 60 seconds)
            import time
            if int(time.time()) % 60 == 0:
                health = await platform.health_check()
                logger.info(f"Health check: {health['platform']}")

    except KeyboardInterrupt:
        logger.info("\n🛑 Shutdown requested...")

    finally:
        # Cleanup
        await shutdown_platform()
        logger.info("✅ Platform stopped successfully!")


if __name__ == "__main__":
    asyncio.run(main())
