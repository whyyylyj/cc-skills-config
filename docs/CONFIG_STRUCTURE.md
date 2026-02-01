# Configuration Structure Guide

本文档说明 Claude Code 配置文件的结构和格式。

## 目录结构

```
~/.claude/                          # Claude Code 配置根目录
├── skills/                         # Skills 配置
│   └── <skill-name>/
│       └── skill.md                # Skill 定义文件
├── mcp_servers/                    # MCP 服务器配置
│   └── <server-name>/
│       └── mcp-server.json         # 服务器配置 JSON
├── commands/                       # 自定义命令
│   └── <command-name>/
│       └── command.md              # 命令定义文件
└── hooks/                          # Hooks 配置
    └── <hook-name>/
        └── hook.sh                 # Hook 脚本
```

## Skill 配置格式

### 文件位置
`skills/<skill-name>/skill.md`

### 格式

```markdown
---
name: skill-name
description: 技能描述
---

# 技能标题

技能的详细说明文档...

## 使用方法
...

## 示例
...
```

### 必需字段

- **name**: 技能名称（唯一标识符）
- **description**: 技能描述（显示在菜单中）

### 可选字段

- 文档内容（Markdown 格式）
- 使用说明
- 示例

## MCP 服务器配置格式

### 文件位置
`mcp_servers/<server-name>/mcp-server.json`

### 格式

```json
{
  "name": "server-name",
  "command": "executable",
  "args": ["arg1", "arg2"],
  "env": {
    "ENV_VAR": "value"
  }
}
```

### 字段说明

- **name** (必需): 服务器名称
- **command** (必需): 启动命令（如 `npx`, `python`, `node`）
- **args** (可选): 命令参数数组
- **env** (可选): 环境变量对象

### 示例

```json
{
  "name": "mysql",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-mysql"],
  "env": {
    "MYSQL_HOST": "localhost",
    "MYSQL_PORT": "3306",
    "MYSQL_USER": "root",
    "MYSQL_PASSWORD": "password",
    "MYSQL_DATABASE": "mydb"
  }
}
```

## Command 配置格式

### 文件位置
`commands/<command-name>/command.md`

### 格式

与 Skill 配置类似，使用 Markdown + Frontmatter：

```markdown
---
name: command-name
description: 命令描述
---

# 命令标题

命令的详细说明...

## 使用方法
...
```

### 调用方式

```
/<command-name> [arguments]
```

### 示例

```
/commit
/commit Fix authentication bug
```

## Hook 配置格式

### 文件位置
`hooks/<hook-name>/hook.sh`

### 格式

Bash 脚本，接收特定参数并返回状态码。

```bash
#!/bin/bash

# 获取参数
PARAM1="$1"
PARAM2="$2"

# 处理逻辑
...

# 返回状态码
# 0 = 成功，继续执行
# 1 = 失败，阻止操作
exit 0
```

### Hook 类型

#### user-prompt-submit
在用户提交提示前触发。

**参数:**
- `$1`: 用户输入的提示文本

**返回:**
- `0`: 允许提交
- `1`: 阻止提交

### 示例

```bash
#!/bin/bash
USER_PROMPT="$1"

# 验证提示长度
if [ ${#USER_PROMPT} -lt 10 ]; then
    echo "提示过短"
    exit 1
fi

exit 0
```

## config.yml 索引格式

配置仓库的 `config.yml` 文件索引所有可用的配置。

### 结构

```yaml
project:
  name: "项目名称"
  version: "1.0.0"
  description: "项目描述"
  repository: "Git 仓库地址"

categories:
  skills:
    - id: "skill-id"
      name: "显示名称"
      description: "技能描述"
      path: "skills/skill-name/skill.md"
      platforms: ["all", "linux", "macos", "windows"]
      dependencies: []

  mcp:
    - id: "mcp-id"
      name: "显示名称"
      description: "MCP 服务器描述"
      path: "mcp/server-name/"
      platforms: ["all"]
      install_script: "mcp/server-name/install.sh"

  commands:
    - id: "command-id"
      name: "显示名称"
      description: "命令描述"
      path: "commands/command-name/command.md"
      platforms: ["all"]

  hooks:
    - id: "hook-id"
      name: "显示名称"
      description: "Hook 描述"
      path: "hooks/hook-name/hook.sh"
      platforms: ["all"]
```

### 字段说明

- **id**: 唯一标识符（小写，连字符分隔）
- **name**: 显示名称
- **description**: 详细描述
- **path**: 相对于仓库根目录的文件路径
- **platforms**: 支持的平台（"all" 或具体平台列表）
- **dependencies**: 依赖的其他配置 ID（可选）
- **install_script**: 安装脚本路径（MCP 专用，可选）

## 平台标识符

- `all`: 所有平台
- `linux`: Linux 系统
- `macos` / `darwin`: macOS 系统
- `windows`: Windows 系统

## 环境变量

在 MCP 配置中，可以使用环境变量引用：

```json
{
  "env": {
    "MYSQL_HOST": "${MYSQL_HOST:-localhost}",
    "MYSQL_PORT": "${MYSQL_PORT:-3306}"
  }
}
```

语法：`${VARIABLE_NAME:-default_value}`

## 最佳实践

### Skills
1. 提供清晰的使用说明
2. 包含实际示例
3. 说明技能的限制和前提条件

### MCP Servers
1. 使用环境变量存储敏感信息
2. 提供安装脚本
3. 验证连接配置

### Commands
1. 名称简短且易于记忆
2. 提供参数说明
3. 包含使用示例

### Hooks
1. 快速执行，避免长时间阻塞
2. 提供有用的反馈信息
3. 默认允许操作（保守策略）

## 验证配置

在安装配置后，验证其是否正确配置：

1. **Skills**: 在 Claude Code 中使用 `/<skill-name>` 调用
2. **MCP**: 检查 MCP 服务器是否启动并可用
3. **Commands**: 测试命令调用
4. **Hooks**: 触发相关操作观察 hook 执行

## 故障排除

### MCP 服务器无法启动
1. 检查命令和参数是否正确
2. 验证环境变量是否设置
3. 查看服务器日志

### Skill 未显示
1. 确认 `skill.md` 文件存在
2. 检查 Frontmatter 格式是否正确
3. 重启 Claude Code

### Hook 不执行
1. 确认文件有执行权限 (`chmod +x`)
2. 检查脚本语法 (`bash -n hook.sh`)
3. 验证 hook 名称是否正确
