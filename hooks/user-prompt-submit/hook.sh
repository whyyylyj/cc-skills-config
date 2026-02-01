#!/bin/bash
# User Prompt Submit Hook
# 在用户提交提示前进行验证和增强

# 获取用户输入
USER_PROMPT="$1"

# 5. 自动检测语言并配置
SETTINGS_FILE="$HOME/.claude/settings.json"

# 检测语言（中文包含中文字符，英文不包含）
if [[ "$USER_PROMPT" =~ [\p{Han}]+ ]]; then
    # 中文提示
    LANGUAGE="Chinese"
else
    # 英文或其他语言，默认中文
    LANGUAGE="Chinese"
fi

# 更新配置文件中的语言设置
if [ -f "$SETTINGS_FILE" ]; then
    # 检查是否已有 language 设置
    if grep -q '"language"' "$SETTINGS_FILE"; then
        # 更新现有设置
        sed -i.bak 's/"language": "[^"]*"/"language": "'$LANGUAGE'"/' "$SETTINGS_FILE"
    else
        # 添加新设置
        sed -i.bak 's/^}/  "language": "'$LANGUAGE'"\n}/' "$SETTINGS_FILE"
    fi
    # 删除备份文件
    rm -f "${SETTINGS_FILE}.bak"
else
    # 创建新配置文件
    cat > "$SETTINGS_FILE" << EOF
{
  "language": "$LANGUAGE"
}
EOF
fi

echo "✅ 已设置语言为: $LANGUAGE"

# 1. 检查提示长度
PROMPT_LENGTH=${#USER_PROMPT}
MIN_LENGTH=10

if [ "$PROMPT_LENGTH" -lt "$MIN_LENGTH" ]; then
    echo "警告: 提示过短（少于 $MIN_LENGTH 个字符）"
    echo "建议提供更多上下文信息以获得更好的结果"
    # 不阻止提交，只是警告
fi

# 2. 检查是否包含上下文
if [[ ! "$USER_PROMPT" =~ @(在|使用|根据|基于|请) ]] && [ "$PROMPT_LENGTH" -lt 50 ]; then
    echo "提示: 添加更多上下文可能有助于 Claude 更好地理解你的需求"
fi

# 3. 检查敏感信息模式（简单示例）
if [[ "$USER_PROMPT" =~ @(password|secret|token|key)\s*[:=]\s*\S+ ]]; then
    echo "警告: 提示中可能包含敏感信息（密码、密钥等）"
    echo "请确认是否安全"
fi

# 4. 记录提示历史（可选）
HISTORY_FILE="$HOME/.claude/prompt_history.txt"
mkdir -p "$(dirname "$HISTORY_FILE")"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] $USER_PROMPT" >> "$HISTORY_FILE"

# 不阻塞提交，返回 0 表示成功
exit 0
