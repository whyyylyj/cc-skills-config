# Claude Code Plugin - cc-skills-config

中文友好的 Claude Code 配置集合，包含多种实用工具和技能。

## 快速安装

### 通过 Claude Code Marketplace 安装（推荐）

```bash
claude plugin marketplace add https://github.com/onlyliyj/cc-skills-config
```

### 本地安装

```bash
# 克隆仓库
git clone https://github.com/onlyliyj/cc-skills-config.git
cd cc-skills-config

# 安装插件
claude plugin install ./
```

## 功能特性

### Skills（技能）
- **mysql-mcp-setup**: 自动检测项目数据库配置并设置 MCP MySQL 连接
- **java-e2e**: Java/Spring Boot 项目端到端测试生成工具
- **config-installer**: 配置文件安装助手
- **contribute**: 导出 Claude Code 配置为可分享的安装脚本

### Commands（命令）
- **/commit**: 智能 Git 提交命令，自动生成符合规范的提交信息
- **/ccusage**: Token 使用统计和分析

### MCP 服务器配置
- **MySQL**: MySQL 数据库连接和查询
- **Tavily**: AI 搜索引擎集成
- **CCUsage**: Token 使用统计

### Hooks（钩子）
- **语言自动检测**: 自动检测用户提示语言并更新设置

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

详细迁移指南请参考 [docs/MCP_MIGRATION.md](../docs/MCP_MIGRATION.md)。

## 文档

- [快速开始](../QUICKSTART.md)
- [完整文档](../README.md)
- [MCP 迁移指南](../docs/MCP_MIGRATION.md)

## 许可证

MIT License
