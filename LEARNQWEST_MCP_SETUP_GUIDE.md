# LearnQwest MCP Filesystem Setup Guide

**Complete guide to setting up the MCP Filesystem Server for LearnQwest integration**

This guide walks you through setting up the Model Context Protocol (MCP) Filesystem Server to enable Claude Desktop and Cursor to access your LearnQwest directories securely.

---

## Table of Contents

- [What is MCP?](#what-is-mcp)
- [Prerequisites](#prerequisites)
- [Quick Setup](#quick-setup)
- [Detailed Configuration](#detailed-configuration)
  - [Claude Desktop Setup](#claude-desktop-setup)
  - [Cursor Setup](#cursor-setup)
- [Verify Your Setup](#verify-your-setup)
- [LearnQwest Directory Structure](#learnqwest-directory-structure)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)

---

## What is MCP?

**Model Context Protocol (MCP)** is a standardized protocol that allows AI assistants like Claude to securely interact with external tools and data sources. The MCP Filesystem Server specifically provides:

- ✅ Controlled access to specified directories
- ✅ File reading and writing capabilities
- ✅ Directory listing and navigation
- ✅ File search and manipulation
- ✅ Security through explicit allow-listing

**Why use MCP for LearnQwest?**
- Secure, controlled access to your LearnQwest directories
- Enables AI agents to directly manage your files
- Provides filesystem tools to Claude/Cursor
- Maintains security through directory whitelisting

---

## Prerequisites

Before you begin, ensure you have:

- [ ] Node.js 18+ installed (for npx command)
- [ ] Claude Desktop or Cursor IDE installed
- [ ] LearnQwest directories created on your system
- [ ] Basic understanding of JSON configuration files
- [ ] Administrator/write access to your LearnQwest folders

**Check Node.js Installation:**
```bash
node --version
# Should output v18.x.x or higher
```

**If Node.js is not installed:**
- Windows: Download from https://nodejs.org
- macOS: `brew install node`
- Linux: `sudo apt install nodejs npm` or `sudo yum install nodejs npm`

---

## Quick Setup

### Step 1: Verify LearnQwest Directories Exist

**Windows:**
```powershell
# Check if directories exist
dir C:\LearnQwest
dir C:\Users\Link\Documents\DROPZONE_INBOX
```

**macOS/Linux (for testing):**
```bash
# Create mock directories for testing
mkdir -p ~/LearnQwest/ADA
mkdir -p ~/Documents/DROPZONE_INBOX
```

### Step 2: Configure MCP for Your Platform

Choose your platform below and follow the configuration steps.

---

## Detailed Configuration

### Claude Desktop Setup

#### For Windows

1. **Locate Claude Desktop Config File:**
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

   Full path typically:
   ```
   C:\Users\[YourUsername]\AppData\Roaming\Claude\claude_desktop_config.json
   ```

2. **Edit the Config File:**

   Open the file in a text editor (Notepad, VS Code, etc.) and add:

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

   **Important Notes:**
   - Replace `Link` with your actual Windows username
   - Use forward slashes (/) even on Windows
   - Keep the `-y` flag to auto-confirm npx prompts

3. **Save the File**

4. **Restart Claude Desktop Completely:**
   - Quit Claude (File → Quit, or right-click system tray icon)
   - Wait 5 seconds
   - Relaunch Claude Desktop

#### For macOS

1. **Locate Claude Desktop Config File:**
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. **Edit the Config File:**

   ```bash
   # Open in default editor
   open ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Or use nano
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

   Add this configuration:

   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "/Users/Link/LearnQwest",
           "/Users/Link/Documents/DROPZONE_INBOX"
         ]
       }
     }
   }
   ```

   **Important Notes:**
   - Replace `/Users/Link` with your actual home directory path
   - Use absolute paths, not `~`
   - Keep the `-y` flag

3. **Save the File** (Ctrl+O in nano, then Ctrl+X to exit)

4. **Restart Claude Desktop:**
   ```bash
   # Quit Claude
   osascript -e 'quit app "Claude"'

   # Wait a moment, then reopen
   open -a Claude
   ```

#### For Linux

1. **Locate Claude Desktop Config File:**
   ```
   ~/.config/Claude/claude_desktop_config.json
   ```

2. **Edit the Config File:**

   ```bash
   nano ~/.config/Claude/claude_desktop_config.json
   ```

   Add this configuration:

   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "/home/link/LearnQwest",
           "/home/link/Documents/DROPZONE_INBOX"
         ]
       }
     }
   }
   ```

3. **Save and Restart Claude Desktop**

---

### Cursor Setup

#### For Windows

1. **Open Cursor Settings:**
   - Press `Ctrl+,` or go to File → Preferences → Settings
   - Search for "MCP" in the settings search bar

2. **Locate MCP Configuration Section:**
   - Or directly edit: `%APPDATA%\Cursor\User\settings.json`

3. **Add MCP Configuration:**

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

4. **Restart Cursor:**
   - Close all Cursor windows
   - Reopen Cursor

#### For macOS/Linux

1. **Open Cursor Settings:**
   - Press `Cmd+,` (macOS) or `Ctrl+,` (Linux)
   - Search for "MCP"

2. **Add MCP Configuration:**

   macOS:
   ```json
   {
     "mcp": {
       "servers": {
         "filesystem": {
           "command": "npx",
           "args": [
             "-y",
             "@modelcontextprotocol/server-filesystem",
             "/Users/Link/LearnQwest",
             "/Users/Link/Documents/DROPZONE_INBOX"
           ]
         }
       }
     }
   }
   ```

   Linux:
   ```json
   {
     "mcp": {
       "servers": {
         "filesystem": {
           "command": "npx",
           "args": [
             "-y",
             "@modelcontextprotocol/server-filesystem",
             "/home/link/LearnQwest",
             "/home/link/Documents/DROPZONE_INBOX"
           ]
         }
       }
     }
   }
   ```

3. **Restart Cursor**

---

## Verify Your Setup

### In Claude Desktop

Once you've configured and restarted Claude Desktop, test the connection:

**Test 1: List Allowed Directories**
```
List all allowed directories in the filesystem
```

**Expected Response:**
```
The following directories are allowed:
- C:/LearnQwest (or /Users/Link/LearnQwest)
- C:/Users/Link/Documents/DROPZONE_INBOX
```

**Test 2: Read a File**
```
Read the file C:/LearnQwest/ADA/core_assistant.py
```

**Expected Response:**
- File contents displayed, or
- File not found error (which confirms access is working, file just doesn't exist yet)

**Test 3: List Directory Contents**
```
List all files in C:/LearnQwest
```

**Expected Response:**
- Directory listing showing files and subdirectories

### In Cursor

**Test 1: Check MCP Status**
- Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
- Type "MCP Status"
- Should show "Filesystem: Connected"

**Test 2: Use Filesystem Tools**
In Cursor's AI chat:
```
Show me the directory structure of C:/LearnQwest
```

### Troubleshooting Verification

If tests fail, see [Troubleshooting](#troubleshooting) section below.

---

## LearnQwest Directory Structure

### Recommended Structure

```
C:/LearnQwest/
├── ADA/
│   ├── core_assistant.py
│   ├── config.json
│   └── modules/
│       ├── nlp/
│       ├── reasoning/
│       └── memory/
├── Projects/
│   ├── Project1/
│   └── Project2/
├── Documentation/
│   ├── guides/
│   ├── api/
│   └── architecture/
├── Data/
│   ├── datasets/
│   └── exports/
├── Logs/
│   └── [date-stamped logs]
└── Scripts/
    ├── automation/
    └── utilities/

C:/Users/Link/Documents/DROPZONE_INBOX/
├── [incoming files - processed automatically]
└── [files get routed to appropriate LearnQwest directories]
```

### Creating the Structure

**Windows (PowerShell):**
```powershell
# Create main LearnQwest structure
New-Item -ItemType Directory -Path "C:\LearnQwest\ADA\modules\nlp"
New-Item -ItemType Directory -Path "C:\LearnQwest\ADA\modules\reasoning"
New-Item -ItemType Directory -Path "C:\LearnQwest\ADA\modules\memory"
New-Item -ItemType Directory -Path "C:\LearnQwest\Projects"
New-Item -ItemType Directory -Path "C:\LearnQwest\Documentation\guides"
New-Item -ItemType Directory -Path "C:\LearnQwest\Documentation\api"
New-Item -ItemType Directory -Path "C:\LearnQwest\Documentation\architecture"
New-Item -ItemType Directory -Path "C:\LearnQwest\Data\datasets"
New-Item -ItemType Directory -Path "C:\LearnQwest\Data\exports"
New-Item -ItemType Directory -Path "C:\LearnQwest\Logs"
New-Item -ItemType Directory -Path "C:\LearnQwest\Scripts\automation"
New-Item -ItemType Directory -Path "C:\LearnQwest\Scripts\utilities"

# Create DROPZONE_INBOX
New-Item -ItemType Directory -Path "C:\Users\Link\Documents\DROPZONE_INBOX"
```

**macOS/Linux (Bash):**
```bash
# Create main LearnQwest structure
mkdir -p ~/LearnQwest/ADA/modules/{nlp,reasoning,memory}
mkdir -p ~/LearnQwest/{Projects,Data/{datasets,exports},Logs}
mkdir -p ~/LearnQwest/Documentation/{guides,api,architecture}
mkdir -p ~/LearnQwest/Scripts/{automation,utilities}

# Create DROPZONE_INBOX
mkdir -p ~/Documents/DROPZONE_INBOX
```

---

## Security Considerations

### Directory Whitelisting

**Important:** The MCP Filesystem Server ONLY allows access to explicitly listed directories.

- ✅ **Safe:** Only `C:/LearnQwest` and `C:/Users/Link/Documents/DROPZONE_INBOX` are accessible
- ❌ **Blocked:** All other directories are completely inaccessible
- ✅ **Sandboxed:** AI cannot access system files, other user directories, etc.

### Adding More Directories

To allow access to additional directories, add them to the `args` array:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/LearnQwest",
        "C:/Users/Link/Documents/DROPZONE_INBOX",
        "C:/Users/Link/Documents/Projects",
        "C:/Data/Exports"
      ]
    }
  }
}
```

### Best Practices

1. **Principle of Least Privilege:**
   - Only allow access to directories the AI actually needs
   - Don't grant access to your entire home directory or system drive

2. **Sensitive Data:**
   - Don't allow access to directories containing:
     - Passwords or credentials
     - Personal financial information
     - Sensitive work documents
     - System configuration files

3. **Regular Audits:**
   - Periodically review your MCP configuration
   - Remove access to directories no longer needed
   - Check logs for unexpected file operations

4. **Backups:**
   - Maintain backups of important LearnQwest data
   - AI agents can modify/delete files (with confirmation)
   - Have a recovery strategy

---

## Troubleshooting

### Issue 1: MCP Server Not Connecting

**Symptoms:**
- Filesystem tools not available in Claude/Cursor
- "MCP server not connected" errors

**Solutions:**

1. **Verify Node.js Installation:**
   ```bash
   node --version
   npm --version
   ```
   Both should return version numbers.

2. **Check Configuration Syntax:**
   - Ensure JSON is valid (no trailing commas, proper quotes)
   - Use a JSON validator: https://jsonlint.com

3. **Verify File Paths:**
   - Ensure directories actually exist
   - Check for typos in paths
   - Use forward slashes (/) even on Windows

4. **Restart Completely:**
   - Close Claude/Cursor completely
   - Wait 10 seconds
   - Reopen

5. **Check Logs:**

   Claude Desktop logs location:
   - Windows: `%APPDATA%\Claude\logs`
   - macOS: `~/Library/Logs/Claude`
   - Linux: `~/.config/Claude/logs`

### Issue 2: Permission Denied Errors

**Symptoms:**
- "Permission denied" when trying to read/write files

**Solutions:**

1. **Check Directory Permissions:**
   ```bash
   # Windows (PowerShell)
   Get-Acl C:\LearnQwest | Format-List

   # macOS/Linux
   ls -la ~/LearnQwest
   ```

2. **Grant Write Permissions:**
   ```bash
   # Windows (PowerShell - Run as Administrator)
   icacls "C:\LearnQwest" /grant Users:F /T

   # macOS/Linux
   chmod -R u+rwX ~/LearnQwest
   ```

3. **Check User Ownership:**
   Ensure the directories are owned by your user account

### Issue 3: Files Not Found

**Symptoms:**
- AI reports files don't exist when they do

**Solutions:**

1. **Check Path Format:**
   - Windows: `C:/LearnQwest/file.txt` (forward slashes!)
   - macOS/Linux: `/Users/Link/LearnQwest/file.txt`

2. **Verify Directory is Allowed:**
   - The directory must be in the MCP `args` list
   - Check spelling and case sensitivity

3. **Test with Absolute Paths:**
   - Always use full, absolute paths
   - Don't use `~` or relative paths

### Issue 4: npx Command Fails

**Symptoms:**
- MCP server fails to start
- Error about `npx` not found

**Solutions:**

1. **Install Node.js:**
   - Download from https://nodejs.org
   - Restart terminal/computer after installation

2. **Update npm:**
   ```bash
   npm install -g npm@latest
   ```

3. **Clear npm Cache:**
   ```bash
   npm cache clean --force
   ```

4. **Manually Install MCP Server:**
   ```bash
   npm install -g @modelcontextprotocol/server-filesystem
   ```

### Issue 5: Configuration Not Loading

**Symptoms:**
- Changes to config file not taking effect

**Solutions:**

1. **Verify Config File Location:**
   - Make sure you're editing the correct file
   - Search for `claude_desktop_config.json` on your system

2. **Check JSON Syntax:**
   - Use a JSON validator
   - Look for missing commas, quotes, brackets

3. **Complete Restart:**
   - Quit application completely
   - Kill any background processes
   - Clear cache if available
   - Restart application

4. **Check for Multiple Config Files:**
   - Ensure you don't have conflicting configs
   - Only one config file should exist per application

---

## Advanced Configuration

### Multiple Filesystem Servers

You can configure multiple filesystem servers with different access:

```json
{
  "mcpServers": {
    "learnqwest": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/LearnQwest"
      ]
    },
    "dropzone": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/Users/Link/Documents/DROPZONE_INBOX"
      ]
    },
    "projects": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/Users/Link/Projects"
      ]
    }
  }
}
```

### Environment Variables

Use environment variables for dynamic paths:

**Windows (PowerShell):**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${env:USERPROFILE}/LearnQwest",
        "${env:USERPROFILE}/Documents/DROPZONE_INBOX"
      ]
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${HOME}/LearnQwest",
        "${HOME}/Documents/DROPZONE_INBOX"
      ]
    }
  }
}
```

### Logging and Debugging

Enable verbose logging for troubleshooting:

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
      ],
      "env": {
        "DEBUG": "*"
      }
    }
  }
}
```

