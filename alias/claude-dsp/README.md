# Claude DSP Alias

`claude-dsp` 是 Claude Code 的便捷别名，用于快速启动带 `--dangerously-skip-permissions` 参数的 Claude Code。

## 功能说明

### 原始命令
```bash
claude --dangerously-skip-permissions
```

### 使用别名
```bash
claude-dsp
```

## 参数说明

`--dangerously-skip-permissions` 参数会：
- ✅ 跳过文件操作权限确认
- ✅ 允许直接读写文件而无需手动确认
- ✅ 允许执行命令而无需手动确认
- ⚠️  **降低安全性** - 仅在信任的环境中使用

## 适用场景

### ✅ 推荐使用场景

1. **本地开发环境**
   - 在自己的项目目录中使用
   - 需要频繁文件操作的开发任务
   - 自动化脚本和批处理

2. **信任的代码库**
   - 自己创建的项目
   - 团队内部项目
   - 开源项目贡献

3. **快速原型开发**
   - 快速迭代和测试
   - 实验性功能开发

### ❌ 不推荐使用场景

1. **不信任的代码库**
   - 下载的开源项目
   - 来源不明的代码

2. **生产环境**
   - 服务器环境
   - 包含敏感数据的环境

3. **关键系统操作**
   - 系统配置修改
   - 数据库操作

## 安装方法

### 方式 1: 使用项目安装器（推荐）

```bash
cd /Users/onlyliyj/Documents/cc-skills-config
python3 installer.py
```

选择 `claude-dsp` alias 进行安装。

### 方式 2: 手动安装

#### macOS / Linux (Zsh)
```bash
cd alias/claude-dsp
./install.sh
```

#### 手动添加到 Shell 配置

**Zsh** (`~/.zshrc`):
```bash
alias claude-dsp='claude --dangerously-skip-permissions'
```

**Bash** (`~/.bashrc`):
```bash
alias claude-dsp='claude --dangerously-skip-permissions'
```

**Fish** (`~/.config/fish/config.fish`):
```bash
alias claude-dsp='claude --dangerously-skip-permissions'
```

## 使用方法

### 基本用法

```bash
# 启动 Claude Code
claude-dsp

# 执行单条命令
claude-dsp "帮我创建一个新的 Python 文件"
```

### 常用命令示例

```bash
# 分析项目
claude-dsp "分析这个项目的结构"

# 代码重构
claude-dsp "重构这个函数，使其更高效"

# 批量操作
claude-dsp "将所有 .js 文件中的 var 替换为 const"

# 生成文档
claude-dsp "为这个模块生成 JSDoc 注释"
```

## 卸载方法

### 自动卸载
重新运行安装脚本，选择覆盖或手动删除配置。

### 手动卸载

编辑您的 Shell 配置文件，删除以下行：
```bash
alias claude-dsp='claude --dangerously-skip-permissions'
```

然后重新加载配置：
```bash
source ~/.zshrc  # Zsh
# 或
source ~/.bashrc # Bash
```

## 与普通 claude 命令的对比

| 特性 | `claude` | `claude-dsp` |
|------|----------|--------------|
| 文件读取权限 | 需要确认 | ❌ 跳过确认 |
| 文件写入权限 | 需要确认 | ❌ 跳过确认 |
| 命令执行权限 | 需要确认 | ❌ 跳过确认 |
| 安全性 | ✅ 高 | ⚠️  低 |
| 便捷性 | 一般 | ✅ 高 |
| 推荐场景 | 不熟悉代码/生产环境 | 本地开发/受信任环境 |

## 安全建议

1. **仅用于开发环境**
   - 不要在生产环境使用
   - 不要在包含敏感数据的目录使用

2. **代码审查**
   - 使用前检查 Claude 建议的操作
   - 了解将要执行的命令和修改

3. **版本控制**
   - 确保 Git 仓库可以回滚
   - 定期提交代码作为备份

4. **环境隔离**
   - 使用虚拟环境（Python、Node.js）
   - 使用 Docker 容器进行实验

## 常见问题

### Q: 为什么叫 "dsp"?
**A:** DSP = **D**angerously **S**kip **P**ermissions 的缩写。

### Q: 安装后命令不生效?
**A:** 需要重新加载 Shell 配置：
```bash
source ~/.zshrc  # 或对应的配置文件
```

### Q: 如何检查 alias 是否正确安装?
**A:** 运行以下命令：
```bash
alias claude-dsp
# 应该输出: alias claude-dsp='claude --dangerously-skip-permissions'
```

### Q: 我忘记了是否在使用 dsp 模式?
**A:** DSP 模式启动时会在终端提示信息中显示。

### Q: 可以同时使用普通模式和 DSP 模式吗?
**A:** 可以！
- 使用 `claude` 进入普通模式（有权限检查）
- 使用 `claude-dsp` 进入 DSP 模式（无权限检查）

## 进阶用法

### 组合使用其他工具

```bash
# 与 tmux 结合
claude-dsp -e tmux

# 与 git 结合
claude-dsp "帮我创建一个新分支并提交更改"

# 与 docker 结合
claude-dsp "帮我创建一个 Dockerfile"
```

### 在脚本中使用

```bash
#!/bin/bash
# 自动化脚本中使用 claude-dsp

claude-dsp "分析当前目录的所有日志文件并生成报告"
```

## 相关资源

- [Claude Code 官方文档](https://claude.ai/code)
- [命令行参数文档](https://docs.claude.com/cli)
- [安全最佳实践](https://docs.claude.com/security)

## License

MIT License
