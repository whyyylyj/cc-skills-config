# MCP 服务器配置迁移指南

本文档说明如何配置和使用本项目中提供的 MCP（Model Context Protocol）服务器。

## 概述

本项目提供三个 MCP 服务器配置：

| 服务器 | 用途 | 依赖 |
|--------|------|------|
| **MySQL** | MySQL 数据库连接和查询 | npx @modelcontextprotocol/server-mysql |
| **Tavily** | AI 搜索引擎集成 | npx @tavily/mcp-server |
| **CCUsage** | Token 使用统计 | npx @ccusage/mcp@latest |

配置文件位于 `mcp-configs/mcp-servers.json`。

---

## 配置方式

### 方式一：使用 mysql-mcp-setup Skill（推荐）

**MySQL MCP** 配置可以通过 skill 自动完成：

```bash
/call mysql-mcp-setup
```

该 skill 会自动：
1. 检测项目类型（Spring Boot、Node.js、Python、Go、PHP、Ruby）
2. 查找数据库配置文件（`.env`、`application.yml`、`settings.py` 等）
3. 提取数据库连接参数
4. 生成或更新 `~/.claude.json` 中的 MCP 配置

### 方式二：手动配置

#### 步骤 1：打开 Claude Code 配置文件

配置文件位置：
- **macOS/Linux**: `~/.claude.json`
- **Windows**: `%APPDATA%\claude\claude.json`

如果文件不存在，创建一个新文件：

```json
{
  "mcpServers": {}
}
```

#### 步骤 2：复制所需的 MCP 服务器配置

从 `mcp-configs/mcp-servers.json` 复制需要的配置到 `mcpServers` 部分。

---

## 详细配置说明

### MySQL MCP 服务器

```json
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": {
        "MYSQL_HOST": "${MYSQL_HOST:-localhost}",
        "MYSQL_PORT": "${MYSQL_PORT:-3306}",
        "MYSQL_USER": "${MYSQL_USER:-root}",
        "MYSQL_PASSWORD": "${MYSQL_PASSWORD:-}",
        "MYSQL_DATABASE": "${MYSQL_DATABASE:-}"
      }
    }
  }
}
```

**环境变量设置方式：**

1. **方式 A：直接填写值**

```json
"env": {
  "MYSQL_HOST": "localhost",
  "MYSQL_PORT": "3306",
  "MYSQL_USER": "root",
  "MYSQL_PASSWORD": "your-password",
  "MYSQL_DATABASE": "mydb"
}
```

2. **方式 B：使用环境变量**（推荐）

在 `~/.zshrc` 或 `~/.bashrc` 中设置：

```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=your-password
export MYSQL_DATABASE=mydb
```

然后在 `claude.json` 中使用 `${VAR:-default}` 语法引用。

3. **方式 C：使用 .env 文件**

创建 `~/.claude.env`：

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=mydb
```

### Tavily MCP 服务器

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server"],
      "env": {
        "TAVILY_API_KEY": "${TAVILY_API_KEY:-}"
      }
    }
  }
}
```

**获取 API Key：**
1. 访问 [https://tavily.com](https://tavily.com)
2. 注册账号并获取 API Key
3. 设置环境变量 `TAVILY_API_KEY`

### CCUsage MCP 服务器

```json
{
  "mcpServers": {
    "ccusage": {
      "command": "npx",
      "args": ["-y", "@ccusage/mcp@latest"],
      "env": {
        "CCUSAGE_MODE": "${CCUSAGE_MODE:-auto}",
        "CCUSAGE_TRANSPORT": "${CCUSAGE_TRANSPORT:-stdio}",
        "CCUSAGE_PORT": "${CCUSAGE_PORT:-8080}"
      }
    }
  }
}
```

**配置说明：**
- `CCUSAGE_MODE`: 运行模式（默认：auto）
- `CCUSAGE_TRANSPORT`: 传输方式（默认：stdio）
- `CCUSAGE_PORT`: 端口（默认：8080，HTTP 模式使用）

---

## 完整配置示例

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
        "MYSQL_PASSWORD": "password",
        "MYSQL_DATABASE": "mydb"
      }
    },
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server"],
      "env": {
        "TAVILY_API_KEY": "tvly-your-api-key"
      }
    },
    "ccusage": {
      "command": "npx",
      "args": ["-y", "@ccusage/mcp@latest"],
      "env": {
        "CCUSAGE_MODE": "auto",
        "CCUSAGE_TRANSPORT": "stdio"
      }
    }
  }
}
```

---

## 验证配置

### 重启 Claude Code

配置完成后，重启 Claude Code 应用。

### 检查 MCP 连接

在 Claude Code 中，可以通过以下方式验证：

1. **查看可用工具**：在对话中询问 "有哪些 MCP 工具可用？"
2. **测试 MySQL 连接**：
   ```
   请使用 mysql-mcp 列出数据库中的所有表
   ```

3. **测试 Tavily 搜索**：
   ```
   请使用 tavily 搜索 "Claude Code 最新功能"
   ```

4. **查看 Token 使用**：
   ```
   /ccusage
   ```

---

## 故障排除

### 问题：MCP 服务器无法启动

**解决方案：**
1. 确认 Node.js 已安装：`node --version`
2. 手动测试 npx：`npx -y @modelcontextprotocol/server-mysql --version`
3. 检查 Claude Code 日志

### 问题：MySQL 连接失败

**解决方案：**
1. 确认数据库服务正在运行
2. 检查连接参数（主机、端口、用户名、密码、数据库名）
3. 确认数据库用户有足够权限
4. 测试连接：`mysql -h localhost -u root -p`

### 问题：Tavily API 调用失败

**解决方案：**
1. 确认 API Key 有效
2. 检查 API 配额是否用尽
3. 访问 [Tavily 控制台](https://tavily.com) 查看使用情况

---

## 更多资源

- [MCP 协议文档](https://modelcontextprotocol.io/)
- [Claude Code 文档](https://docs.anthropic.com/claude/code)
- [MySQL MCP 服务器](https://github.com/modelcontextprotocol/servers/tree/main/src/mysql)
- [Tavily MCP 服务器](https://github.com/tavily/mcp-server)
