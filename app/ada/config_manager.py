"""Configuration Manager - Environment-aware configuration for ADA orchestration.

Manages:
- Agent configuration loading
- Environment detection
- Dynamic scaling policies
- Integration endpoint configuration
"""

import json
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Any


class DeploymentEnvironment(Enum):
    """Deployment environment types."""
    LOCAL = "local"
    CLOUD_RUN = "cloud_run"
    AGENT_ENGINE = "agent_engine"
    VERTEX_AI = "vertex_ai"


class ScalingPolicy(Enum):
    """Agent scaling policies."""
    FIXED = "fixed"  # Fixed number of agents
    AUTO = "auto"    # Auto-scale based on load
    BURST = "burst"  # Scale on demand with burst capacity


@dataclass
class AgentConfig:
    """Configuration for an individual agent."""
    name: str
    tier: int
    model: str = "gemini-2.5-flash"
    max_concurrent_tasks: int = 1
    timeout_seconds: int = 300
    enabled: bool = True
    scaling_policy: ScalingPolicy = ScalingPolicy.FIXED
    min_instances: int = 1
    max_instances: int = 1
    auto_scale_threshold: float = 0.8  # 80% load triggers scaling


@dataclass
class IntegrationConfig:
    """External integration endpoints."""
    teamlink_endpoint: Optional[str] = None
    teamlink_api_key: Optional[str] = None
    comet_endpoint: Optional[str] = None
    comet_api_key: Optional[str] = None


@dataclass
class DatabaseConfig:
    """Database connection configuration."""
    # PostgreSQL
    postgres_host: Optional[str] = None
    postgres_port: int = 5432
    postgres_database: Optional[str] = None
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None

    # Neo4j
    neo4j_uri: Optional[str] = None
    neo4j_user: Optional[str] = None
    neo4j_password: Optional[str] = None

    # BigQuery
    bigquery_project: Optional[str] = None
    bigquery_dataset: Optional[str] = None

    # GCS
    gcs_bucket: Optional[str] = None


