# 快速开始指南

## 5 分钟快速上手

### 方式一：Claude Code Marketplace 安装（推荐）

如果你已经在 `cc-skills-config` 目录中，可以直接安装当前目录：

```bash
claude plugin marketplace add .
```

或者从 GitHub 仓库安装：

```bash
claude plugin marketplace add https://github.com/onlyliyj/cc-skills-config
```

### 方式二：使用安装脚本

#### 步骤 1: 安装依赖

```bash
pip install -r requirements.txt
```

#### 步骤 2: 运行安装程序

```bash
python3 installer.py
```

#### 步骤 3: 选择要安装的配置

你会看到如下菜单：

```
==================================================
Claude Code 配置仓库安装程序
当前平台: DARWIN
配置目录: /Users/yourname/.claude
==================================================
1. Skills
2. MCP 服务器
3. 自定义命令
4. Hooks
5. 全部安装
6. 查看已安装配置
0. 退出

请选择 (0-6):
```

#### 步骤 4: 重启 Claude Code

安装完成后，重启 Claude Code 应用即可使用新配置。

## 常用配置

### mysql-mcp-setup（推荐）

自动检测项目数据库配置并设置 MySQL MCP 连接：

```
/call mysql-mcp-setup
```

支持的项目类型：
- Spring Boot
- Node.js
- Python (Django, Flask)
- Go
- PHP
- Ruby

### java-e2e

为 Java/Spring Boot 项目生成 E2E 测试：

```
/call java-e2e
```

### Smart Commit

智能 Git 提交：

```
/commit
```

### CCUsage

Token 使用统计：

```
/ccusage
```

### Contribute

导出本地配置为可分享的安装脚本：

```
/call contribute
```

## 目录结构

安装后，配置文件位于：

- **macOS**: `~/.claude/`
- **Linux**: `~/.claude/`
- **Windows**: `%APPDATA%\claude\`

## MCP 服务器配置

### MySQL MCP

使用 `mysql-mcp-setup` skill 自动配置：

```
/call mysql-mcp-setup
```

或手动配置 `~/.claude.json`：

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "root",
        "MYSQL_PASSWORD": "your-password",
        "MYSQL_DATABASE": "your-database"
      }
    }
  }
}
```

详细配置请参考 [docs/MCP_MIGRATION.md](docs/MCP_MIGRATION.md)。

## 需要帮助？

- 📖 查看 [README.md](README.md) 了解更多
- 📖 查看 [CLAUDE.md](CLAUDE.md) 了解配置格式
- 📖 查看 [docs/MCP_MIGRATION.md](docs/MCP_MIGRATION.md) 了解 MCP 配置
- 🐛 遇到问题？创建 GitHub Issue

## 卸载配置

### Marketplace 安装的配置

```bash
claude plugin remove cc-skills-config
```

### 手动安装的配置

```bash
# 删除已安装的配置
rm -rf ~/.claude/skills/skill-name
rm -rf ~/.claude/mcp_servers/server-name
rm -rf ~/.claude/commands/command-name
rm -rf ~/.claude/hooks/hook-name
```

## 更新配置

### Marketplace 安装

```bash
claude plugin update cc-skills-config
```

### 手动安装

```bash
cd cc-skills-config
git pull
python3 installer.py
```
