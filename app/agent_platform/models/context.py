"""
Universal Context Protocol models.

All agents share context through a unified graph structure.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ContextType(str, Enum):
    """Types of context nodes in the graph."""

    # Personal context
    HEALTH = "health"
    FINANCE = "finance"
    SCHEDULE = "schedule"
    GOAL = "goal"
    HABIT = "habit"

    # Work context
    PROJECT = "project"
    TASK = "task"
    CODE = "code"
    MEETING = "meeting"

    # Learning context
    SKILL = "skill"
    LEARNING_PATH = "learning_path"
    RESOURCE = "resource"
    JOURNAL_ENTRY = "journal_entry"

    # Social context
    PERSON = "person"
    RELATIONSHIP = "relationship"
    NETWORK = "network"

    # System context
    AGENT = "agent"
    EVENT = "event"
    INSIGHT = "insight"
    PATTERN = "pattern"

    # Generic
    ENTITY = "entity"


class RelationType(str, Enum):
    """Types of relationships between context nodes."""

    # Temporal
    BEFORE = "before"
    AFTER = "after"
    DURING = "during"

    # Causal
    CAUSES = "causes"
    CAUSED_BY = "caused_by"
    INFLUENCES = "influences"

    # Hierarchical
    PARENT_OF = "parent_of"
    CHILD_OF = "child_of"
    PART_OF = "part_of"

    # Associative
    RELATED_TO = "related_to"
    SIMILAR_TO = "similar_to"
    DEPENDS_ON = "depends_on"

    # Agent-specific
    CREATED_BY = "created_by"
    PROCESSED_BY = "processed_by"
    OBSERVED_BY = "observed_by"

    # Custom
    CUSTOM = "custom"


class ContextNode(BaseModel):
    """A node in the universal context graph."""

    node_id: str
    node_type: ContextType
    label: str
    properties: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str | None = None  # Agent that created this node
    tags: list[str] = Field(default_factory=list)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class ContextRelationship(BaseModel):
    """A relationship between two context nodes."""

    from_node_id: str
    to_node_id: str
    relation_type: RelationType | str
    properties: dict[str, Any] = Field(default_factory=dict)
    weight: float = 1.0  # Strength of relationship
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str | None = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class ContextQuery(BaseModel):
    """Query the context graph."""

    query_type: str  # "cypher", "pattern", "temporal", "causal"
    query: str | dict[str, Any]
    parameters: dict[str, Any] = Field(default_factory=dict)
    limit: int = 100
    include_relationships: bool = True


class ContextUpdate(BaseModel):
    """Update or create context."""

    operation: str  # "create", "update", "delete", "merge"
    node: ContextNode | None = None
    relationship: ContextRelationship | None = None
    nodes: list[ContextNode] = Field(default_factory=list)
    relationships: list[ContextRelationship] = Field(default_factory=list)


class Insight(BaseModel):
    """An insight derived from context analysis."""

    insight_id: str
    title: str
    description: str
    insight_type: str  # "correlation", "pattern", "anomaly", "prediction"
    confidence: float  # 0.0 to 1.0
    supporting_data: dict[str, Any] = Field(default_factory=dict)
    affected_nodes: list[str] = Field(default_factory=list)
    generated_by: str  # Agent that generated this
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actionable: bool = False
    actions: list[dict[str, Any]] = Field(default_factory=list)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
