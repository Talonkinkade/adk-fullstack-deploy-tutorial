"""ADA (Autonomous Development Agent) Orchestration Layer.

TIER 1: Master control plane for LearnQwest multi-agent system.

Provides:
- Agent lifecycle management
- Request routing and load balancing
- Health monitoring and auto-recovery
- Central agent registry
"""

from .orchestrator import ADAOrchestrator
from .registry import AgentRegistry
from .config_manager import ConfigManager
from .health_monitor import HealthMonitor
from .router import RequestRouter

__all__ = [
    "ADAOrchestrator",
    "AgentRegistry",
    "ConfigManager",
    "HealthMonitor",
    "RequestRouter",
]

__version__ = "1.0.0"
__tier__ = 1
