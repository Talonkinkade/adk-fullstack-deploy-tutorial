"""Comet Workflow Integration - Integration with Comet agentic workflows.

Provides:
- Workflow chaining
- Event bus integration
- Hybrid ADA-Comet orchestration
- Cross-workflow communication
"""

from typing import Any, Dict, List, Optional

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class CometIntegration:
    """Integration with Comet agentic workflow system.

    Features:
    - Workflow execution
    - Workflow chaining (Comet → ADA → Comet)
    - Event-driven triggers
    - Status synchronization
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str,
        timeout: int = 60
    ):
        """Initialize Comet integration.

        Args:
            endpoint: Comet API endpoint
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

    def execute_workflow(
        self,
        workflow_id: str,
        inputs: Dict[str, Any]
    ) -> Optional[Dict]:
        """Execute a Comet workflow.

        Args:
            workflow_id: Workflow identifier
            inputs: Workflow input parameters

        Returns:
            Workflow execution result or None
        """
        url = f"{self.endpoint}/api/workflows/{workflow_id}/execute"

        payload = {
            "inputs": inputs,
            "source": "learnqwest_ada",
        }

        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()

            return None

        except requests.RequestException as e:
            print(f"Comet workflow execution error: {e}")
            return None

    def chain_workflow(
        self,
        workflow_id: str,
        ada_task_id: str,
        chain_config: Dict[str, Any]
    ) -> bool:
        """Chain a Comet workflow with ADA task.

        Args:
            workflow_id: Comet workflow ID
            ada_task_id: ADA task ID to chain
            chain_config: Chaining configuration

        Returns:
            True if chain created successfully
        """
        url = f"{self.endpoint}/api/workflows/chain"

        payload = {
            "comet_workflow_id": workflow_id,
            "ada_task_id": ada_task_id,
            "config": chain_config,
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
            print(f"Comet chain error: {e}")
            return False

    def subscribe_to_event(
        self,
        event_type: str,
        callback_url: str
    ) -> bool:
        """Subscribe to Comet events.

        Args:
            event_type: Type of event to subscribe to
            callback_url: Webhook URL for callbacks

        Returns:
            True if subscription successful
        """
        url = f"{self.endpoint}/api/events/subscribe"

        payload = {
            "event_type": event_type,
            "callback_url": callback_url,
            "subscriber": "learnqwest_ada",
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
            print(f"Comet subscription error: {e}")
            return False

    def get_workflow_status(
        self,
        execution_id: str
    ) -> Optional[Dict]:
        """Get status of a workflow execution.

        Args:
            execution_id: Execution identifier

        Returns:
            Status dictionary or None
        """
        url = f"{self.endpoint}/api/executions/{execution_id}/status"

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
            print(f"Comet status error: {e}")
            return None

    def list_workflows(self) -> List[Dict]:
        """List available Comet workflows.

        Returns:
            List of workflow definitions
        """
        url = f"{self.endpoint}/api/workflows"

        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json().get("workflows", [])

            return []

        except requests.RequestException as e:
            print(f"Comet list error: {e}")
            return []

    def health_check(self) -> bool:
        """Check if Comet is reachable.

        Returns:
            True if healthy
        """
        url = f"{self.endpoint}/health"

        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200

        except requests.RequestException:
            return False
