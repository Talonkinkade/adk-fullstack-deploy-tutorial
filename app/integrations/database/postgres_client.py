"""PostgreSQL Client - Structured data storage for sessions, users, and worklogs.

Stores:
- Session data
- User profiles
- Agent worklogs
- Task metadata
- Performance metrics
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from contextlib import contextmanager

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor, Json
    from psycopg2.pool import ThreadedConnectionPool
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


class PostgreSQLClient:
    """PostgreSQL client for LearnQwest data storage.

    Tables:
    - sessions: ADK session data
    - users: User profiles
    - worklogs: Agent worklog entries
    - tasks: Task metadata
    - agent_metrics: Agent performance metrics
    """

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        min_connections: int = 1,
        max_connections: int = 10
    ):
        """Initialize PostgreSQL client.

        Args:
            host: Database host
            port: Database port
            database: Database name
            user: Database user
            password: Database password
            min_connections: Minimum connections in pool
            max_connections: Maximum connections in pool
        """
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2 not installed. Install with: pip install psycopg2-binary")

        self.pool = ThreadedConnectionPool(
            min_connections,
            max_connections,
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

    @contextmanager
    def get_connection(self):
        """Get a connection from the pool."""
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)

    @contextmanager
    def get_cursor(self, dict_cursor: bool = True):
        """Get a cursor (auto-commits on success)."""
        with self.get_connection() as conn:
            cursor_factory = RealDictCursor if dict_cursor else None
            cursor = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()

    def init_schema(self) -> None:
        """Initialize database schema."""
        schema_sql = """
        -- Sessions table
        CREATE TABLE IF NOT EXISTS sessions (
            session_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            app_name VARCHAR(255),
            state JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_user_id (user_id),
            INDEX idx_created_at (created_at)
        );

        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(255) PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            email VARCHAR(255),
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Worklogs table
        CREATE TABLE IF NOT EXISTS worklogs (
            entry_id VARCHAR(255) PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            agent_id VARCHAR(255),
            raw_content TEXT,
            parsed_data JSONB,
            sentiment_score FLOAT,
            confidence_score FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_timestamp (timestamp),
            INDEX idx_agent_id (agent_id)
        );

        -- Tasks table
        CREATE TABLE IF NOT EXISTS tasks (
            task_id VARCHAR(255) PRIMARY KEY,
            task_type VARCHAR(100),
            status VARCHAR(50),
            agent_id VARCHAR(255),
            agent_name VARCHAR(255),
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            duration_seconds FLOAT,
            success BOOLEAN,
            error_message TEXT,
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_agent_id (agent_id),
            INDEX idx_status (status),
            INDEX idx_created_at (created_at)
        );

        -- Agent metrics table
        CREATE TABLE IF NOT EXISTS agent_metrics (
            metric_id SERIAL PRIMARY KEY,
            agent_id VARCHAR(255) NOT NULL,
            agent_name VARCHAR(255),
            timestamp TIMESTAMP NOT NULL,
            total_tasks INTEGER DEFAULT 0,
            successful_tasks INTEGER DEFAULT 0,
            failed_tasks INTEGER DEFAULT 0,
            avg_response_time_ms FLOAT,
            current_load INTEGER DEFAULT 0,
            success_rate FLOAT,
            metadata JSONB,
            INDEX idx_agent_id (agent_id),
            INDEX idx_timestamp (timestamp)
        );

        -- Leaderboard table
        CREATE TABLE IF NOT EXISTS leaderboard (
            entry_id SERIAL PRIMARY KEY,
            agent_id VARCHAR(255) NOT NULL,
            agent_name VARCHAR(255),
            score FLOAT NOT NULL,
            rank INTEGER,
            period VARCHAR(50),
            metrics JSONB,
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_agent_id (agent_id),
            INDEX idx_period (period),
            INDEX idx_score (score DESC)
        );
        """

        with self.get_cursor(dict_cursor=False) as cursor:
            cursor.execute(schema_sql)

    # Session operations
    def create_session(
        self,
        session_id: str,
        user_id: str,
        app_name: str,
        state: Optional[Dict] = None
    ) -> bool:
        """Create a new session."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO sessions (session_id, user_id, app_name, state)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (session_id) DO NOTHING
            """, (session_id, user_id, app_name, Json(state or {})))
            return cursor.rowcount > 0

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM sessions WHERE session_id = %s
            """, (session_id,))
            return dict(cursor.fetchone()) if cursor.rowcount > 0 else None

    def update_session_state(self, session_id: str, state: Dict) -> bool:
        """Update session state."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                UPDATE sessions
                SET state = %s, last_update_time = CURRENT_TIMESTAMP
                WHERE session_id = %s
            """, (Json(state), session_id))
            return cursor.rowcount > 0

    # Worklog operations
    def insert_worklog(
        self,
        entry_id: str,
        timestamp: datetime,
        agent_id: str,
        raw_content: str,
        parsed_data: Dict,
        sentiment_score: Optional[float] = None,
        confidence_score: Optional[float] = None
    ) -> bool:
        """Insert a worklog entry."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO worklogs
                (entry_id, timestamp, agent_id, raw_content, parsed_data, sentiment_score, confidence_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (entry_id) DO NOTHING
            """, (entry_id, timestamp, agent_id, raw_content, Json(parsed_data),
                  sentiment_score, confidence_score))
            return cursor.rowcount > 0

    def get_agent_worklogs(
        self,
        agent_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get worklogs for an agent."""
        with self.get_cursor() as cursor:
            query = "SELECT * FROM worklogs WHERE agent_id = %s"
            params = [agent_id]

            if start_time:
                query += " AND timestamp >= %s"
                params.append(start_time)

            if end_time:
                query += " AND timestamp <= %s"
                params.append(end_time)

            query += " ORDER BY timestamp DESC LIMIT %s"
            params.append(limit)

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    # Task operations
    def insert_task(self, task_metadata: Dict) -> bool:
        """Insert task metadata."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO tasks
                (task_id, task_type, status, agent_id, agent_name, start_time,
                 end_time, duration_seconds, success, error_message, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (task_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    end_time = EXCLUDED.end_time,
                    duration_seconds = EXCLUDED.duration_seconds,
                    success = EXCLUDED.success,
                    error_message = EXCLUDED.error_message,
                    metadata = EXCLUDED.metadata
            """, (
                task_metadata['task_id'],
                task_metadata.get('task_type'),
                task_metadata.get('status'),
                task_metadata.get('agent_id'),
                task_metadata.get('agent_name'),
                task_metadata.get('start_time'),
                task_metadata.get('end_time'),
                task_metadata.get('duration_seconds'),
                task_metadata.get('success'),
                task_metadata.get('error_message'),
                Json(task_metadata.get('metadata', {}))
            ))
            return cursor.rowcount > 0

    # Agent metrics operations
    def record_agent_metrics(
        self,
        agent_id: str,
        agent_name: str,
        metrics: Dict
    ) -> bool:
        """Record agent performance metrics."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO agent_metrics
                (agent_id, agent_name, timestamp, total_tasks, successful_tasks,
                 failed_tasks, avg_response_time_ms, current_load, success_rate, metadata)
                VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s)
            """, (
                agent_id,
                agent_name,
                metrics.get('total_tasks', 0),
                metrics.get('successful_tasks', 0),
                metrics.get('failed_tasks', 0),
                metrics.get('avg_response_time_ms', 0.0),
                metrics.get('current_load', 0),
                metrics.get('success_rate', 0.0),
                Json(metrics.get('metadata', {}))
            ))
            return cursor.rowcount > 0

    def get_agent_metrics(
        self,
        agent_id: str,
        start_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get agent metrics history."""
        with self.get_cursor() as cursor:
            if start_time:
                cursor.execute("""
                    SELECT * FROM agent_metrics
                    WHERE agent_id = %s AND timestamp >= %s
                    ORDER BY timestamp DESC LIMIT %s
                """, (agent_id, start_time, limit))
            else:
                cursor.execute("""
                    SELECT * FROM agent_metrics
                    WHERE agent_id = %s
                    ORDER BY timestamp DESC LIMIT %s
                """, (agent_id, limit))

            return [dict(row) for row in cursor.fetchall()]

    # Leaderboard operations
    def update_leaderboard(
        self,
        agent_id: str,
        agent_name: str,
        score: float,
        period: str,
        metrics: Dict
    ) -> bool:
        """Update leaderboard entry."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO leaderboard
                (agent_id, agent_name, score, period, metrics)
                VALUES (%s, %s, %s, %s, %s)
            """, (agent_id, agent_name, score, period, Json(metrics)))
            return cursor.rowcount > 0

    def get_leaderboard(
        self,
        period: str = "all_time",
        limit: int = 100
    ) -> List[Dict]:
        """Get leaderboard rankings."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT *,
                       ROW_NUMBER() OVER (ORDER BY score DESC) as rank
                FROM leaderboard
                WHERE period = %s
                ORDER BY score DESC
                LIMIT %s
            """, (period, limit))
            return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Close all connections in the pool."""
        self.pool.closeall()
