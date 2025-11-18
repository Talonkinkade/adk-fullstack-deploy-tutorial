"""
ADA - Autonomous Development Architect
Crew Orchestration System for AI Agent Management

This module provides the core orchestration logic for forming and managing
AI agent crews across complex multi-step tasks.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import uuid


class AgentRole(Enum):
    """Available agent types in the ADA ecosystem"""
    ARCHITECT = "Claude-Code"  # Planning, architecture, orchestration
    GENERATOR = "Aider"  # Code implementation, refactoring
    VALIDATOR = "Windsurf"  # Testing, validation, quality checks
    PARSER = "Parser-Ion"  # Documentation, parsing, analysis
    SPECIALIST = "Cline"  # Specialized tasks, research


class AgentStatus(Enum):
    """Status of an agent's task execution"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"
    BLOCKED = "blocked"


class CoordinationMode(Enum):
    """How agents coordinate their work"""
    SEQUENTIAL = "sequential"  # Agent A → B → C (handoffs)
    PARALLEL = "parallel"  # Agents work simultaneously
    DYNAMIC = "dynamic"  # Spawn agents as needed


class CrewType(Enum):
    """Types of agent crews that can be formed"""
    SOLO = "solo"  # Single agent
    SEQUENTIAL_CREW = "sequential"  # Pipeline of agents
    PARALLEL_CREW = "parallel"  # Concurrent agents with sync point
    TASK_FORCE = "task_force"  # Dynamic spawning crew


@dataclass
class AgentTask:
    """Represents a task assigned to an agent"""
    agent_role: AgentRole
    task_description: str
    input_files: List[str] = field(default_factory=list)
    output_files: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    time_budget_minutes: int = 60
    status: AgentStatus = AgentStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    handoff_notes: str = ""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def start(self) -> None:
        """Mark task as started"""
        self.status = AgentStatus.IN_PROGRESS
        self.started_at = datetime.now()

    def complete(self, handoff_notes: str = "") -> None:
        """Mark task as completed"""
        self.status = AgentStatus.COMPLETE
        self.completed_at = datetime.now()
        self.handoff_notes = handoff_notes

    def fail(self, reason: str) -> None:
        """Mark task as failed"""
        self.status = AgentStatus.FAILED
        self.handoff_notes = f"FAILED: {reason}"

    @property
    def duration_minutes(self) -> Optional[int]:
        """Calculate task duration in minutes"""
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            return int(delta.total_seconds() / 60)
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "task_id": self.task_id,
            "agent_role": self.agent_role.value,
            "task_description": self.task_description,
            "input_files": self.input_files,
            "output_files": self.output_files,
            "success_criteria": self.success_criteria,
            "time_budget_minutes": self.time_budget_minutes,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_minutes": self.duration_minutes,
            "handoff_notes": self.handoff_notes,
        }


