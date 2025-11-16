"""
Configuration for Anthropic Claude Agent

This file handles all configuration needed to run your agent with Claude.
"""

import os
from dataclasses import dataclass
from pathlib import Path


# =============================================================================
# STEP 1: Load Environment Variables
# =============================================================================


def load_environment_variables() -> None:
    """Load environment variables from .env file if it exists."""
    try:
        from dotenv import load_dotenv

        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            print(f"✅ Loaded environment variables from {env_file}")
        else:
            print(f"ℹ️  No .env file found at {env_file}")
    except ImportError:
        print("ℹ️  python-dotenv not installed, skipping .env file loading")


# =============================================================================
# STEP 2: Basic Configuration
# =============================================================================


@dataclass
class AgentConfiguration:
    """Main configuration for your agent."""

    # The AI model to use - Claude Sonnet 4.5
    model: str = os.environ.get("MODEL", "claude-sonnet-4-5-20250929")

    # Agent name (can have hyphens, used for display)
    deployment_name: str = os.environ.get("AGENT_NAME", "goal-planning-agent")

    # Anthropic API Key
    anthropic_api_key: str | None = None

    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000

    def __post_init__(self) -> None:
        """Load environment variables and validate required settings."""

        # Load environment variables first
        load_environment_variables()

        # Validate and set API key
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.anthropic_api_key:
            raise ValueError(
                "❌ Missing ANTHROPIC_API_KEY environment variable!\n"
                "Please set it in your .env file.\n"
                "You can get an API key from: https://console.anthropic.com/"
            )

        # Override host/port from environment if provided
        self.host = os.environ.get("API_HOST", self.host)
        self.port = int(os.environ.get("API_PORT", str(self.port)))

    @property
    def internal_agent_name(self) -> str:
        """
        Convert deployment name to a valid Python identifier.

        Replaces hyphens with underscores and ensures it's a valid identifier.
        """
        # Convert hyphens to underscores and make it a valid identifier
        name = self.deployment_name.replace("-", "_")

        # Ensure it starts with a letter or underscore
        if not name[0].isalpha() and name[0] != "_":
            name = f"agent_{name}"

        return name


# =============================================================================
# STEP 3: Initialize Configuration
# =============================================================================


def get_config() -> AgentConfiguration:
    """Get or create the configuration singleton."""
    global _config
    if _config is None:
        _config = AgentConfiguration()
        # Print summary
        print("\n📋 Configuration Summary:")
        print(f"  Agent Name: {_config.deployment_name}")
        print(f"  Internal Name: {_config.internal_agent_name}")
        print(f"  Model: {_config.model}")
        print(f"  API Key: {'✓ Set' if _config.anthropic_api_key else '✗ Missing'}")
        print(f"  Server: {_config.host}:{_config.port}")
        print("=" * 50)
    return _config


# Lazy-loaded configuration singleton
_config: AgentConfiguration | None = None
config = get_config()
