"""Agent Template Generator - Generate agent code templates from analyzed features."""

from typing import Dict, List

from .feature_analyzer import AnalyzedFeature


class AgentTemplateGenerator:
    """Generate agent templates from analyzed features.

    Outputs:
    - Agent manifest (metadata)
    - Code template structure
    - ADK integration points
    """

    def generate(self, analyzed: AnalyzedFeature) -> Dict:
        """Generate agent template from analyzed feature.

        Args:
            analyzed: Analyzed feature specification

        Returns:
            Template dictionary with all agent components
        """
        agent_id = self._generate_agent_id(analyzed.name)

        template = {
            # Identity
            "agent_id": agent_id,
            "name": analyzed.name,
            "description": analyzed.description,
            "tier": analyzed.suggested_tier,

            # Capabilities
            "capabilities": list(analyzed.capabilities),
            "model": analyzed.suggested_model,
            "max_concurrent_tasks": analyzed.max_concurrent_tasks,

            # Interface
            "inputs": analyzed.inputs,
            "outputs": analyzed.outputs,
            "dependencies": list(analyzed.dependencies),

            # Code
            "code_template": self._generate_code_template(analyzed),

            # Metadata
            "metadata": analyzed.metadata,
        }

        return template

    def _generate_agent_id(self, name: str) -> str:
        """Generate agent ID from name.

        Args:
            name: Agent name

        Returns:
            Agent ID (snake_case)
        """
        # Convert to snake_case
        agent_id = name.lower().replace(" ", "_").replace("-", "_")

        # Remove special characters
        agent_id = "".join(c for c in agent_id if c.isalnum() or c == "_")

        # Add suffix
        agent_id = f"agent_{agent_id}"

        return agent_id

    def _generate_code_template(self, analyzed: AnalyzedFeature) -> str:
        """Generate Python code template for agent.

        Args:
            analyzed: Analyzed feature

        Returns:
            Python code as string
        """
        # Extract input parameters
        input_params = ", ".join([
            f"{inp['name']}: Any" for inp in analyzed.inputs
        ])

        # Generate imports
        imports = ["from typing import Any, Dict, List, Optional"]
        imports.append("from google.genai.adk import LlmAgent")

        if analyzed.dependencies:
            for dep in analyzed.dependencies:
                imports.append(f"import {dep}")

        imports_str = "\n".join(imports)

        # Generate docstring
        docstring = f'''    """{analyzed.description}

    Auto-generated agent from feature conversion.

    Capabilities: {', '.join(analyzed.capabilities)}
    Tier: {analyzed.suggested_tier}
    """'''

        # Generate template
        template = f'''{imports_str}


class {self._to_camel_case(analyzed.name)}Agent(LlmAgent):
{docstring}

    def __init__(self):
        """Initialize agent."""
        super().__init__(
            name="{analyzed.name}",
            model="{analyzed.suggested_model}",
            description="{analyzed.description}",
        )

    async def execute(self, {input_params}) -> Dict[str, Any]:
        """Execute agent task.

        Args:
{self._generate_arg_docs(analyzed.inputs)}

        Returns:
            Execution result
        """
        # TODO: Implement agent logic
        # Original code:
        # {self._indent_code(analyzed.original_code or "# No code provided")}

        result = {{
            "status": "completed",
            "message": "Agent executed successfully",
            # Add your outputs here
        }}

        return result


# Agent factory function
def create_agent() -> {self._to_camel_case(analyzed.name)}Agent:
    """Create and return agent instance."""
    return {self._to_camel_case(analyzed.name)}Agent()
'''

        return template

    def _to_camel_case(self, text: str) -> str:
        """Convert text to CamelCase.

        Args:
            text: Input text

        Returns:
            CamelCase string
        """
        words = text.replace("_", " ").replace("-", " ").split()
        return "".join(word.capitalize() for word in words)

    def _generate_arg_docs(self, inputs: List[Dict]) -> str:
        """Generate argument documentation.

        Args:
            inputs: List of input specifications

        Returns:
            Formatted docstring arguments
        """
        if not inputs:
            return "            (none)"

        lines = []
        for inp in inputs:
            lines.append(f"            {inp['name']}: {inp.get('description', 'Input parameter')}")

        return "\n".join(lines)

    def _indent_code(self, code: str, indent: int = 8) -> str:
        """Indent code block.

        Args:
            code: Code to indent
            indent: Number of spaces

        Returns:
            Indented code
        """
        indent_str = " " * indent
        lines = code.split("\n")
        return "\n".join(f"{indent_str}# {line}" for line in lines)