@dataclass
class Crew:
    """Represents a team of agents working together"""
    crew_name: str
    crew_type: CrewType
    coordination_mode: CoordinationMode
    agents: List[AgentTask] = field(default_factory=list)
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: datetime = field(default_factory=datetime.now)
    max_concurrent_agents: int = 5

    def add_agent(self, task: AgentTask) -> None:
        """Add an agent task to the crew"""
        self.agents.append(task)

    def get_next_pending_agent(self) -> Optional[AgentTask]:
        """Get the next agent that needs to run (for sequential mode)"""
        for agent in self.agents:
            if agent.status == AgentStatus.PENDING:
                return agent
        return None

    def get_active_agents(self) -> List[AgentTask]:
        """Get all currently active agents"""
        return [a for a in self.agents if a.status == AgentStatus.IN_PROGRESS]

    def get_completed_agents(self) -> List[AgentTask]:
        """Get all completed agents"""
        return [a for a in self.agents if a.status == AgentStatus.COMPLETE]

    def is_complete(self) -> bool:
        """Check if all agents have completed their tasks"""
        return all(a.status == AgentStatus.COMPLETE for a in self.agents)

    def has_failures(self) -> bool:
        """Check if any agents have failed"""
        return any(a.status == AgentStatus.FAILED for a in self.agents)

    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage"""
        if not self.agents:
            return 0.0
        completed = len(self.get_completed_agents())
        return (completed / len(self.agents)) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "session_id": self.session_id,
            "crew_name": self.crew_name,
            "crew_type": self.crew_type.value,
            "coordination_mode": self.coordination_mode.value,
            "created_at": self.created_at.isoformat(),
            "max_concurrent_agents": self.max_concurrent_agents,
            "completion_percentage": self.completion_percentage,
            "is_complete": self.is_complete(),
            "has_failures": self.has_failures(),
            "agents": [agent.to_dict() for agent in self.agents],
        }


class ADAOrchestrator:
    """
    Main orchestrator for ADA crew management

    Responsibilities:
    - Analyze task complexity
    - Form appropriate crews
    - Generate agent prompts
    - Track progress
    - Handle dynamic spawning
    """

    def __init__(self, project_name: str, base_dir: Path):
        self.project_name = project_name
        self.base_dir = Path(base_dir)
        self.sessions_dir = self.base_dir / "docs" / "sessions" / "BMAD"
        self.workflows_dir = self.base_dir / "docs" / "workflows"
        self.active_crews: Dict[str, Crew] = {}

        # Ensure directories exist
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.workflows_dir.mkdir(parents=True, exist_ok=True)

    def analyze_task_complexity(
        self,
        goal: str,
        has_dependencies: bool = True,
        uncertainty_level: str = "low"
    ) -> CrewType:
        """
        Analyze task and determine appropriate crew type

        Args:
            goal: The session goal description
            has_dependencies: Whether tasks have sequential dependencies
            uncertainty_level: "low", "medium", or "high"

        Returns:
            Recommended CrewType
        """
        # Simple heuristic-based analysis
        words = goal.lower().split()

        # Check for complexity indicators
        complex_keywords = ["architecture", "design", "implement", "integrate", "deploy"]
        simple_keywords = ["fix", "update", "refactor", "document"]

        is_complex = any(kw in words for kw in complex_keywords)
        is_simple = any(kw in words for kw in simple_keywords) and len(words) < 10

        # Decision tree
        if is_simple and not has_dependencies:
            return CrewType.SOLO
        elif is_complex and uncertainty_level == "high":
            return CrewType.TASK_FORCE
        elif has_dependencies:
            return CrewType.SEQUENTIAL_CREW
        else:
            return CrewType.PARALLEL_CREW

    def form_crew(
        self,
        crew_name: str,
        crew_type: CrewType,
        coordination_mode: CoordinationMode,
    ) -> Crew:
        """
        Create a new crew

        Args:
            crew_name: Human-readable name for the crew
            crew_type: Type of crew to form
            coordination_mode: How agents coordinate

        Returns:
            Newly formed Crew
        """
        crew = Crew(
            crew_name=crew_name,
            crew_type=crew_type,
            coordination_mode=coordination_mode,
        )
        self.active_crews[crew.session_id] = crew
        return crew

    def generate_agent_prompt(
        self,
        task: AgentTask,
        session_id: str,
        crew_name: str,
        baseline_context: str,
        previous_agent_output: Optional[str] = None,
    ) -> str:
        """
        Generate a detailed prompt for an agent

        Args:
            task: The AgentTask to generate prompt for
            session_id: Session ID for tracking
            crew_name: Name of the crew this agent belongs to
            baseline_context: Context from BMAD baseline section
            previous_agent_output: Output from previous agent (for sequential crews)

        Returns:
            Formatted prompt string ready to send to agent
        """
        prompt = f"""# {task.agent_role.value} Mission Brief

**Session**: {session_id}
**Crew**: {crew_name}
**Your Role**: {task.agent_role.name}
**Task ID**: {task.task_id}

