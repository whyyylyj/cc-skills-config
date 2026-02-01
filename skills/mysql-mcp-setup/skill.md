---
name: mysql-mcp-setup
description: 自动检测项目数据库配置并设置 MCP MySQL 连接工具。支持 Spring Boot, Node.js, Python, Go, PHP, Ruby 等多种项目类型。
tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
---

# MySQL MCP Setup Skill

自动检测项目中的数据库配置文件，并交互式地配置 MCP MySQL 连接工具。

## 工作流程

### Phase 1: 项目类型检测

首先检测当前目录的项目类型，通过查找标志性文件：

1. **Java/Spring Boot**: `pom.xml`, `build.gradle`, `src/main/java`
2. **Node.js**: `package.json`, `node_modules`
3. **Python**: `requirements.txt`, `setup.py`, `pyproject.toml`, `manage.py` (Django)
4. **Go**: `go.mod`, `main.go`
5. **PHP**: `composer.json`
6. **Ruby**: `Gemfile`

执行步骤：
- 使用 `Glob` 查找上述标志性文件
- 确定项目类型
- 输出检测结果：`检测到项目类型: [Spring Boot/Node.js/Python/etc.]`

### Phase 2: 数据库配置文件定位

根据项目类型，查找对应的数据库配置文件：

**Spring Boot**:
- `application.properties`
- `application.yml`
- `application.yaml`
- `src/main/resources/application*.properties`
- `src/main/resources/application*.yml`

**Node.js**:
- `.env`
- `config.js`
- `config.json`
- `database.js`
- `dbconfig.js`

**Python**:
- `.env`
- `settings.py` (Django)
- `config.py`
- `database.ini`
- `alembic.ini`

**Go**:
- `.env`
- `config.yaml`
- `config.yml`
- `config.go`

**PHP**:
- `.env`
- `config.php`
- `.env.local`

**Ruby**:
- `config/database.yml`
- `.env`

**通用配置**:
- `database.json`
- `dbconfig.json`

执行步骤：
- 使用 `Glob` 查找配置文件（支持多级目录）
- 如果找到多个配置文件，列出所有找到的文件
- 使用 `AskUserQuestion` 让用户选择使用哪个配置文件，或者使用所有找到的配置

### Phase 3: 提取数据库连接信息

根据不同的配置文件格式，解析数据库连接参数。

#### 配置解析策略

**Spring Boot - application.properties**:
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
spring.datasource.username=user
spring.datasource.password=pass
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
```

解析规则：
- 使用正则表达式提取 JDBC URL: `jdbc:mysql://([^:]+):(\d+)/(.+)`
- 提取 username 和 password
- 默认端口: 3306

**Spring Boot - application.yml**:
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: user
    password: pass
```

解析规则：
- 读取 YAML 内容
- 提取 `spring.datasource.url`, `spring.datasource.username`, `spring.datasource.password`

**Node.js - .env**:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=user
DB_PASSWORD=pass
DB_NAME=mydb

# 或者其他命名变体
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=mydb

DATABASE_URL=mysql://user:pass@localhost:3306/mydb
```

解析规则：
- 使用 `Grep` 搜索关键字：`DB_HOST`, `MYSQL_HOST`, `DATABASE_HOST`
- 搜索端口：`DB_PORT`, `MYSQL_PORT`, `DATABASE_PORT`
- 搜索用户名：`DB_USER`, `MYSQL_USER`, `DATABASE_USER`, `DB_USERNAME`
- 搜索密码：`DB_PASSWORD`, `MYSQL_PASSWORD`, `DATABASE_PASSWORD`
- 搜索数据库名：`DB_NAME`, `MYSQL_DATABASE`, `DATABASE_NAME`, `DB_DATABASE`
- 解析 `DATABASE_URL` 格式: `mysql://user:pass@host:port/dbname`

