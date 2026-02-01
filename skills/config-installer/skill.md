---
name: config-installer
description: 从 Git 仓库安装 Claude Code 配置（Skills、MCP、Commands、Hooks）
---

# Config Installer Skill

使用 config-installer skill 从共享 Git 仓库安装 Claude Code 配置。

## 使用方法

当用户请求安装配置仓库时，请按以下步骤操作：

1. **确认仓库地址**
   - 默认仓库: `https://github.com/your-username/claude-configs.git`
   - 或使用用户指定的仓库地址

2. **克隆仓库**
   ```bash
   git clone <repo_url> claude-configs
   cd claude-configs
   ```

3. **运行安装程序**
   ```bash
   python3 installer.py
   ```

4. **根据用户选择安装配置**
   - 交互式菜单会显示所有可用配置
   - 用户可以选择安装单个配置或全部安装
   - 安装程序会自动处理平台兼容性

## 参数说明

- `repo_url` (可选): Git 仓库地址，默认为官方仓库

## 示例

```
用户: 安装 Claude Code 配置仓库

Claude:
1. 克隆配置仓库...
2. 运行安装程序...
3. 显示安装选项菜单
4. 根据用户选择安装配置
```

## 注意事项

- 安装程序会自动检测当前平台并过滤不兼容的配置
- 配置会安装到 `~/.claude/` (macOS/Linux) 或 `%APPDATA%\claude\` (Windows)
- 某些 MCP 服务器可能需要额外的依赖或环境变量
