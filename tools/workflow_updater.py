#!/usr/bin/env python3
"""
LearnQwest Workflow Diagram Updater
Team LINK - Digital Self Partnership Tool

Programmatically append new agents, connections, and updates to the living Mermaid diagram.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional


class WorkflowUpdater:
    """Manages updates to the LearnQwest Mermaid workflow diagram."""

    def __init__(self, workflow_file: str = "LEARNQWEST_WORKFLOW.mmd"):
        self.workflow_path = Path(workflow_file)
        self.content: List[str] = []
        self.load()

    def load(self) -> None:
        """Load current workflow diagram."""
        if self.workflow_path.exists():
            self.content = self.workflow_path.read_text().splitlines()
        else:
            raise FileNotFoundError(f"Workflow file not found: {self.workflow_path}")

    def save(self) -> None:
        """Save updated workflow diagram."""
        self.workflow_path.write_text("\n".join(self.content) + "\n")

    def add_changelog_entry(self, description: str) -> None:
        """Add entry to changelog at top of file."""
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        changelog_line = f"%% {timestamp}: {description}"

        # Find changelog section and insert after header
        for i, line in enumerate(self.content):
            if "%% CHANGELOG:" in line:
                # Insert after the CHANGELOG: line
                self.content.insert(i + 1, changelog_line)
                break

    def add_agent(
        self,
        agent_id: str,
        agent_name: str,
        description: str,
        tier: str,
        status: str = "Planned",
    ) -> str:
        """
        Add a new agent node to the diagram.

        Args:
            agent_id: Unique identifier (e.g., "Ion-Quiz-V2")
            agent_name: Display name
            description: What the agent does
            tier: Which tier subgraph to add to (e.g., "Tier4_Generation")
            status: Current status (Planned/Development/Deployed)

        Returns:
            The node definition that was added
        """
        timestamp = datetime.now().strftime("%Y-%m-%d")
        node_def = f'        {agent_id}["{agent_name}<br/>{description}<br/>{timestamp}<br/>Status: {status}"]'

        # Find the tier subgraph and append before closing
        in_target_tier = False
        for i, line in enumerate(self.content):
            if f'subgraph {tier}[' in line:
                in_target_tier = True
            elif in_target_tier and line.strip() == "end":
                # Insert before the 'end' of this subgraph
                self.content.insert(i, node_def)
                self.add_changelog_entry(f"Added agent {agent_id} to {tier}")
                return node_def

        raise ValueError(f"Tier {tier} not found in diagram")

    def add_connection(
        self,
        from_node: str,
        to_node: str,
        label: str = "",
        connection_type: str = "-->",
    ) -> str:
        """
        Add a connection between two nodes.

        Args:
            from_node: Source node ID
            to_node: Target node ID
            label: Edge label describing the relationship
            connection_type: Arrow type (-->, -..->, ==>, etc.)

        Returns:
            The connection definition that was added
        """
        if label:
            conn_def = f"        {from_node} {connection_type}|{label}| {to_node}"
        else:
            conn_def = f"        {from_node} {connection_type} {to_node}"

        # Find the CROSS-TIER CONNECTIONS section or create it
        for i, line in enumerate(self.content):
            if "CROSS-TIER CONNECTIONS" in line:
                # Find the end of this section
                for j in range(i, len(self.content)):
                    if self.content[j].strip().startswith("%%") and j > i + 2:
                        self.content.insert(j, conn_def)
                        self.add_changelog_entry(
                            f"Connected {from_node} to {to_node}"
                        )
                        return conn_def

        # If section not found, append at end before styling
        for i, line in enumerate(self.content):
            if "STYLING" in line:
                self.content.insert(i - 1, conn_def)
                self.add_changelog_entry(f"Connected {from_node} to {to_node}")
                return conn_def

        raise ValueError("Could not find appropriate section for connection")

    def add_subgraph(
        self, subgraph_id: str, title: str, description: str = ""
    ) -> None:
        """Add a new functional subgraph to the diagram."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        subgraph_header = f"""
    %% ============================================================================
    %% {title.upper()}
    %% Added: {timestamp}
    %% {description}
    %% ============================================================================
    subgraph {subgraph_id}["{title}"]
    end
"""
        # Insert before STYLING section
        for i, line in enumerate(self.content):
            if "STYLING" in line:
                self.content.insert(i - 1, subgraph_header)
                self.add_changelog_entry(f"Added subgraph {subgraph_id}: {title}")
                break

    def update_agent_status(self, agent_id: str, new_status: str) -> None:
        """Update the status of an existing agent."""
        for i, line in enumerate(self.content):
            if agent_id in line and "Status:" in line:
                # Replace the status
                updated_line = re.sub(
                    r"Status: \w+", f"Status: {new_status}", line
                )
                self.content[i] = updated_line
                self.add_changelog_entry(f"Updated {agent_id} status to {new_status}")
                break

    def get_agent_count(self) -> int:
        """Count total number of agents in the diagram."""
        count = 0
        for line in self.content:
            if "Ion-" in line and "[" in line and "]" in line:
                count += 1
        return count

    def search_agents(self, keyword: str) -> List[str]:
        """Search for agents containing keyword."""
        results = []
        for line in self.content:
            if keyword.lower() in line.lower() and "Ion-" in line:
                results.append(line.strip())
        return results


def main():
    """Example usage of WorkflowUpdater."""
    updater = WorkflowUpdater("LEARNQWEST_WORKFLOW.mmd")

    print(f"[OK] Loaded workflow diagram")
    print(f"Total agents: {updater.get_agent_count()}")

    # Example: Add a new agent
    # updater.add_agent(
    #     agent_id="Ion-CodeReviewer-v1",
    #     agent_name="Ion Code Reviewer",
    #     description="Reviews generated code",
    #     tier="Tier6_QA",
    #     status="Development"
    # )

    # Example: Add a connection
    # updater.add_connection(
    #     from_node="Ion-CodeReviewer-v1",
    #     to_node="ComplianceValidator",
    #     label="code review results"
    # )

    # Example: Update status
    # updater.update_agent_status("Ion-YouTube-Collector", "Deployed")

    # updater.save()
    # print("[FIRE] Workflow diagram updated!")


if __name__ == "__main__":
    main()
