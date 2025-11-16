"""Worklog Parser - Extract structured data from agent worklogs.

Processes:
- Raw log files
- Event streams
- Structured logging output
- ADK session events

Extracts:
- Task start/completion timestamps
- Agent interactions
- Resource consumption
- Errors and warnings
- Performance metrics
"""

import re
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from ..schemas.worklog_schema import (
    WorklogEntrySchema,
    TaskMetadata,
    TaskStatus,
    TaskType,
)


@dataclass
class WorklogEntry:
    """Single worklog entry before parsing."""
    timestamp: datetime
    content: str
    source: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorklogParser:
    """Parse worklogs and extract structured data.

    Supports multiple log formats:
    - Standard logging format (timestamp + message)
    - ADK event format (JSON-based)
    - Custom worklog format (markdown/plain text)
    """

    # Regex patterns for common log formats
    TIMESTAMP_PATTERNS = [
        r'^\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',  # ISO format
        r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',   # Standard format
        r'^(\w{3} \d{2}, \d{4} \d{2}:\d{2}:\d{2})',  # Human readable
    ]

    TASK_START_PATTERNS = [
        r'(?:start(?:ing|ed)?|begin(?:ning)?|initiat(?:ing|ed)?)\s+task[:\s]+(\S+)',
        r'task[:\s]+(\S+)\s+(?:start|begin)',
        r'> Task:\s+(\S+)',
    ]

    TASK_COMPLETE_PATTERNS = [
        r'(?:complet(?:ed|ing)|finish(?:ed|ing)|done)\s+task[:\s]+(\S+)',
        r'task[:\s]+(\S+)\s+(?:complete|finish|done)',
        r'✓\s+(\S+)',
    ]

    TASK_FAILED_PATTERNS = [
        r'(?:fail(?:ed|ing)|error)\s+task[:\s]+(\S+)',
        r'task[:\s]+(\S+)\s+(?:fail|error)',
        r'✗\s+(\S+)',
    ]

    ERROR_PATTERNS = [
        r'ERROR[:|\s]+(.+)',
        r'Exception:\s+(.+)',
        r'Failed:\s+(.+)',
    ]

    WARNING_PATTERNS = [
        r'WARNING[:|\s]+(.+)',
        r'WARN[:|\s]+(.+)',
    ]

    FILE_MODIFIED_PATTERN = r'(?:modified|changed|updated|created):\s+([^\s]+\.(?:py|ts|js|json|md|yaml|yml))'

    LINES_CHANGED_PATTERN = r'(\d+)\s+lines?\s+(?:changed|modified|added|deleted)'

    def __init__(self):
        """Initialize worklog parser."""
        self.task_tracking: Dict[str, TaskMetadata] = {}

    def parse_log_file(self, file_path: str) -> List[WorklogEntrySchema]:
        """Parse a log file into structured entries.

        Args:
            file_path: Path to log file

        Returns:
            List of parsed worklog entries
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.parse_log_content(content)

    def parse_log_content(self, content: str) -> List[WorklogEntrySchema]:
        """Parse log content into structured entries.

        Args:
            content: Raw log content

        Returns:
            List of parsed worklog entries
        """
        entries = []
        lines = content.split('\n')

        current_entry = None
        current_timestamp = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try to extract timestamp
            timestamp = self._extract_timestamp(line)
            if timestamp:
                # Save previous entry if exists
                if current_entry and current_timestamp:
                    parsed = self._parse_entry(current_entry, current_timestamp)
                    if parsed:
                        entries.append(parsed)

                # Start new entry
                current_timestamp = timestamp
                current_entry = line
            elif current_entry:
                # Continuation of current entry
                current_entry += "\n" + line

        # Don't forget last entry
        if current_entry and current_timestamp:
            parsed = self._parse_entry(current_entry, current_timestamp)
            if parsed:
                entries.append(parsed)

        return entries

    def parse_entries(self, entries: List[WorklogEntry]) -> List[WorklogEntrySchema]:
        """Parse multiple worklog entries.

        Args:
            entries: List of raw worklog entries

        Returns:
            List of structured entries
        """
        return [
            self._parse_entry(entry.content, entry.timestamp, entry.metadata)
            for entry in entries
        ]

    def _extract_timestamp(self, line: str) -> Optional[datetime]:
        """Extract timestamp from log line."""
        for pattern in self.TIMESTAMP_PATTERNS:
            match = re.search(pattern, line)
            if match:
                timestamp_str = match.group(1)
                try:
                    # Try ISO format first
                    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                except ValueError:
                    try:
                        # Try standard format
                        return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        continue
        return None

    def _parse_entry(
        self,
        content: str,
        timestamp: datetime,
        metadata: Optional[Dict[str, Any]] = None
    ) -> WorklogEntrySchema:
        """Parse a single worklog entry into structured format.

        Args:
            content: Raw log content
            timestamp: Entry timestamp
            metadata: Optional metadata

        Returns:
            Structured worklog entry
        """
        entry = WorklogEntrySchema(
            entry_id=f"{timestamp.isoformat()}_{hash(content) & 0xFFFF:04x}",
            timestamp=timestamp,
            raw_content=content,
        )

        # Extract tasks
        entry.tasks = self._extract_tasks(content, timestamp)

        # Extract agent collaborations
        entry.agent_collaborations = self._extract_agent_interactions(content)

        # Extract resource usage
        entry.resource_usage = self._extract_resource_usage(content)

        # Analyze sentiment (basic keyword-based for now)
        entry.sentiment_score = self._analyze_sentiment(content)
        entry.confidence_score = 0.7  # Placeholder

        return entry

    def _extract_tasks(self, content: str, timestamp: datetime) -> List[TaskMetadata]:
        """Extract task information from content."""
        tasks = []

        # Check for task starts
        for pattern in self.TASK_START_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                task_id = match.group(1)
                task = TaskMetadata(
                    task_id=task_id,
                    task_type=self._infer_task_type(content),
                    status=TaskStatus.STARTED,
                    start_time=timestamp,
                    agent_name=self._extract_agent_name(content),
                )
                # Track for later completion
                self.task_tracking[task_id] = task
                tasks.append(task)

        # Check for task completions
        for pattern in self.TASK_COMPLETE_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                task_id = match.group(1)
                if task_id in self.task_tracking:
                    task = self.task_tracking[task_id]
                    task.status = TaskStatus.COMPLETED
                    task.end_time = timestamp
                    task.success = True
                    if task.start_time:
                        task.duration_seconds = (timestamp - task.start_time).total_seconds()
                else:
                    task = TaskMetadata(
                        task_id=task_id,
                        task_type=self._infer_task_type(content),
                        status=TaskStatus.COMPLETED,
                        end_time=timestamp,
                        success=True,
                    )
                tasks.append(task)

        # Check for task failures
        for pattern in self.TASK_FAILED_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                task_id = match.group(1)
                error_msg = self._extract_error(content)

                if task_id in self.task_tracking:
                    task = self.task_tracking[task_id]
                    task.status = TaskStatus.FAILED
                    task.end_time = timestamp
                    task.success = False
                    task.error_message = error_msg
                else:
                    task = TaskMetadata(
                        task_id=task_id,
                        task_type=self._infer_task_type(content),
                        status=TaskStatus.FAILED,
                        end_time=timestamp,
                        success=False,
                        error_message=error_msg,
                    )
                tasks.append(task)

        # Extract file modifications
        files_modified = re.findall(self.FILE_MODIFIED_PATTERN, content, re.IGNORECASE)
        if files_modified and tasks:
            tasks[-1].files_modified = files_modified

        # Extract lines changed
        lines_match = re.search(self.LINES_CHANGED_PATTERN, content, re.IGNORECASE)
        if lines_match and tasks:
            tasks[-1].lines_changed = int(lines_match.group(1))

        # Extract warnings
        warnings = []
        for pattern in self.WARNING_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            warnings.extend(matches)
        if warnings and tasks:
            tasks[-1].warnings = warnings

        return tasks

    def _infer_task_type(self, content: str) -> TaskType:
        """Infer task type from content."""
        content_lower = content.lower()

        if any(word in content_lower for word in ['test', 'pytest', 'jest', 'unittest']):
            return TaskType.TESTING
        elif any(word in content_lower for word in ['deploy', 'deployment', 'release']):
            return TaskType.DEPLOYMENT
        elif any(word in content_lower for word in ['review', 'lint', 'check']):
            return TaskType.CODE_REVIEW
        elif any(word in content_lower for word in ['debug', 'fix', 'bug']):
            return TaskType.DEBUGGING
        elif any(word in content_lower for word in ['document', 'readme', 'docs']):
            return TaskType.DOCUMENTATION
        elif any(word in content_lower for word in ['analyze', 'analytics', 'metrics']):
            return TaskType.ANALYTICS
        elif any(word in content_lower for word in ['parse', 'process', 'data']):
            return TaskType.DATA_PROCESSING
        elif any(word in content_lower for word in ['plan', 'design', 'architect']):
            return TaskType.PLANNING
        elif any(word in content_lower for word in ['generate', 'create', 'implement', 'code']):
            return TaskType.CODE_GENERATION
        else:
            return TaskType.RESEARCH

    def _extract_agent_name(self, content: str) -> Optional[str]:
        """Extract agent name from content."""
        agent_pattern = r'(?:agent|by|from):\s+([A-Za-z0-9_-]+)'
        match = re.search(agent_pattern, content, re.IGNORECASE)
        return match.group(1) if match else None

    def _extract_error(self, content: str) -> Optional[str]:
        """Extract error message from content."""
        for pattern in self.ERROR_PATTERNS:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _extract_agent_interactions(self, content: str) -> List[str]:
        """Extract agent collaboration events."""
        interactions = []
        patterns = [
            r'(?:with|collaborat(?:ed|ing)|to)\s+agent[:\s]+([A-Za-z0-9_-]+)',
            r'agent[:\s]+([A-Za-z0-9_-]+)\s+(?:assist|help|work)',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            interactions.extend(matches)
        return list(set(interactions))  # Remove duplicates

    def _extract_resource_usage(self, content: str) -> Dict[str, float]:
        """Extract resource usage metrics."""
        resources = {}

        # CPU usage
        cpu_match = re.search(r'cpu[:\s]+(\d+(?:\.\d+)?)%?', content, re.IGNORECASE)
        if cpu_match:
            resources['cpu_percent'] = float(cpu_match.group(1))

        # Memory usage
        mem_match = re.search(r'mem(?:ory)?[:\s]+(\d+(?:\.\d+)?)\s*(mb|gb)?', content, re.IGNORECASE)
        if mem_match:
            mem_value = float(mem_match.group(1))
            unit = mem_match.group(2).lower() if mem_match.group(2) else 'mb'
            if unit == 'gb':
                mem_value *= 1024
            resources['memory_mb'] = mem_value

        # Execution time
        time_match = re.search(r'(?:took|duration|time)[:\s]+(\d+(?:\.\d+)?)\s*(ms|s|min)?', content, re.IGNORECASE)
        if time_match:
            time_value = float(time_match.group(1))
            unit = time_match.group(2).lower() if time_match.group(2) else 's'
            if unit == 'ms':
                time_value /= 1000
            elif unit == 'min':
                time_value *= 60
            resources['execution_seconds'] = time_value

        return resources

    def _analyze_sentiment(self, content: str) -> float:
        """Basic sentiment analysis using keyword matching.

        Returns:
            Score from -1.0 (negative) to 1.0 (positive)
        """
        positive_words = [
            'success', 'complete', 'done', 'fixed', 'improved',
            'optimized', 'passed', 'working', 'resolved'
        ]
        negative_words = [
            'error', 'fail', 'bug', 'issue', 'problem',
            'blocked', 'crash', 'timeout', 'warning'
        ]

        content_lower = content.lower()

        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)

        total = positive_count + negative_count
        if total == 0:
            return 0.0

        return (positive_count - negative_count) / total

    def get_task_statistics(self) -> dict:
        """Get statistics about tracked tasks."""
        if not self.task_tracking:
            return {
                "total_tasks": 0,
                "completed": 0,
                "failed": 0,
                "in_progress": 0,
            }

        stats = {
            "total_tasks": len(self.task_tracking),
            "completed": 0,
            "failed": 0,
            "in_progress": 0,
            "avg_duration_seconds": 0.0,
        }

        durations = []
        for task in self.task_tracking.values():
            if task.status == TaskStatus.COMPLETED:
                stats["completed"] += 1
            elif task.status == TaskStatus.FAILED:
                stats["failed"] += 1
            elif task.status in [TaskStatus.STARTED, TaskStatus.IN_PROGRESS]:
                stats["in_progress"] += 1

            if task.duration_seconds:
                durations.append(task.duration_seconds)

        if durations:
            stats["avg_duration_seconds"] = sum(durations) / len(durations)

        return stats
