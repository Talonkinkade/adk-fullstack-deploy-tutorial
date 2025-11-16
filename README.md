# ADK Fullstack Deploy Tutorial

Production-ready fullstack template showing how to wire a Python ADK backend to a modern Next.js frontend with streaming responses, local development, and deployment paths to Vertex AI Agent Engine and Vercel.

This repo contains:

- Backend: Python app using Google ADK to run a goal-planning LLM agent
- Frontend: Next.js app with a chat UI, activity timeline, and SSE streaming
- Make targets and scripts to run locally and deploy

## Quickstart

Prerequisites:

- Python 3.10–3.12
- Node.js 18+ (recommended: LTS)
- uv (installed automatically by Makefile if missing)
- Google Cloud SDK for cloud deployment

Setup and run locally (backend + frontend):

```bash
make install
cp app/.env.example app/.env  # if present, otherwise see Backend env below
make dev
```

By default the frontend runs at `http://localhost:3000` and proxies chat requests to the local ADK backend at `http://127.0.0.1:8000` via `nextjs/src/app/api/run_sse/route.ts`.

## Features

- Goal-planning LLM agent powered by Google ADK (`app/agent.py`)
- **LearnQwest Agents**: Suite of specialized agents for filesystem, documentation, and workflow automation (`app/learnqwest_agents.py`)
- Environment-driven routing to either local backend or Vertex AI Agent Engine
- Robust SSE pipeline with JSON-fragment processing for Agent Engine
- Chat UI with message list, streaming content, and activity timeline
- Health checks and helpful error formatting
- **MCP Filesystem Integration**: Secure file access through Model Context Protocol

## Tech Stack

- Backend: Python, `google-adk`, `vertexai`, `python-dotenv`
- Frontend: Next.js 15, React 19, TailwindCSS, shadcn/ui
- Tooling: `uv` for Python deps, ESLint + Jest for the frontend, Ruff + Mypy for backend linting/type-checking

## Project Structure

```
app/                       # Python ADK backend
  agent.py                 # Root agent definition (goal-planning)
  agent_engine_app.py      # Deployment helper for Vertex AI Agent Engine
  config.py                # Env loading, Vertex init, deployment config
  utils/                   # GCS + tracing helpers

nextjs/                    # Next.js frontend
  src/app/api/health       # Proxies health checks to backend
  src/app/api/run_sse      # Streaming endpoint (local or Agent Engine)
  src/lib/config.ts        # Env detection + endpoint resolution
  src/lib/handlers/        # Streaming handlers (local/agent-engine)
  src/components/chat/     # Chat UI and timeline components

Makefile                   # install/dev/lint + Agent Engine deploy helper
pyproject.toml             # Python deps and linters
```

## Backend

### Agent

`app/agent.py` defines an ADK `LlmAgent` with built-in planning enabled. It accepts a high-level goal and produces a structured plan and execution steps. The model defaults to `gemini-2.5-flash` and can be changed via env.

### Environment

Create `app/.env` with at least the following for local development and deployment:

```bash
# Required
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Staging bucket for Vertex AI/Agent Engine packaging
# Provide a valid bucket identifier. Example: my-staging-bucket
# (Do not include gs:// prefix.)
GOOGLE_CLOUD_STAGING_BUCKET=my-staging-bucket

# Optional
MODEL=gemini-2.5-flash
AGENT_NAME=goal-planning-agent
EXTRA_PACKAGES=./app
REQUIREMENTS_FILE=.requirements.txt
```

Notes:

- Configuration is validated at import time in `app/config.py` and initializes Vertex AI.
- The Makefile’s deploy target will generate `.requirements.txt` for Agent Engine using `uv export`.

### Run the backend (dev)

The Makefile starts the ADK API server for you:

```bash
make dev-backend
# or run both backend and frontend together
make dev
```

This uses `uv run adk api_server app --allow_origins="*"` which serves the ADK HTTP API at `http://127.0.0.1:8000`.

## Frontend

### Environment

Create `nextjs/.env.local`:

Local backend (default):

```bash
BACKEND_URL=http://127.0.0.1:8000
NODE_ENV=development
```

Agent Engine (direct streaming):

```bash
AGENT_ENGINE_ENDPOINT=https://us-central1-aiplatform.googleapis.com/v1/projects/your-project/locations/us-central1/reasoningEngines/YOUR_ENGINE_ID

# Required when calling Agent Engine directly (e.g. Vercel):
# Base64-encoded service account JSON with permissions for Agent Engine
GOOGLE_SERVICE_ACCOUNT_KEY_BASE64=eyJ0eXAiOiJKV1QiLCJh...  # base64 JSON

NODE_ENV=production
```

Cloud Run (if you host your own proxy backend):

```bash
CLOUD_RUN_SERVICE_URL=https://your-service-url.a.run.app
NODE_ENV=production
```

The frontend auto-detects the deployment mode in `nextjs/src/lib/config.ts` and will:

