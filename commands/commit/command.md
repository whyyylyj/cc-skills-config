---
name: commit
description: 智能 Git 提交命令，分析更改并生成有意义的提交信息
---

# Smart Commit Command

智能分析 Git 更改并生成有意义的提交信息。

## 功能

1. **自动分析更改**
   - 运行 `git status` 和 `git diff`
   - 识别新增、修改、删除的文件
   - 分析代码变更的性质

2. **生成提交信息**
   - 使用 AI 分析代码变更
   - 生成符合规范的提交信息
   - 包含简洁的标题和详细的描述

3. **执行提交**
   - 添加相关文件
   - 创建提交
   - 可选：推送到远程仓库

## 使用方法

```
/commit
```

或者指定提交信息：

```
/commit Fix authentication bug in login flow
```

## 提交信息格式

生成的提交信息遵循以下格式：

```
<type>: <subject>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Type 类型

- **feat**: 新功能
- **fix**: 修复 bug
- **docs**: 文档更新
- **style**: 代码格式调整
- **refactor**: 重构代码
- **test**: 测试相关
- **chore**: 构建/工具相关

## 示例

输入：
```
/commit
```

输出：
```
feat: Add user authentication system

- Implement login/logout functionality
- Add JWT token management
- Create user session handling

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## 注意事项

- 建议在提交前先运行测试
- 确保没有包含敏感信息
- 检查暂存的文件是否正确