@dataclass
class ADAConfig:
    """Master ADA orchestrator configuration."""

    # Environment
    environment: DeploymentEnvironment = DeploymentEnvironment.LOCAL

    # Google Cloud
    project_id: Optional[str] = None
    location: str = "us-central1"

    # ADK
    adk_endpoint: str = "http://127.0.0.1:8000"
    agent_engine_endpoint: Optional[str] = None

    # Agent configuration
    agent_configs: Dict[str, AgentConfig] = field(default_factory=dict)

    # Integrations
    integrations: IntegrationConfig = field(default_factory=IntegrationConfig)

    # Databases
    databases: DatabaseConfig = field(default_factory=DatabaseConfig)

    # Performance
    max_total_agents: int = 100
    health_check_interval_seconds: int = 30
    request_timeout_seconds: int = 300

    # Logging
    log_level: str = "INFO"
    enable_tracing: bool = True
    enable_metrics: bool = True

    # Paths
    config_dir: Path = Path("config")
    logs_dir: Path = Path("logs")

    @classmethod
    def from_env(cls) -> "ADAConfig":
        """Create configuration from environment variables."""
        config = cls()

        # Detect environment
        config.environment = cls._detect_environment()

        # Google Cloud
        config.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        config.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        # Endpoints
        config.adk_endpoint = os.getenv("ADK_ENDPOINT", "http://127.0.0.1:8000")
        config.agent_engine_endpoint = os.getenv("AGENT_ENGINE_ENDPOINT")

        # Integrations
        config.integrations.teamlink_endpoint = os.getenv("TEAMLINK_ENDPOINT")
        config.integrations.teamlink_api_key = os.getenv("TEAMLINK_API_KEY")
        config.integrations.comet_endpoint = os.getenv("COMET_ENDPOINT")
        config.integrations.comet_api_key = os.getenv("COMET_API_KEY")

        # Databases - PostgreSQL
        config.databases.postgres_host = os.getenv("POSTGRES_HOST")
        config.databases.postgres_port = int(os.getenv("POSTGRES_PORT", "5432"))
        config.databases.postgres_database = os.getenv("POSTGRES_DATABASE", "learnqwest")
        config.databases.postgres_user = os.getenv("POSTGRES_USER")
        config.databases.postgres_password = os.getenv("POSTGRES_PASSWORD")

        # Databases - Neo4j
        config.databases.neo4j_uri = os.getenv("NEO4J_URI")
        config.databases.neo4j_user = os.getenv("NEO4J_USER")
        config.databases.neo4j_password = os.getenv("NEO4J_PASSWORD")

        # Databases - BigQuery
        config.databases.bigquery_project = os.getenv("BIGQUERY_PROJECT", config.project_id)
        config.databases.bigquery_dataset = os.getenv("BIGQUERY_DATASET", "learnqwest_metrics")

        # Databases - GCS
        config.databases.gcs_bucket = os.getenv("GCS_BUCKET")

        # Performance tuning
        config.max_total_agents = int(os.getenv("MAX_TOTAL_AGENTS", "100"))
        config.health_check_interval_seconds = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))

        # Logging
        config.log_level = os.getenv("LOG_LEVEL", "INFO")
        config.enable_tracing = os.getenv("ENABLE_TRACING", "true").lower() == "true"
        config.enable_metrics = os.getenv("ENABLE_METRICS", "true").lower() == "true"

        return config

    @classmethod
    def from_file(cls, config_path: Path) -> "ADAConfig":
        """Load configuration from JSON file."""
        with open(config_path, 'r') as f:
            data = json.load(f)

        config = cls()

        # Parse environment
        if "environment" in data:
            config.environment = DeploymentEnvironment(data["environment"])

        # Google Cloud
        config.project_id = data.get("project_id")
        config.location = data.get("location", "us-central1")

        # Endpoints
        config.adk_endpoint = data.get("adk_endpoint", "http://127.0.0.1:8000")
        config.agent_engine_endpoint = data.get("agent_engine_endpoint")

        # Load agent configs
        for agent_name, agent_data in data.get("agents", {}).items():
            scaling_policy = ScalingPolicy(agent_data.get("scaling_policy", "fixed"))
            agent_config = AgentConfig(
                name=agent_name,
                tier=agent_data.get("tier", 4),
                model=agent_data.get("model", "gemini-2.5-flash"),
                max_concurrent_tasks=agent_data.get("max_concurrent_tasks", 1),
                timeout_seconds=agent_data.get("timeout_seconds", 300),
                enabled=agent_data.get("enabled", True),
                scaling_policy=scaling_policy,
                min_instances=agent_data.get("min_instances", 1),
                max_instances=agent_data.get("max_instances", 1),
            )
            config.agent_configs[agent_name] = agent_config

        # Integrations
        integrations_data = data.get("integrations", {})
        config.integrations = IntegrationConfig(
            teamlink_endpoint=integrations_data.get("teamlink_endpoint"),
            teamlink_api_key=integrations_data.get("teamlink_api_key"),
            comet_endpoint=integrations_data.get("comet_endpoint"),
            comet_api_key=integrations_data.get("comet_api_key"),
        )

        # Databases
        db_data = data.get("databases", {})
        config.databases = DatabaseConfig(
            postgres_host=db_data.get("postgres_host"),
            postgres_port=db_data.get("postgres_port", 5432),
            postgres_database=db_data.get("postgres_database", "learnqwest"),
            postgres_user=db_data.get("postgres_user"),
            postgres_password=db_data.get("postgres_password"),
            neo4j_uri=db_data.get("neo4j_uri"),
            neo4j_user=db_data.get("neo4j_user"),
            neo4j_password=db_data.get("neo4j_password"),
            bigquery_project=db_data.get("bigquery_project"),
            bigquery_dataset=db_data.get("bigquery_dataset", "learnqwest_metrics"),
            gcs_bucket=db_data.get("gcs_bucket"),
        )

        return config

    @staticmethod
    def _detect_environment() -> DeploymentEnvironment:
        """Auto-detect deployment environment."""
        if os.getenv("AGENT_ENGINE_ENDPOINT"):
            return DeploymentEnvironment.AGENT_ENGINE

        if os.getenv("K_SERVICE") or os.getenv("CLOUD_RUN_SERVICE_URL"):
            return DeploymentEnvironment.CLOUD_RUN

        if os.getenv("VERTEX_AI_DEPLOYMENT"):
            return DeploymentEnvironment.VERTEX_AI

        return DeploymentEnvironment.LOCAL

    def get_endpoint(self) -> str:
        """Get appropriate endpoint based on environment."""
        if self.environment == DeploymentEnvironment.AGENT_ENGINE and self.agent_engine_endpoint:
            return self.agent_engine_endpoint
        return self.adk_endpoint

    def is_cloud_deployment(self) -> bool:
        """Check if running in cloud environment."""
        return self.environment in [
            DeploymentEnvironment.CLOUD_RUN,
            DeploymentEnvironment.AGENT_ENGINE,
            DeploymentEnvironment.VERTEX_AI,
        ]

    def validate(self) -> tuple[bool, list[str]]:
        """Validate configuration.

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Check required cloud config
        if self.is_cloud_deployment():
            if not self.project_id:
                errors.append("GOOGLE_CLOUD_PROJECT required for cloud deployment")

        # Check database connections if configured
        if self.databases.postgres_host:
            if not self.databases.postgres_user or not self.databases.postgres_password:
                errors.append("PostgreSQL credentials incomplete")

        if self.databases.neo4j_uri:
            if not self.databases.neo4j_user or not self.databases.neo4j_password:
                errors.append("Neo4j credentials incomplete")

        # Check integration credentials
        if self.integrations.teamlink_endpoint and not self.integrations.teamlink_api_key:
            errors.append("TeamLink API key required when endpoint is configured")

        if self.integrations.comet_endpoint and not self.integrations.comet_api_key:
            errors.append("Comet API key required when endpoint is configured")

        return (len(errors) == 0, errors)

    def to_dict(self) -> dict:
        """Serialize configuration to dictionary."""
        return {
            "environment": self.environment.value,
            "project_id": self.project_id,
            "location": self.location,
            "adk_endpoint": self.adk_endpoint,
            "agent_engine_endpoint": self.agent_engine_endpoint,
            "max_total_agents": self.max_total_agents,
            "health_check_interval_seconds": self.health_check_interval_seconds,
            "log_level": self.log_level,
            "enable_tracing": self.enable_tracing,
            "enable_metrics": self.enable_metrics,
        }

    def summary(self) -> str:
        """Get configuration summary."""
        return f"""ADA Configuration Summary:
Environment: {self.environment.value}
Project: {self.project_id or 'Not set'}
Location: {self.location}
Endpoint: {self.get_endpoint()}
Max Agents: {self.max_total_agents}
Tracing: {'Enabled' if self.enable_tracing else 'Disabled'}
Metrics: {'Enabled' if self.enable_metrics else 'Disabled'}
Agent Configs: {len(self.agent_configs)} loaded
"""


# Global configuration instance
_global_config: Optional[ADAConfig] = None


def get_config() -> ADAConfig:
    """Get global configuration instance (singleton)."""
    global _global_config
    if _global_config is None:
        # Try to load from file first, fall back to env
        config_path = Path("config/ada_config.json")
        if config_path.exists():
            _global_config = ADAConfig.from_file(config_path)
        else:
            _global_config = ADAConfig.from_env()

    return _global_config


def init_config(config: ADAConfig) -> None:
    """Initialize global configuration with custom config."""
    global _global_config
    _global_config = config
