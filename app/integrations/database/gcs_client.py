"""GCS Client - Cloud Storage for artifacts, logs, and overflow data.

Stores:
- Configuration files (JSON)
- Log files
- Artifacts and outputs
- Large payload overflow from Cloud Trace
- Backup data
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    from google.cloud import storage
    from google.cloud.exceptions import NotFound
    GCS_AVAILABLE = True
except ImportError:
    GCS_AVAILABLE = False


class GCSClient:
    """Google Cloud Storage client for LearnQwest.

    Bucket structure:
    - config/: Configuration files
    - logs/: Log files
    - artifacts/: Agent output artifacts
    - traces/: Overflow trace data
    - backups/: Backup data
    """

    def __init__(self, bucket_name: str, project_id: Optional[str] = None):
        """Initialize GCS client.

        Args:
            bucket_name: GCS bucket name
            project_id: GCP project ID (optional)
        """
        if not GCS_AVAILABLE:
            raise ImportError("google-cloud-storage not installed. Install with: pip install google-cloud-storage")

        self.client = storage.Client(project=project_id) if project_id else storage.Client()
        self.bucket_name = bucket_name
        self.bucket = None

        # Initialize bucket
        self._init_bucket()

    def _init_bucket(self) -> None:
        """Initialize or get bucket."""
        try:
            self.bucket = self.client.get_bucket(self.bucket_name)
        except NotFound:
            # Create bucket if it doesn't exist
            self.bucket = self.client.create_bucket(self.bucket_name)
            print(f"Created bucket: {self.bucket_name}")

    def upload_file(
        self,
        local_path: Union[str, Path],
        gcs_path: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """Upload a file to GCS.

        Args:
            local_path: Local file path
            gcs_path: Destination path in GCS
            metadata: Optional metadata

        Returns:
            GCS URI (gs://bucket/path)
        """
        blob = self.bucket.blob(gcs_path)

        if metadata:
            blob.metadata = metadata

        blob.upload_from_filename(str(local_path))

        return f"gs://{self.bucket_name}/{gcs_path}"

    def download_file(
        self,
        gcs_path: str,
        local_path: Union[str, Path]
    ) -> bool:
        """Download a file from GCS.

        Args:
            gcs_path: Source path in GCS
            local_path: Destination local path

        Returns:
            True if successful
        """
        blob = self.bucket.blob(gcs_path)

        try:
            blob.download_to_filename(str(local_path))
            return True
        except NotFound:
            return False

    def upload_json(
        self,
        data: Dict[str, Any],
        gcs_path: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """Upload JSON data to GCS.

        Args:
            data: Dictionary to upload as JSON
            gcs_path: Destination path in GCS
            metadata: Optional metadata

        Returns:
            GCS URI
        """
        blob = self.bucket.blob(gcs_path)

        if metadata:
            blob.metadata = metadata

        blob.upload_from_string(
            json.dumps(data, indent=2),
            content_type='application/json'
        )

        return f"gs://{self.bucket_name}/{gcs_path}"

    def download_json(self, gcs_path: str) -> Optional[Dict[str, Any]]:
        """Download and parse JSON from GCS.

        Args:
            gcs_path: Source path in GCS

        Returns:
            Parsed JSON data or None if not found
        """
        blob = self.bucket.blob(gcs_path)

        try:
            content = blob.download_as_text()
            return json.loads(content)
        except NotFound:
            return None

    def upload_string(
        self,
        content: str,
        gcs_path: str,
        content_type: str = 'text/plain',
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """Upload string content to GCS.

        Args:
            content: String content
            gcs_path: Destination path in GCS
            content_type: Content type (default: text/plain)
            metadata: Optional metadata

        Returns:
            GCS URI
        """
        blob = self.bucket.blob(gcs_path)

        if metadata:
            blob.metadata = metadata

        blob.upload_from_string(content, content_type=content_type)

        return f"gs://{self.bucket_name}/{gcs_path}"

    def download_string(self, gcs_path: str) -> Optional[str]:
        """Download string content from GCS.

        Args:
            gcs_path: Source path in GCS

        Returns:
            String content or None if not found
        """
        blob = self.bucket.blob(gcs_path)

        try:
            return blob.download_as_text()
        except NotFound:
            return None

    def list_files(
        self,
        prefix: str = "",
        delimiter: Optional[str] = None
    ) -> List[str]:
        """List files in bucket with optional prefix.

        Args:
            prefix: File path prefix to filter
            delimiter: Delimiter for directory-like listing

        Returns:
            List of file paths
        """
        blobs = self.client.list_blobs(
            self.bucket_name,
            prefix=prefix,
            delimiter=delimiter
        )

        return [blob.name for blob in blobs]

    def delete_file(self, gcs_path: str) -> bool:
        """Delete a file from GCS.

        Args:
            gcs_path: Path to delete

        Returns:
            True if successful
        """
        blob = self.bucket.blob(gcs_path)

        try:
            blob.delete()
            return True
        except NotFound:
            return False

    def file_exists(self, gcs_path: str) -> bool:
        """Check if a file exists in GCS.

        Args:
            gcs_path: Path to check

        Returns:
            True if file exists
        """
        blob = self.bucket.blob(gcs_path)
        return blob.exists()

    def get_file_metadata(self, gcs_path: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a file.

        Args:
            gcs_path: Path to file

        Returns:
            Metadata dictionary or None if not found
        """
        blob = self.bucket.blob(gcs_path)

        try:
            blob.reload()
            return {
                "name": blob.name,
                "size": blob.size,
                "content_type": blob.content_type,
                "created": blob.time_created.isoformat() if blob.time_created else None,
                "updated": blob.updated.isoformat() if blob.updated else None,
                "metadata": blob.metadata or {},
            }
        except NotFound:
            return None

    def generate_signed_url(
        self,
        gcs_path: str,
        expiration_minutes: int = 60
    ) -> Optional[str]:
        """Generate a signed URL for temporary access.

        Args:
            gcs_path: Path to file
            expiration_minutes: URL expiration time in minutes

        Returns:
            Signed URL or None if file not found
        """
        blob = self.bucket.blob(gcs_path)

        if not blob.exists():
            return None

        url = blob.generate_signed_url(
            expiration=timedelta(minutes=expiration_minutes)
        )

        return url

    # Convenience methods for LearnQwest structure
    def save_config(self, config_name: str, config_data: Dict) -> str:
        """Save configuration file.

        Args:
            config_name: Configuration name
            config_data: Configuration dictionary

        Returns:
            GCS URI
        """
        gcs_path = f"config/{config_name}.json"
        return self.upload_json(config_data, gcs_path)

    def load_config(self, config_name: str) -> Optional[Dict]:
        """Load configuration file.

        Args:
            config_name: Configuration name

        Returns:
            Configuration dictionary or None
        """
        gcs_path = f"config/{config_name}.json"
        return self.download_json(gcs_path)

    def save_log(
        self,
        log_name: str,
        log_content: str,
        timestamp: Optional[datetime] = None
    ) -> str:
        """Save log file.

        Args:
            log_name: Log file name
            log_content: Log content
            timestamp: Optional timestamp (defaults to now)

        Returns:
            GCS URI
        """
        if timestamp is None:
            timestamp = datetime.utcnow()

        date_path = timestamp.strftime("%Y/%m/%d")
        gcs_path = f"logs/{date_path}/{log_name}"

        return self.upload_string(
            log_content,
            gcs_path,
            content_type='text/plain',
            metadata={"timestamp": timestamp.isoformat()}
        )

    def save_artifact(
        self,
        agent_id: str,
        artifact_name: str,
        artifact_data: Union[str, Dict],
        timestamp: Optional[datetime] = None
    ) -> str:
        """Save agent artifact.

        Args:
            agent_id: Agent identifier
            artifact_name: Artifact name
            artifact_data: Artifact content (string or dict)
            timestamp: Optional timestamp

        Returns:
            GCS URI
        """
        if timestamp is None:
            timestamp = datetime.utcnow()

        date_path = timestamp.strftime("%Y/%m/%d")
        gcs_path = f"artifacts/{agent_id}/{date_path}/{artifact_name}"

        if isinstance(artifact_data, dict):
            return self.upload_json(artifact_data, gcs_path)
        else:
            return self.upload_string(artifact_data, gcs_path)

    def save_trace_overflow(
        self,
        trace_id: str,
        span_id: str,
        payload: Dict[str, Any]
    ) -> str:
        """Save overflow trace data (for payloads > 256KB).

        Args:
            trace_id: Trace identifier
            span_id: Span identifier
            payload: Payload to store

        Returns:
            GCS URI
        """
        gcs_path = f"traces/{trace_id}/{span_id}.json"
        return self.upload_json(payload, gcs_path)

    def load_trace_overflow(
        self,
        trace_id: str,
        span_id: str
    ) -> Optional[Dict[str, Any]]:
        """Load overflow trace data.

        Args:
            trace_id: Trace identifier
            span_id: Span identifier

        Returns:
            Payload dictionary or None
        """
        gcs_path = f"traces/{trace_id}/{span_id}.json"
        return self.download_json(gcs_path)
