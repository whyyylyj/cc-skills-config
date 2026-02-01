#!/bin/bash
# Claude DSP (Dangerously Skip Permissions) Alias 安装脚本

echo "==================================="
echo "  Claude DSP Alias 安装向导"
echo "==================================="
echo ""

# 检测当前 shell - 优先检查 $SHELL 环境变量，更可靠
CURRENT_SHELL=""
SHELL_CONFIG=""

# 首先检查 $SHELL 环境变量（用户的默认 shell）
case "$SHELL" in
    */zsh)
        CURRENT_SHELL="zsh"
        SHELL_CONFIG="$HOME/.zshrc"
        ;;
    */bash)
        CURRENT_SHELL="bash"
        SHELL_CONFIG="$HOME/.bashrc"
        ;;
    */fish)
        CURRENT_SHELL="fish"
        SHELL_CONFIG="$HOME/.config/fish/config.fish"
        ;;
    *)
        # 如果 $SHELL 检测失败，尝试使用版本变量检测
        if [ -n "$ZSH_VERSION" ]; then
            CURRENT_SHELL="zsh"
            SHELL_CONFIG="$HOME/.zshrc"
        elif [ -n "$BASH_VERSION" ]; then
            CURRENT_SHELL="bash"
            SHELL_CONFIG="$HOME/.bashrc"
        elif [ -n "$FISH_VERSION" ]; then
            CURRENT_SHELL="fish"
            SHELL_CONFIG="$HOME/.config/fish/config.fish"
        else
            echo "⚠️  警告: 无法检测到支持的 Shell (zsh/bash/fish)"
            echo "请手动添加 alias 到您的 Shell 配置文件"
            exit 1
        fi
        ;;
esac

echo "检测到 Shell: $CURRENT_SHELL"
echo "配置文件: $SHELL_CONFIG"
echo ""

# 检查 claude 命令是否存在
echo "🔍 检查 Claude Code 安装..."
if command -v claude &> /dev/null; then
    CLAUDE_PATH=$(command -v claude)
    echo "✓ 找到 Claude Code: $CLAUDE_PATH"
else
    echo "⚠️  未找到 'claude' 命令"
    echo ""
    echo "Claude Code 可能未安装或未添加到 PATH"

    # 尝试常见的安装路径
    COMMON_PATHS=(
        "/usr/local/bin/claude"
        "/opt/homebrew/bin/claude"
        "$HOME/.local/bin/claude"
        "$HOME/bin/claude"
        "/app/bin/claude"
    )

    FOUND_PATH=""
    for path in "${COMMON_PATHS[@]}"; do
        if [ -f "$path" ]; then
            FOUND_PATH="$path"
            echo "✓ 在常见路径找到: $FOUND_PATH"
            break
        fi
    done

    if [ -z "$FOUND_PATH" ]; then
        echo ""
        read -p "请输入 Claude Code 的完整路径 (例如: /usr/local/bin/claude): " input_path
        if [ -n "$input_path" ] && [ -f "$input_path" ]; then
            CLAUDE_PATH="$input_path"
            echo "✓ 使用路径: $CLAUDE_PATH"
        else
            echo "❌ 错误: 文件不存在或路径为空"
            echo "请先安装 Claude Code: https://claude.ai/code"
            exit 1
        fi
    else
        CLAUDE_PATH="$FOUND_PATH"
    fi
fi
echo ""

# 说明功能
echo "📝 功能说明"
echo "-----------------------------------"
echo "此 alias 将添加快捷命令:"
echo "  claude-dsp -> claude --dangerously-skip-permissions"
echo ""
echo "⚠️  警告: --dangerously-skip-permissions 会跳过权限检查"
echo "  仅在信任的环境中使用，避免执行危险操作"
echo ""

# 确认安装
read -p "是否继续安装? [Y/n]: " confirm
if [[ $confirm =~ ^[Nn]$ ]]; then
    echo "安装已取消"
    exit 0
fi

echo ""

# 检查是否已存在
if grep -q "alias claude-dsp=" "$SHELL_CONFIG" 2>/dev/null; then
    echo "⚠️  检测到已存在 claude-dsp alias"
    read -p "是否覆盖现有配置? [y/N]: " overwrite
    if [[ ! $overwrite =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi

    # 删除旧的 alias 行
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS 使用 -i '' 需要 backup
        sed -i '' '/^alias claude-dsp=/d' "$SHELL_CONFIG"
    else
        sed -i '/^alias claude-dsp=/d' "$SHELL_CONFIG"
    fi
    echo "✓ 已移除旧配置"
fi

# 添加 alias
ALIAS_LINE="alias claude-dsp='claude --dangerously-skip-permissions'"

# 根据不同 shell 添加不同的配置
if [ "$CURRENT_SHELL" = "fish" ]; then
    ALIAS_LINE="alias claude-dsp='claude --dangerously-skip-permissions'"
    echo "" >> "$SHELL_CONFIG"
    echo "# Claude DSP Alias (Added by claude-configs installer)" >> "$SHELL_CONFIG"
    echo "$ALIAS_LINE" >> "$SHELL_CONFIG"
else
    echo "" >> "$SHELL_CONFIG"
    echo "# Claude DSP Alias (Added by claude-configs installer)" >> "$SHELL_CONFIG"
    echo "$ALIAS_LINE" >> "$SHELL_CONFIG"
fi

echo "✓ 已添加 alias 到 $SHELL_CONFIG"
echo ""

# 提示重新加载
echo "📋 安装完成！"
echo ""
echo "请运行以下命令使配置生效:"
if [ "$CURRENT_SHELL" = "zsh" ]; then
    echo "  source ~/.zshrc"
elif [ "$CURRENT_SHELL" = "bash" ]; then
    echo "  source ~/.bashrc"
elif [ "$CURRENT_SHELL" = "fish" ]; then
    echo "  source ~/.config/fish/config.fish"
fi
echo ""
echo "或重新打开终端"
echo ""
echo "使用方法:"
echo "  claude-dsp [命令]"
echo "  例如: claude-dsp '帮我分析这个文件'"
echo ""
echo "⚠️  安全提示: 此命令会跳过权限检查，请确保只在安全的环境中使用"
