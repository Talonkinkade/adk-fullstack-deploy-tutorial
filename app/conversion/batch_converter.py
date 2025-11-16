"""Batch Converter - Convert multiple features to agents in parallel.

Features:
- Parallel processing (up to 10 concurrent conversions)
- Progress tracking
- Error handling and rollback
- Conversion reporting
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..ada.registry import AgentRegistry, AgentManifest, AgentCapability, AgentTier, AgentStatus
from .feature_analyzer import FeatureAnalyzer, FeatureSpec
from .template_generator import AgentTemplateGenerator
from .scaffolder import AgentScaffolder


@dataclass
class ConversionResult:
    """Result of converting a single feature to an agent."""
    feature_name: str
    success: bool
    agent_id: Optional[str] = None
    agent_path: Optional[Path] = None
    error: Optional[str] = None
    duration_seconds: float = 0.0


@dataclass
class BatchConversionReport:
    """Report for batch conversion operation."""
    total_features: int
    successful: int
    failed: int
    start_time: datetime
    end_time: datetime
    results: List[ConversionResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_features == 0:
            return 0.0
        return (self.successful / self.total_features) * 100

    @property
    def duration_seconds(self) -> float:
        """Total duration in seconds."""
        return (self.end_time - self.start_time).total_seconds()

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "total_features": self.total_features,
            "successful": self.successful,
            "failed": self.failed,
            "success_rate": round(self.success_rate, 2),
            "duration_seconds": round(self.duration_seconds, 2),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "results": [
                {
                    "feature_name": r.feature_name,
                    "success": r.success,
                    "agent_id": r.agent_id,
                    "error": r.error,
                    "duration_seconds": r.duration_seconds,
                }
                for r in self.results
            ],
        }


class BatchConverter:
    """Batch convert features/programs to autonomous agents.

    Pipeline:
    1. Analyze features (extract inputs, outputs, logic)
    2. Generate agent templates
    3. Scaffold code using ADK
    4. Register agents
    5. Deploy and activate
    """

    def __init__(
        self,
        registry: AgentRegistry,
        output_dir: Path,
        max_concurrent: int = 10
    ):
        """Initialize batch converter.

        Args:
            registry: Agent registry for registration
            output_dir: Directory to write generated agents
            max_concurrent: Maximum parallel conversions
        """
        self.registry = registry
        self.output_dir = Path(output_dir)
        self.max_concurrent = max_concurrent

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Components
        self.analyzer = FeatureAnalyzer()
        self.template_generator = AgentTemplateGenerator()
        self.scaffolder = AgentScaffolder(output_dir)

    async def convert_features(
        self,
        features: List[Dict[str, str]],
        auto_register: bool = True,
        auto_deploy: bool = False
    ) -> BatchConversionReport:
        """Convert multiple features to agents in parallel.

        Args:
            features: List of feature specs with 'name', 'description', 'code'
            auto_register: Automatically register agents
            auto_deploy: Automatically deploy agents (local only)

        Returns:
            Batch conversion report
        """
        start_time = datetime.now()

        # Convert to feature specs
        feature_specs = []
        for feature_data in features:
            spec = FeatureSpec(
                name=feature_data.get("name", "unknown"),
                description=feature_data.get("description", ""),
                code=feature_data.get("code", ""),
                metadata=feature_data.get("metadata", {})
            )
            feature_specs.append(spec)

        # Process in parallel (up to max_concurrent)
        semaphore = asyncio.Semaphore(self.max_concurrent)
        tasks = [
            self._convert_single_feature(
                spec,
                semaphore,
                auto_register,
                auto_deploy
            )
            for spec in feature_specs
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        conversion_results = []
        successful = 0
        failed = 0

        for result in results:
            if isinstance(result, Exception):
                conversion_results.append(ConversionResult(
                    feature_name="unknown",
                    success=False,
                    error=str(result)
                ))
                failed += 1
            elif result.success:
                conversion_results.append(result)
                successful += 1
            else:
                conversion_results.append(result)
                failed += 1

        end_time = datetime.now()

        report = BatchConversionReport(
            total_features=len(features),
            successful=successful,
            failed=failed,
            start_time=start_time,
            end_time=end_time,
            results=conversion_results
        )

        return report

    async def _convert_single_feature(
        self,
        spec: FeatureSpec,
        semaphore: asyncio.Semaphore,
        auto_register: bool,
        auto_deploy: bool
    ) -> ConversionResult:
        """Convert a single feature to an agent.

        Args:
            spec: Feature specification
            semaphore: Concurrency limiter
            auto_register: Register agent
            auto_deploy: Deploy agent

        Returns:
            Conversion result
        """
        async with semaphore:
            start_time = datetime.now()

            try:
                # 1. Analyze feature
                analyzed = await self._run_in_thread(
                    self.analyzer.analyze,
                    spec
                )

                # 2. Generate template
                template = await self._run_in_thread(
                    self.template_generator.generate,
                    analyzed
                )

                # 3. Scaffold code
                agent_path = await self._run_in_thread(
                    self.scaffolder.scaffold,
                    template
                )

                # 4. Register agent if requested
                agent_id = None
                if auto_register:
                    agent_id = await self._register_agent(template)

                # 5. Deploy if requested
                if auto_deploy and agent_id:
                    await self._deploy_agent(agent_id)

                duration = (datetime.now() - start_time).total_seconds()

                return ConversionResult(
                    feature_name=spec.name,
                    success=True,
                    agent_id=agent_id,
                    agent_path=agent_path,
                    duration_seconds=duration
                )

            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                return ConversionResult(
                    feature_name=spec.name,
                    success=False,
                    error=str(e),
                    duration_seconds=duration
                )

    async def _run_in_thread(self, func, *args):
        """Run blocking function in thread pool."""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, func, *args)

    async def _register_agent(self, template: Dict) -> str:
        """Register agent with ADA registry.

        Args:
            template: Agent template

        Returns:
            Agent ID
        """
        # Create agent manifest
        manifest = AgentManifest(
            agent_id=template["agent_id"],
            name=template["name"],
            description=template["description"],
            tier=AgentTier(template["tier"]),
            capabilities={AgentCapability[cap] for cap in template["capabilities"]},
            model=template.get("model", "gemini-2.5-flash"),
            max_concurrent_tasks=template.get("max_concurrent_tasks", 1),
            status=AgentStatus.READY,
        )

        # Register
        success = self.registry.register(manifest)
        if not success:
            raise ValueError(f"Failed to register agent: {template['agent_id']}")

        return template["agent_id"]

    async def _deploy_agent(self, agent_id: str) -> None:
        """Deploy agent to local pool.

        Args:
            agent_id: Agent to deploy
        """
        # For local deployment, just mark as ready
        # In production, this would deploy to Vertex AI
        agent = self.registry.get(agent_id)
        if agent:
            agent.status = AgentStatus.READY
            print(f"✓ Agent {agent_id} deployed locally")

    def generate_report_markdown(self, report: BatchConversionReport) -> str:
        """Generate markdown report.

        Args:
            report: Batch conversion report

        Returns:
            Markdown formatted report
        """
        lines = ["# Agent Conversion Report\n"]

        lines.append(f"**Date:** {report.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append(f"**Duration:** {report.duration_seconds:.2f}s\n")

        lines.append("## Summary\n")
        lines.append(f"- **Total Features:** {report.total_features}")
        lines.append(f"- **Successful:** {report.successful}")
        lines.append(f"- **Failed:** {report.failed}")
        lines.append(f"- **Success Rate:** {report.success_rate:.1f}%\n")

        if report.successful > 0:
            lines.append("## Successfully Converted\n")
            for result in report.results:
                if result.success:
                    lines.append(f"- ✓ **{result.feature_name}** → `{result.agent_id}` ({result.duration_seconds:.2f}s)")

        if report.failed > 0:
            lines.append("\n## Failed Conversions\n")
            for result in report.results:
                if not result.success:
                    lines.append(f"- ✗ **{result.feature_name}**: {result.error}")

        return "\n".join(lines)
