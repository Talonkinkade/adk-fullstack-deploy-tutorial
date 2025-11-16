"""Feature Analyzer - Extract agent specifications from feature code.

Extracts:
- Inputs and outputs
- Dependencies
- Core logic
- Appropriate tier and capabilities
"""

import ast
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class FeatureSpec:
    """Raw feature/program specification."""
    name: str
    description: str
    code: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class AnalyzedFeature:
    """Analyzed feature with extracted specifications."""
    name: str
    description: str

    # Extracted components
    inputs: List[Dict[str, str]] = field(default_factory=list)
    outputs: List[Dict[str, str]] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)
    capabilities: Set[str] = field(default_factory=list)

    # Agent configuration
    suggested_tier: int = 4  # Default to worker tier
    suggested_model: str = "gemini-2.5-flash"
    max_concurrent_tasks: int = 1

    # Original data
    original_code: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


class FeatureAnalyzer:
    """Analyze features and extract agent specifications.

    Uses:
    - AST parsing for Python code
    - Regex patterns for general text
    - Heuristics for capability detection
    """

    # Capability keywords
    CAPABILITY_KEYWORDS = {
        "CODE_GENERATION": ["generate", "create", "build", "implement", "write code"],
        "CODE_REVIEW": ["review", "lint", "check", "validate", "analyze"],
        "TESTING": ["test", "pytest", "jest", "unittest", "verify"],
        "DEPLOYMENT": ["deploy", "release", "publish", "push"],
        "DATA_PROCESSING": ["parse", "process", "transform", "extract"],
        "ANALYTICS": ["analyze", "metrics", "statistics", "report"],
        "MONITORING": ["monitor", "track", "observe", "alert"],
        "DOCUMENTATION": ["document", "readme", "docs", "generate docs"],
    }

    # Tier indicators
    TIER_INDICATORS = {
        1: ["orchestrate", "manage all", "coordinate system"],
        2: ["plan", "decompose", "allocate", "prioritize"],
        3: ["coordinate", "manage workers", "distribute"],
        4: ["execute", "implement", "process", "handle"],
    }

    def analyze(self, spec: FeatureSpec) -> AnalyzedFeature:
        """Analyze a feature and extract specifications.

        Args:
            spec: Feature specification

        Returns:
            Analyzed feature with extracted components
        """
        analyzed = AnalyzedFeature(
            name=spec.name,
            description=spec.description,
            original_code=spec.code,
            metadata=spec.metadata
        )

        # Extract capabilities from description
        analyzed.capabilities = self._extract_capabilities(spec.description)

        # Determine tier
        analyzed.suggested_tier = self._determine_tier(spec.description)

        # If code is provided, analyze it
        if spec.code:
            # Try to parse as Python
            try:
                analyzed.inputs, analyzed.outputs = self._analyze_python_code(spec.code)
                analyzed.dependencies = self._extract_python_dependencies(spec.code)
            except SyntaxError:
                # Not valid Python, use heuristics
                analyzed.inputs, analyzed.outputs = self._analyze_generic_code(spec.code)
                analyzed.dependencies = self._extract_generic_dependencies(spec.code)

        return analyzed

    def _extract_capabilities(self, description: str) -> Set[str]:
        """Extract capabilities from description.

        Args:
            description: Feature description

        Returns:
            Set of capability names
        """
        capabilities = set()
        description_lower = description.lower()

        for capability, keywords in self.CAPABILITY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    capabilities.add(capability)
                    break

        # Default to CODE_GENERATION if no specific capability found
        if not capabilities:
            capabilities.add("CODE_GENERATION")

        return capabilities

    def _determine_tier(self, description: str) -> int:
        """Determine appropriate tier from description.

        Args:
            description: Feature description

        Returns:
            Tier number (1-4, defaults to 4)
        """
        description_lower = description.lower()

        for tier, indicators in self.TIER_INDICATORS.items():
            for indicator in indicators:
                if indicator in description_lower:
                    return tier

        # Default to tier 4 (worker agent)
        return 4

    def _analyze_python_code(self, code: str) -> tuple[List[Dict], List[Dict]]:
        """Analyze Python code using AST.

        Args:
            code: Python source code

        Returns:
            Tuple of (inputs, outputs)
        """
        tree = ast.parse(code)

        inputs = []
        outputs = []

        # Find function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Extract parameters as inputs
                for arg in node.args.args:
                    inputs.append({
                        "name": arg.arg,
                        "type": "any",  # Could enhance with type hints
                        "description": f"Input parameter: {arg.arg}"
                    })

                # Extract return statements as outputs
                for child in ast.walk(node):
                    if isinstance(child, ast.Return):
                        outputs.append({
                            "name": "result",
                            "type": "any",
                            "description": "Function return value"
                        })
                        break

        return inputs, outputs

    def _extract_python_dependencies(self, code: str) -> Set[str]:
        """Extract Python import dependencies.

        Args:
            code: Python source code

        Returns:
            Set of dependency names
        """
        dependencies = set()

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencies.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dependencies.add(node.module.split('.')[0])
        except SyntaxError:
            pass

        return dependencies

    def _analyze_generic_code(self, code: str) -> tuple[List[Dict], List[Dict]]:
        """Analyze code using heuristics (non-Python).

        Args:
            code: Source code

        Returns:
            Tuple of (inputs, outputs)
        """
        inputs = []
        outputs = []

        # Look for function-like patterns
        function_pattern = r'function\s+\w+\s*\((.*?)\)'
        matches = re.findall(function_pattern, code, re.IGNORECASE)

        for match in matches:
            # Extract parameters
            params = [p.strip() for p in match.split(',') if p.strip()]
            for param in params:
                inputs.append({
                    "name": param,
                    "type": "any",
                    "description": f"Input parameter: {param}"
                })

        # Assume there's an output if there's a function
        if matches:
            outputs.append({
                "name": "result",
                "type": "any",
                "description": "Function output"
            })

        return inputs, outputs

    def _extract_generic_dependencies(self, code: str) -> Set[str]:
        """Extract dependencies from generic code.

        Args:
            code: Source code

        Returns:
            Set of dependency names
        """
        dependencies = set()

        # Look for import/require patterns
        patterns = [
            r'import\s+(\w+)',
            r'from\s+(\w+)\s+import',
            r'require\(["\'](\w+)["\']\)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, code)
            dependencies.update(matches)

        return dependencies
