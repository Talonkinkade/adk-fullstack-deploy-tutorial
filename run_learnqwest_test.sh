#!/bin/bash
#
# LearnQwest Agent Test Script
# Uses your $980 Google Cloud credits - estimated cost: $0.20-0.50
#

echo "================================================================================"
echo "🚀 LearnQwest Agent System - Gemini 2.0 Flash Experimental"
echo "================================================================================"
echo ""
echo "📊 Credit Usage: ~$0.20-0.50 for this test (you have \$980 remaining)"
echo "🤖 Model: gemini-2.0-flash-exp (UPGRADED for best performance)"
echo ""
echo "This will:"
echo "  1. Start the ADK API server with LearnQwest agents"
echo "  2. Test filesystem, documentation, workflow, and orchestrator agents"
echo "  3. Generate comprehensive reports and recommendations"
echo ""
echo "💰 Estimated Cost Breakdown:"
echo "  - Starting server: \$0.00 (no API calls)"
echo "  - Filesystem agent test: ~\$0.05-0.10"
echo "  - Documentation agent test: ~\$0.10-0.15"
echo "  - Workflow agent test: ~\$0.05-0.10"
echo "  - Orchestrator test: ~\$0.10-0.20"
echo "  - Total: ~\$0.30-0.55"
echo ""
read -p "Press ENTER to start the ADK server (or Ctrl+C to cancel)..."

echo ""
echo "🔧 Starting ADK API Server with LearnQwest agents..."
echo ""

# Start the ADK API server
# This makes all agents available at http://127.0.0.1:8000
uv run adk api_server app --allow_origins="*"
