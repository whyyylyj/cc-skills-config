# Tavily MCP Server

Tavily 是一个专为 AI 代理设计的搜索 API，提供实时、准确的网络搜索能力。

## 功能特点

- 🌐 **实时网络搜索**：获取最新信息和新闻
- 🔍 **智能问答**：基于搜索结果的智能答案生成
- 📊 **深度研究**：支持复杂查询和多源信息聚合
- 🚀 **高性能**：专为 AI 应用优化的响应速度
- 🆓 **免费层**：每月 1000 次免费调用
- 🔧 **跨平台**：支持 macOS、Linux 和 Windows

## 获取 API Key

1. 访问 [https://www.tavily.com/](https://www.tavily.com/)
2. 点击 "Sign Up" 或 "Get Started" 注册账号
3. 登录后进入 Dashboard
4. 在左侧菜单找到 "API Keys"
5. 复制您的 API Key（格式：`tvly-xxxxxxxxxxxxx`）

## 安装方法

### 方式 1: 使用项目安装器（推荐）

```bash
cd /Users/onlyliyj/Documents/cc-skills-config
python3 installer.py
```

选择 "tavily" MCP Server 进行安装。

### 方式 2: 手动安装

```bash
cd mcp/tavily
python3 install.py
```

安装脚本会：
1. 检测您的操作系统（macOS/Linux/Windows）
2. 检查 Node.js 和 npm 是否已安装
3. 引导您选择安装类型（Claude Desktop 或 Claude Code CLI）
4. 显示如何设置 API Key 环境变量
5. 自动配置 MCP 服务器

## 环境变量设置

### macOS / Linux (Zsh)

在 `~/.zshrc` 中添加：

```bash
export TAVILY_API_KEY="tvly-your_api_key_here"
```

然后执行：`source ~/.zshrc`

### macOS / Linux (Bash)

在 `~/.bashrc` 中添加：

```bash
export TAVILY_API_KEY="tvly-your_api_key_here"
```

然后执行：`source ~/.bashrc`

### Windows

**方法 1 - 系统环境变量:**
1. 右键点击 "此电脑" → "属性"
2. 点击 "高级系统设置"
3. 点击 "环境变量"
4. 在 "用户变量" 中添加：
   - 变量名: `TAVILY_API_KEY`
   - 变量值: `your_api_key_here`

**方法 2 - PowerShell 临时设置:**
```powershell
$env:TAVILY_API_KEY="your_api_key_here"
```

## 使用方法

安装完成并设置 API Key 后，在 Claude 中即可使用以下功能：

### 网络搜索
```
搜索最新的 AI 技术动态
查询 Python 3.12 的新特性
```

### 深度问答
```
对比 React 和 Vue 的优缺点
解释量子计算的基本原理
```

### 实时信息
```
今天的天气情况
最新的科技新闻
```

## 配置文件说明

### Claude Desktop 配置

安装脚本会在配置文件中添加：

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

### Claude Code CLI 配置

安装脚本会在配置文件中添加：

```json
{
  "mcpServers": {
    "tavily": {
      "type": "http",
      "url": "https://mcp.tavily.com/mcp/?tavilyApiKey=${TAVILY_API_KEY}"
    }
  }
}
```

**优势：**
- **安全性**：API Key 不会被硬编码到配置文件中
- **灵活性**：可以在 Shell 配置文件中设置环境变量
- **可分享**：配置文件可以安全地分享给团队成员使用

## 系统要求

- Python 3.6+
- Node.js 和 npm（用于运行 MCP 服务器）
- Claude Desktop 或 Claude Code CLI

## API 配额

- **免费层**：每月 1,000 次调用
- **付费计划**：根据需求选择更高配额

查看详细定价：https://www.tavily.com/pricing

## 文档

- [官方文档](https://docs.tavily.com/)
- [API 参考](https://docs.tavily.com/docs/tavily-api/rest-api)
- [Python SDK](https://docs.tavily.com/docs/python-sdk)
- [JavaScript SDK](https://docs.tavily.com/docs/js-sdk)

## 常见问题

### 安装后无法使用

1. **确保设置了 API Key 环境变量**
2. **重启 Claude Desktop 或 Claude Code CLI**
3. **检查 Node.js 和 npm 是否正确安装**

### API Key 验证失败

确保：
1. API Key 格式正确（以 `tvly-` 开头）
2. API Key 已正确复制（没有多余空格）
3. 账号处于激活状态

### 搜索结果不准确

尝试：
1. 使用更具体的关键词
2. 启用深度搜索模式
3. 调整搜索参数

### 超出配额限制

1. 检查 [Dashboard](https://www.tavily.com/dashboard) 中的使用情况
2. 考虑升级到付费计划
3. 优化搜索查询减少不必要的调用

## 跨平台支持

本安装脚本使用 Python 编写，提供以下平台的完整支持：

| 平台 | 支持状态 | 说明 |
|------|---------|------|
| macOS | ✅ 完全支持 | 包括 Intel 和 Apple Silicon |
| Linux | ✅ 完全支持 | 包括主流发行版 |
| Windows | ✅ 完全支持 | 包括 WSL 和原生 Windows |
| WSL | ✅ 完全支持 | 自动检测并使用 Windows 配置 |

## 技术支持

- 邮箱: support@tavily.com
- Discord: https://discord.gg/tavily
- Twitter: [@tavilyai](https://twitter.com/tavilyai)

## License

MIT License - 详见 [Tavily GitHub](https://github.com/tavily)