**Python - Django settings.py**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'user',
        'PASSWORD': 'pass',
        'NAME': 'mydb'
    }
}
```

解析规则：
- 使用 `Grep` 提取 `DATABASES` 字典
- 解析 `HOST`, `PORT`, `USER`, `PASSWORD`, `NAME` 字段

**通用 JSON 配置**:
```json
{
  "database": {
    "host": "localhost",
    "port": 3306,
    "user": "user",
    "password": "pass",
    "database": "mydb"
  }
}
```

解析规则：
- 读取 JSON 文件
- 提取数据库相关字段

执行步骤：
- 使用 `Read` 读取配置文件内容
- 使用 `Grep` 提取关键配置项
- 使用正则表达式解析 JDBC URL 或环境变量
- 验证必需参数是否存在（host, user, password, database）
- 设置默认值：port=3306

### Phase 4: 生成 MCP 配置

构建标准的 MCP MySQL 配置 JSON。

**配置结构**:
```json
{
  "mcpServers": {
    "mysql-<project-name>": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "user",
        "MYSQL_PASSWORD": "password",
        "MYSQL_DATABASE": "database"
      }
    }
  }
}
```

**MCP 服务器命名规则**:
- 使用当前目录名称作为服务器名称
- 例如：`mysql-myproject`, `mysql-blog-api`
- 如果目录名是通用的（如 `app`, `server`），则使用 `mysql-default`

执行步骤：
- 获取当前目录名称：使用 `Bash` 执行 `basename $(pwd)`
- 构建 MCP 服务器名称：`mysql-<dirname>`
- 构建完整的 MCP 配置 JSON 对象
- 输出配置摘要（不显示明文密码）

### Phase 5: 更新配置文件

读取现有的 Claude Desktop 配置文件，合并新的 MySQL 配置。

**配置文件路径**:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

执行步骤：
1. 检测操作系统，确定配置文件路径
2. 使用 `Read` 读取现有配置文件（如果存在）
3. 解析现有配置的 JSON
4. 检查是否已存在同名 MCP 服务器配置
5. 如果存在，询问用户是否覆盖
6. 合并新配置到现有配置
7. 使用 `Write` 写入更新后的配置文件
8. 备份原配置文件（可选）

**配置合并逻辑**:
```python
# 伪代码示例
existing_config = read_config_file()
if "mysql-project" in existing_config["mcpServers"]:
    # 询问用户是否覆盖
    user_choice = ask_user("配置已存在，是否覆盖？", ["覆盖", "取消", "创建新名称"])
    if user_choice == "取消":
        return
    elif user_choice == "创建新名称":
        server_name = generate_unique_name()

existing_config["mcpServers"][server_name] = new_mysql_config
write_config_file(existing_config)
```

### Phase 6: 验证和提示

验证配置文件格式，并提供后续步骤提示。

执行步骤：
1. 验证 JSON 格式是否正确
2. 验证必需字段是否齐全
3. 输出配置摘要
4. 提示用户重启 Claude Desktop
5. 提供测试连接的命令

**输出示例**:
```
✅ MCP MySQL 配置已成功添加！

配置详情：
- 服务器名称: mysql-myproject
- 数据库主机: localhost
- 数据库端口: 3306
- 数据库名称: mydb
- 用户名: user

后续步骤：
1. 重启 Claude Desktop 应用
2. 重启后，MCP MySQL 工具将可用
3. 使用以下命令测试连接：
   - mcp__mysql__test_connection
   - mcp__mysql__list_tables

⚠️  安全提醒：
- 配置文件中包含明文密码，请注意保护
- 建议使用环境变量或密钥管理工具
- 不要将配置文件提交到版本控制系统
```

## 支持的项目类型

| 项目类型 | 标志性文件 | 配置文件 |
|---------|-----------|---------|
| Spring Boot | pom.xml, build.gradle | application.properties, application.yml |
| Node.js | package.json | .env, config.js, database.js |
| Python Django | manage.py, settings.py | settings.py, .env |
| Python Flask | app.py, requirements.txt | .env, config.py |
| Python General | requirements.txt, setup.py | .env, database.ini |
| Go | go.mod | .env, config.yaml |
| PHP | composer.json | .env, config.php |
| Ruby | Gemfile | config/database.yml, .env |

## 使用示例

### 示例 1: Spring Boot 项目

**用户输入**:
```
/mysql-mcp-setup
```

**执行流程**:
1. 检测到项目类型: Spring Boot
2. 找到配置文件: `src/main/resources/application.properties`
3. 提取数据库配置:
   - URL: jdbc:mysql://localhost:3306/myapp
   - Username: root
   - Password: secret
4. 生成 MCP 配置: `mysql-myapp`
5. 更新配置文件
6. 输出成功提示

### 示例 2: Node.js 项目（多个配置文件）

**用户输入**:
```
/mysql-mcp-setup
```

**执行流程**:
1. 检测到项目类型: Node.js
2. 找到多个配置文件:
   - `.env`
   - `config/database.js`
3. 询问用户选择:
   - 选项 1: 使用 .env
   - 选项 2: 使用 config/database.js
   - 选项 3: 使用所有配置
4. 根据用户选择继续配置...

### 示例 3: 未找到配置文件

**执行流程**:
1. 检测项目类型
2. 未找到支持的数据库配置文件
3. 输出提示:
```
❌ 未找到支持的数据库配置文件