---

## Context (from BMAD Baseline)

{baseline_context}

---

## Your Specific Task

{task.task_description}

---

## Success Criteria (ALL must be met)

"""
        for i, criterion in enumerate(task.success_criteria, 1):
            prompt += f"{i}. ✅ {criterion}\n"

        prompt += f"""
---

## Input Files

"""
        if task.input_files:
            for file_path in task.input_files:
                prompt += f"- `{file_path}`\n"
        else:
            prompt += "- No input files specified\n"

        if previous_agent_output:
            prompt += f"""
---

## Handoff from Previous Agent

{previous_agent_output}

"""

        prompt += f"""
---

## Expected Deliverables

"""
        for file_path in task.output_files:
            prompt += f"- `{file_path}`\n"

        prompt += f"""
---

## Time Budget

**Allocated Time**: {task.time_budget_minutes} minutes

---

## Handoff Instructions

When you complete your task:

1. **Update BMAD**: Add your status to the [A] AGENT DISPATCH section
2. **Save Deliverables**: Ensure all files are saved to the correct paths
3. **Document Decisions**: Note any key decisions you made
4. **Signal Completion**: Update your task status and provide handoff notes

---

## BEGIN MISSION

You may now start your task. Good luck! 🚀
"""
        return prompt

    def spawn_specialist(
        self,
        crew: Crew,
        parent_task: AgentTask,
        specialist_role: str,
        specialist_task: str,
        output_files: List[str],
    ) -> AgentTask:
        """
        Dynamically spawn a specialist agent during execution

        Args:
            crew: The crew to add the specialist to
            parent_task: The task that spawned this specialist
            specialist_role: Description of specialist role
            specialist_task: What the specialist needs to do
            output_files: Expected outputs from specialist

        Returns:
            The newly spawned AgentTask
        """
        # Choose appropriate agent for the specialist role
        # This is a simple heuristic - could be more sophisticated
        if "database" in specialist_role.lower() or "schema" in specialist_role.lower():
            agent_role = AgentRole.GENERATOR
        elif "security" in specialist_role.lower() or "auth" in specialist_role.lower():
            agent_role = AgentRole.SPECIALIST
        elif "test" in specialist_role.lower():
            agent_role = AgentRole.VALIDATOR
        else:
            agent_role = AgentRole.SPECIALIST

        specialist_task_obj = AgentTask(
            agent_role=agent_role,
            task_description=f"[SPAWNED BY {parent_task.agent_role.value}] {specialist_task}",
            output_files=output_files,
            success_criteria=[f"Complete specialized task: {specialist_role}"],
            time_budget_minutes=30,
        )

        # Insert after parent task in the crew
        parent_index = crew.agents.index(parent_task)
        crew.agents.insert(parent_index + 1, specialist_task_obj)

        return specialist_task_obj

    def save_crew_manifest(self, crew: Crew) -> Path:
        """
        Save crew configuration to JSON file

        Args:
            crew: The crew to save

        Returns:
            Path to saved manifest file
        """
        manifest_path = self.sessions_dir / f"crew_manifest_{crew.session_id}.json"

        with open(manifest_path, "w") as f:
            json.dump(crew.to_dict(), f, indent=2)

        return manifest_path

    def load_crew_manifest(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load crew manifest from JSON file

        Args:
            session_id: Session ID to load

        Returns:
            Crew manifest dictionary or None if not found
        """
        manifest_path = self.sessions_dir / f"crew_manifest_{session_id}.json"

        if not manifest_path.exists():
            return None

        with open(manifest_path, "r") as f:
            return json.load(f)

    def get_crew_status_report(self, crew: Crew) -> str:
        """
        Generate a human-readable status report for a crew

        Args:
            crew: The crew to report on

        Returns:
            Formatted status report string
        """
        report = f"""
# Crew Status Report

**Crew**: {crew.crew_name}
**Session ID**: {crew.session_id}
**Type**: {crew.crew_type.value}
**Mode**: {crew.coordination_mode.value}
**Progress**: {crew.completion_percentage:.1f}%

## Agent Status

"""
        for i, agent in enumerate(crew.agents, 1):
            status_emoji = {
                AgentStatus.PENDING: "⏳",
                AgentStatus.IN_PROGRESS: "🔄",
                AgentStatus.COMPLETE: "✅",
                AgentStatus.FAILED: "❌",
                AgentStatus.BLOCKED: "⚠️",
            }[agent.status]

            report += f"{i}. {status_emoji} **{agent.agent_role.value}** ({agent.status.value})\n"
            report += f"   - Task: {agent.task_description[:60]}...\n"
            if agent.duration_minutes:
                report += f"   - Duration: {agent.duration_minutes}min\n"
            report += "\n"

        if crew.is_complete():
            report += "## 🎉 Crew Complete!\n\n"
            total_time = sum(
                a.duration_minutes for a in crew.agents if a.duration_minutes
            )
            report += f"Total time: {total_time} minutes\n"
        elif crew.has_failures():
            report += "## ⚠️ Crew Has Failures\n\n"
            failed_agents = [a for a in crew.agents if a.status == AgentStatus.FAILED]
            for agent in failed_agents:
                report += f"- {agent.agent_role.value}: {agent.handoff_notes}\n"

        return report