Check logs:
- Claude Desktop: `%APPDATA%\Claude\logs` or `~/Library/Logs/Claude`
- Cursor: View in Developer Tools Console

---

## Next Steps

Once you have MCP configured and verified:

1. **Read the Agent Documentation:**
   - See `LEARNQWEST_AGENTS_DOCUMENTATION.md`
   - Learn about the available LearnQwest agents

2. **Test the Agents:**
   - Try organizing files with the Filesystem Agent
   - Generate documentation with the Documentation Agent
   - Create workflows with the Workflow Agent

3. **Deploy to Production:**
   - Deploy agents to Vertex AI Agent Engine
   - Set up automated workflows
   - Integrate with your existing systems

4. **Customize:**
   - Modify agent instructions for your needs
   - Add custom tools and capabilities
   - Create new specialized agents

---

## Resources

- **MCP Documentation:** https://github.com/modelcontextprotocol
- **MCP Filesystem Server:** https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- **Claude Desktop:** https://claude.ai/download
- **Cursor IDE:** https://cursor.sh
- **Node.js:** https://nodejs.org

---

## Support

If you need help:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review MCP server logs
3. Verify your configuration with JSON validator
4. Test with simple operations first
5. Consult the LearnQwest Agents Documentation

---

**Last Updated:** 2024-11-16
**Version:** 1.0.0

