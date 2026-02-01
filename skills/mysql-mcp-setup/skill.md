---
name: mysql-mcp-setup
description: 自动检测项目数据库配置并设置 MCP MySQL 连接工具。支持 Spring Boot, Node.js, Python, Go, PHP, Ruby 等多种项目类型. 针对Claude Code CLI优化，已验证环境变量名称和npm包名.
tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
scope: project
---

# MySQL MCP Setup Skill (Claude Code CLI 版本)

自动检测项目中的数据库配置文件，并交互式地配置 MCP MySQL 连接工具。

**⚠️ 重要说明**: 本技能针对 Claude Code CLI 优化，使用项目级 `.mcp.json` 配置，而非 Claude Desktop 应用配置。

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
- `init_configs/application*.yml` (常见于多环境配置)

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

**Spring Boot - application.yml (多数据源支持)**:
```yaml
spring:
   datasource:
      url: jdbc:mysql://localhost:3306/mydb
      username: user
      password: pass

   # 多数据源示例
   datasource1:
      jdbc-url: jdbc:mysql://host1:3306/db1
      username: user1
      password: pass1

   datasource2:
      jdbc-url: jdbc:mysql://host2:3306/db2
      username: user2
      password: pass2
```

解析规则：
- 读取 YAML 内容
- 提取所有数据源配置
- 支持多种配置格式：`spring.datasource.*`, `datasource*.*`, 自定义数据源名称
- 为每个数据源生成独立的 MCP 服务器配置

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
MYSQL_PASS=password
MYSQL_DB=mydb

DATABASE_URL=mysql://user:pass@localhost:3306/mydb
```

解析规则：
- 使用 `Grep` 搜索关键字：`DB_HOST`, `MYSQL_HOST`, `DATABASE_HOST`
- 搜索端口：`DB_PORT`, `MYSQL_PORT`, `DATABASE_PORT`
- 搜索用户名：`DB_USER`, `MYSQL_USER`, `DATABASE_USER`, `DB_USERNAME`
- 搜索密码：`DB_PASSWORD`, `MYSQL_PASS`, `DATABASE_PASSWORD`
- 搜索数据库名：`DB_NAME`, `MYSQL_DB`, `DATABASE_NAME`, `DB_DATABASE`
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

**⚠️ 关键配置要点** (基于实际验证经验):

1. **正确的 npm 包名**: `mcp-server-mysql` (NOT `@modelcontextprotocol/server-mysql`)
2. **正确的环境变量名**:
   - `MYSQL_HOST` ✓
   - `MYSQL_PORT` ✓
   - `MYSQL_USER` ✓
   - `MYSQL_PASS` ✓ (NOT `MYSQL_PASSWORD`)
   - `MYSQL_DB` ✓ (NOT `MYSQL_DATABASE`)

**配置结构**:
```json
{
   "mcpServers": {
      "mysql-<project-name>-<db-name>": {
         "command": "npx",
         "args": ["-y", "mcp-server-mysql"],
         "env": {
            "MYSQL_HOST": "localhost",
            "MYSQL_PORT": "3306",
            "MYSQL_USER": "user",
            "MYSQL_PASS": "password",
            "MYSQL_DB": "database"
         }
      }
   }
}
```

**MCP 服务器命名规则**:
- 基础格式: `mysql-<project-name>-<database-name>`
- 例如：`mysql-mom-robo-mommp`, `mysql-blog-api-users`
- 使用项目目录名 + 数据库名的组合
- 如果配置了多个数据源，每个数据源生成独立的服务器配置

执行步骤：
- 获取当前目录名称：使用 `Bash` 执行 `basename $(pwd)`
- 为每个数据源构建唯一的 MCP 服务器名称
- 构建完整的 MCP 配置 JSON 对象
- 输出配置摘要（不显示明文密码）

### Phase 5: 更新 Claude Code CLI 配置文件

**⚠️ 重要**: Claude Code CLI 使用项目根目录的 `.mcp.json` 文件，而非 Claude Desktop 的配置文件。

**配置文件路径**:
- 项目根目录: `.mcp.json` (新建)
- 项目设置: `.claude/settings.local.json` (更新)

执行步骤：

1. **创建 `.mcp.json` 文件**:
   - 在项目根目录创建 `.mcp.json`
   - 包含所有 MySQL 数据库的 MCP 服务器配置
   - 使用正确的 npm 包名和环境变量名

2. **更新 `.claude/settings.local.json`**:
   - 添加 `enableAllProjectMcpServers: true` 以自动启用所有项目级 MCP 服务器
   - 或使用 `enabledMcpjsonServers` 数组指定要启用的服务器

3. **更新 `.gitignore`**:
   - 添加 `.mcp.json` 以防止敏感信息被提交到版本控制

**配置文件示例**:

`.mcp.json`:
```json
{
   "mcpServers": {
      "mysql-mom-robo-mommp": {
         "command": "npx",
         "args": ["-y", "mcp-server-mysql"],
         "env": {
            "MYSQL_HOST": "sh-mom-dydb.wmcloud-qa.com",
            "MYSQL_PORT": "3306",
            "MYSQL_USER": "app_mommp_rw",
            "MYSQL_PASS": "RU2rkQRwPG1p72Ion",
            "MYSQL_DB": "mommp"
         }
      },
      "mysql-mom-robo-bigdata": {
         "command": "npx",
         "args": ["-y", "mcp-server-mysql"],
         "env": {
            "MYSQL_HOST": "db-bigdata-ro.wmcloud.com",
            "MYSQL_PORT": "3312",
            "MYSQL_USER": "app_momrobo_ro",
            "MYSQL_PASS": "password",
            "MYSQL_DB": "bigdata"
         }
      }
   }
}
```

`.claude/settings.local.json`:
```json
{
   "permissions": {
      "allow": ["*"]
   },
   "enableAllProjectMcpServers": true
}
```

`.gitignore`:
```
# MCP配置文件 (包含敏感信息)
.mcp.json
.claude/mcp-configs/
```

**配置合并逻辑**:
```python
# 伪代码示例
import json

