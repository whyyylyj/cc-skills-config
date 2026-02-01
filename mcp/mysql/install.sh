#!/bin/bash
# MySQL MCP Server 安装脚本

echo "正在安装 MySQL MCP Server..."

# 检查 npx 是否可用
if ! command -v npx &> /dev/null; then
    echo "错误: npx 未找到"
    echo "请先安装 Node.js 和 npm"
    exit 1
fi

# 检查 MySQL 连接信息
if [ -z "$MYSQL_HOST" ]; then
    read -p "MySQL Host (default: localhost): " input_host
    export MYSQL_HOST="${input_host:-localhost}"
fi

if [ -z "$MYSQL_PORT" ]; then
    read -p "MySQL Port (default: 3306): " input_port
    export MYSQL_PORT="${input_port:-3306}"
fi

if [ -z "$MYSQL_USER" ]; then
    read -p "MySQL User (default: root): " input_user
    export MYSQL_USER="${input_user:-root}"
fi

if [ -z "$MYSQL_PASSWORD" ]; then
    read -s -p "MySQL Password: " input_password
    export MYSQL_PASSWORD="$input_password"
    echo
fi

if [ -z "$MYSQL_DATABASE" ]; then
    read -p "MySQL Database (default: test): " input_database
    export MYSQL_DATABASE="${input_database:-test}"
fi

# 测试连接
echo "测试 MySQL 连接..."
mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1" &> /dev/null

if [ $? -eq 0 ]; then
    echo "✓ MySQL 连接成功"
else
    echo "警告: 无法连接到 MySQL 服务器"
    echo "请检查连接信息并稍后在配置文件中修改"
fi

echo "✓ MySQL MCP Server 配置完成"
echo "请确保在 Claude Code 中启用此 MCP 服务器"