支持以下配置文件格式：
- Spring Boot: application.properties, application.yml
- Node.js: .env, config.js
- Python: settings.py, .env
- Go: config.yaml
- 通用: database.json

手动配置提示：
如果您的配置文件使用自定义格式，请手动创建 MCP 配置：
1. 打开 ~/Library/Application Support/Claude/claude_desktop_config.json
2. 添加以下配置：
{
  "mcpServers": {
    "mysql-your-project": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": {
        "MYSQL_HOST": "your-host",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "your-user",
        "MYSQL_PASSWORD": "your-password",
        "MYSQL_DATABASE": "your-database"
      }
    }
  }
}
```

## 实现要点

### 关键实现技巧

1. **文件查找模式**:
   - 使用 `Glob` 巯找多个模式：`**/application*.properties`, `**/.env`
   - 支持递归搜索子目录

2. **配置解析**:
   - 对于 `.env` 文件，使用 `Grep` 提取关键字
   - 对于 YAML 文件，使用文本模式匹配（避免依赖 YAML 解析库）
   - 对于 JSON 文件，直接读取和解析

3. **JDBC URL 解析**:
   - 正则表达式: `jdbc:mysql://([^:]+)(?::(\d+))?/([^?]+)`
   - 提取 host, port (可选), database

4. **DATABASE_URL 解析**:
   - 正则表达式: `mysql://([^:]+):([^@]+)@([^:]+):?(\d+)?/(.+)`
   - 提取 username, password, host, port (可选), database

5. **错误处理**:
   - 如果配置文件不存在，输出友好的错误提示
   - 如果必需参数缺失，提示用户手动配置
   - 如果配置文件格式错误，显示具体的错误位置

### 安全考虑

1. **密码保护**:
   - 不在输出中显示明文密码
   - 使用 `******` 替换密码显示
   - 警告用户配置文件中的明文密码风险

2. **配置文件权限**:
   - 检查配置文件权限是否过于开放
   - 建议设置合适的文件权限

3. **敏感信息警告**:
   - 提醒用户不要将配置文件提交到 Git
   - 建议 `.env` 文件添加到 `.gitignore`

## 测试验证

完成配置后，可以使用以下 MCP 工具验证连接：

```bash
# 测试连接
mcp__mysql__test_connection

# 列出所有表
mcp__mysql__list_tables

# 查询表数据
mcp__mysql__run_select_query
```

## 故障排查

### 常见问题

**1. 配置文件未找到**:
- 检查当前目录是否是项目根目录
- 确认配置文件名称是否匹配
- 尝试手动指定配置文件路径

**2. 无法解析配置**:
- 检查配置文件格式是否正确
- 确认必需的配置项是否齐全
- 查看配置文件是否有语法错误

**3. MCP 配置写入失败**:
- 检查 Claude Desktop 配置目录权限
- 确认配置文件路径是否正确
- 尝试手动创建配置文件

**4. 连接测试失败**:
- 验证数据库是否正在运行
- 检查数据库用户名和密码是否正确
- 确认数据库端口是否正确
- 测试网络连接是否正常

## 后续优化方向

1. **多数据库支持**: PostgreSQL, MongoDB, SQLite
2. **多环境配置**: 支持 dev, test, prod 环境切换
3. **交互式配置**: 让用户选择使用哪个数据库配置
4. **连接测试**: 自动测试数据库连接是否成功
5. **配置回滚**: 备份和恢复配置文件功能
6. **配置验证**: 更严格的配置格式验证
7. **批量配置**: 支持一次配置多个数据库连接
