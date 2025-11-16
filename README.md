# Claude Fullstack Deploy Tutorial

Production-ready fullstack template showing how to wire an Anthropic Claude backend to a modern Next.js frontend with streaming responses and local development.

This repo contains:

- Backend: Python app using Anthropic Claude to run a goal-planning LLM agent
- Frontend: Next.js app with a chat UI, activity timeline, and SSE streaming
- Make targets and scripts to run locally

## Quickstart

Prerequisites:

- Python 3.10–3.12
- Node.js 18+ (recommended: LTS)
- uv (installed automatically by Makefile if missing)
- Anthropic API key ([get one here](https://console.anthropic.com/))

Setup and run locally (backend + frontend):

```bash
make install
cp app/.env.example app/.env
# Edit app/.env and add your ANTHROPIC_API_KEY
make dev
```

By default the frontend runs at `http://localhost:3000` and proxies chat requests to the local backend at `http://127.0.0.1:8000` via `nextjs/src/app/api/run_sse/route.ts`.

## Features

- Goal-planning LLM agent powered by **Claude Sonnet 4.5** (`app/agent.py`)
- Real-time SSE streaming for responsive chat experience
- Chat UI with message list, streaming content, and activity timeline
- Health checks and helpful error formatting
- Session-based conversation history

## Tech Stack

- Backend: Python, `anthropic`, `fastapi`, `uvicorn`, `python-dotenv`
- Frontend: Next.js 15, React 19, TailwindCSS, shadcn/ui
- Tooling: `uv` for Python deps, ESLint + Jest for the frontend, Ruff + Mypy for backend linting/type-checking

## Project Structure

```
app/                       # Python backend
  agent.py                 # Claude agent wrapper (goal-planning)
  api_server.py            # FastAPI server with SSE streaming
  config.py                # Environment configuration
  .env.example             # Example environment variables

nextjs/                    # Next.js frontend
  src/app/api/health       # Proxies health checks to backend
  src/app/api/run_sse      # Streaming endpoint
  src/lib/config.ts        # Env detection + endpoint resolution
  src/lib/handlers/        # Streaming handlers
  src/components/chat/     # Chat UI and timeline components

Makefile                   # install/dev/lint targets
pyproject.toml             # Python deps and linters
```

## Backend

### Agent

`app/agent.py` defines a `ClaudeAgent` class that wraps the Anthropic API. It accepts a high-level goal and produces a structured plan and execution steps using **Claude Sonnet 4.5** (the latest and most capable Claude model).

The agent has both synchronous and asynchronous interfaces, with support for streaming responses.

### Environment

Create `app/.env` with at least the following for local development:

```bash
# Required: Your Anthropic API Key
# Get one from: https://console.anthropic.com/
ANTHROPIC_API_KEY=your-api-key-here

# Optional: Agent name (default: goal-planning-agent)
AGENT_NAME=goal-planning-agent

# Optional: Claude model to use (default: claude-sonnet-4-5-20250929)
MODEL=claude-sonnet-4-5-20250929
# Other options:
# - claude-sonnet-4-5-20250929 (latest, most capable)
# - claude-opus-4-20250514 (most powerful, slower)
# - claude-3-5-sonnet-20241022 (previous generation)

# Optional: API server settings (default: 127.0.0.1:8000)
API_HOST=127.0.0.1
API_PORT=8000
```

Notes:

- Configuration is validated when the server starts in `app/config.py`
- The server will not start without a valid `ANTHROPIC_API_KEY`

### Run the backend (dev)

The Makefile starts the FastAPI server for you:

```bash
make dev-backend
# or run both backend and frontend together
make dev
```

This uses `uv run python app/api_server.py` which serves the FastAPI HTTP API at `http://127.0.0.1:8000`.

The backend provides these endpoints:
- `GET /` - Health check and server info
- `GET /health` - Detailed health check
- `POST /run_sse` - SSE streaming endpoint for chat
- `GET /sessions/{session_id}/history` - Get session history
- `DELETE /sessions/{session_id}` - Clear session history

## Frontend

### Environment

Create `nextjs/.env.local`:

Local backend (default):

```bash
BACKEND_URL=http://127.0.0.1:8000
NODE_ENV=development
```

The frontend will automatically use the local backend at `http://127.0.0.1:8000`.

### Run the frontend (dev)

```bash
npm --prefix nextjs install
npm --prefix nextjs run dev
```

Open `http://localhost:3000`.

## Streaming Architecture

- API route `nextjs/src/app/api/run_sse/route.ts` orchestrates streaming and delegates to:
  - `run-sse-local-backend-handler.ts` for local backend
- The backend streams Claude's response in real-time using Server-Sent Events (SSE)
- The frontend processes the SSE stream and renders incremental text updates

## Lint and Type-Check

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

## Health Checks

`GET /api/health` on the frontend forwards to the backend health endpoint (`/health`). Configure backend URL via env as described above.

## Model Upgrade

This project uses **Claude Sonnet 4.5** (`claude-sonnet-4-5-20250929`), which is:
- The latest and most capable Claude model as of January 2025
- More advanced than previous Sonnet and Opus versions
- Optimized for complex reasoning and planning tasks

To use a different model, set the `MODEL` environment variable in `app/.env`.

## Troubleshooting

- **Missing API key**: Ensure `ANTHROPIC_API_KEY` is set in `app/.env`. Get one from [Anthropic Console](https://console.anthropic.com/).
- **Local streaming issues**: Verify `BACKEND_URL` in `nextjs/.env.local` and that `make dev-backend` is running.
- **Import errors**: Run `uv sync` to install all dependencies.

## License

Apache-2.0 (unless noted otherwise in third-party files).
