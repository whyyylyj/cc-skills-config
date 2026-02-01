# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a configuration repository for Claude Code containing Skills, MCP servers, Commands, and Hooks that users can install via:
1. **Claude Code Marketplace** (recommended): `claude plugin marketplace add https://github.com/onlyliyj/cc-skills-config`
2. **Interactive installer**: `python3 installer.py`
3. **Manual installation**: Copy files to `~/.claude/` directory

The repository provides a centralized way to share and distribute Claude Code configurations.

## Installation and Usage

### Option 1: Claude Code Marketplace (Recommended)
```bash
claude plugin marketplace add https://github.com/onlyliyj/cc-skills-config
```

### Option 2: Interactive Installer
```bash
# Install dependencies
pip install -r requirements.txt

# Run the interactive installer
python3 installer.py
```

### Option 3: Manual Installation
Copy configuration files to:
- **macOS/Linux**: `~/.claude/`
- **Windows**: `%APPDATA%\claude\`

### Testing Configuration Changes
After modifying configurations, test them by:
1. Running `installer.py` and selecting the modified configuration
2. Verifying the installation in the Claude Code config directory
3. Restarting Claude Code to load the new configuration

## Architecture

### Marketplace Plugin Structure (`.claude-plugin/`)

**plugin.json**: Core plugin manifest that defines:
- Plugin metadata (name, version, description, author)
- Skills and commands directories
- Permissions required

**marketplace.json**: Marketplace listing that defines:
- Plugin owner information
- Plugin metadata for marketplace display
- Category and tags

### Core Components (Legacy)

**installer.py**: Interactive Python installer that:
- Detects the platform (macOS/Linux/Windows)
- Locates the Claude Code config directory (`~/.claude`)
- Reads `config.yml` for the configuration index
- Provides menu-driven installation of individual or all configurations
- Copies files to appropriate locations with correct permissions

**config.yml**: Central configuration index that defines:
- Project metadata (name, version, description)
- Categorized configurations (skills, mcp, commands, hooks)
- Platform compatibility for each configuration
- File paths and optional dependencies

### Configuration Types

**Skills** (`skills/<name>/skill.md`):
- Markdown files with YAML frontmatter
- Frontmatter fields: `name`, `description`, optional `tools`
- Contain documentation and usage instructions for the skill
- Example: `mysql-mcp-setup` skill auto-detects project database configs

**MCP Configs** (`mcp-configs/mcp-servers.json`):
- Combined MCP server configurations
- Contains MySQL, Tavily, and CCUsage server configs
- Can be used as templates for `~/.claude.json`
- Or use `mysql-mcp-setup` skill for automatic configuration

**Commands** (`commands/<name>/command.md`):
- Similar format to skills with frontmatter
- Define custom slash commands (e.g., `/commit`)
- Invoked via `/<command-name>`

**Hooks** (`hooks/hooks.json`):
- JSON format hook configurations
- Automatically detect language (Chinese/English) from user prompts
- Cross-platform compatible

### Configuration Installation Paths

The installer copies configurations to:
- Skills: `~/.claude/skills/<name>/skill.md`
- MCP Servers: `~/.claude/mcp_servers/<name>/` (legacy)
- Commands: `~/.claude/commands/<name>/command.md`
- Hooks: `~/.claude/hooks/<name>/hook.sh` (legacy)

On Windows, paths use `%APPDATA%\claude\` instead of `~/.claude`.

### MCP Configuration

**Option 1**: Use `mysql-mcp-setup` skill for automatic configuration
**Option 2**: Manually copy from `mcp-configs/mcp-servers.json` to `~/.claude.json`

See [docs/MCP_MIGRATION.md](docs/MCP_MIGRATION.md) for details.

### MySQL MCP Setup Skill Architecture

The `mysql-mcp-setup` skill demonstrates the complexity of configurations:

1. **Project Type Detection**: Searches for marker files (`pom.xml`, `package.json`, `requirements.txt`, etc.) to identify Spring Boot, Node.js, Python, Go, PHP, or Ruby projects

2. **Config File Discovery**: Uses glob patterns to find database configuration files (`.env`, `application.yml`, `settings.py`, etc.)

3. **Config Parsing**: Extracts database connection parameters using:
   - Regex for JDBC URLs: `jdbc:mysql://([^:]+):?(\d+)?/(.+)`
   - Grep for environment variables in `.env` files
   - YAML/JSON parsing for structured configs

4. **MCP Config Generation**: Creates `claude_desktop_config.json` with server name based on directory name

5. **Config Merge**: Intelligently merges with existing config, handling conflicts

## Key Implementation Details

### installer.py Methods

- `_get_claude_config_dir()`: Platform-specific config directory resolution
- `filter_by_platform()`: Filters configurations by current OS
- `install_skill()`, `install_mcp()`, `install_command()`, `install_hook()`: Copy files to target directories
- `_category_menu()`: Interactive menu for each category
- `_install_all()`: Batch installation
- `_list_installed()`: Show currently installed configurations

### Config File Format (config.yml)

```yaml
categories:
  skills:
    - id: "unique-id"
      name: "Display Name"
      description: "Description"
      path: "relative/path/to/skill.md"
      platforms: ["all"]  # or ["linux", "macos", "windows"]
      dependencies: []  # optional: list of other config IDs
```

### Skill Frontmatter Format

```markdown
---
name: skill-name
description: Skill description
tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
---

# Skill Documentation

Detailed usage instructions...
```

### MCP Server JSON Format

```json
{
  "name": "server-name",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-name"],
  "env": {
    "ENV_VAR": "value",
    "OPTIONAL_VAR": "${VAR:-default}"
  }
}
```

## Common Tasks

### Adding a New Configuration

1. Create the configuration file in the appropriate directory
2. Add an entry to `config.yml` with all required fields
3. Test with `python3 installer.py`
4. Verify the configuration loads correctly in Claude Code

### Modifying Existing Configurations

1. Edit the configuration file (skill.md, mcp-server.json, etc.)
2. Re-run `installer.py` to reinstall
3. Restart Claude Code to reload the configuration

### Platform-Specific Behavior

The installer automatically detects the platform via `platform.system()`:
- `"Darwin"` → macOS
- `"Linux"` → Linux
- `"Windows"` → Windows

Configurations are only shown if they support the current platform (via `platforms: ["all"]` or specific platform list).
