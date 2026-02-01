# cc-skills-config

中文友好的 Claude Code 配置集合，包含 MySQL 数据库工具、智能 Git 提交、Token 统计等实用工具。

## 快速开始

### 方式一：通过 Claude Code Marketplace 安装（推荐）

```bash
claude plugin marketplace add https://github.com/onlyliyj/cc-skills-config
```

### 方式二：使用安装脚本

```bash
# 克隆仓库
git clone https://github.com/onlyliyj/cc-skills-config.git
cd cc-skills-config

# 运行交互式安装程序
python3 installer.py
```

### 方式三：手动安装

复制配置文件到 Claude Code 配置目录：

- **macOS**: `~/.claude/`
- **Linux**: `~/.claude/`
- **Windows**: `%APPDATA%\claude\`

## 项目结构

```
cc-skills-config/
├── .claude-plugin/              # Claude Code Plugin 清单（Marketplace）
│   ├── plugin.json              # 核心插件清单
│   ├── marketplace.json         # Marketplace 清单
│   └── README.md                # 插件说明
├── skills/                      # Skill 配置
│   ├── config-installer/        # 配置安装助手
│   ├── java-e2e/                # Java E2E 测试生成
│   ├── mysql-mcp-setup/         # MySQL MCP 自动配置
│   └── contribute/              # 配置导出工具
├── commands/                    # 自定义命令
│   ├── commit/                  # 智能 Git 提交
│   └── ccusage/                 # Token 使用统计
├── mcp-configs/                 # MCP 服务器配置
│   └── mcp-servers.json         # 合并的 MCP 配置模板
├── hooks/                       # Hook 配置
│   └── hooks.json               # 语言检测钩子
├── alias/                       # DSP 别名配置
├── docs/                        # 文档
│   └── MCP_MIGRATION.md         # MCP 迁移指南
├── config.yml                   # 配置索引（向后兼容）
└── installer.py                 # 交互式安装脚本
```

## 功能特性

### Skills（技能）

| Skill | 描述 |
|-------|------|
| **mysql-mcp-setup** | 自动检测项目数据库配置并设置 MCP MySQL 连接，支持 Spring Boot、Node.js、Python、Go、PHP、Ruby 等项目 |
| **java-e2e** | 为 Java/Spring Boot 项目生成端到端测试，支持 SQLite、Thymeleaf、Spring Security |
| **config-installer** | 从仓库安装配置文件的助手 |
| **contribute** | 将本地配置导出为可分享的安装脚本 |

### Commands（命令）

| Command | 描述 |
|---------|------|
| **/commit** | 智能 Git 提交，自动生成符合规范的提交信息 |
| **/ccusage** | Token 使用统计和分析 |

### MCP 服务器配置

| Server | 描述 |
|--------|------|
| **MySQL** | MySQL 数据库连接和查询 |
| **Tavily** | AI 搜索引擎集成 |
| **CCUsage** | Token 使用统计 |

### Hooks（钩子）

| Hook | 描述 |
|------|------|
| **语言检测** | 自动检测用户提示语言（中文/英文）并更新设置 |

## MCP 服务器配置

本项目提供 MCP 服务器配置模板，位于 `mcp-configs/mcp-servers.json`。

### 配置方式

#### 方式一：使用 mysql-mcp-setup Skill 自动配置

```bash
# 在你的项目中调用 skill
/call mysql-mcp-setup
```

该 skill 会自动检测项目类型和数据库配置，生成正确的 MCP 配置。

#### 方式二：手动配置

1. 复制 `mcp-configs/mcp-servers.json` 中的所需配置
2. 粘贴到 `~/.claude.json` 的 `mcpServers` 部分
3. 设置环境变量（如 `MYSQL_HOST`、`TAVILY_API_KEY` 等）

详细迁移指南请参考 [docs/MCP_MIGRATION.md](docs/MCP_MIGRATION.md)。

## 安装脚本功能

`installer.py` 脚本提供：

- 交互式菜单，支持选择性安装
- 平台特定配置过滤
- 自动依赖检测
- 批量安装或单独安装
- 跨平台支持（macOS、Linux、Windows）

## 文档

- [快速开始](QUICKSTART.md)
- [MCP 迁移指南](docs/MCP_MIGRATION.md)
- [配置结构说明](CLAUDE.md)

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](docs/CONTRIBUTING.md) 了解指南。

### 添加新配置

1. 在相应目录创建配置文件
2. 添加条目到 `config.yml`
3. 使用 `installer.py` 测试
4. 提交 Pull Request

## 许可证

MIT License - 自由使用和修改。

## 链接

- [Claude Code 文档](https://docs.anthropic.com/claude/code)
- [MCP 服务器文档](https://modelcontextprotocol.io/)
