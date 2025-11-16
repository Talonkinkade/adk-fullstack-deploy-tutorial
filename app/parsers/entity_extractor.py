"""Entity Extractor - Extract named entities from logs and diaries.

Extracts:
- Agent names
- Task IDs
- File paths
- Technologies/tools mentioned
- People/team names
- Dates and timestamps
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Set


class EntityType(Enum):
    """Types of entities to extract."""
    AGENT = "agent"
    TASK_ID = "task_id"
    FILE_PATH = "file_path"
    TECHNOLOGY = "technology"
    PERSON = "person"
    TEAM = "team"
    DATE = "date"
    URL = "url"
    ERROR_TYPE = "error_type"


@dataclass
class ExtractedEntity:
    """An extracted entity with metadata."""
    entity_type: EntityType
    value: str
    context: str = ""  # Surrounding text
    confidence: float = 1.0
    start_pos: int = 0
    end_pos: int = 0


class EntityExtractor:
    """Extract named entities from unstructured text.

    Uses regex patterns and keyword matching for fast extraction.
    """

    # Technology/tool patterns
    TECH_KEYWORDS = [
        'python', 'javascript', 'typescript', 'java', 'go', 'rust',
        'react', 'nextjs', 'vue', 'angular',
        'postgres', 'postgresql', 'mysql', 'mongodb', 'redis', 'neo4j',
        'docker', 'kubernetes', 'k8s',
        'aws', 'gcp', 'azure', 'vertex', 'vertexai',
        'git', 'github', 'gitlab',
        'pytest', 'jest', 'mocha',
        'npm', 'pip', 'yarn', 'pnpm',
        'gemini', 'openai', 'claude', 'llm',
    ]

    # Error type patterns
    ERROR_TYPES = [
        'TypeError', 'ValueError', 'AttributeError', 'KeyError',
        'IndexError', 'RuntimeError', 'SyntaxError',
        'ConnectionError', 'TimeoutError', 'PermissionError',
    ]

    # Patterns
    FILE_PATH_PATTERN = r'(?:[./]?[\w-]+/)*[\w-]+\.[\w]{1,5}'
    URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'
    TASK_ID_PATTERN = r'\b(?:task|TASK)[-_]?(\w{3,})\b'
    AGENT_NAME_PATTERN = r'\b(?:agent|Agent)[-_:\s]+([A-Za-z0-9_-]+)'
    DATE_PATTERN = r'\b\d{4}-\d{2}-\d{2}\b'

    def __init__(self):
        """Initialize entity extractor."""
        pass

    def extract_all(self, text: str) -> List[ExtractedEntity]:
        """Extract all entities from text.

        Args:
            text: Text to extract from

        Returns:
            List of extracted entities
        """
        entities = []

        # Extract each type
        entities.extend(self.extract_file_paths(text))
        entities.extend(self.extract_urls(text))
        entities.extend(self.extract_task_ids(text))
        entities.extend(self.extract_agent_names(text))
        entities.extend(self.extract_dates(text))
        entities.extend(self.extract_technologies(text))
        entities.extend(self.extract_error_types(text))

        return entities

    def extract_file_paths(self, text: str) -> List[ExtractedEntity]:
        """Extract file paths."""
        entities = []
        for match in re.finditer(self.FILE_PATH_PATTERN, text):
            path = match.group(0)
            # Filter out likely false positives
            if '.' in path and not path.startswith('http'):
                entities.append(ExtractedEntity(
                    entity_type=EntityType.FILE_PATH,
                    value=path,
                    start_pos=match.start(),
                    end_pos=match.end(),
                    context=self._get_context(text, match.start(), match.end()),
                ))
        return entities

    def extract_urls(self, text: str) -> List[ExtractedEntity]:
        """Extract URLs."""
        entities = []
        for match in re.finditer(self.URL_PATTERN, text):
            entities.append(ExtractedEntity(
                entity_type=EntityType.URL,
                value=match.group(0),
                start_pos=match.start(),
                end_pos=match.end(),
                context=self._get_context(text, match.start(), match.end()),
            ))
        return entities

    def extract_task_ids(self, text: str) -> List[ExtractedEntity]:
        """Extract task IDs."""
        entities = []
        for match in re.finditer(self.TASK_ID_PATTERN, text, re.IGNORECASE):
            entities.append(ExtractedEntity(
                entity_type=EntityType.TASK_ID,
                value=match.group(1),
                start_pos=match.start(),
                end_pos=match.end(),
                context=self._get_context(text, match.start(), match.end()),
            ))
        return entities

    def extract_agent_names(self, text: str) -> List[ExtractedEntity]:
        """Extract agent names."""
        entities = []
        for match in re.finditer(self.AGENT_NAME_PATTERN, text):
            entities.append(ExtractedEntity(
                entity_type=EntityType.AGENT,
                value=match.group(1),
                start_pos=match.start(),
                end_pos=match.end(),
                context=self._get_context(text, match.start(), match.end()),
            ))
        return entities

    def extract_dates(self, text: str) -> List[ExtractedEntity]:
        """Extract dates in ISO format."""
        entities = []
        for match in re.finditer(self.DATE_PATTERN, text):
            entities.append(ExtractedEntity(
                entity_type=EntityType.DATE,
                value=match.group(0),
                start_pos=match.start(),
                end_pos=match.end(),
                context=self._get_context(text, match.start(), match.end()),
            ))
        return entities

    def extract_technologies(self, text: str) -> List[ExtractedEntity]:
        """Extract technology/tool mentions."""
        entities = []
        text_lower = text.lower()

        for tech in self.TECH_KEYWORDS:
            # Find all occurrences
            pattern = r'\b' + re.escape(tech) + r'\b'
            for match in re.finditer(pattern, text_lower):
                entities.append(ExtractedEntity(
                    entity_type=EntityType.TECHNOLOGY,
                    value=tech,
                    start_pos=match.start(),
                    end_pos=match.end(),
                    context=self._get_context(text, match.start(), match.end()),
                    confidence=0.9,
                ))

        return entities

    def extract_error_types(self, text: str) -> List[ExtractedEntity]:
        """Extract error type mentions."""
        entities = []

        for error_type in self.ERROR_TYPES:
            pattern = r'\b' + re.escape(error_type) + r'\b'
            for match in re.finditer(pattern, text):
                entities.append(ExtractedEntity(
                    entity_type=EntityType.ERROR_TYPE,
                    value=error_type,
                    start_pos=match.start(),
                    end_pos=match.end(),
                    context=self._get_context(text, match.start(), match.end()),
                ))

        return entities

    def _get_context(self, text: str, start: int, end: int, window: int = 50) -> str:
        """Get surrounding context for an entity.

        Args:
            text: Full text
            start: Entity start position
            end: Entity end position
            window: Characters to include before and after

        Returns:
            Context string
        """
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end].strip()

    def get_entity_summary(self, entities: List[ExtractedEntity]) -> Dict[str, List[str]]:
        """Get summary of extracted entities by type.

        Args:
            entities: List of extracted entities

        Returns:
            Dictionary mapping entity type to unique values
        """
        summary: Dict[str, Set[str]] = {}

        for entity in entities:
            type_key = entity.entity_type.value
            if type_key not in summary:
                summary[type_key] = set()
            summary[type_key].add(entity.value)

        # Convert sets to sorted lists
        return {
            entity_type: sorted(values)
            for entity_type, values in summary.items()
        }

    def get_statistics(self, entities: List[ExtractedEntity]) -> dict:
        """Get statistics about extracted entities.

        Args:
            entities: List of extracted entities

        Returns:
            Statistics dictionary
        """
        type_counts = {}
        for entity in entities:
            type_key = entity.entity_type.value
            type_counts[type_key] = type_counts.get(type_key, 0) + 1

        return {
            "total_entities": len(entities),
            "by_type": type_counts,
            "unique_values": len(set(e.value for e in entities)),
        }
