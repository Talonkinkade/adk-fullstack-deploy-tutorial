"""TeamLink_MasterControl Bridge - Integration with TeamLink ecosystem.

Provides:
- State synchronization between LearnQwest and TeamLink
- Cross-system messaging
- Shared agent registry
- Workflow coordination
"""

import json
from typing import Any, Dict, List, Optional

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class TeamLinkBridge:
    """Bridge to TeamLink_MasterControl system.

    Features:
    - Agent state sync
    - Message passing
    - Event propagation
    - Shared resource management
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str,
        timeout: int = 30
    ):
        """Initialize TeamLink bridge.

        Args:
            endpoint: TeamLink API endpoint
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library not installed. Install with: pip install requests")

        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def sync_agent_state(
        self,
        agent_id: str,
        state: Dict[str, Any]
    ) -> bool:
        """Sync agent state to TeamLink.

        Args:
            agent_id: Agent identifier
            state: Agent state to sync

        Returns:
            True if successful
        """
        url = f"{self.endpoint}/api/agents/{agent_id}/state"

        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=state,
                timeout=self.timeout
            )

            return response.status_code == 200

        except requests.RequestException as e:
            print(f"TeamLink sync error: {e}")
            return False

    def get_agent_state(self, agent_id: str) -> Optional[Dict]:
        """Get agent state from TeamLink.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent state dictionary or None
        """
        url = f"{self.endpoint}/api/agents/{agent_id}/state"

        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()

            return None

        except requests.RequestException as e:
            print(f"TeamLink fetch error: {e}")
            return None

    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message: Dict[str, Any]
    ) -> bool:
        """Send message to another agent via TeamLink.

        Args:
            from_agent: Source agent ID
            to_agent: Target agent ID
            message: Message payload

        Returns:
            True if successful
        """
        url = f"{self.endpoint}/api/messages"

        payload = {
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "timestamp": self._get_timestamp(),
        }

        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            return response.status_code == 200

        except requests.RequestException as e:
            print(f"TeamLink message error: {e}")
            return False

    def get_messages(
        self,
        agent_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """Get messages for an agent.

        Args:
            agent_id: Agent identifier
            limit: Maximum messages to fetch

        Returns:
            List of messages
        """
        url = f"{self.endpoint}/api/agents/{agent_id}/messages"

        params = {"limit": limit}

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json().get("messages", [])

            return []

        except requests.RequestException as e:
            print(f"TeamLink fetch messages error: {e}")
            return []

    def propagate_event(
        self,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> bool:
        """Propagate event to TeamLink event bus.

        Args:
            event_type: Type of event
            event_data: Event payload

        Returns:
            True if successful
        """
        url = f"{self.endpoint}/api/events"

        payload = {
            "type": event_type,
            "data": event_data,
            "source": "learnqwest",
            "timestamp": self._get_timestamp(),
        }

        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            return response.status_code == 200

        except requests.RequestException as e:
            print(f"TeamLink event error: {e}")
            return False

    def health_check(self) -> bool:
        """Check if TeamLink is reachable.

        Returns:
            True if healthy
        """
        url = f"{self.endpoint}/health"

        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200

        except requests.RequestException:
            return False

    def _get_timestamp(self) -> str:
        """Get current ISO timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
