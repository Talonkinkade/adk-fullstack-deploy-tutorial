#!/usr/bin/env python3
"""
Test script for LearnQwest agents.
This script demonstrates the capabilities of each agent and uses Google Cloud credits.

Usage:
    python test_learnqwest_agents.py
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

# Import the LearnQwest agents
from app.learnqwest_agents import (
    learnqwest_filesystem_agent,
    learnqwest_documentation_agent,
    learnqwest_workflow_agent,
    learnqwest_orchestrator_agent,
)


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_result(agent_name: str, result):
    """Print agent result in a formatted way."""
    print(f"\n📊 {agent_name} Response:")
    print("-" * 80)
    if hasattr(result, 'output_key'):
        print(f"Output Key: {result.output_key}")
    if hasattr(result, 'text'):
        print(result.text)
    else:
        print(result)
    print("-" * 80)


async def test_filesystem_agent():
    """Test the LearnQwest Filesystem Agent."""
    print_section("TEST 1: LearnQwest Filesystem Agent")

    query = """
    Analyze the contents of /home/user/DROPZONE_INBOX and provide:
    1. A list of all files found
    2. File types and their purposes
    3. Suggested organization into LearnQwest directories
    4. A plan for routing these files
    """

    print(f"🤖 Query: {query.strip()}\n")
    print("⏳ Calling Filesystem Agent (this uses Google Cloud credits)...\n")

    # This is where credits are used - calling the Gemini API
    result = await learnqwest_filesystem_agent.run_async(query)

    print_result("Filesystem Agent", result)
    return result


async def test_documentation_agent():
    """Test the LearnQwest Documentation Agent."""
    print_section("TEST 2: LearnQwest Documentation Agent")

    query = """
    Create a comprehensive README.md for the AI Assistant project located at
    /home/user/LearnQwest/Projects/AIAssistant.

    The README should include:
    1. Project overview
    2. Features and capabilities
    3. Setup instructions
    4. Usage examples
    5. Architecture overview
    """

    print(f"🤖 Query: {query.strip()}\n")
    print("⏳ Calling Documentation Agent (this uses Google Cloud credits)...\n")

    # This is where credits are used
    result = await learnqwest_documentation_agent.run_async(query)

    print_result("Documentation Agent", result)
    return result


async def test_workflow_agent():
    """Test the LearnQwest Workflow Agent."""
    print_section("TEST 3: LearnQwest Workflow Agent")

    query = """
    Design an automated workflow for processing files in /home/user/DROPZONE_INBOX.

    The workflow should:
    1. Monitor DROPZONE_INBOX for new files
    2. Analyze file types (.csv, .md, .txt, .py, etc.)
    3. Route files to appropriate LearnQwest directories:
       - .py files → /home/user/LearnQwest/ADA/modules/
       - .md files → /home/user/LearnQwest/Documentation/
       - .csv/.txt files → /home/user/LearnQwest/Data/
    4. Log all operations
    5. Handle errors gracefully

    Provide a detailed workflow specification.
    """

    print(f"🤖 Query: {query.strip()}\n")
    print("⏳ Calling Workflow Agent (this uses Google Cloud credits)...\n")

    # This is where credits are used
    result = await learnqwest_workflow_agent.run_async(query)

    print_result("Workflow Agent", result)
    return result


async def test_orchestrator_agent():
    """Test the LearnQwest Orchestrator Agent."""
    print_section("TEST 4: LearnQwest Orchestrator Agent (Multi-Agent)")

    query = """
    I need to set up a complete AI project workspace. Please:

    1. Analyze and organize the files in /home/user/DROPZONE_INBOX
    2. Create comprehensive documentation for the project
    3. Set up automated workflows for ongoing file management

    Coordinate between the filesystem, documentation, and workflow agents to
    accomplish this complete setup. Provide a detailed execution plan and results.
    """

    print(f"🤖 Query: {query.strip()}\n")
    print("⏳ Calling Orchestrator Agent (this uses MORE credits - multi-agent)...\n")

    # This is where MORE credits are used - orchestrator may call multiple agents
    result = await learnqwest_orchestrator_agent.run_async(query)

    print_result("Orchestrator Agent", result)
    return result


async def run_all_tests():
    """Run all agent tests."""
    print_section("🚀 LearnQwest Agent Testing Suite")
    print("This test suite will call Google Cloud Gemini API and use your credits.")
    print(f"Started at: {datetime.now().isoformat()}")

    # Track credit usage estimation
    print("\n💰 Estimated Credit Usage:")
    print("  - Each agent call: ~$0.01 - $0.05 (depending on response length)")
    print("  - Total for all tests: ~$0.05 - $0.20")
    print("  - Orchestrator test: ~$0.10 - $0.30 (multi-agent coordination)")

    input("\n⚠️  Press ENTER to continue with testing (or Ctrl+C to cancel)...")

    results = {}

    try:
        # Test 1: Filesystem Agent
        results['filesystem'] = await test_filesystem_agent()

        # Test 2: Documentation Agent
        results['documentation'] = await test_documentation_agent()

        # Test 3: Workflow Agent
        results['workflow'] = await test_workflow_agent()

        # Test 4: Orchestrator Agent (complex multi-agent test)
        results['orchestrator'] = await test_orchestrator_agent()

        # Summary
        print_section("✅ All Tests Completed Successfully!")
        print(f"Completed at: {datetime.now().isoformat()}")
        print("\n📊 Test Summary:")
        print(f"  - Filesystem Agent: ✓ Completed")
        print(f"  - Documentation Agent: ✓ Completed")
        print(f"  - Workflow Agent: ✓ Completed")
        print(f"  - Orchestrator Agent: ✓ Completed")

        # Save results
        results_file = Path("test_results.json")
        with open(results_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "tests_run": list(results.keys()),
                "status": "success"
            }, f, indent=2)

        print(f"\n💾 Results saved to: {results_file}")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


async def quick_test():
    """Run a quick single agent test."""
    print_section("🚀 Quick Test: Filesystem Agent Only")
    print("This will use minimal credits (~$0.01-0.02)")

    query = "List and analyze the files in /home/user/DROPZONE_INBOX"
    print(f"🤖 Query: {query}\n")

    input("⚠️  Press ENTER to continue (or Ctrl+C to cancel)...")

    result = await learnqwest_filesystem_agent.run_async(query)
    print_result("Filesystem Agent", result)

    print("\n✅ Quick test completed!")
    return 0


def main():
    """Main entry point."""
    import sys

    print("=" * 80)
    print("  LearnQwest Agent Test Suite")
    print("=" * 80)
    print("\nTest Options:")
    print("  1. Quick Test (single agent, minimal credits)")
    print("  2. Full Test Suite (all agents, more credits)")
    print("  3. Exit")

    choice = input("\nSelect option (1-3): ").strip()

    if choice == "1":
        return asyncio.run(quick_test())
    elif choice == "2":
        return asyncio.run(run_all_tests())
    elif choice == "3":
        print("Exiting...")
        return 0
    else:
        print("Invalid choice. Exiting...")
        return 1


if __name__ == "__main__":
    exit(main())
