# LearnQwest Agents Documentation

**Built with Google ADK (Agent Development Kit)**

This document provides comprehensive documentation for the LearnQwest agent system - a suite of intelligent agents designed to manage filesystem operations, documentation, and workflows within the LearnQwest ecosystem.

---

## Table of Contents

- [Overview](#overview)
- [Agent Architecture](#agent-architecture)
- [Available Agents](#available-agents)
  - [1. LearnQwest Filesystem Agent](#1-learnqwest-filesystem-agent)
  - [2. LearnQwest Documentation Agent](#2-learnqwest-documentation-agent)
  - [3. LearnQwest Workflow Agent](#3-learnqwest-workflow-agent)
  - [4. LearnQwest Orchestrator Agent](#4-learnqwest-orchestrator-agent)
- [Setup & Configuration](#setup--configuration)
- [Usage Examples](#usage-examples)
- [Integration with MCP Filesystem](#integration-with-mcp-filesystem)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

The LearnQwest agent system consists of four specialized AI agents built on Google's Agent Development Kit (ADK). These agents work together to provide intelligent automation for file management, documentation generation, and workflow orchestration.

**Key Features:**
- Intelligent file and directory management
- Automated documentation generation and maintenance
- Workflow automation and optimization
- Multi-agent orchestration for complex tasks
- Built-in planning and thinking capabilities
- Integration with MCP (Model Context Protocol) filesystem tools

**Technology Stack:**
- Google ADK (Agent Development Kit)
- Gemini 2.5 Flash (default model)
- Built-in planning with thinking capabilities
- MCP Filesystem Server integration

---

## Agent Architecture

```
┌─────────────────────────────────────────────────────────┐
│         LearnQwest Orchestrator Agent                    │
│         (Master Coordinator)                             │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Filesystem  │  │Documentation │  │  Workflow    │
│    Agent     │  │    Agent     │  │    Agent     │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┴─────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  MCP Filesystem │
              │     Server      │
              └─────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │   LearnQwest    │
              │  Directories    │
              └─────────────────┘
```

**Design Principles:**
- **Separation of Concerns**: Each agent has a specific, focused responsibility
- **Orchestration**: The orchestrator coordinates complex multi-agent tasks
- **Extensibility**: Easy to add new specialized agents
- **Safety**: Built-in safeguards for file operations
- **Observability**: Clear logging and status reporting

---

## Available Agents

### 1. LearnQwest Filesystem Agent

**Agent Name:** `learnqwest-filesystem-agent`

**Purpose:** Intelligent management of files and directories within the LearnQwest ecosystem.

**Capabilities:**
- ✅ List and search files in allowed directories
- ✅ Read and analyze file contents
- ✅ Create new files with appropriate content
- ✅ Modify existing files intelligently
- ✅ Organize files into logical structures
- ✅ Monitor directories for changes
- ✅ Generate file reports and summaries

**Safety Features:**
- Directory permission verification
- No destructive operations without confirmation
- Backup awareness for critical operations
- Respects file access restrictions
- Comprehensive operation logging

**LearnQwest Directory Structure:**
```
C:/LearnQwest/
├── ADA/
│   ├── core_assistant.py
│   └── [other AI-related files]
└── [other LearnQwest directories]

C:/Users/Link/Documents/
└── DROPZONE_INBOX/
    └── [incoming files and documents]
```

**Example Use Cases:**
- Organize incoming files from DROPZONE_INBOX
- Analyze and categorize documents
- Generate file inventory reports
- Automated file cleanup and maintenance
- Search for specific content across directories

**Response Format:**
```markdown
## Operation Summary
Brief description of requested operation

## Analysis
Current state and requirements analysis

## Actions Taken
- Action 1: Details
- Action 2: Details

## Results
Outcome with relevant details

## Recommendations
Follow-up suggestions
```

---

### 2. LearnQwest Documentation Agent

**Agent Name:** `learnqwest-documentation-agent`

**Purpose:** Create, maintain, and organize comprehensive documentation.

**Capabilities:**
- ✅ Generate README files and project overviews
- ✅ Create API documentation with examples
- ✅ Write step-by-step guides and tutorials
- ✅ Document system architecture and design
- ✅ Maintain technical reference documentation
- ✅ Create and update change logs
- ✅ Review and improve existing documentation

**Documentation Standards:**
- Clear, concise language
- Practical examples and use cases
- Consistent formatting and structure
- High-level overviews + detailed references
- Code samples with explanations
- Troubleshooting sections

**Document Types:**
- **README files**: Project overviews and getting started
- **API docs**: Endpoints, parameters, examples
- **Guides**: Step-by-step instructions
- **Architecture**: System design documentation
- **Reference**: Detailed technical references
- **Changelogs**: Version history and updates

**Standard Documentation Structure:**
```markdown
# Title
Brief 1-2 sentence description

## Overview
High-level introduction

## Prerequisites
Requirements before starting

## Quick Start
Fastest path to success

## Detailed Guide
Comprehensive sections

## Examples
Practical code samples

## Troubleshooting
Common issues and solutions

## Reference
Technical details

## Additional Resources
Related links and docs
```

**Example Use Cases:**
- Generate README for new projects
- Document Python code and APIs
- Create user guides for workflows
- Maintain architecture documentation
- Update technical references
- Generate migration guides

---

### 3. LearnQwest Workflow Agent

**Agent Name:** `learnqwest-workflow-agent`

**Purpose:** Design, automate, and optimize workflows for maximum productivity.

**Capabilities:**
- ✅ Create efficient workflow processes
- ✅ Automate repetitive tasks
- ✅ Integrate different tools and systems
- ✅ Optimize existing workflows
- ✅ Monitor workflow execution and performance
- ✅ Handle errors gracefully

**Workflow Components:**
- **Triggers**: Events that start workflows
- **Actions**: Steps to execute
- **Conditions**: Flow control logic
- **Notifications**: Alerts and updates
- **Error Handling**: Failure management

**Common Workflow Patterns:**

**1. File Processing Workflow:**
```
Monitor DROPZONE_INBOX
  ↓
Analyze file type/content
  ↓
Route to appropriate directory
  ↓
Trigger processing
  ↓
Archive/cleanup
```

**2. Documentation Workflow:**
```
Detect code changes
  ↓
Generate/update docs
  ↓
Create changelog
  ↓
Publish documentation
```

**3. Integration Workflow:**
```
Receive external data
  ↓
Transform/validate
  ↓
Store appropriately
  ↓
Trigger downstream processes
```

**Design Principles:**
- Keep workflows simple and focused
- Make workflows observable and debuggable
- Handle errors gracefully
- Provide clear status information
- Make workflows idempotent
- Comprehensive logging

**Example Use Cases:**
- Automated file routing and processing
- Continuous documentation updates
- Integration with external systems
- Scheduled maintenance tasks
- Event-driven automation

---

### 4. LearnQwest Orchestrator Agent

**Agent Name:** `learnqwest-orchestrator`

**Purpose:** Master coordinator that orchestrates complex multi-agent tasks.

**Capabilities:**
- ✅ Analyze complex user requests
- ✅ Determine which specialized agents to involve
- ✅ Coordinate multi-agent workflows
- ✅ Synthesize results from multiple agents
- ✅ Ensure task completion across all aspects

**Orchestration Process:**
```
1. UNDERSTAND
   Analyze complete user request
   ↓
2. DECOMPOSE
   Break into agent-specific tasks
   ↓
3. COORDINATE
   Engage specialized agents
   ↓
4. INTEGRATE
   Combine results
   ↓
5. VERIFY
   Ensure completion
```

**Example Orchestration:**

**User Request:** *"Set up a new Python project in LearnQwest with full documentation and automated workflows"*

**Orchestrator Plan:**
1. **Filesystem Agent**:
   - Create project directory structure
   - Set up Python package structure
   - Create __init__.py files

2. **Documentation Agent**:
   - Generate README.md
   - Create API documentation templates
   - Write setup guide

3. **Workflow Agent**:
   - Set up automated testing workflow
   - Create documentation update workflow
   - Configure file processing workflows

4. **Integration**:
   - Verify all components work together
   - Test workflows end-to-end

5. **Verification**:
   - Confirm project structure
   - Validate documentation
   - Test automated workflows

**Example Use Cases:**
- Complex project setup and initialization
- Multi-step migration tasks
- Comprehensive system updates
- End-to-end automation setup

---

## Setup & Configuration

### Prerequisites

1. **Python Environment**:
   ```bash
   Python 3.10-3.12
   uv (for dependency management)
   ```

2. **Google Cloud Setup**:
   ```bash
   # Install gcloud CLI
   # Authenticate
   gcloud auth application-default login

   # Set project
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Environment Variables**:
   Create `app/.env`:
   ```bash
   GOOGLE_CLOUD_PROJECT=your-gcp-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_CLOUD_STAGING_BUCKET=your-staging-bucket
   MODEL=gemini-2.5-flash
   AGENT_NAME=learnqwest-orchestrator
   ```

### Installation

1. **Clone and Install**:
   ```bash
   git clone <repository>
   cd adk-fullstack-deploy-tutorial
   make install
   ```

2. **Configure Environment**:
   ```bash
   cp app/.env.example app/.env
   # Edit app/.env with your values
   ```

3. **Install MCP Filesystem Server** (for Claude Desktop/Cursor):
   See [MCP Filesystem Configuration](#integration-with-mcp-filesystem) below

### Running the Agents

**Local Development**:
```bash
# Start the ADK backend with LearnQwest agents
make dev-backend

# The agents are available at:
# http://127.0.0.1:8000
```

**Deploy to Vertex AI Agent Engine**:
```bash
# Deploy all agents
make deploy-adk

# This deploys the agent system to Google Cloud
# and returns an endpoint URL
```

---

## Integration with MCP Filesystem

The LearnQwest agents integrate with the Model Context Protocol (MCP) Filesystem Server to provide secure, controlled access to your LearnQwest directories.

### MCP Configuration

**For Claude Desktop**, add to your config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/LearnQwest",
        "C:/Users/Link/Documents/DROPZONE_INBOX"
      ]
    }
  }
}
```

**For Cursor**, add to your MCP settings:

```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": [
          "-y",
          "@modelcontextprotocol/server-filesystem",
          "C:/LearnQwest",
          "C:/Users/Link/Documents/DROPZONE_INBOX"
        ]
      }
    }
  }
}
```

### Verify MCP Connection

**In Claude Desktop/Cursor**:

1. **List Allowed Directories**:
   ```
   List all allowed directories in the filesystem
   ```

   Expected response:
   ```
   - C:/LearnQwest
   - C:/Users/Link/Documents/DROPZONE_INBOX
   ```

2. **Test File Access**:
   ```
   Read the file C:/LearnQwest/ADA/core_assistant.py
   ```

3. **Test Directory Listing**:
   ```
   List all files in C:/LearnQwest/ADA
   ```

### MCP Filesystem Tools Available

When MCP is configured, the following tools become available:

- `read_file`: Read file contents
- `read_multiple_files`: Read multiple files at once
- `write_file`: Write content to a file
- `create_directory`: Create new directories
- `list_directory`: List directory contents
- `directory_tree`: Get directory tree structure
- `move_file`: Move/rename files
- `search_files`: Search for files by pattern
- `get_file_info`: Get file metadata

---

## Usage Examples

### Example 1: Organize Incoming Files

**Request:**
```
Use the LearnQwest Filesystem Agent to organize all files in my DROPZONE_INBOX
```

**Agent Response:**
```markdown
## Operation Summary
Organizing files from DROPZONE_INBOX into appropriate LearnQwest directories

## Analysis
Found 15 files in DROPZONE_INBOX:
- 5 Python files (.py)
- 3 Markdown documents (.md)
- 4 Data files (.json, .csv)
- 3 Images (.png, .jpg)

## Actions Taken
- Created directory: C:/LearnQwest/Python/imports_2024-01
- Moved 5 Python files to C:/LearnQwest/Python/imports_2024-01
- Moved 3 Markdown files to C:/LearnQwest/Documentation
- Moved 4 data files to C:/LearnQwest/Data
- Moved 3 images to C:/LearnQwest/Media

## Results
✓ All 15 files organized successfully
✓ DROPZONE_INBOX is now empty
✓ Created organizational summary log

## Recommendations
- Set up automated workflow for future file processing
- Consider adding file naming conventions
- Create index of organized files
```

### Example 2: Generate Project Documentation

**Request:**
```
Use the Documentation Agent to create comprehensive documentation for my
new Python project in C:/LearnQwest/Projects/MyProject
```

**Agent Response:**
```markdown
## Documentation Generated

Created the following documentation files:

1. ✓ README.md - Project overview and quick start
2. ✓ ARCHITECTURE.md - System design and structure
3. ✓ API_REFERENCE.md - API documentation
4. ✓ CONTRIBUTING.md - Contribution guidelines
5. ✓ CHANGELOG.md - Version history template

All documentation follows best practices with:
- Clear structure and formatting
- Practical examples
- Code samples
- Troubleshooting sections
```

### Example 3: Set Up Automated Workflow

**Request:**
```
Use the Workflow Agent to create an automated workflow that monitors
DROPZONE_INBOX and routes files based on type
```

**Agent Response:**
```markdown
## Workflow: Automated File Router

### Trigger
File added to C:/Users/Link/Documents/DROPZONE_INBOX

### Steps
1. Detect new file in DROPZONE_INBOX
2. Analyze file type and extension
3. Determine destination based on rules:
   - .py → C:/LearnQwest/Python/imports_[date]
   - .md → C:/LearnQwest/Documentation
   - .json, .csv → C:/LearnQwest/Data
   - .png, .jpg → C:/LearnQwest/Media
4. Move file to destination
5. Create log entry
6. Send notification (optional)

### Error Handling
- Invalid file types: Move to C:/LearnQwest/Unsorted
- Duplicate files: Append timestamp to filename
- Permission errors: Log and alert user

### Success Criteria
- File moved from DROPZONE_INBOX to appropriate location
- Log entry created
- DROPZONE_INBOX remains organized

### Monitoring & Logging
- All operations logged to C:/LearnQwest/Logs/file_router.log
- Weekly summary reports
- Error notifications for failed operations
```

### Example 4: Complex Orchestration

**Request:**
```
Use the Orchestrator to set up a complete new project called "AIAssistant"
with proper structure, documentation, and workflows
```

**Orchestrator Response:**
```markdown
## Request Analysis
Setting up a complete new project "AIAssistant" with:
- Proper directory structure
- Comprehensive documentation
- Automated workflows

## Orchestration Plan

### Phase 1: Filesystem Agent
- Create project directory: C:/LearnQwest/Projects/AIAssistant
- Set up Python package structure
- Create necessary subdirectories (src, tests, docs, etc.)

### Phase 2: Documentation Agent
- Generate README.md
- Create API documentation
- Write setup and usage guides
- Create CONTRIBUTING.md

### Phase 3: Workflow Agent
- Set up automated testing workflow
- Create documentation update workflow
- Configure code quality checks

### Integration
- Verify all components work together
- Test workflows end-to-end

## Execution

✓ Phase 1 Complete: Project structure created
✓ Phase 2 Complete: Documentation generated
✓ Phase 3 Complete: Workflows configured
✓ Integration testing passed

## Results Summary

Created complete project setup:
- Directory structure with src/, tests/, docs/, logs/
- 5 documentation files (README, ARCHITECTURE, API_REFERENCE, etc.)
- 3 automated workflows (testing, documentation, quality checks)
- All components integrated and tested

Project is ready for development!

## Verification
✓ Directory structure exists
✓ All documentation files present and properly formatted
✓ Workflows tested and operational
✓ Git repository initialized (optional)
```

---

## Best Practices

### 1. File Operations

**DO:**
- ✅ Always verify file paths before operations
- ✅ Use relative paths within LearnQwest directories
- ✅ Check file permissions before writing
- ✅ Create backups for critical operations
- ✅ Log all file operations

**DON'T:**
- ❌ Delete files without confirmation
- ❌ Modify files outside allowed directories
- ❌ Ignore file access errors
- ❌ Skip validation steps
- ❌ Perform operations without logging

### 2. Documentation

**DO:**
- ✅ Keep documentation up-to-date with code
- ✅ Include practical examples
- ✅ Use consistent formatting
- ✅ Add troubleshooting sections
- ✅ Link related documentation

**DON'T:**
- ❌ Write documentation without testing examples
- ❌ Use jargon without explanation
- ❌ Create documentation that's too brief
- ❌ Forget to update docs when code changes
- ❌ Skip code samples

### 3. Workflows

**DO:**
- ✅ Design simple, focused workflows
- ✅ Include comprehensive error handling
- ✅ Provide clear status information
- ✅ Log all workflow actions
- ✅ Make workflows idempotent

**DON'T:**
- ❌ Create overly complex workflows
- ❌ Ignore error conditions
- ❌ Skip logging
- ❌ Create workflows without testing
- ❌ Forget to document workflows

### 4. Agent Selection

**Use Filesystem Agent when:**
- Working directly with files and directories
- Organizing or searching files
- Reading/writing file contents

**Use Documentation Agent when:**
- Creating new documentation
- Updating existing docs
- Generating reference material

**Use Workflow Agent when:**
- Automating repetitive tasks
- Designing processes
- Integrating systems

**Use Orchestrator Agent when:**
- Task requires multiple agents
- Complex multi-step operations
- Coordinating different aspects

---

## Troubleshooting

### Common Issues

#### 1. Agent Not Responding

**Symptoms:**
- Agent doesn't respond to requests
- Timeout errors

**Solutions:**
```bash
# Check if backend is running
curl http://127.0.0.1:8000/health

# Restart backend
make dev-backend

# Check logs
tail -f logs/adk_server.log
```

#### 2. File Permission Errors

**Symptoms:**
- "Permission denied" errors
- Unable to read/write files

**Solutions:**
- Verify MCP filesystem configuration includes the directory
- Check Windows file permissions
- Ensure Claude/Cursor has necessary access
- Review MCP allowed directories list

#### 3. MCP Connection Issues

**Symptoms:**
- Filesystem tools not available
- "MCP server not connected" errors

**Solutions:**
```bash
# For Claude Desktop:
# 1. Quit Claude completely
# 2. Check config file:
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 3. Restart Claude

# For Cursor:
# 1. Check MCP settings in Cursor preferences
# 2. Restart Cursor
# 3. Verify MCP server is running
```

#### 4. Agent Configuration Errors

**Symptoms:**
- Vertex AI initialization errors
- Model not found errors

**Solutions:**
```bash
# Check environment variables
cat app/.env

# Verify required variables are set:
# - GOOGLE_CLOUD_PROJECT
# - GOOGLE_CLOUD_LOCATION
# - GOOGLE_CLOUD_STAGING_BUCKET

# Authenticate with Google Cloud
gcloud auth application-default login

# Set correct project
gcloud config set project YOUR_PROJECT_ID
```

#### 5. Deployment Issues

**Symptoms:**
- `make deploy-adk` fails
- Agent Engine deployment errors

**Solutions:**
```bash
# Verify GCS bucket exists
gsutil ls gs://your-staging-bucket

# Create bucket if needed
gsutil mb gs://your-staging-bucket

# Check gcloud authentication
gcloud auth list

# Verify project permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID
```

### Debug Mode

Enable detailed logging:

```bash
# In app/.env, add:
LOG_LEVEL=DEBUG

# Restart backend
make dev-backend

# View detailed logs
tail -f logs/adk_server.log
```

### Getting Help

If you encounter issues:

1. Check the logs in `logs/` directory
2. Verify environment configuration in `app/.env`
3. Test MCP connection with simple file operations
4. Review agent responses for error messages
5. Check Google Cloud quotas and permissions

---

## Additional Resources

- [Google ADK Documentation](https://cloud.google.com/vertex-ai/docs/agent-builder)
- [MCP Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agent-engine)

---

## Version History

- **v1.0.0** (2024-11-16): Initial release
  - LearnQwest Filesystem Agent
  - LearnQwest Documentation Agent
  - LearnQwest Workflow Agent
  - LearnQwest Orchestrator Agent
  - MCP Filesystem integration
  - Comprehensive documentation

---

## License

Apache-2.0 (unless noted otherwise in third-party files)

---

**Built with ❤️ using Google ADK**
