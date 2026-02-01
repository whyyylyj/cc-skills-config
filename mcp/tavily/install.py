#!/usr/bin/env python3
"""
Tavily MCP Server 安装脚本
支持 macOS、Linux 和 Windows
兼容 Claude Desktop 和 Claude Code CLI
"""

import os
import sys
import json
import platform
import subprocess
import shutil
from pathlib import Path
from datetime import datetime


class Colors:
    """终端颜色输出"""
    if sys.platform == "win32":
        # Windows 可能不支持 ANSI 颜色
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        BOLD = ""
        RESET = ""
    else:
        RED = "\033[0;31m"
        GREEN = "\033[0;32m"
        YELLOW = "\033[1;33m"
        BLUE = "\033[0;34m"
        BOLD = "\033[1m"
        RESET = "\033[0m"


def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")


def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")


def print_info(msg):
    print(f"{Colors.YELLOW}ℹ {msg}{Colors.RESET}")


def print_header(msg):
    print(f"{Colors.BLUE}{msg}{Colors.RESET}")


def detect_os():
    """检测操作系统"""
    system = platform.system()
    if system == "Darwin":
        return "macos"
    elif system == "Linux":
        # 检测是否是 WSL
        try:
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower():
                    return "wsl"
        except:
            pass
        return "linux"
    elif system == "Windows":
        return "windows"
    else:
        return "unknown"


def get_claude_desktop_config_path():
    """获取 Claude Desktop 配置文件路径"""
    os_type = detect_os()

    if os_type == "macos":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"

    elif os_type in ["linux", "wsl"]:
        # WSL 环境下尝试访问 Windows 路径
        if os_type == "wsl":
            windows_users = Path("/mnt/c/Users")
            if windows_users.exists():
                for user_dir in windows_users.iterdir():
                    if user_dir.is_dir():
                        claude_path = user_dir / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
                        if claude_path.exists():
                            return claude_path

        # Linux 默认路径
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"

    elif os_type == "windows":
        appdata = os.environ.get("APPDATA", "")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"

    return None


def get_claude_cli_config_path():
    """获取 Claude Code CLI 配置文件路径"""
    return Path.home() / ".claude.json"


def command_exists(cmd):
    """检查命令是否存在"""
    return shutil.which(cmd) is not None


def show_welcome():
    """显示欢迎信息"""
    print("=" * 50)
    print("  Tavily MCP Server 安装向导")
    print("=" * 50)
    print()
    print_info(f"检测到操作系统: {detect_os()}")
    print()


def check_dependencies():
    """检查系统依赖"""
    print_info("检查系统依赖...")
    print()

    # 检查 npx
    if command_exists("npx"):
        print_success("npx 已安装")
        try:
            result = subprocess.run(["npx", "--version"], capture_output=True, text=True)
            print(f"   版本: {result.stdout.strip()}")
        except:
            print("   版本: 未知")
    else:
        print_error("未找到 npx")
        print()
        print("请先安装 Node.js 和 npm:")
        print("  - macOS: brew install node")
        print("  - Linux: 访问 https://nodejs.org/")
        print("  - Windows: 下载并安装 https://nodejs.org/")
        return False

    # 检查 node
    if command_exists("node"):
        print_success("node 已安装")
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            print(f"   版本: {result.stdout.strip()}")
        except:
            print("   版本: 未知")
    else:
        print_error("未找到 node")
        print()
        print("修改配置文件需要 node，请安装 Node.js")
        return False

    print()
    return True


def show_api_key_guide():
    """显示 API Key 获取指南"""
    print()
    print_header("📝 Tavily API Key 获取指南")
    print("-" * 50)
    print("1. 访问 Tavily 官网: https://www.tavily.com/")
    print("2. 点击右上角的 'Sign Up' 或 'Get Started' 按钮")
    print("3. 注册账号（支持 Google/GitHub 账号登录）")
    print("4. 登录后进入 Dashboard")
    print("5. 在左侧菜单找到 'API Keys' 或点击 'Get API Key'")
    print("6. 复制您的 API Key（格式类似: tvly-xxxxxxxxxxxxx）")
    print()
    print_info("💡 Tavily 提供免费层，每月可免费调用 1000 次")
    print()
    print_header("🔐 设置 API Key 环境变量")
    print("-" * 50)

    os_type = detect_os()

    if os_type in ["macos", "linux", "wsl"]:
        # 检测 shell 类型
        shell = os.environ.get("SHELL", "")
        if "zsh" in shell or Path.home() / ".zshrc" in Path.home().iterdir():
            print("请将以下行添加到您的 Shell 配置文件中:")
            print("  文件: ~/.zshrc")
            print("  添加: export TAVILY_API_KEY=\"your_api_key_here\"")
            print()
            print("然后执行: source ~/.zshrc")
        else:
            print("请将以下行添加到您的 Shell 配置文件中:")
            print("  文件: ~/.bashrc")
            print("  添加: export TAVILY_API_KEY=\"your_api_key_here\"")
            print()
            print("然后执行: source ~/.bashrc")

    elif os_type == "windows":
        print("Windows 方法 1 - 使用系统环境变量:")
        print("  1. 右键点击 '此电脑' -> '属性'")
        print("  2. 点击 '高级系统设置'")
        print("  3. 点击 '环境变量'")
        print("  4. 在 '用户变量' 中添加:")
        print("     变量名: TAVILY_API_KEY")
        print("     变量值: your_api_key_here")
        print()
        print("Windows 方法 2 - 使用 PowerShell 临时设置:")
        print("  $env:TAVILY_API_KEY=\"your_api_key_here\"")

    print()