# Example usage / Factory functions

def create_content_pipeline_crew(orchestrator: ADAOrchestrator) -> Crew:
    """
    Factory function: Create a content pipeline crew for YouTube → TEKS alignment

    Example of Type B: Sequential Crew
    """
    crew = orchestrator.form_crew(
        crew_name="Content Pipeline Crew #1",
        crew_type=CrewType.SEQUENTIAL_CREW,
        coordination_mode=CoordinationMode.SEQUENTIAL,
    )

    # Agent 1: Fetch YouTube transcript
    crew.add_agent(AgentTask(
        agent_role=AgentRole.PARSER,
        task_description="Fetch YouTube video metadata and transcript",
        input_files=["user_provided_url.txt"],
        output_files=["data/transcript.json"],
        success_criteria=[
            "Video metadata retrieved successfully",
            "Full transcript extracted",
            "JSON file validates against schema",
        ],
        time_budget_minutes=15,
    ))

    # Agent 2: Structure transcript
    crew.add_agent(AgentTask(
        agent_role=AgentRole.PARSER,
        task_description="Clean and structure the raw transcript",
        input_files=["data/transcript.json"],
        output_files=["data/structured_content.md"],
        success_criteria=[
            "Transcript cleaned of noise",
            "Content organized into sections",
            "Markdown formatting correct",
        ],
        time_budget_minutes=10,
    ))

    # Agent 3: Generate summary
    crew.add_agent(AgentTask(
        agent_role=AgentRole.ARCHITECT,
        task_description="Generate summary with key concepts extracted",
        input_files=["data/structured_content.md"],
        output_files=["data/summary_with_concepts.md"],
        success_criteria=[
            "Summary is concise (< 500 words)",
            "Key concepts identified",
            "Educational value clear",
        ],
        time_budget_minutes=20,
    ))

    # Agent 4: TEKS alignment
    crew.add_agent(AgentTask(
        agent_role=AgentRole.SPECIALIST,
        task_description="Align concepts to TEKS standards",
        input_files=["data/summary_with_concepts.md", "data/teks_database.json"],
        output_files=["data/teks_aligned_lesson.json"],
        success_criteria=[
            "All concepts mapped to TEKS codes",
            "Grade level appropriate",
            "JSON schema validates",
        ],
        time_budget_minutes=30,
    ))

    # Final validation
    crew.add_agent(AgentTask(
        agent_role=AgentRole.VALIDATOR,
        task_description="Validate complete pipeline output",
        input_files=["data/teks_aligned_lesson.json"],
        output_files=["data/validation_report.md"],
        success_criteria=[
            "All files exist and are valid",
            "TEKS alignment accuracy > 95%",
            "No schema errors",
        ],
        time_budget_minutes=10,
    ))

    return crew


