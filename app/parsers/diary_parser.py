"""Diary Parser - Process natural language work diaries using LLM.

Extracts:
- Daily accomplishments
- Blockers and challenges
- Collaboration events
- Learning insights
- Sentiment and morale indicators
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any

from google import genai
from google.genai import types


@dataclass
class DiaryEntry:
    """Structured diary entry extracted from natural language."""
    entry_id: str
    date: datetime
    author: str

    # Extracted content
    accomplishments: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    collaborations: List[str] = field(default_factory=list)
    learnings: List[str] = field(default_factory=list)
    goals_for_tomorrow: List[str] = field(default_factory=list)

    # Sentiment analysis
    morale_score: Optional[float] = None  # 0-10 scale
    productivity_score: Optional[float] = None  # 0-10 scale
    sentiment: Optional[str] = None  # "positive", "neutral", "negative"

    # Metadata
    raw_content: str = ""
    tags: List[str] = field(default_factory=list)
    confidence: float = 0.0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "entry_id": self.entry_id,
            "date": self.date.isoformat(),
            "author": self.author,
            "accomplishments": self.accomplishments,
            "blockers": self.blockers,
            "collaborations": self.collaborations,
            "learnings": self.learnings,
            "goals_for_tomorrow": self.goals_for_tomorrow,
            "morale_score": self.morale_score,
            "productivity_score": self.productivity_score,
            "sentiment": self.sentiment,
            "tags": self.tags,
            "confidence": self.confidence,
        }


class DiaryParser:
    """Parse natural language work diaries using LLM.

    Uses Gemini to extract structured information from free-form text.
    """

    EXTRACTION_PROMPT = """You are an AI assistant that extracts structured information from work diary entries.

Given a diary entry, extract the following information in JSON format:

{
  "accomplishments": ["list of things accomplished"],
  "blockers": ["list of challenges or blockers faced"],
  "collaborations": ["list of people or teams collaborated with"],
  "learnings": ["list of things learned"],
  "goals_for_tomorrow": ["list of goals for the next day"],
  "morale_score": <number 0-10, where 10 is very positive>,
  "productivity_score": <number 0-10, where 10 is very productive>,
  "sentiment": "<positive|neutral|negative>",
  "tags": ["relevant", "topic", "tags"]
}

Diary Entry:
---
{diary_content}
---

