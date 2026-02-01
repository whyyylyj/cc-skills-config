# Contributing Guide

感谢你对 Claude Code Configs 项目的贡献！

## 如何贡献

### 报告问题

如果你发现了 bug 或有功能建议：

1. 检查 [Issues](../../issues) 是否已存在相同问题
2. 如果没有，创建新的 Issue，包含：
   - 清晰的标题
   - 详细的问题描述
   - 复现步骤（如果是 bug）
   - 预期行为
   - 环境信息（操作系统、Claude Code 版本等）

### 提交配置

你可以贡献以下类型的配置：

- **Skills**: 新的技能配置
- **MCP Servers**: MCP 服务器配置
- **Commands**: 自定义命令
- **Hooks**: Hook 脚本

#### 步骤

1. **Fork 仓库**
   ```bash
   # 在 GitHub 上 fork 项目
   git clone https://github.com/your-username/claude-configs.git
   cd claude-configs
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-config-name
   ```

3. **添加配置文件**

   根据配置类型创建相应的文件：

   **Skill:**
   ```
   skills/your-skill-name/skill.md
   ```

   **MCP Server:**
   ```
   mcp/your-mcp-name/
   ├── mcp-server.json
   └── install.sh (可选)
   ```

   **Command:**
   ```
   commands/your-command-name/command.md
   ```

   **Hook:**
   ```
   hooks/your-hook-name/hook.sh
   ```

4. **更新 config.yml**

   在相应类别下添加你的配置：

   ```yaml
   skills:
     - id: "your-skill-id"
       name: "Your Skill Name"
       description: "技能描述"
       path: "skills/your-skill-name/skill.md"
       platforms: ["all"]
       dependencies: []
   ```

5. **测试配置**

   ```bash
   # 使用安装程序测试
   python3 installer.py

   # 选择你的配置进行安装
   # 验证配置是否正常工作
   ```

6. **提交更改**

   ```bash
   git add .
   git commit -m "Add: Your new configuration"
   git push origin feature/your-config-name
   ```

7. **创建 Pull Request**

   - 在 GitHub 上创建 PR
   - 填写 PR 模板
   - 等待审查

## 配置指南

### Skills

**优秀的 Skill 应该：**
- ✅ 有明确、单一的用途
- ✅ 提供详细的使用说明
- ✅ 包含实际示例
- ✅ 说明依赖和前提条件
- ✅ 使用清晰简洁的语言

**Skill 模板：**

```markdown
---
name: your-skill-name
description: 简短描述（一句话）
---

# 技能标题

## 功能描述

详细说明这个技能做什么...

## 使用方法

调用方式和参数说明...

## 示例

```
用户: 示例输入
Claude: 示例输出
```

## 前提条件

- 依赖项 1
- 依赖项 2

## 注意事项

任何使用限制或注意事项...
```

### MCP Servers

**MCP 配置应该：**
- ✅ 使用环境变量存储敏感信息
- ✅ 提供默认值
- ✅ 包含安装脚本（如果需要）
- ✅ 说明配置要求

**MCP 配置模板：**

```json
{
  "name": "server-name",
  "command": "executable",
  "args": ["--arg", "value"],
  "env": {
    "REQUIRED_VAR": "${REQUIRED_VAR}",
    "OPTIONAL_VAR": "${OPTIONAL_VAR:-default}"
  }
}
```

**安装脚本模板：**

```bash
#!/bin/bash
set -e

echo "正在安装 MCP Server..."

# 检查依赖
if ! command -v executable &> /dev/null; then
    echo "错误: 需要安装 executable"
    exit 1
fi

# 配置检查
# ...

echo "✓ 安装完成"
```

### Commands

**Command 应该：**
- ✅ 名称简短易记
- ✅ 功能明确
- ✅ 提供参数说明
- ✅ 包含使用示例

**Command 模板：**

```markdown
---
name: your-command
description: 命令描述
---

# 命令标题

命令的详细说明...

## 使用方法

```
/your-command [参数]
```

## 参数

- `param1`: 参数说明
- `param2`: 参数说明

## 示例

```
/your-command value
```
```

### Hooks

**Hook 应该：**
- ✅ 快速执行
- ✅ 提供有用反馈
- ✅ 默认允许操作
- ✅ 有明确的失败条件

**Hook 模板：**

```bash
#!/bin/bash
# Hook 说明

# 获取参数
INPUT="$1"

# 验证逻辑
if [ condition ]; then
    echo "错误信息"
    exit 1  # 阻止操作
fi

# 成功
exit 0
```

## 代码审查标准

你的 PR 将根据以下标准审查：

1. **正确性**: 配置格式正确，可以正常工作
2. **文档**: 有清晰的说明和使用示例
3. **安全性**: 不包含恶意代码或安全风险
4. **兼容性**: 在目标平台上正常运行
5. **实用性**: 解决实际问题，有使用价值

## 测试要求

提交前请确保：

- ✅ 使用 `installer.py` 成功安装配置
- ✅ 配置在 Claude Code 中正常工作
- ✅ 文档完整且准确
- ✅ 没有拼写或语法错误

## 版本控制

### 分支命名

- `feature/xxx`: 新功能
- `fix/xxx`: Bug 修复
- `docs/xxx`: 文档更新
- `refactor/xxx`: 重构

### 提交信息

使用语义化提交信息：

```
type: subject

body

footer
```

类型：
- `Add`: 添加新配置
- `Update`: 更新现有配置
- `Fix`: 修复问题
- `Docs`: 文档更新
- `Refactor`: 重构

示例：

```
Add: MySQL MCP Server configuration

- Add mcp-server.json with environment variables
- Add installation script
- Update config.yml

Closes #123
```

## 风格指南

### YAML
- 使用 2 空格缩进
- 列表项使用 `-`
- 字符串优先使用双引号

### Markdown
- 标题层级清晰
- 代码块指定语言
- 使用列表组织信息
- 添加适当的空行

### Bash
- 使用 `set -e` 错误时退出
- 添加注释说明复杂逻辑
- 使用 `[[ ]]` 而非 `[ ]`
- 引用变量：`"$variable"`

## 获取帮助

如果你有任何问题：

1. 查看 [文档](docs/)
2. 搜索 [Issues](../../issues)
3. 创建新的 Issue 或 Discussion
4. 在 PR 中提问

## 行为准则

- 尊重所有贡献者
- 接受建设性反馈
- 关注问题而非个人
- 乐于助人，友善待人

## 许可证

通过贡献，你同意你的贡献将在与项目相同的 [MIT License](../../LICENSE) 下发布。

## 致谢

感谢所有贡献者！你的贡献让 Claude Code 变得更强大。

---

有问题？随时联系我们！
