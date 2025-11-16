"""
Goal Planning Agent using Anthropic Claude

This agent takes goals and breaks them down into actionable tasks and subtasks.
"""

from datetime import datetime, timezone
from typing import AsyncIterator, Iterator

from anthropic import Anthropic, AsyncAnthropic
from anthropic.types import MessageStreamEvent, TextBlock

from app.config import config

# System prompt for the goal planning agent
AGENT_SYSTEM_PROMPT = f"""
You are an intelligent goal planning and execution agent.
Your primary function is to take any user goal or request and systematically
break it down into concrete, actionable tasks and subtasks.

**Your Core Capabilities:**
1. **Goal Analysis**: Understand and analyze user goals, requests, or questions
2. **Task Decomposition**: Break down complex goals into logical, sequential tasks
3. **Subtask Creation**: Further decompose tasks into specific, actionable subtasks
4. **Planning & Execution**: Create detailed execution plans with clear steps
5. **Progress Tracking**: Monitor and report on task completion progress

**Your Planning Process:**
1. **Understand the Goal**: Carefully analyze what the user wants to achieve
2. **Break Down into Tasks**: Identify the main tasks needed to accomplish the goal
3. **Create Subtasks**: For each task, create specific, actionable subtasks
4. **Prioritize & Sequence**: Determine the optimal order of execution
5. **Execute & Monitor**: Work through the plan systematically
6. **Adapt & Refine**: Adjust the plan based on progress and feedback

**Task Creation Guidelines:**
- Tasks should be specific and measurable
- Include clear success criteria for each task
- Consider dependencies between tasks
- Estimate time/effort required
- Identify potential obstacles and mitigation strategies

**Response Format:**
When given a goal, structure your response as:

## Goal Analysis
[Clear understanding of what the user wants to achieve]

## Task Breakdown
### Task 1: [Task Name]
- **Description**: [What needs to be done]
- **Subtasks**:
  - [ ] Subtask 1.1: [Specific action]
  - [ ] Subtask 1.2: [Specific action]
- **Success Criteria**: [How to know it's complete]
- **Dependencies**: [What needs to be done first]

### Task 2: [Task Name]
[Similar format...]

## Execution Plan
[Step-by-step plan with timeline and priorities]

## Next Steps
[Immediate actions to take]

**Current Context:**
- Current date: {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
- You have advanced reasoning capabilities
- Always be thorough in your planning and consider multiple approaches
- Ask clarifying questions if the goal is ambiguous

Remember: Your strength is in systematic planning and breaking down complexity into manageable parts. Use your reasoning process to ensure comprehensive and well-structured plans.
"""


class ClaudeAgent:
    """
    Goal Planning Agent using Anthropic's Claude.

    This agent provides both synchronous and asynchronous interfaces
    for interacting with Claude.
    """

    def __init__(self):
        """Initialize the Claude agent with API credentials."""
        self.client = Anthropic(api_key=config.anthropic_api_key)
        self.async_client = AsyncAnthropic(api_key=config.anthropic_api_key)
        self.model = config.model
        self.system_prompt = AGENT_SYSTEM_PROMPT

    def chat(self, message: str, max_tokens: int = 4096) -> str:
        """
        Send a message to Claude and get a response.

        Args:
            message: The user's message/goal
            max_tokens: Maximum tokens in the response

        Returns:
            Claude's response as a string
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": message}],
        )

        # Extract text from response
        content_blocks = response.content
        text_blocks = [block for block in content_blocks if isinstance(block, TextBlock)]
        return "".join(block.text for block in text_blocks)

    def stream_chat(
        self, message: str, max_tokens: int = 4096
    ) -> Iterator[MessageStreamEvent]:
        """
        Stream a response from Claude.

        Args:
            message: The user's message/goal
            max_tokens: Maximum tokens in the response

        Yields:
            Stream events from Claude
        """
        with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": message}],
        ) as stream:
            for event in stream:
                yield event

    async def async_chat(self, message: str, max_tokens: int = 4096) -> str:
        """
        Async version of chat.

        Args:
            message: The user's message/goal
            max_tokens: Maximum tokens in the response

        Returns:
            Claude's response as a string
        """
        response = await self.async_client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": message}],
        )

        # Extract text from response
        content_blocks = response.content
        text_blocks = [block for block in content_blocks if isinstance(block, TextBlock)]
        return "".join(block.text for block in text_blocks)

    async def async_stream_chat(
        self, message: str, max_tokens: int = 4096
    ) -> AsyncIterator[MessageStreamEvent]:
        """
        Async streaming version of chat.

        Args:
            message: The user's message/goal
            max_tokens: Maximum tokens in the response

        Yields:
            Stream events from Claude
        """
        async with self.async_client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": message}],
        ) as stream:
            async for event in stream:
                yield event


# Create a singleton instance
root_agent = ClaudeAgent()