# 读取现有配置
try:
    with open('.mcp.json', 'r') as f:
        existing_config = json.load(f)
except FileNotFoundError:
    existing_config = {"mcpServers": {}}

# 检查服务器是否已存在
for server_name, server_config in new_mysql_configs.items():
    if server_name in existing_config["mcpServers"]:
        user_choice = ask_user(f"配置 {server_name} 已存在，是否覆盖？",
                              ["覆盖", "跳过", "取消"])
        if user_choice == "跳过":
            continue
        elif user_choice == "取消":
            return

    existing_config["mcpServers"][server_name] = server_config

# 写入配置
with open('.mcp.json', 'w') as f:
    json.dump(existing_config, f, indent=2)
    f.write('\n')
```

### Phase 6: 更新 .gitignore

确保敏感配置文件不会被提交到版本控制系统。

执行步骤：
1. 使用 `Read` 读取现有的 `.gitignore` 文件
2. 检查是否已包含 `.mcp.json` 和 `.claude/mcp-configs/`
3. 如果不存在，添加到文件末尾
4. 使用 `Edit` 或 `Write` 更新文件

**添加的内容**:
```gitignore
# MCP配置文件 (包含敏感信息)
.mcp.json
.claude/mcp-configs/
```

### Phase 7: 验证和提示

验证配置文件格式，并提供后续步骤提示。

执行步骤：
1. 验证 JSON 格式是否正确
2. 验证必需字段是否齐全
3. 验证环境变量名称是否正确
4. 验证 npm 包名是否正确
5. 输出配置摘要
6. 提示用户重启 Claude Code CLI
7. 提供测试连接的命令

**输出示例**:
```
✅ MCP MySQL 配置已成功添加！

配置详情：
- 配置文件位置: .mcp.json
- 配置的服务器数量: 2
- 服务器列表:
  • mysql-mom-robo-mommp
  • mysql-mom-robo-bigdata

数据源详情：
1. mysql-mom-robo-mommp
   - 数据库主机: sh-mom-dydb.wmcloud-qa.com
   - 数据库端口: 3306
   - 数据库名称: mommp
   - 用户名: app_mommp_rw

2. mysql-mom-robo-bigdata
   - 数据库主机: db-bigdata-ro.wmcloud.com
   - 数据库端口: 3312
   - 数据库名称: bigdata
   - 用户名: app_momrobo_ro

后续步骤：
1. 重启 Claude Code CLI 会话
2. 重启后，使用 /mcp list 验证服务器是否加载
3. 使用以下命令测试连接：
   - mcp__mysql-mom-robo-mommp__mysql_query
   - mcp__mysql-mom-robo-bigdata__mysql_query

⚠️  安全提醒：
- .mcp.json 已添加到 .gitignore
- 配置文件中包含明文密码，请注意保护
- 建议使用只读账户进行查询操作
- 定期更新数据库密码