def create_backend_architecture_crew(orchestrator: ADAOrchestrator) -> Crew:
    """
    Factory function: Create a crew for backend architecture decision

    Example of Type B: Sequential Crew with decision-making
    """
    crew = orchestrator.form_crew(
        crew_name="Backend Architecture Pipeline",
        crew_type=CrewType.SEQUENTIAL_CREW,
        coordination_mode=CoordinationMode.SEQUENTIAL,
    )

    # Agent 1: Architecture comparison
    crew.add_agent(AgentTask(
        agent_role=AgentRole.ARCHITECT,
        task_description="Compare backend architectures (PostgreSQL, Neo4j, JSON) and recommend winner",
        input_files=["docs/requirements.md"],
        output_files=[
            "docs/architecture/backend-decision.md",
            "docs/architecture/cost-analysis.md",
        ],
        success_criteria=[
            "All 3 options evaluated on cost, performance, scalability",
            "Clear recommendation with rationale",
            "Implementation roadmap provided",
        ],
        time_budget_minutes=45,
    ))

    # Agent 2: Schema generation
    crew.add_agent(AgentTask(
        agent_role=AgentRole.GENERATOR,
        task_description="Generate database schema and ORM models for chosen architecture",
        input_files=["docs/architecture/backend-decision.md"],
        output_files=[
            "app/models/schema.sql",
            "app/models/user.py",
            "app/models/course.py",
            "app/models/teks.py",
        ],
        success_criteria=[
            "Schema matches requirements",
            "ORM models pass type-checking",
            "Relationships correctly defined",
        ],
        time_budget_minutes=60,
    ))

    # Agent 3: Integration tests
    crew.add_agent(AgentTask(
        agent_role=AgentRole.VALIDATOR,
        task_description="Write integration tests for ORM models",
        input_files=["app/models/*.py"],
        output_files=["tests/integration/test_models.py"],
        success_criteria=[
            "100% model method coverage",
            "All tests pass",
            "Edge cases covered",
        ],
        time_budget_minutes=30,
    ))

    return crew


if __name__ == "__main__":
    # Example: Create and use the orchestrator
    ada = ADAOrchestrator(
        project_name="LearnQwest-ADK-Fullstack",
        base_dir=Path("/home/user/adk-fullstack-deploy-tutorial")
    )

    # Analyze a task
    task_goal = "Decide on backend architecture and implement schema"
    crew_type = ada.analyze_task_complexity(
        goal=task_goal,
        has_dependencies=True,
        uncertainty_level="medium"
    )
    print(f"Recommended crew type: {crew_type}")

    # Form a crew
    crew = create_backend_architecture_crew(ada)

    # Save manifest
    manifest_path = ada.save_crew_manifest(crew)
    print(f"Crew manifest saved to: {manifest_path}")

    # Get status
    status_report = ada.get_crew_status_report(crew)
    print(status_report)

    # Simulate agent execution
    print("\n=== Simulating Agent Execution ===\n")

    # Agent 1 starts and completes
    agent1 = crew.agents[0]
    agent1.start()
    print(f"Agent 1 ({agent1.agent_role.value}) started...")

    # Generate prompt for agent 1
    prompt = ada.generate_agent_prompt(
        task=agent1,
        session_id=crew.session_id,
        crew_name=crew.crew_name,
        baseline_context="Current backend: None. Need to choose architecture.",
    )
    print(f"\nGenerated prompt for {agent1.agent_role.value}:")
    print(prompt[:200] + "...\n")

    # Complete agent 1
    agent1.complete(handoff_notes="PostgreSQL chosen. See docs/architecture/backend-decision.md for rationale.")

    # Status update
    print(ada.get_crew_status_report(crew))
