"""Worklog data schemas and types."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class TaskStatus(Enum):
    """Task execution status."""
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskType(Enum):
    """Types of tasks in worklogs."""
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    DEBUGGING = "debugging"
    DEPLOYMENT = "deployment"
    DOCUMENTATION = "documentation"
    DATA_PROCESSING = "data_processing"
    ANALYTICS = "analytics"
    PLANNING = "planning"
    RESEARCH = "research"


@dataclass
class TaskMetadata:
    """Metadata extracted from task execution."""
    task_id: str
    task_type: TaskType
    status: TaskStatus

    # Timing
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None

    # Agent info
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None

    # Context
    files_modified: List[str] = field(default_factory=list)
    lines_changed: int = 0
    tests_run: int = 0
    tests_passed: int = 0

    # Outcome
    success: bool = False
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

    # Metadata
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "status": self.status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "files_modified": self.files_modified,
            "lines_changed": self.lines_changed,
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "success": self.success,
            "error_message": self.error_message,
            "warnings": self.warnings,
            "tags": self.tags,
            "dependencies": self.dependencies,
        }


@dataclass
class WorklogEntrySchema:
    """Structured worklog entry schema."""
    entry_id: str
    timestamp: datetime
    raw_content: str

    # Extracted structured data
    tasks: List[TaskMetadata] = field(default_factory=list)

    # Agent interactions
    agent_collaborations: List[str] = field(default_factory=list)

    # Resources
    resource_usage: Dict[str, float] = field(default_factory=dict)

    # Sentiment/tone (for natural language logs)
    sentiment_score: Optional[float] = None  # -1.0 to 1.0
    confidence_score: Optional[float] = None  # 0.0 to 1.0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp.isoformat(),
            "raw_content": self.raw_content,
            "tasks": [task.to_dict() for task in self.tasks],
            "agent_collaborations": self.agent_collaborations,
            "resource_usage": self.resource_usage,
            "sentiment_score": self.sentiment_score,
            "confidence_score": self.confidence_score,
        }