💡 常见问题：
- 如果 /mcp list 看不到服务器，检查 enableAllProjectMcpServers 是否为 true
- 如果连接失败，检查网络和VPN连接
- 工具命名格式: mcp__<server-name>__<action>
```

## 支持的项目类型

| 项目类型 | 标志性文件 | 配置文件 |
|---------|-----------|---------|
| Spring Boot | pom.xml, build.gradle | application.properties, application.yml, init_configs/application*.yml |
| Node.js | package.json | .env, config.js, database.js |
| Python Django | manage.py, settings.py | settings.py, .env |
| Python Flask | app.py, requirements.txt | .env, config.py |
| Python General | requirements.txt, setup.py | .env, database.ini |
| Go | go.mod | .env, config.yaml |
| PHP | composer.json | .env, config.php |
| Ruby | Gemfile | config/database.yml, .env |

## 使用示例

### 示例 1: Spring Boot 项目（单数据源）

**用户输入**:
```
/mysql-mcp-setup
```

**执行流程**:
1. 检测到项目类型: Spring Boot
2. 找到配置文件: `init_configs/application-qa.yml`
3. 提取数据库配置:
   - URL: jdbc:mysql://localhost:3306/myapp
   - Username: root
   - Password: secret
4. 生成 MCP 配置: `mysql-myapp-main`
5. 创建 `.mcp.json` 文件
6. 更新 `.claude/settings.local.json`
7. 更新 `.gitignore`
8. 输出成功提示

### 示例 2: Spring Boot 项目（多数据源）

**用户输入**:
```
/mysql-mcp-setup
```

**执行流程**:
1. 检测到项目类型: Spring Boot
2. 找到配置文件: `init_configs/application-qa.yml`
3. 提取多个数据源配置:
   - 数据源1 (mommp): host1, port1, user1, pass1, db1
   - 数据源2 (bigdata): host2, port2, user2, pass2, db2
   - 数据源3 (datayesdb): host3, port3, user3, pass3, db3
4. 为每个数据源生成独立的 MCP 配置:
   - `mysql-myapp-mommp`
   - `mysql-myapp-bigdata`
   - `mysql-myapp-datayesdb`
5. 创建 `.mcp.json` 文件，包含所有三个服务器配置
6. 更新 `.claude/settings.local.json`
7. 输出成功提示，列出所有配置的服务器

### 示例 3: Node.js 项目（多个配置文件）

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

### 示例 4: 未找到配置文件

**执行流程**:
1. 检测项目类型
2. 未找到支持的数据库配置文件
3. 输出提示:
```
❌ 未找到支持的数据库配置文件

支持以下配置文件格式：
- Spring Boot: application.properties, application.yml, init_configs/application*.yml
- Node.js: .env, config.js
- Python: settings.py, .env
- Go: config.yaml
- 通用: database.json

