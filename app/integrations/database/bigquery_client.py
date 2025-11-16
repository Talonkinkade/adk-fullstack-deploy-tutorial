"""BigQuery Client - Time-series analytics and aggregations.

Stores:
- Time-series agent metrics
- Performance analytics
- Aggregated statistics
- Historical trends
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

try:
    from google.cloud import bigquery
    BIGQUERY_AVAILABLE = True
except ImportError:
    BIGQUERY_AVAILABLE = False


class BigQueryClient:
    """BigQuery client for analytics and time-series data.

    Tables:
    - agent_metrics_timeseries: Time-series agent performance data
    - task_analytics: Aggregated task statistics
    - daily_summaries: Daily performance summaries
    """

    def __init__(self, project_id: str, dataset_id: str = "learnqwest_metrics"):
        """Initialize BigQuery client.

        Args:
            project_id: GCP project ID
            dataset_id: BigQuery dataset name
        """
        if not BIGQUERY_AVAILABLE:
            raise ImportError("google-cloud-bigquery not installed. Install with: pip install google-cloud-bigquery")

        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.dataset_ref = f"{project_id}.{dataset_id}"

    def init_schema(self) -> None:
        """Initialize BigQuery dataset and tables."""
        # Create dataset if not exists
        dataset = bigquery.Dataset(self.dataset_ref)
        dataset.location = "US"
        try:
            self.client.create_dataset(dataset, exists_ok=True)
        except Exception as e:
            print(f"Dataset creation warning: {e}")

        # Create tables
        self._create_metrics_table()
        self._create_task_analytics_table()
        self._create_daily_summaries_table()

    def _create_metrics_table(self) -> None:
        """Create agent metrics time-series table."""
        schema = [
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("agent_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("agent_name", "STRING"),
            bigquery.SchemaField("tier", "INTEGER"),
            bigquery.SchemaField("total_tasks", "INTEGER"),
            bigquery.SchemaField("successful_tasks", "INTEGER"),
            bigquery.SchemaField("failed_tasks", "INTEGER"),
            bigquery.SchemaField("avg_response_time_ms", "FLOAT"),
            bigquery.SchemaField("current_load", "INTEGER"),
            bigquery.SchemaField("success_rate", "FLOAT"),
            bigquery.SchemaField("metadata", "JSON"),
        ]

        table_ref = f"{self.dataset_ref}.agent_metrics_timeseries"
        table = bigquery.Table(table_ref, schema=schema)

        # Partition by timestamp (daily)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="timestamp"
        )

        # Cluster by agent_id for faster queries
        table.clustering_fields = ["agent_id"]

        try:
            self.client.create_table(table, exists_ok=True)
        except Exception as e:
            print(f"Table creation warning: {e}")

    def _create_task_analytics_table(self) -> None:
        """Create task analytics table."""
        schema = [
            bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("agent_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("task_type", "STRING"),
            bigquery.SchemaField("total_tasks", "INTEGER"),
            bigquery.SchemaField("successful_tasks", "INTEGER"),
            bigquery.SchemaField("failed_tasks", "INTEGER"),
            bigquery.SchemaField("avg_duration_seconds", "FLOAT"),
            bigquery.SchemaField("total_duration_seconds", "FLOAT"),
        ]

        table_ref = f"{self.dataset_ref}.task_analytics"
        table = bigquery.Table(table_ref, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="date"
        )

        try:
            self.client.create_table(table, exists_ok=True)
        except Exception as e:
            print(f"Table creation warning: {e}")

    def _create_daily_summaries_table(self) -> None:
        """Create daily summaries table."""
        schema = [
            bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("total_agents", "INTEGER"),
            bigquery.SchemaField("active_agents", "INTEGER"),
            bigquery.SchemaField("total_tasks", "INTEGER"),
            bigquery.SchemaField("successful_tasks", "INTEGER"),
            bigquery.SchemaField("failed_tasks", "INTEGER"),
            bigquery.SchemaField("avg_success_rate", "FLOAT"),
            bigquery.SchemaField("avg_response_time_ms", "FLOAT"),
            bigquery.SchemaField("top_performers", "JSON"),
        ]

        table_ref = f"{self.dataset_ref}.daily_summaries"
        table = bigquery.Table(table_ref, schema=schema)

        try:
            self.client.create_table(table, exists_ok=True)
        except Exception as e:
            print(f"Table creation warning: {e}")

    def insert_metrics(
        self,
        agent_id: str,
        agent_name: str,
        tier: int,
        metrics: Dict[str, Any],
        timestamp: Optional[datetime] = None
    ) -> bool:
        """Insert agent metrics data point.

        Args:
            agent_id: Agent identifier
            agent_name: Agent name
            tier: Agent tier (1-8)
            metrics: Metrics dictionary
            timestamp: Timestamp (defaults to now)

        Returns:
            True if successful
        """
        if timestamp is None:
            timestamp = datetime.utcnow()

        row = {
            "timestamp": timestamp.isoformat(),
            "agent_id": agent_id,
            "agent_name": agent_name,
            "tier": tier,
            "total_tasks": metrics.get("total_tasks", 0),
            "successful_tasks": metrics.get("successful_tasks", 0),
            "failed_tasks": metrics.get("failed_tasks", 0),
            "avg_response_time_ms": metrics.get("avg_response_time_ms", 0.0),
            "current_load": metrics.get("current_load", 0),
            "success_rate": metrics.get("success_rate", 0.0),
            "metadata": metrics.get("metadata", {}),
        }

        table_ref = f"{self.dataset_ref}.agent_metrics_timeseries"
        errors = self.client.insert_rows_json(table_ref, [row])

        if errors:
            print(f"BigQuery insert errors: {errors}")
            return False
        return True

    def get_agent_metrics(
        self,
        agent_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Dict]:
        """Get agent metrics time-series.

        Args:
            agent_id: Agent identifier
            start_time: Start of time range
            end_time: End of time range

        Returns:
            List of metric records
        """
        if start_time is None:
            start_time = datetime.utcnow() - timedelta(days=7)
        if end_time is None:
            end_time = datetime.utcnow()

        query = f"""
            SELECT *
            FROM `{self.dataset_ref}.agent_metrics_timeseries`
            WHERE agent_id = @agent_id
              AND timestamp BETWEEN @start_time AND @end_time
            ORDER BY timestamp ASC
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("agent_id", "STRING", agent_id),
                bigquery.ScalarQueryParameter("start_time", "TIMESTAMP", start_time),
                bigquery.ScalarQueryParameter("end_time", "TIMESTAMP", end_time),
            ]
        )

        results = self.client.query(query, job_config=job_config)
        return [dict(row) for row in results]

    def get_top_performers(
        self,
        metric: str = "success_rate",
        limit: int = 10,
        time_range_hours: int = 24
    ) -> List[Dict]:
        """Get top performing agents.

        Args:
            metric: Metric to rank by (success_rate, avg_response_time_ms, total_tasks)
            limit: Number of agents to return
            time_range_hours: Time range in hours

        Returns:
            List of top performers
        """
        start_time = datetime.utcnow() - timedelta(hours=time_range_hours)

        query = f"""
            SELECT
                agent_id,
                agent_name,
                AVG({metric}) as avg_{metric},
                COUNT(*) as data_points
            FROM `{self.dataset_ref}.agent_metrics_timeseries`
            WHERE timestamp >= @start_time
            GROUP BY agent_id, agent_name
            ORDER BY avg_{metric} DESC
            LIMIT @limit
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("start_time", "TIMESTAMP", start_time),
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
            ]
        )

        results = self.client.query(query, job_config=job_config)
        return [dict(row) for row in results]

    def get_daily_summary(self, date: Optional[datetime] = None) -> Optional[Dict]:
        """Get daily summary for a specific date.

        Args:
            date: Date to get summary for (defaults to today)

        Returns:
            Summary dictionary or None
        """
        if date is None:
            date = datetime.utcnow().date()
        elif isinstance(date, datetime):
            date = date.date()

        query = f"""
            SELECT *
            FROM `{self.dataset_ref}.daily_summaries`
            WHERE date = @date
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("date", "DATE", date),
            ]
        )

        results = self.client.query(query, job_config=job_config)
        row = next(iter(results), None)
        return dict(row) if row else None

    def aggregate_daily_summary(self, date: Optional[datetime] = None) -> bool:
        """Aggregate and store daily summary.

        Args:
            date: Date to aggregate (defaults to yesterday)

        Returns:
            True if successful
        """
        if date is None:
            date = (datetime.utcnow() - timedelta(days=1)).date()
        elif isinstance(date, datetime):
            date = date.date()

        # Aggregate metrics for the day
        query = f"""
            INSERT INTO `{self.dataset_ref}.daily_summaries`
            SELECT
                DATE(timestamp) as date,
                COUNT(DISTINCT agent_id) as total_agents,
                COUNT(DISTINCT CASE WHEN total_tasks > 0 THEN agent_id END) as active_agents,
                SUM(total_tasks) as total_tasks,
                SUM(successful_tasks) as successful_tasks,
                SUM(failed_tasks) as failed_tasks,
                AVG(success_rate) as avg_success_rate,
                AVG(avg_response_time_ms) as avg_response_time_ms,
                TO_JSON_STRING(ARRAY_AGG(
                    STRUCT(agent_id, agent_name, success_rate)
                    ORDER BY success_rate DESC
                    LIMIT 10
                )) as top_performers
            FROM `{self.dataset_ref}.agent_metrics_timeseries`
            WHERE DATE(timestamp) = @date
            GROUP BY DATE(timestamp)
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("date", "DATE", date),
            ]
        )

        try:
            self.client.query(query, job_config=job_config).result()
            return True
        except Exception as e:
            print(f"Daily summary aggregation error: {e}")
            return False

    def get_trend_analysis(
        self,
        agent_id: str,
        metric: str = "success_rate",
        days: int = 30
    ) -> Dict:
        """Analyze trend for an agent metric over time.

        Args:
            agent_id: Agent identifier
            metric: Metric to analyze
            days: Number of days to analyze

        Returns:
            Trend analysis with slope, average, min, max
        """
        start_time = datetime.utcnow() - timedelta(days=days)

        query = f"""
            WITH daily_avg AS (
                SELECT
                    DATE(timestamp) as date,
                    AVG({metric}) as value
                FROM `{self.dataset_ref}.agent_metrics_timeseries`
                WHERE agent_id = @agent_id
                  AND timestamp >= @start_time
                GROUP BY DATE(timestamp)
                ORDER BY date ASC
            )
            SELECT
                AVG(value) as avg_value,
                MIN(value) as min_value,
                MAX(value) as max_value,
                STDDEV(value) as std_dev,
                -- Linear regression slope (simplified)
                (COUNT(*) * SUM(UNIX_DATE(date) * value) - SUM(UNIX_DATE(date)) * SUM(value)) /
                (COUNT(*) * SUM(UNIX_DATE(date) * UNIX_DATE(date)) - SUM(UNIX_DATE(date)) * SUM(UNIX_DATE(date))) as trend_slope
            FROM daily_avg
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("agent_id", "STRING", agent_id),
                bigquery.ScalarQueryParameter("start_time", "TIMESTAMP", start_time),
            ]
        )

        results = self.client.query(query, job_config=job_config)
        row = next(iter(results), None)

        if row:
            return {
                "agent_id": agent_id,
                "metric": metric,
                "days_analyzed": days,
                "avg": float(row["avg_value"]) if row["avg_value"] else 0.0,
                "min": float(row["min_value"]) if row["min_value"] else 0.0,
                "max": float(row["max_value"]) if row["max_value"] else 0.0,
                "std_dev": float(row["std_dev"]) if row["std_dev"] else 0.0,
                "trend": "improving" if (row["trend_slope"] or 0) > 0 else "declining",
                "trend_slope": float(row["trend_slope"]) if row["trend_slope"] else 0.0,
            }

        return {}
