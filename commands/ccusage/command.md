---
name: ccusage
description: 统计和分析 Claude Token 使用量，支持按日、月、周、会话等多种维度查看消耗情况
tools: Bash
---

# CCUsage Token 统计工具

## 功能说明

ccusage 是一个用于统计和分析 Anthropic Claude Token 使用量的命令行工具，支持以下功能：

- 📊 多维度统计：按日、月、周、会话、计费块等维度查看 Token 消耗
- 💰 成本计算：自动计算使用成本，支持不同模型的定价
- 📈 可视化展示：彩色输出，支持紧凑模式便于截图分享
- 🔍 高级过滤：支持按日期范围、项目名称过滤
- 📁 数据导出：支持 JSON 格式输出，可与 jq 等工具配合使用
- ⏱️ 实时状态：提供状态栏显示，可集成到 Claude Code hooks

## 使用示例

### 基础使用

```bash
# 查看每日 Token 使用统计
/ccusage daily

# 查看每月 Token 使用统计
/ccusage monthly

# 查看会话级 Token 使用统计
/ccusage session
```

### 高级选项

```bash
# 查看近7天的使用统计
/ccusage daily --since $(date -v-7d +%Y%m%d)

# 按 JSON 格式输出
/ccusage daily --json

# 显示模型成本细分
/ccusage daily --breakdown

# 按项目名称过滤
/ccusage daily --project "我的项目"
```

### 紧凑模式（适合截图）

```bash
/ccusage daily --compact
```

## 配置说明

ccusage 会自动从 Claude Code 的日志文件中读取使用数据，无需额外配置。首次运行时会自动初始化缓存。

### 环境变量

- `CCUSAGE_MODE`: 成本计算模式（auto/calculate/display）
- `CCUSAGE_TIMEZONE`: 时区设置（默认使用系统时区）
- `CCUSAGE_LOCALE`: 区域设置（默认 en-CA）
- `FORCE_COLOR`: 强制启用彩色输出
- `NO_COLOR`: 禁用彩色输出

## 更多帮助

```bash
# 查看命令帮助
/ccusage --help

# 查看特定子命令帮助
/ccusage daily --help
```
