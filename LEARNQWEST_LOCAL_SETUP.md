# LearnQwest Local Setup - Complete!

## ✅ What's Been Set Up

### 1. LearnQwest Directory Structure
Created at `/home/user/LearnQwest/`:
```
/home/user/LearnQwest/
├── ADA/
│   ├── core_assistant.py       (Sample Python module)
│   ├── config.json            (Configuration file)
│   └── modules/
│       ├── nlp/
│       ├── reasoning/
│       └── memory/
├── Projects/
│   └── AIAssistant/
│       └── README.md
├── Documentation/
│   ├── guides/
│   │   └── getting-started.md
│   ├── api/
│   └── architecture/
├── Data/
│   ├── datasets/
│   └── exports/
├── Logs/
└── Scripts/
    ├── automation/
    └── utilities/

/home/user/DROPZONE_INBOX/
├── sample_data.csv         (Sample CSV data)
├── notes.md               (Markdown notes)
└── research_paper.txt     (Text document)
```

### 2. Upgraded AI Agents (Gemini 2.0 Flash Experimental)

All four agents upgraded to use **`gemini-2.0-flash-exp`** for superior reasoning:

1. **`learnqwest_filesystem_agent`** - File and directory management
2. **`learnqwest_documentation_agent`** - Documentation generation
3. **`learnqwest_workflow_agent`** - Workflow automation
4. **`learnqwest_orchestrator`** - Multi-agent coordinator

### 3. Test Scripts Created

- `quick_test.py` - Python test script (for direct agent testing)
- `test_learnqwest_agents.py` - Comprehensive async test suite
- `run_learnqwest_test.sh` - Shell script to start ADK server

### 4. Configuration Files

- `app/.env` - Environment configuration
- `.claude/mcp-config.example.json` - MCP filesystem configuration example

---

## 🚀 How to Test the Agents (Uses Your $980 Credits)

### Option 1: Start ADK Server & Test via API (RECOMMENDED)

This is the proper way to test the agents:

```bash
# 1. Start the ADK API server
./run_learnqwest_test.sh

# Server will start at http://127.0.0.1:8000
# Press Ctrl+C to stop when done
```

Then in another terminal:

```bash
# 2. Test an agent via HTTP API
curl -X POST http://127.0.0.1:8000/agents/learnqwest_filesystem_agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Analyze the files in /home/user/DROPZONE_INBOX and provide recommendations for organizing them"
  }'
```

### Option 2: Use the Frontend (Full Stack)

```bash
# 1. Start both backend and frontend
make dev

# 2. Open http://localhost:3000
# 3. Chat with the LearnQwest agents through the UI
```

### Option 3: Deploy to Vertex AI (Production)

```bash
# Requires Google Cloud authentication
# Uses your $980 credits for deployment + hosting

make deploy-adk
```

---

## 💰 Credit Usage Estimates

### Testing Locally (Option 1 or 2):
- **Per agent call**: $0.02 - $0.10
- **10 test calls**: $0.20 - $1.00
- **100 test calls**: $2.00 - $10.00

### Deploying to Vertex AI (Option 3):
- **Deployment**: $0.00 (one-time, free)
- **Hosting**: ~$0.50/hour when idle
- **API calls**: $0.02 - $0.10 per call
- **Monthly cost (light usage)**: $10-50

**With $980 in credits, you can:**
- Make **10,000+ agent calls** locally
- Run **production deployment** for **~20-30 days** with moderate usage
- Plenty of headroom for experimentation!

---

## 🎯 What Each Agent Does

### 1. Filesystem Agent
```bash
# Example tasks:
- "Analyze all files in DROPZONE_INBOX"
- "Organize files by type into LearnQwest directories"
- "Create a file inventory report"
- "Search for Python files containing 'import google'"
```

### 2. Documentation Agent
```bash
# Example tasks:
- "Create a README for /home/user/LearnQwest/Projects/AIAssistant"
- "Generate API documentation from core_assistant.py"
- "Write a getting started guide for new users"
- "Create architecture documentation for the LearnQwest system"
```

### 3. Workflow Agent
```bash
# Example tasks:
- "Design a workflow to automatically process DROPZONE_INBOX files"
- "Create a workflow for automated documentation updates"
- "Set up a file routing system based on file types"
- "Design an integration workflow for external data sources"
```

### 4. Orchestrator Agent
```bash
# Example tasks (coordinates multiple agents):
- "Set up a complete new project with files, docs, and workflows"
- "Analyze DROPZONE_INBOX, create docs, and set up automated workflows"
- "Build a comprehensive project workspace from scratch"
```

---

## 📊 Agent Capabilities with Upgraded Model

**Gemini 2.0 Flash Experimental** provides:

✅ **Superior reasoning** - Better task decomposition and planning
✅ **Longer context** - Handle larger files and more complex queries
✅ **Better code generation** - More accurate Python/documentation generation
✅ **Improved thinking** - Built-in planning with detailed reasoning
✅ **Faster responses** - Optimized flash model architecture

---

## 🔧 Troubleshooting

### Server won't start?
```bash
# Check if dependencies are installed
make install

# Verify environment
cat app/.env

# Try starting manually
uv run adk api_server app --allow_origins="*"
```

### Agent errors?
```bash
# Check logs
tail -f logs/*.log

# Verify Google Cloud authentication
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

### Need to change the model?
Edit `app/learnqwest_agents.py`:
```python
# Change this line (line 20):
LEARNQWEST_MODEL = "gemini-2.0-flash-exp"

# Options:
# - "gemini-2.0-flash-exp" (current - best performance)
# - "gemini-1.5-pro" (more expensive, even better quality)
# - "gemini-2.5-flash" (cheaper, still good)
```

---

## 📚 Documentation

- **Complete Guide**: See `LEARNQWEST_AGENTS_DOCUMENTATION.md`
- **MCP Setup**: See `LEARNQWEST_MCP_SETUP_GUIDE.md`
- **Main README**: See `README.md` (updated with LearnQwest section)

---

## 🎉 You're Ready!

Everything is set up and ready to use your $980 in Google Cloud credits!

**Quick Start:**
```bash
# Start the server
./run_learnqwest_test.sh

# In another terminal, test an agent
curl -X POST http://127.0.0.1:8000/agents/learnqwest_filesystem_agent/run \
  -H "Content-Type: application/json" \
  -d '{"input": "List all files in /home/user/DROPZONE_INBOX"}'
```

Happy testing! 🚀