- Use Agent Engine when `AGENT_ENGINE_ENDPOINT` is set
- Use Cloud Run when `CLOUD_RUN_SERVICE_URL` (or Cloud env vars) are present
- Default to local backend otherwise

### Run the frontend (dev)

```bash
npm --prefix nextjs install
npm --prefix nextjs run dev
```

Open `http://localhost:3000`.

## Streaming Architecture

- API route `nextjs/src/app/api/run_sse/route.ts` orchestrates streaming and delegates to:
  - `run-sse-local-backend-handler.ts` for local ADK backend
  - `run-sse-agent-engine-handler.ts` when using Agent Engine
- For Agent Engine, JSON fragments are transformed into SSE format on the server so the UI can render incremental `text` and `thought` parts consistently.

## Lint, Type-Check, and Tests

Python (from repo root):

```bash
make lint
```

Node/TypeScript (from repo root):

```bash
npm --prefix nextjs run lint
npm --prefix nextjs run test
```

Tip: Prefer linting and type-checking for fast feedback during development instead of full builds.

## Deployments

### Deploy the Agent to Vertex AI Agent Engine

Prerequisites:

- `gcloud auth application-default login`
- `gcloud config set project YOUR_PROJECT_ID`
- A GCS bucket for packaging (match `GOOGLE_CLOUD_STAGING_BUCKET` in `app/.env`)

Deploy:

```bash
make deploy-adk
```

What it does:

- Exports Python dependencies to `.requirements.txt` using uv
- Packages and deploys the ADK app via `app/agent_engine_app.py`
- Creates a logs/data bucket for artifacts if missing
- Outputs deployment metadata to `logs/deployment_metadata.json`

After deployment, set `AGENT_ENGINE_ENDPOINT` in `nextjs/.env.local` with the returned Reasoning Engine endpoint to stream from Agent Engine directly.

### Deploy the Frontend (Vercel)

Use `NEXTJS_VERCEL_DEPLOYMENT_GUIDE.md` for step-by-step instructions. In short:

- Set environment variables in Vercel (at minimum `AGENT_ENGINE_ENDPOINT` and `GOOGLE_SERVICE_ACCOUNT_KEY_BASE64` if using Agent Engine)
- Push your repo and import the `nextjs` app into Vercel

## Health Checks

`GET /api/health` on the frontend forwards to the backend health endpoint (`/health`). Configure backend URL/endpoint via env as described above.

## LearnQwest Agents

This repository includes a comprehensive suite of specialized AI agents designed for the LearnQwest ecosystem:

### Available Agents

1. **LearnQwest Filesystem Agent** (`learnqwest-filesystem-agent`)
   - Intelligent file and directory management
   - File organization, reading, writing, and analysis
   - Secure operations with built-in safety checks

2. **LearnQwest Documentation Agent** (`learnqwest-documentation-agent`)
   - Automated documentation generation and maintenance
   - Creates README files, API docs, guides, and tutorials
   - Maintains consistent formatting and best practices

3. **LearnQwest Workflow Agent** (`learnqwest-workflow-agent`)
   - Designs and automates workflows
   - Integrates different tools and systems
   - Optimizes repetitive tasks

4. **LearnQwest Orchestrator Agent** (`learnqwest-orchestrator`)
   - Master coordinator for complex multi-agent tasks
   - Orchestrates filesystem, documentation, and workflow agents
   - Handles end-to-end task completion

### Quick Start with LearnQwest Agents

1. **Set up MCP Filesystem** (for Claude Desktop/Cursor):
   ```bash
   # See LEARNQWEST_MCP_SETUP_GUIDE.md for complete instructions
   ```

2. **Import LearnQwest agents** in your code:
   ```python
   from app.learnqwest_agents import (
       learnqwest_filesystem_agent,
       learnqwest_documentation_agent,
       learnqwest_workflow_agent,
       learnqwest_orchestrator_agent,
   )
   ```

3. **Use an agent:**
   ```python
   # Example: Use the orchestrator for complex tasks
   response = learnqwest_orchestrator_agent.run(
       "Set up a new Python project with documentation and workflows"
   )
   ```

### Documentation

- **Complete Agent Documentation**: See `LEARNQWEST_AGENTS_DOCUMENTATION.md`
- **MCP Setup Guide**: See `LEARNQWEST_MCP_SETUP_GUIDE.md`

The LearnQwest agents integrate seamlessly with the MCP Filesystem Server to provide secure, intelligent file management and automation capabilities.

## Troubleshooting

- Missing Google Cloud envs: `app/config.py` validates env on import. Ensure `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `GOOGLE_CLOUD_STAGING_BUCKET` are set in `app/.env`.
- Authentication for Agent Engine from the frontend requires `GOOGLE_SERVICE_ACCOUNT_KEY_BASE64` with correct scopes.
- Local streaming issues: verify `BACKEND_URL` in `nextjs/.env.local` and that `make dev-backend` is running.

## License

Apache-2.0 (unless noted otherwise in third-party files).
