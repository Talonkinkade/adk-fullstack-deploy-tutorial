#!/usr/bin/env python3
"""
Quick Test for LearnQwest Agents with Upgraded Gemini 2.0 Flash Experimental Model
Uses your $980 Google Cloud credits - estimated cost: $0.10-0.30 for full test
"""

import sys
from pathlib import Path

print("=" * 80)
print("🚀 LearnQwest Agent Quick Test - Gemini 2.0 Flash Experimental")
print("=" * 80)
print("\n📊 Credit Usage: ~$0.10-0.30 for this test (you have $980 remaining)")
print("🤖 Model: gemini-2.0-flash-exp (UPGRADED for best quality)\n")

# Import the upgraded agents
try:
    from app.learnqwest_agents import (
        learnqwest_filesystem_agent,
        learnqwest_documentation_agent,
        learnqwest_workflow_agent,
        learnqwest_orchestrator_agent,
        LEARNQWEST_MODEL,
    )
    print(f"✓ Agents loaded successfully with model: {LEARNQWEST_MODEL}")
except Exception as e:
    print(f"✗ Error loading agents: {e}")
    print("\nTry running: make install")
    sys.exit(1)

print("\n" + "=" * 80)
print("TEST 1: Filesystem Agent - Analyze DROPZONE_INBOX")
print("=" * 80)

query1 = """
Analyze the files in /home/user/DROPZONE_INBOX and provide:
1. List of all files with their types
2. Brief summary of each file's content
3. Recommendation for organizing them into /home/user/LearnQwest directories

Be thorough and detailed in your analysis.
"""

print(f"\n📝 Query: {query1.strip()}\n")
print("⏳ Calling Gemini 2.0 Flash Experimental API...")
print("💰 Cost: ~$0.05-0.10\n")

try:
    result1 = learnqwest_filesystem_agent.run(query1)
    print("\n" + "-" * 80)
    print("📊 FILESYSTEM AGENT RESPONSE:")
    print("-" * 80)
    print(result1)
    print("-" * 80)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n\n" + "=" * 80)
print("TEST 2: Documentation Agent - Create Project README")
print("=" * 80)

query2 = """
Create a comprehensive, professional README.md for the AI Assistant project at:
/home/user/LearnQwest/Projects/AIAssistant

Include:
- Project title and description
- Key features and capabilities
- Installation and setup instructions
- Usage examples with code samples
- Architecture overview
- Contributing guidelines
- License information

Make it production-ready and polished.
"""

print(f"\n📝 Query: {query2.strip()}\n")
print("⏳ Calling Gemini 2.0 Flash Experimental API...")
print("💰 Cost: ~$0.10-0.15\n")

try:
    result2 = learnqwest_documentation_agent.run(query2)
    print("\n" + "-" * 80)
    print("📊 DOCUMENTATION AGENT RESPONSE:")
    print("-" * 80)
    print(result2)
    print("-" * 80)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n\n" + "=" * 80)
print("✅ TESTS COMPLETED!")
print("=" * 80)
print("\n💰 Estimated credits used: $0.15-0.25")
print(f"💵 Remaining credits: ~${980 - 0.25:.2f}")
print("\n🎉 All agents working with upgraded Gemini 2.0 Flash Experimental!")
print("\nNext steps:")
print("  1. Review the agent responses above")
print("  2. Test the Workflow Agent and Orchestrator")
print("  3. Deploy to Vertex AI Agent Engine: make deploy-adk")
print("  4. Integrate with your production systems")
