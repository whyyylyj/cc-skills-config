#!/usr/bin/env python3
"""
Claude Code 配置仓库交互式安装程序
"""

import os
import sys
import platform
import yaml
import shutil
from pathlib import Path

class ConfigInstaller:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.claude_config_dir = self._get_claude_config_dir()
        self.config = self._load_config()

    def _get_claude_config_dir(self):
        """获取 Claude Code 配置目录"""
        home = Path.home()
        # macOS/Linux: ~/.claude
        # Windows: %APPDATA%/claude
        if self.os_type in ["darwin", "linux"]:
            return home / ".claude"
        else:
            return Path(os.getenv("APPDATA")) / "claude"

    def _load_config(self):
        """加载 config.yml"""
        config_path = Path(__file__).parent / "config.yml"
        if not config_path.exists():
            print(f"错误: 找不到配置文件 {config_path}")
            sys.exit(1)

        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def detect_platform(self):
        """检测当前平台"""
        return self.os_type

    def filter_by_platform(self, items):
        """根据平台过滤可用配置"""
        return [item for item in items
                if "all" in item.get("platforms", [])
                or self.os_type in item.get("platforms", [])]

    def display_menu(self, category, items):
        """显示交互式菜单"""
        print(f"\n{'='*50}")
        print(f"可用的 {category.upper()} 配置:")
        print(f"{'='*50}")
        for i, item in enumerate(items, 1):
            print(f"{i}. {item['name']}")
            print(f"   {item['description']}")
        print(f"0. 返回上一级")

    def install_skill(self, skill_path):
        """安装 Skill 配置"""
        src = Path(__file__).parent / skill_path
        skill_name = Path(skill_path).parent.name
        dst = self.claude_config_dir / "skills" / skill_name

        # 创建目标目录
        dst.mkdir(parents=True, exist_ok=True)

        # 复制 skill.md 文件
        src_file = src
        if src.is_dir():
            src_file = src / "skill.md"
            if not src_file.exists():
                print(f"警告: 找不到 {src_file}")
                return False

        dst_file = dst / "skill.md"
        shutil.copy2(src_file, dst_file)
        print(f"✓ 已安装 Skill: {skill_name}")
        return True

    def install_mcp(self, mcp_path, install_script):
        """安装 MCP 服务器配置"""
        mcp_name = Path(mcp_path).name

        # 如果有安装脚本，先执行
        if install_script:
            script_path = Path(__file__).parent / install_script
            if script_path.exists():
                print(f"执行安装脚本: {install_script}")
                result = os.system(f"bash '{script_path}'")
                if result != 0:
                    print(f"警告: 安装脚本执行失败")
                    return False

        # 复制 MCP 配置文件
        src = Path(__file__).parent / mcp_path
        dst = self.claude_config_dir / "mcp_servers" / mcp_name
        dst.mkdir(parents=True, exist_ok=True)

        # 复制所有配置文件
        for item in src.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                shutil.copy2(item, dst / item.name)

        print(f"✓ 已安装 MCP 服务器: {mcp_name}")
        return True

    def install_command(self, cmd_path):
        """安装自定义命令"""
        src = Path(__file__).parent / cmd_path
        cmd_name = Path(cmd_path).parent.name
        dst = self.claude_config_dir / "commands" / cmd_name

        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst / "command.md")
        print(f"✓ 已安装命令: {cmd_name}")
        return True

    def install_hook(self, hook_path):
        """安装 Hook 配置"""
        src = Path(__file__).parent / hook_path
        hook_name = Path(hook_path).parent.name
        dst = self.claude_config_dir / "hooks" / hook_name

        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst / "hook.sh")

        # 设置可执行权限
        hook_file = dst / "hook.sh"
        os.chmod(hook_file, 0o755)
        print(f"✓ 已安装 Hook: {hook_name}")
        return True

    def interactive_menu(self):
        """交互式主菜单"""
        while True:
            print(f"\n{'='*50}")
            print("Claude Code 配置仓库安装程序")
            print(f"当前平台: {self.os_type.upper()}")
            print(f"配置目录: {self.claude_config_dir}")
            print(f"{'='*50}")
            print("1. Skills")
            print("2. MCP 服务器")
            print("3. 自定义命令")
            print("4. Hooks")
            print("5. 全部安装")
            print("6. 查看已安装配置")
            print("0. 退出")

            choice = input("\n请选择 (0-6): ").strip()

            if choice == "0":
                print("再见！")
                break
            elif choice == "1":
                self._category_menu("skills")
            elif choice == "2":
                self._category_menu("mcp")
            elif choice == "3":
                self._category_menu("commands")
            elif choice == "4":
                self._category_menu("hooks")
            elif choice == "5":
                self._install_all()
            elif choice == "6":
                self._list_installed()
            else:
                print("无效的选择")

    def _category_menu(self, category):
        """分类菜单"""
        items = self.filter_by_platform(self.config["categories"][category])

        if not items:
            print(f"\n当前平台 ({self.os_type}) 没有可用的 {category} 配置")
            return

        self.display_menu(category, items)

        choice = input(f"\n请选择要安装的 {category} (0-{len(items)}): ").strip()

        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                item = items[idx]
                confirm = input(f"确认安装 {item['name']}? (y/n): ").strip().lower()
                if confirm == "y":
                    if category == "skills":
                        self.install_skill(item["path"])
                    elif category == "mcp":
                        self.install_mcp(item["path"], item.get("install_script"))
                    elif category == "commands":
                        self.install_command(item["path"])
                    elif category == "hooks":
                        self.install_hook(item["path"])
            else:
                print("无效的选择")
        except (ValueError, IndexError):
            print("无效的选择")

    def _install_all(self):
        """安装所有配置"""
        confirm = input("确认安装所有配置? (y/n): ").strip().lower()
        if confirm == "y":
            for category in ["skills", "mcp", "commands", "hooks"]:
                items = self.filter_by_platform(self.config["categories"][category])
                if not items:
                    continue

                print(f"\n{'='*50}")
                print(f"安装 {category.upper()}...")
                print(f"{'='*50}")

                for item in items:
                    print(f"\n安装 {item['name']}...")
                    if category == "skills":
                        self.install_skill(item["path"])
                    elif category == "mcp":
                        self.install_mcp(item["path"], item.get("install_script"))
                    elif category == "commands":
                        self.install_command(item["path"])
                    elif category == "hooks":
                        self.install_hook(item["path"])

            print("\n✓ 所有配置安装完成！")

    def _list_installed(self):
        """列出已安装的配置"""
        print(f"\n{'='*50}")
        print("已安装的配置")
        print(f"{'='*50}")

        # Skills
        skills_dir = self.claude_config_dir / "skills"
        if skills_dir.exists():
            skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
            if skills:
                print(f"\nSkills ({len(skills)}):")
                for skill in skills:
                    print(f"  - {skill}")

        # MCP Servers
        mcp_dir = self.claude_config_dir / "mcp_servers"
        if mcp_dir.exists():
            mcps = [d.name for d in mcp_dir.iterdir() if d.is_dir()]
            if mcps:
                print(f"\nMCP 服务器 ({len(mcps)}):")
                for mcp in mcps:
                    print(f"  - {mcp}")

        # Commands
        cmd_dir = self.claude_config_dir / "commands"
        if cmd_dir.exists():
            cmds = [d.name for d in cmd_dir.iterdir() if d.is_dir()]
            if cmds:
                print(f"\n自定义命令 ({len(cmds)}):")
                for cmd in cmds:
                    print(f"  - {cmd}")

        # Hooks
        hooks_dir = self.claude_config_dir / "hooks"
        if hooks_dir.exists():
            hooks = [d.name for d in hooks_dir.iterdir() if d.is_dir()]
            if hooks:
                print(f"\nHooks ({len(hooks)}):")
                for hook in hooks:
                    print(f"  - {hook}")

        print(f"{'='*50}\n")

def main():
    print("正在加载配置...")
    print("\n💡 提示：你也可以通过 Claude Code Marketplace 安装此配置：")
    print("   claude plugin marketplace add https://github.com/onlyliyj/cc-skills-config\n")
    try:
        installer = ConfigInstaller()
        installer.interactive_menu()
    except KeyboardInterrupt:
        print("\n\n安装已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