手动配置提示：
如果您的配置文件使用自定义格式，请手动创建 .mcp.json 文件：
1. 在项目根目录创建 .mcp.json
2. 添加以下配置：
{
  "mcpServers": {
    "mysql-your-project": {
      "command": "npx",
      "args": ["-y", "mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "your-host",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "your-user",
        "MYSQL_PASS": "your-password",
        "MYSQL_DB": "your-database"
      }
    }
  }
}
3. 在 .claude/settings.local.json 中添加 "enableAllProjectMcpServers": true
4. 重启 Claude Code CLI
```

## 实现要点

### 关键实现技巧

1. **文件查找模式**:
   - 使用 `Glob` 查找多个模式：`**/application*.properties`, `**/.env`, `**/init_configs/*.yml`
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

### 关键配置验证 (基于实际经验)

**⚠️ 必须验证的配置项**:

1. **npm 包名**: 必须是 `mcp-server-mysql`，不是 `@modelcontextprotocol/server-mysql`
2. **环境变量名**: 必须使用 `MYSQL_PASS` 和 `MYSQL_DB`，不是 `MYSQL_PASSWORD` 和 `MYSQL_DATABASE`
3. **配置文件位置**: 必须是项目根目录的 `.mcp.json`，不是 `~/.claude/mcp_servers/`
4. **settings 配置**: 必须在 `.claude/settings.local.json` 中设置 `enableAllProjectMcpServers: true`

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
   - 自动将 `.mcp.json` 和 `.claude/mcp-configs/` 添加到 `.gitignore`

## 测试验证

完成配置后，可以使用以下 MCP 工具验证连接：

```bash
# 验证 MCP 服务器已加载
/mcp list

# 查询数据库信息
mcp__mysql-mom-robo-mommp__mysql_query "SELECT DATABASE(), USER(), VERSION()"

# 列出所有表
mcp__mysql-mom-robo-mommp__mysql_query "SHOW TABLES"

# 查询表数据
mcp__mysql-mom-robo-mommp__mysql_query "SELECT COUNT(*) FROM account"
```

**工具命名格式**: `mcp__<server-name>__<action>`

示例:
- `mcp__mysql-mom-robo-mommp__mysql_query`
- `mcp__mysql-mom-robo-bigdata__mysql_query`
- `mcp__mysql-mom-robo-datayesdb__mysql_query`

## 故障排查

### 常见问题

**1. `/mcp list` 看不到配置的 MySQL 服务器**:

**检查步骤**:
- ✅ 确认 `.mcp.json` 文件在项目根目录
- ✅ 确认 `.claude/settings.local.json` 包含 `enableAllProjectMcpServers: true`
- ✅ 确认 JSON 格式正确（可以使用 `jq` 或在线工具验证）
- ✅ 完全重启 Claude Code CLI 会话

**修复方法**:
```bash
# 检查配置文件
cat .mcp.json
cat .claude/settings.local.json

# 验证 JSON 格式
cat .mcp.json | jq .

# 重启 Claude Code CLI
# 完全退出当前会话，然后重新启动
```

**2. MCP 工具调用时报错 "Access denied ... (using password: NO)"**:

**原因**: 环境变量名称错误，使用了 `MYSQL_PASSWORD` 而不是 `MYSQL_PASS`

**修复方法**:
```bash
# 更新 .mcp.json 中的环境变量名
# MYSQL_PASSWORD → MYSQL_PASS
# MYSQL_DATABASE → MYSQL_DB

python3 << 'EOF'
import json

with open('.mcp.json', 'r') as f:
    data = json.load(f)

for server_name, server_config in data.get('mcpServers', {}).items():
    if 'env' in server_config:
        env = server_config['env']
        if 'MYSQL_PASSWORD' in env:
            env['MYSQL_PASS'] = env.pop('MYSQL_PASSWORD')
        if 'MYSQL_DATABASE' in env:
            env['MYSQL_DB'] = env.pop('MYSQL_DATABASE')

with open('.mcp.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
EOF
```

**3. npm 包不存在或 404 错误**:

**原因**: 使用了错误的 npm 包名 `@modelcontextprotocol/server-mysql`

**修复方法**:
```bash
# 更新 .mcp.json 中的 npm 包名
# "@modelcontextprotocol/server-mysql" → "mcp-server-mysql"

python3 << 'EOF'
import json

with open('.mcp.json', 'r') as f:
    data = json.load(f)

for server_name, server_config in data.get('mcpServers', {}).items():
    if 'args' in server_config and '@modelcontextprotocol/server-mysql' in server_config['args']:
        server_config['args'] = ["-y", "mcp-server-mysql"]

with open('.mcp.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
EOF
```

**4. 数据库连接失败**:

**检查步骤**:
1. ✅ 测试网络连通性
   ```bash
   ping sh-mom-dydb.wmcloud-qa.com
   ```

2. ✅ 使用 Node.js 测试数据库凭据
   ```bash
   cd /tmp && npm install mysql2
   node -e "
   const mysql = require('mysql2/promise');
   (async () => {
     try {
       const connection = await mysql.createConnection({
         host: 'your-host',
         port: 3306,
         user: 'your-user',
         password: 'your-password',
         database: 'your-db'
       });
       console.log('✅ Connection successful!');
       await connection.end();
     } catch (error) {
       console.error('❌ Connection failed:', error.message);
     }
   })();
   "
   ```

3. ✅ 检查 VPN/网络环境
   - 确保连接到正确的内网
   - 验证防火墙设置

**5. 配置文件未找到**:
- 检查当前目录是否是项目根目录
- 确认配置文件名称是否匹配
- 尝试手动指定配置文件路径

**6. 无法解析配置**:
- 检查配置文件格式是否正确
- 确认必需的配置项是否齐全
- 查看配置文件是否有语法错误

**7. MCP 配置写入失败**:
- 检查项目目录权限
- 确认配置文件路径是否正确
- 尝试手动创建配置文件

## 后续优化方向

1. **多数据库支持**: PostgreSQL, MongoDB, SQLite
2. **多环境配置**: 支持 dev, test, prod 环境切换
3. **交互式配置**: 让用户选择使用哪个数据库配置
4. **连接测试**: 自动测试数据库连接是否成功
5. **配置回滚**: 备份和恢复配置文件功能
6. **配置验证**: 更严格的配置格式验证
7. **批量配置**: 支持一次配置多个数据库连接（已支持多数据源）

## 参考资源

- **MySQL MCP Server**: https://www.npmjs.com/package/mcp-server-mysql
- **Claude Code MCP 文档**: https://github.com/anthropics/claude-code
- **项目配置示例**: `.claude/MCP_MYSQL_SETUP.md` (本项目的配置记录)

---

**最后更新**: 2026-02-01
**版本**: 2.1 (Claude Code CLI 优化版)
**验证状态**: ✅ 已验证 (8个MySQL数据库配置成功)

---

## 实战经验总结

### ✅ 成功案例 (2026-02-01)

**项目**: mom-fund-research (Spring Boot Maven 多模块项目)

**检测结果**:
- 项目类型: Spring Boot (检测到 `pom.xml`)
- 配置文件: `init_configs/application-qa.yml`
- Git分支: `develop_qa` (自动选择对应环境的配置)

**提取的数据源** (6个):
1. **mommp** - 主业务数据库 (sh-mom-dydb.wmcloud-qa.com:3306)
2. **datayesdb** - DataYes数据库 (db-datayesdb-ro.wmcloud.com:3313)
3. **bigdata** - 大数据平台 (db-bigdata-ro.wmcloud.com:3312)
4. **smartdb** - 智能数据库 (内网IP: 10.22.160.107:3390)
5. **datapub** - 数据发布库 (db-datapub.wmcloud-stg.com:3318)
6. **mom_ind** - 指标数据库 (sh-mom-dydb.wmcloud-qa.com:3306)

**关键成功因素**:
1. ✅ 使用正确分支的配置文件 (develop_qa → application-qa.yml)
2. ✅ 正确识别多数据源配置 (包括自定义命名的数据源)
3. ✅ 环境变量名称完全正确 (`MYSQL_PASS`, `MYSQL_DB`)
4. ✅ `.gitignore` 已预先配置好相关条目
5. ✅ `.claude/settings.local.json` 已包含 `enableAllProjectMcpServers: true`

**生成的MCP服务器**:
```
mysql-mom-fund-research-mommp
mysql-mom-fund-research-datayesdb
mysql-mom-fund-research-bigdata
mysql-mom-fund-research-smartdb
mysql-mom-fund-research-datapub
mysql-mom-fund-research-mom-ind
```

**用户后续操作**:
1. 重启 Claude Code CLI 会话
2. 运行 `/mcp list` 验证服务器加载
3. 使用 `mcp__mysql-mom-fund-research-mommp__mysql_query "SELECT COUNT(*) FROM account"` 测试

### 💡 新增经验要点

1. **多环境配置文件自动选择**:
   - 检测 Git 分支名称，优先选择匹配环境的配置文件
   - 如 `develop_qa` 分支 → `application-qa.yml`
   - `develop` 分支 → `application-dev.yml`
   - `master/main` 分支 → `application-prod.yml` (如存在)

2. **MCP服务器命名规范改进**:
   - 格式: `mysql-<project-name>-<database-name>`
   - `<project-name>` 使用 `basename $(pwd)` 获取真实项目目录名
   - 不要使用硬编码或示例名称（如 `myapp`, `demo` 等）

3. **内网IP地址支持**:
   - 配置文件中可能包含内网IP (如 `10.22.160.107`)
   - MCP工具完全支持IP地址作为主机名
   - 需确保用户连接到正确的VPN/内网环境

4. **配置验证清单** (新增):
   - [ ] JSON格式正确 (`python3 -m json.tool` 验证)
   - [ ] npm包名: `mcp-server-mysql` (不是 `@modelcontextprotocol/*`)
   - [ ] 环境变量: `MYSQL_PASS`, `MYSQL_DB` (不是其他变体)
   - [ ] 配置文件位置: 项目根目录 `.mcp.json`
   - [ ] settings配置: `enableAllProjectMcpServers: true`
   - [ ] .gitignore保护: `.mcp.json` 已添加

5. **用户友好的输出格式**:
   ```
   ✅ MCP MySQL 配置已成功创建！

   配置详情：
   - 配置文件位置: .mcp.json
   - 配置的服务器数量: 6
   - 服务器列表:
     • mysql-<project>-<db1>
     • mysql-<project>-<db2>
     ...

   下一步：
   1. 重启 Claude Code CLI 会话
   2. 运行: /mcp list
   3. 测试: mcp__mysql-<project>-<db>__mysql_query "..."
   ```
