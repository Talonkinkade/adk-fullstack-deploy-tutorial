"""
FastAPI Server for Claude Agent

This server provides a compatible API interface for the Claude agent,
replacing the Google ADK API server.
"""

import json
from datetime import datetime
from typing import Dict, List

from anthropic.types import (
    ContentBlockDeltaEvent,
    ContentBlockStartEvent,
    MessageStartEvent,
    MessageStopEvent,
)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.agent import root_agent
from app.config import config

# Initialize FastAPI app
app = FastAPI(
    title=config.deployment_name,
    description="Goal Planning Agent powered by Claude",
    version="1.0.0",
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class MessagePart(BaseModel):
    """Part of a message (text content)"""

    text: str


class NewMessage(BaseModel):
    """New message from user"""

    parts: List[MessagePart]
    role: str = "user"


class RunSSERequest(BaseModel):
    """Request format for SSE streaming endpoint"""

    appName: str
    userId: str
    sessionId: str
    newMessage: NewMessage
    streaming: bool = True


# In-memory session storage
# In a production app, you'd use Redis or a database
sessions: Dict[str, List[Dict]] = {}


def get_session_history(session_id: str) -> List[Dict]:
    """Get chat history for a session"""
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]


def add_to_session_history(
    session_id: str, role: str, content: str, timestamp: str | None = None
) -> None:
    """Add a message to session history"""
    if session_id not in sessions:
        sessions[session_id] = []

    sessions[session_id].append(
        {
            "role": role,
            "content": content,
            "timestamp": timestamp or datetime.utcnow().isoformat(),
        }
    )


async def generate_sse_events(message: str, session_id: str, user_id: str):
    """
    Generate Server-Sent Events from Claude's streaming response.

    This mimics the ADK SSE format that the frontend expects.
    """
    # Add user message to history
    add_to_session_history(session_id, "user", message)

    # Track the assistant's response
    assistant_response = ""

    try:
        # Send initial connection event
        yield f"data: {json.dumps({'type': 'connection', 'status': 'connected'})}\n\n"

        # Stream from Claude
        async for event in root_agent.async_stream_chat(message):
            # Handle different event types from Anthropic streaming
            if isinstance(event, MessageStartEvent):
                # Message started
                yield f"data: {json.dumps({'type': 'message_start'})}\n\n"

            elif isinstance(event, ContentBlockStartEvent):
                # Content block started
                yield f"data: {json.dumps({'type': 'content_start', 'index': event.index})}\n\n"

            elif isinstance(event, ContentBlockDeltaEvent):
                # Text delta - this is the actual content
                if hasattr(event.delta, "text"):
                    text_chunk = event.delta.text
                    assistant_response += text_chunk

                    # Send text chunk in ADK-compatible format
                    yield f"data: {json.dumps({'type': 'text', 'text': text_chunk})}\n\n"

            elif isinstance(event, MessageStopEvent):
                # Message complete
                # Add assistant response to history
                add_to_session_history(session_id, "assistant", assistant_response)

                yield f"data: {json.dumps({'type': 'message_stop'})}\n\n"

        # Send completion event
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    except Exception as e:
        # Send error event
        error_msg = str(e)
        yield f"data: {json.dumps({'type': 'error', 'error': error_msg})}\n\n"


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "ok",
        "agent": config.deployment_name,
        "model": config.model,
        "message": "Claude Goal Planning Agent is running",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": config.deployment_name,
        "model": config.model,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/run_sse")
async def run_sse(request: RunSSERequest):
    """
    SSE streaming endpoint compatible with ADK format.

    This endpoint accepts the same request format as the ADK api_server
    and returns Server-Sent Events for real-time streaming.
    """
    try:
        # Extract message text from parts
        message_text = " ".join(part.text for part in request.newMessage.parts)

        if not message_text.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # Return streaming response
        return StreamingResponse(
            generate_sse_events(message_text, request.sessionId, request.userId),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/sessions/{session_id}/history")
async def get_session_history_endpoint(session_id: str):
    """Get chat history for a session"""
    return {"sessionId": session_id, "history": get_session_history(session_id)}


@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear a session's history"""
    if session_id in sessions:
        del sessions[session_id]
    return {"status": "ok", "message": f"Session {session_id} cleared"}


if __name__ == "__main__":
    import uvicorn

    print(f"\n🚀 Starting {config.deployment_name}")
    print(f"📍 Server: http://{config.host}:{config.port}")
    print(f"🤖 Model: {config.model}")
    print(f"📡 SSE Endpoint: http://{config.host}:{config.port}/run_sse")
    print("=" * 50)

    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info",
    )