Return ONLY the JSON object, no additional text.
"""

    def __init__(self, model: str = "gemini-2.5-flash"):
        """Initialize diary parser.

        Args:
            model: Gemini model to use for parsing
        """
        self.model_name = model
        self.client = genai.Client()

    def parse_entry(
        self,
        content: str,
        author: str,
        date: Optional[datetime] = None
    ) -> DiaryEntry:
        """Parse a single diary entry.

        Args:
            content: Raw diary content
            author: Entry author
            date: Entry date (defaults to now)

        Returns:
            Structured diary entry
        """
        if date is None:
            date = datetime.now()

        # Use LLM to extract structured data
        extracted_data = self._extract_with_llm(content)

        # Create diary entry
        entry = DiaryEntry(
            entry_id=f"{author}_{date.strftime('%Y%m%d')}",
            date=date,
            author=author,
            raw_content=content,
            accomplishments=extracted_data.get("accomplishments", []),
            blockers=extracted_data.get("blockers", []),
            collaborations=extracted_data.get("collaborations", []),
            learnings=extracted_data.get("learnings", []),
            goals_for_tomorrow=extracted_data.get("goals_for_tomorrow", []),
            morale_score=extracted_data.get("morale_score"),
            productivity_score=extracted_data.get("productivity_score"),
            sentiment=extracted_data.get("sentiment"),
            tags=extracted_data.get("tags", []),
            confidence=extracted_data.get("confidence", 0.8),
        )

        return entry

    def parse_batch(
        self,
        entries: List[Dict[str, Any]]
    ) -> List[DiaryEntry]:
        """Parse multiple diary entries.

        Args:
            entries: List of dicts with 'content', 'author', and optional 'date'

        Returns:
            List of structured diary entries
        """
        results = []
        for entry_data in entries:
            parsed = self.parse_entry(
                content=entry_data["content"],
                author=entry_data["author"],
                date=entry_data.get("date")
            )
            results.append(parsed)
        return results

    def _extract_with_llm(self, content: str) -> dict:
        """Use LLM to extract structured data from diary content.

        Args:
            content: Raw diary content

        Returns:
            Dictionary of extracted fields
        """
        prompt = self.EXTRACTION_PROMPT.format(diary_content=content)

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,  # Low temperature for consistency
                    max_output_tokens=2048,
                )
            )

            # Extract JSON from response
            response_text = response.text.strip()

            # Try to parse JSON
            # Sometimes the model includes markdown code blocks
            if "```json" in response_text:
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_match:
                    response_text = json_match.group(1)
            elif "```" in response_text:
                json_match = re.search(r'```\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_match:
                    response_text = json_match.group(1)

            extracted = json.loads(response_text)
            return extracted

        except Exception as e:
            print(f"Error extracting diary data with LLM: {e}")
            # Return default structure on error
            return {
                "accomplishments": [],
                "blockers": [],
                "collaborations": [],
                "learnings": [],
                "goals_for_tomorrow": [],
                "morale_score": None,
                "productivity_score": None,
                "sentiment": "neutral",
                "tags": [],
                "confidence": 0.0,
            }

    def analyze_trends(self, entries: List[DiaryEntry]) -> dict:
        """Analyze trends across multiple diary entries.

        Args:
            entries: List of diary entries

        Returns:
            Dictionary of trend analysis
        """
        if not entries:
            return {"error": "No entries to analyze"}

        # Calculate averages
        morale_scores = [e.morale_score for e in entries if e.morale_score is not None]
        productivity_scores = [e.productivity_score for e in entries if e.productivity_score is not None]

        avg_morale = sum(morale_scores) / len(morale_scores) if morale_scores else None
        avg_productivity = sum(productivity_scores) / len(productivity_scores) if productivity_scores else None

        # Sentiment distribution
        sentiments = [e.sentiment for e in entries if e.sentiment]
        sentiment_counts = {
            "positive": sentiments.count("positive"),
            "neutral": sentiments.count("neutral"),
            "negative": sentiments.count("negative"),
        }

        # Most common blockers
        all_blockers = []
        for entry in entries:
            all_blockers.extend(entry.blockers)

        # Most common learnings
        all_learnings = []
        for entry in entries:
            all_learnings.extend(entry.learnings)

        # Most common collaborators
        all_collaborations = []
        for entry in entries:
            all_collaborations.extend(entry.collaborations)

        return {
            "total_entries": len(entries),
            "date_range": {
                "start": min(e.date for e in entries).isoformat(),
                "end": max(e.date for e in entries).isoformat(),
            },
            "avg_morale": round(avg_morale, 2) if avg_morale else None,
            "avg_productivity": round(avg_productivity, 2) if avg_productivity else None,
            "sentiment_distribution": sentiment_counts,
            "total_accomplishments": sum(len(e.accomplishments) for e in entries),
            "total_blockers": len(all_blockers),
            "total_learnings": len(all_learnings),
            "unique_collaborators": len(set(all_collaborations)),
            "most_common_tags": self._get_top_items(
                [tag for e in entries for tag in e.tags],
                limit=10
            ),
        }

    def _get_top_items(self, items: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """Get most common items from list.

        Args:
            items: List of items
            limit: Maximum number of items to return

        Returns:
            List of dicts with 'item' and 'count'
        """
        from collections import Counter
        counts = Counter(items)
        return [
            {"item": item, "count": count}
            for item, count in counts.most_common(limit)
        ]

    def generate_summary(self, entries: List[DiaryEntry], period: str = "week") -> str:
        """Generate a natural language summary of diary entries.

        Args:
            entries: List of diary entries
            period: Time period ("day", "week", "month")

        Returns:
            Natural language summary
        """
        if not entries:
            return "No diary entries to summarize."

        trends = self.analyze_trends(entries)

        summary_parts = []

        # Header
        summary_parts.append(f"# Work Summary for {period.capitalize()}")
        summary_parts.append(f"Period: {trends['date_range']['start']} to {trends['date_range']['end']}")
        summary_parts.append(f"Total entries: {trends['total_entries']}")
        summary_parts.append("")

        # Morale and productivity
        if trends['avg_morale']:
            summary_parts.append(f"**Average Morale:** {trends['avg_morale']}/10")
        if trends['avg_productivity']:
            summary_parts.append(f"**Average Productivity:** {trends['avg_productivity']}/10")
        summary_parts.append("")

        # Accomplishments
        summary_parts.append(f"## Key Accomplishments ({trends['total_accomplishments']} total)")
        for entry in entries[:3]:  # Show recent 3
            if entry.accomplishments:
                summary_parts.append(f"- {entry.date.strftime('%Y-%m-%d')}: {', '.join(entry.accomplishments[:2])}")
        summary_parts.append("")

        # Blockers
        if trends['total_blockers'] > 0:
            summary_parts.append(f"## Challenges ({trends['total_blockers']} total)")
            all_blockers = [b for e in entries for b in e.blockers]
            for blocker in list(set(all_blockers))[:5]:
                summary_parts.append(f"- {blocker}")
            summary_parts.append("")

        # Learnings
        if trends['total_learnings'] > 0:
            summary_parts.append(f"## Key Learnings ({trends['total_learnings']} total)")
            all_learnings = [l for e in entries for l in e.learnings]
            for learning in list(set(all_learnings))[:5]:
                summary_parts.append(f"- {learning}")
            summary_parts.append("")

        # Collaborations
        if trends['unique_collaborators'] > 0:
            summary_parts.append(f"## Collaborations ({trends['unique_collaborators']} unique collaborators)")
            summary_parts.append("")

        return "\n".join(summary_parts)
