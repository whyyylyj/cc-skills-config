# 快速开始指南

## 5 分钟快速上手

### 步骤 1: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 2: 运行安装程序

```bash
python3 installer.py
```

### 步骤 3: 选择要安装的配置

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

### 步骤 4: 重启 Claude Code

安装完成后，重启 Claude Code 应用即可使用新配置。

## 常用配置

### mysql-mcp-setup（推荐）

自动检测项目数据库配置并设置 MySQL MCP 连接：

```
/mysql-mcp-setup
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
/java-e2e
```

### Smart Commit

智能 Git 提交：

```
/commit
```

## 目录结构

安装后，配置文件位于：

- **macOS**: `~/Library/Application Support/Claude/`
- **Linux**: `~/.config/Claude/`
- **Windows**: `%APPDATA%\Claude\`

## 需要帮助？

- 📖 查看 [README.md](README.md) 了解更多
- 📖 查看 [docs/CONFIG_STRUCTURE.md](docs/CONFIG_STRUCTURE.md) 了解配置格式
- 🐛 遇到问题？创建 GitHub Issue

## 卸载配置

```bash
# 删除已安装的配置
rm -rf ~/.claude/skills/skill-name
rm -rf ~/.claude/mcp_servers/server-name
rm -rf ~/.claude/commands/command-name
rm -rf ~/.claude/hooks/hook-name
```

## 更新配置

```bash
cd claude-configs
git pull
python3 installer.py
```
