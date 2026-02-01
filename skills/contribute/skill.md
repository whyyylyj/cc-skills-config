---
name: contribute
description: 将本地 Claude Code 配置整理成可分享的安装脚本。支持导出 skills, MCP 服务器, commands, hooks，自动过滤敏感信息，检测重复配置。
tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
---

# Contribute Skill

将你的 Claude Code 配置分享给其他人！

## 功能

1. **配置扫描**: 自动扫描 ~/.claude 目录中的所有配置
2. **交互式选择**: 选择要导出的配置项
3. **敏感信息过滤**: 自动检测并替换 API keys, tokens, passwords
4. **重复检测**: 检查与现有配置的重复
5. **生成安装脚本**: 一键生成可分享的 Python 安装程序

## 使用方法

```
/contribute
```

## 导出流程

### Phase 1: 扫描配置
扫描已安装的 skills, MCP 服务器, commands, hooks

### Phase 2: 选择配置
交互式选择要导出的配置项

### Phase 3: 敏感信息处理
自动检测并替换敏感信息为环境变量占位符

### Phase 4: 重复检查
检测与现有配置的重复，提供覆盖/跳过/重命名选项

### Phase 5: 生成输出
生成 installer.py, config.yml, 和配置文件

### Phase 6: 打包分享
生成 README 和环境变量配置说明

## 输出结果

导出的配置将保存到:
```
claude-config-export/
├── installer.py
├── config.yml
├── README.md
├── .env.example          # 环境变量模板
├── skills/
├── mcp_servers/
├── commands/
└── hooks/
```

## 注意事项

- ⚠️ 敏感信息会被替换为环境变量占位符
- ⚠️ 导出前请确认没有包含机密信息
- ⚠️ 建议在分享前检查生成的配置文件
- ⚠️ 环境变量需要在运行前设置

## 示例

### 基本使用

**输入**:
```
/contribute
```

**执行流程**:
1. 扫描到 5 个配置
2. 选择导出 mysql, tavily, commit
3. 检测到敏感信息: TAVILY_API_KEY, MYSQL_PASSWORD
4. 替换为环境变量占位符
5. 生成安装脚本

**输出**:
```
✓ 配置已导出到 claude-config-export/
✓ 生成 installer.py
✓ 生成 config.yml
✓ 生成 README.md
✓ 生成 .env.example

下一步:
1. cd claude-config-export
2. 检查配置文件
3. 分享给其他人或提交到 Git
```
