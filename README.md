# Claude Code Configs

A shareable collection of Skills, MCP servers, Commands, and Hooks configurations for Claude Code.

## 🚀 Quick Start

### Option 1: Using the Installer (Recommended)

```bash
# Clone the repository
git clone <your-repo-url> claude-configs
cd claude-configs

# Run the interactive installer
python3 installer.py
```

### Option 2: Manual Installation

Copy individual configuration files to your Claude Code config directory:

- **macOS/Linux**: `~/.claude/`
- **Windows**: `%APPDATA%\claude\`

## 📁 Project Structure

```
claude-configs/
├── README.md                    # This file
├── installer.py                 # Interactive installation script
├── config.yml                   # Configuration index
├── skills/                      # Skill configurations
├── mcp/                         # MCP server configurations
├── commands/                    # Custom commands
├── hooks/                       # Hook scripts
└── docs/                        # Documentation
```

## 📦 Available Configurations

### Skills
- **config-installer**: Install configs from this repository
- **java-e2e**: Java/Spring Boot end-to-end testing tools
- **mysql-mcp-setup**: MySQL MCP server setup helper

### MCP Servers
- **mysql**: MySQL database connection and management

### Commands
- **commit**: Smart Git commit with AI-generated messages

### Hooks
- **user-prompt-submit**: Pre-submit prompt validation and enhancement

## 🛠️ Installation Script Features

The `installer.py` script provides:

- ✅ Interactive menu for selective installation
- ✅ Platform-specific configuration filtering
- ✅ Automatic dependency detection
- ✅ Install all or individual configurations
- ✅ Cross-platform support (macOS, Linux, Windows)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Adding New Configurations

1. Create the configuration file in the appropriate directory
2. Add an entry to `config.yml`
3. Test with `installer.py`
4. Submit a pull request

## 📖 Documentation

- [Configuration Structure](docs/CONFIG_STRUCTURE.md) - Understanding the configuration format
- [Contributing Guide](docs/CONTRIBUTING.md) - How to contribute

## 📄 License

MIT License - feel free to use and modify for your needs.

## 🔗 Links

- [Claude Code Documentation](https://docs.anthropic.com/claude/code)
- [MCP Server Documentation](https://modelcontextprotocol.io/)
