"""Agent Conversion Pipeline - Batch convert features/programs to autonomous agents.

Supports:
- Feature analysis and capability extraction
- Agent template generation
- Code scaffolding
- Automatic ADK integration
- Batch processing
"""

from .feature_analyzer import FeatureAnalyzer
from .template_generator import AgentTemplateGenerator
from .scaffolder import AgentScaffolder
from .batch_converter import BatchConverter

__all__ = [
    "FeatureAnalyzer",
    "AgentTemplateGenerator",
    "AgentScaffolder",
    "BatchConverter",
]