def backup_config(config_path):
    """备份配置文件"""
    if config_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = config_path.parent / f"{config_path.name}.backup.{timestamp}"
        shutil.copy2(config_path, backup_path)
        print_success(f"已备份配置到: {backup_path}")
        return backup_path
    return None


def configure_claude_desktop(config_path):
    """配置 Claude Desktop"""
    print_header("配置 Claude Desktop")
    print()

    # 备份
    backup_config(config_path)

    # 读取现有配置
    config = {}
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    config = json.loads(content)
        except Exception as e:
            print_info(f"配置文件为空或格式错误，将创建新配置")

    # 确保 mcpServers 存在
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # 配置 Tavily MCP
    config["mcpServers"]["tavily"] = {
        "command": "npx",
        "args": ["-y", "@tavily/mcp-server"],
        "env": {
            "TAVILY_API_KEY": "${TAVILY_API_KEY:-}"
        }
    }

    # 确保父目录存在
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入配置
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print_success("Claude Desktop 配置完成")
    print()
    print_info(f"配置文件: {config_path}")
    print_info("请确保设置 TAVILY_API_KEY 环境变量")


def configure_claude_cli(config_path):
    """配置 Claude Code CLI"""
    print_header("配置 Claude Code CLI")
    print()

    # 备份
    backup_config(config_path)

    # 读取现有配置
    config = {}
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    config = json.loads(content)
        except Exception as e:
            print_info(f"配置文件为空或格式错误，将创建新配置")

    # 确保 mcpServers 存在
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # 配置 Tavily MCP (使用 HTTP remote 方式)
    config["mcpServers"]["tavily"] = {
        "type": "http",
        "url": "https://mcp.tavily.com/mcp/?tavilyApiKey=${TAVILY_API_KEY}"
    }

    # 确保父目录存在
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入配置
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print_success("Claude Code CLI 配置完成")
    print()
    print_info(f"配置文件: {config_path}")
    print_info("请确保设置 TAVILY_API_KEY 环境变量")


def main_menu():
    """主菜单"""
    os_type = detect_os()
    print()
    print_header("请选择安装类型:")
    print("1) Claude Desktop (GUI 应用)")
    print("2) Claude Code CLI (命令行工具)")
    print("3) 同时安装两个版本")
    print("4) 仅显示 API Key 设置说明")
    print("5) 退出")
    print()

    try:
        choice = input("请输入选项 (1-5): ").strip()

        if choice == "1":
            print()
            show_api_key_guide()
            print()
            desktop_config = get_claude_desktop_config_path()
            if desktop_config:
                configure_claude_desktop(desktop_config)
            else:
                print_error("无法确定 Claude Desktop 配置路径")
                sys.exit(1)

        elif choice == "2":
            print()
            show_api_key_guide()
            print()
            cli_config = get_claude_cli_config_path()
            configure_claude_cli(cli_config)

        elif choice == "3":
            print()
            show_api_key_guide()
            print()
            desktop_config = get_claude_desktop_config_path()
            if desktop_config:
                configure_claude_desktop(desktop_config)
                print()

            cli_config = get_claude_cli_config_path()
            configure_claude_cli(cli_config)

        elif choice == "4":
            print()
            show_api_key_guide()
            sys.exit(0)

        elif choice == "5":
            print_info("退出安装")
            sys.exit(0)

        else:
            print_error("无效选项")
            sys.exit(1)

    except KeyboardInterrupt:
        print()
        print_info("安装已取消")
        sys.exit(0)


def show_completion():
    """显示完成信息"""
    print()
    print_header("=" * 50)
    print_success("安装完成！")
    print_header("=" * 50)
    print()
    print("📋 后续步骤:")
    print("-" * 50)
    print("1. 按照上述说明设置 TAVILY_API_KEY 环境变量")
    print("2. 重启 Claude Desktop 或 Claude Code CLI")
    print("3. 在对话中使用搜索功能")
    print()
    print("📚 使用示例:")
    print("  - 搜索最新的 AI 技术动态")
    print("  - 查询 Python 3.12 的新特性")
    print("  - 对比 React 和 Vue 的优缺点")
    print()
    print("📖 文档: https://docs.tavily.com/")
    print()


def main():
    """主函数"""
    try:
        show_welcome()

        # 检查依赖
        if not check_dependencies():
            sys.exit(1)

        # 显示主菜单
        main_menu()

        # 显示完成信息
        show_completion()

    except KeyboardInterrupt:
        print()
        print()
        print_info("安装已取消")
        sys.exit(0)
    except Exception as e:
        print()
        print_error(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
