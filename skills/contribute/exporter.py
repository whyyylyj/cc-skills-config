#!/usr/bin/env python3
"""
Contribute Skill - Configuration Exporter
Exports local Claude Code configurations into a shareable installer package.
"""

import os
import sys
import json
import yaml
import shutil
import platform
from pathlib import Path
from datetime import datetime
import re

class ConfigExporter:
    """Exports Claude Code configurations to a shareable package."""

    # Sensitive field patterns to detect
    SENSITIVE_PATTERNS = [
        r'API[_-]?KEY',
        r'SECRET[_-]?KEY',
        r'PRIVATE[_-]?KEY',
        r'ACCESS[_-]?TOKEN',
        r'AUTH[_-]?TOKEN',
        r'REFRESH[_-]?TOKEN',
        r'PASSWORD',
        r'PASS',
        r'TOKEN',
        r'SECRET',
        r'CREDENTIALS',
        r'API[_-]?SECRET',
    ]

    def __init__(self, output_dir="claude-config-export"):
        """Initialize the exporter."""
        self.os_type = platform.system().lower()
        self.claude_config_dir = self._get_claude_config_dir()
        self.output_dir = Path(output_dir)
        self.scanned_configs = {}
        self.selected_configs = {}
        self.sensitive_vars = {}

    def _get_claude_config_dir(self):
        """Get the Claude Code config directory based on OS."""
        if self.os_type == "windows":
            import os
            appdata = os.environ.get('APPDATA', '')
            return Path(appdata) / 'claude'
        else:
            return Path.home() / '.claude'

    def scan_configurations(self):
        """Scan all installed configurations."""
        print("🔍 Scanning configurations...")
        self.scanned_configs = {
            'skills': self._scan_skills(),
            'mcp_servers': self._scan_mcp_servers(),
            'commands': self._scan_commands(),
            'hooks': self._scan_hooks(),
        }
        self._print_scanned_configs()

    def _scan_skills(self):
        """Scan installed skills."""
        skills_dir = self.claude_config_dir / 'skills'
        if not skills_dir.exists():
            return {}

        skills = {}
        for skill_path in skills_dir.glob('*/skill.md'):
            try:
                content = skill_path.read_text()
                name = self._extract_skill_name(content, skill_path.parent.name)
                description = self._extract_skill_description(content)
                skills[name] = {
                    'path': skill_path,
                    'content': content,
                    'description': description,
                    'type': 'skill'
                }
            except Exception as e:
                print(f"  ⚠️  Error reading skill {skill_path.name}: {e}")
        return skills

    def _scan_mcp_servers(self):
        """Scan installed MCP servers."""
        mcp_dir = self.claude_config_dir / 'mcp_servers'
        if not mcp_dir.exists():
            return {}

        servers = {}
        for server_path in mcp_dir.glob('*/mcp-server.json'):
            try:
                content = server_path.read_text()
                config = json.loads(content)
                name = config.get('name', server_path.parent.name)
                servers[name] = {
                    'path': server_path,
                    'content': content,
                    'config': config,
                    'description': f"MCP Server: {name}",
                    'type': 'mcp'
                }
            except Exception as e:
                print(f"  ⚠️  Error reading MCP server {server_path.name}: {e}")
        return servers

    def _scan_commands(self):
        """Scan installed commands."""
        commands_dir = self.claude_config_dir / 'commands'
        if not commands_dir.exists():
            return {}

        commands = {}
        for cmd_path in commands_dir.glob('*/command.md'):
            try:
                content = cmd_path.read_text()
                name = self._extract_skill_name(content, cmd_path.parent.name)
                description = self._extract_skill_description(content)
                commands[name] = {
                    'path': cmd_path,
                    'content': content,
                    'description': description,
                    'type': 'command'
                }
            except Exception as e:
                print(f"  ⚠️  Error reading command {cmd_path.name}: {e}")
        return commands

    def _scan_hooks(self):
        """Scan installed hooks."""
        hooks_dir = self.claude_config_dir / 'hooks'
        if not hooks_dir.exists():
            return {}

        hooks = {}
        for hook_path in hooks_dir.glob('*/hook.sh'):
            name = hook_path.parent.name
            try:
                content = hook_path.read_text()
                hooks[name] = {
                    'path': hook_path,
                    'content': content,
                    'description': f"Hook: {name}",
                    'type': 'hook'
                }
            except Exception as e:
                print(f"  ⚠️  Error reading hook {hook_path.name}: {e}")
        return hooks

    def _extract_skill_name(self, content, fallback):
        """Extract skill name from frontmatter."""
        match = re.search(r'name:\s*["\']?([^"\']+)["\']?', content)
        return match.group(1) if match else fallback

    def _extract_skill_description(self, content):
        """Extract skill description from frontmatter."""
        match = re.search(r'description:\s*["\']([^"\']+)["\']', content)
        return match.group(1) if match else "No description"

    def _print_scanned_configs(self):
        """Print summary of scanned configurations."""
        total = 0
        for category, configs in self.scanned_configs.items():
            count = len(configs)
            total += count
            if count > 0:
                print(f"\n{category.title()} ({count}):")
                for name, config in configs.items():
                    desc = config.get('description', 'No description')
                    desc_short = desc[:60] + '...' if len(desc) > 60 else desc
                    print(f"  - {name}: {desc_short}")

        if total == 0:
            print("\n❌ No configurations found.")
        else:
            print(f"\n✓ Found {total} total configurations")

    def select_configurations(self):
        """Interactive selection of configurations to export."""
        print("\n📋 Select configurations to export:")
        print("Enter the numbers of items to select (comma-separated), or 'all' for all:")

        # Flatten all configurations into a list with indices
        all_configs = []
        category_map = []

        for category, configs in self.scanned_configs.items():
            if configs:
                category_map.append((category, list(configs.items())))
                print(f"\n{category.title()}:")
                for i, (name, config) in enumerate(configs.items(), 1):
                    all_configs.append((category, name, config))
                    print(f"  {len(all_configs)}. {name}")

        # Get user input
        while True:
            user_input = input("\nYour selection: ").strip()
            if not user_input:
                continue

            if user_input.lower() == 'all':
                # Select all configurations
                self.selected_configs = self.scanned_configs.copy()
                return self.selected_configs

            try:
                indices = [int(i.strip())-1 for i in user_input.split(',')]
                selected = {}

                for idx in indices:
                    if 0 <= idx < len(all_configs):
                        category, name, config = all_configs[idx]
                        if category not in selected:
                            selected[category] = {}
                        selected[category][name] = config

                if selected:
                    self.selected_configs = selected
                    return self.selected_configs
                else:
                    print("❌ No valid selections")
            except ValueError:
                print("❌ Invalid input. Please enter numbers separated by commas.")

    def filter_sensitive_info(self, config_name, mcp_config):
        """Filter sensitive information from MCP server config."""
        if 'env' not in mcp_config:
            return mcp_config, []

        filtered_env = {}
        sensitive_vars = []

        for key, value in mcp_config['env'].items():
            if self._is_sensitive_field(key):
                # Replace with environment variable placeholder
                filtered_env[key] = f"${{{key}:-}}"
                sensitive_vars.append({
                    'name': key,
                    'original_value': value,
                    'config': config_name
                })
            else:
                filtered_env[key] = value

        mcp_config['env'] = filtered_env
        return mcp_config, sensitive_vars

    def filter_sensitive_content(self, content, file_type, config_name):
        """Filter sensitive information from file content."""
        if not content:
            return content, []

        sensitive_vars = []
        lines = content.split('\n')
        filtered_lines = []

        for line in lines:
            # Look for patterns like KEY=value or export KEY=value
            matches = re.findall(r'(export\s+)?(\w+)=([\"\']?)([^\"\']+)([\"\']?)', line)
            for match in matches:
                prefix, key, quote_start, value, quote_end = match
                if self._is_sensitive_field(key):
                    # Replace sensitive value with placeholder
                    filtered_line = f"{prefix}{key}={quote_start}${{{key}:-}}{quote_end}"
                    filtered_lines.append(filtered_line)
                    sensitive_vars.append({
                        'name': key,
                        'original_value': value,
                        'config': config_name,
                        'file_type': file_type
                    })
                    break
            else:
                # No sensitive fields found in this line
                filtered_lines.append(line)

        # Also check for any base64 encoded content that might be sensitive
        base64_pattern = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'
        for i, line in enumerate(filtered_lines):
            if len(line) > 100 and re.match(base64_pattern, line.strip()):
                # This might be a sensitive token, replace with placeholder
                filtered_lines[i] = "[BASE64_CONTENT_FILTERED]"
                sensitive_vars.append({
                    'name': 'BASE64_CONTENT',
                    'original_value': line.strip(),
                    'config': config_name,
                    'file_type': file_type
                })

        return '\n'.join(filtered_lines), sensitive_vars

    def _is_sensitive_field(self, field_name):
        """Check if field name matches sensitive patterns."""
        field_upper = field_name.upper()
        for pattern in self.SENSITIVE_PATTERNS:
            if re.match(pattern, field_upper):
                return True
        return False

    def generate_id_from_name(self, name):
        """Convert name to kebab-case ID."""
        # Convert to lowercase, replace spaces/special chars with hyphens
        id_str = re.sub(r'[^a-zA-Z0-9]+', '-', name.lower())
        # Remove leading/trailing hyphens
        id_str = id_str.strip('-')
        return id_str

    def create_export_package(self, selections, mode='standalone'):
        """Create the export package."""
        print(f"\n📦 Creating export package...")

        # Create output directory structure
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / 'skills').mkdir(exist_ok=True)
        (self.output_dir / 'mcp_servers').mkdir(exist_ok=True)
        (self.output_dir / 'commands').mkdir(exist_ok=True)
        (self.output_dir / 'hooks').mkdir(exist_ok=True)

        # Generate config.yml
        config_data = self._generate_config_yml(selections)

        # Copy configuration files
        all_sensitive_vars = []
        for category, items in selections.items():
            for name, config in items.items():
                dest_dir = self.output_dir / category.rstrip('s') / name
                dest_dir.mkdir(exist_ok=True)

                if category == 'mcp_servers':
                    # Filter sensitive info from MCP configs
                    filtered_config, sensitive = self.filter_sensitive_info(name, config['config'].copy())
                    all_sensitive_vars.extend(sensitive)

                    # Write filtered mcp-server.json
                    with open(dest_dir / 'mcp-server.json', 'w') as f:
                        json.dump(filtered_config, f, indent=2)

                    # Copy install script if exists
                    install_script = config['path'].parent / 'install.sh'
                    if install_script.exists():
                        # Read and filter install script content
                        with open(install_script, 'r') as f:
                            script_content = f.read()
                        filtered_script, script_sensitive = self.filter_sensitive_content(script_content, 'bash_script', name)
                        all_sensitive_vars.extend(script_sensitive)

                        # Write filtered script
                        with open(dest_dir / 'install.sh', 'w') as f:
                            f.write(filtered_script)
                        os.chmod(dest_dir / 'install.sh', 0o755)
                else:
                    # Filter sensitive info from skill/command/hook files
                    with open(config['path'], 'r') as f:
                        file_content = f.read()

                    file_type = category.rstrip('s')
                    filtered_content, sensitive = self.filter_sensitive_content(file_content, file_type, name)
                    all_sensitive_vars.extend(sensitive)

                    # Write filtered file
                    with open(dest_dir / config['path'].name, 'w') as f:
                        f.write(filtered_content)

        # Write config.yml
        with open(self.output_dir / 'config.yml', 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)

        # Generate installer.py
        self._generate_installer_py()

        # Generate README.md
        self._generate_readme(all_sensitive_vars)

        # Generate .env.example
        self._generate_env_example(all_sensitive_vars)

        print(f"\n✓ Configuration exported to {self.output_dir}/")
        print("✓ Generated installer.py")
        print("✓ Generated config.yml")
        print("✓ Generated README.md")
        print("✓ Generated .env.example" if all_sensitive_vars else "  (No .env.example needed)")

        if all_sensitive_vars:
            print(f"\n⚠️  Filtered {len(all_sensitive_vars)} sensitive variable(s)")
            print("   See .env.example for required environment variables")

    def _generate_config_yml(self, selections):
        """Generate config.yml from selections."""
        config = {
            'project': {
                'name': 'Claude Code Config Export',
                'version': '1.0.0',
                'description': 'Exported Claude Code configurations',
                'exported_at': datetime.now().isoformat()
            },
            'categories': {}
        }

        category_map = {
            'skills': 'skills',
            'mcp_servers': 'mcp',
            'commands': 'commands',
            'hooks': 'hooks'
        }

        for source_cat, target_cat in category_map.items():
            items = selections.get(source_cat, {})
            if items:
                config['categories'][target_cat] = []
                for name, config_data in items.items():
                    entry_id = self.generate_id_from_name(name)
                    entry = {
                        'id': entry_id,
                        'name': name,
                        'description': config_data.get('description', ''),
                        'path': f"{source_cat.rstrip('s')}/{name}/{config_data['path'].name}",
                        'platforms': ['all'],
                        'dependencies': []
                    }
                    config['categories'][target_cat].append(entry)

        return config

    def _generate_installer_py(self):
        """Generate installer.py script."""
        installer_content = '''#!/usr/bin/env python3
"""
Claude Code Configuration Installer
Generated by Contribute Skill
"""

import os
import sys
import platform
import yaml
import shutil
from pathlib import Path

class ConfigInstaller:
    """Install Claude Code configurations."""

    def __init__(self):
        self.os_type = platform.system().lower()
        self.claude_config_dir = self._get_claude_config_dir()
        self.config = self._load_config()

    def _get_claude_config_dir(self):
        """Get Claude Code config directory."""
        if self.os_type == "windows":
            import os
            appdata = os.environ.get('APPDATA', '')
            return Path(appdata) / 'claude'
        else:
            return Path.home() / '.claude'

    def _load_config(self):
        """Load config.yml."""
        config_path = Path(__file__).parent / 'config.yml'
        if not config_path.exists():
            print("Error: config.yml not found")
            sys.exit(1)
        with open(config_path) as f:
            return yaml.safe_load(f)

    def install_all(self):
        """Install all configurations."""
        print("Installing all configurations...")
        categories = self.config.get('categories', {})

        for category, items in categories.items():
            for item in items:
                self._install_item(category, item)

        print("\\n✓ Installation complete!")
        print("Please restart Claude Code to load the new configurations.")

    def _install_item(self, category, item):
        """Install a single configuration item."""
        source_path = Path(__file__).parent / item['path']
        dest_path = self.claude_config_dir

        # Map category to destination subdirectory
        dest_map = {
            'skills': dest_path / 'skills' / item['id'],
            'mcp': dest_path / 'mcp_servers' / item['id'],
            'commands': dest_path / 'commands' / item['id'],
            'hooks': dest_path / 'hooks' / item['id']
        }

        dest_dir = dest_map.get(category, dest_path / category)
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Copy files
        if source_path.is_file():
            shutil.copy2(source_path, dest_dir / source_path.name)
            print(f"  ✓ Installed {item['name']}")
        elif source_path.is_dir():
            shutil.copytree(source_path, dest_dir, dirs_exist_ok=True)
            print(f"  ✓ Installed {item['name']}")

        # Make hooks executable
        if category == 'hooks':
            for hook_file in dest_dir.glob('*.sh'):
                os.chmod(hook_file, 0o755)

def main():
    """Main entry point."""
    installer = ConfigInstaller()
    installer.install_all()

if __name__ == '__main__':
    main()
'''
        with open(self.output_dir / 'installer.py', 'w') as f:
            f.write(installer_content)
        os.chmod(self.output_dir / 'installer.py', 0o755)

    def _generate_readme(self, sensitive_vars):
        """Generate README.md."""
        readme_content = f'''# Claude Code Configuration Export

导出的 Claude Code 配置集合。

导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 安装

```bash
# 运行安装脚本
python3 installer.py
```

安装完成后，请重启 Claude Code 以加载新配置。

## 配置说明

'''

        if sensitive_vars:
            readme_content += '### 需要配置环境变量的 MCP 服务器\n\n'
            readme_content += '以下 MCP 服务器需要配置环境变量才能正常工作：\n\n'

            # Group by config
            vars_by_config = {}
            for var in sensitive_vars:
                config = var['config']
                if config not in vars_by_config:
                    vars_by_config[config] = []
                vars_by_config[config].append(var['name'])

            for config, vars_list in vars_by_config.items():
                readme_content += f'#### {config}\n\n'
                readme_content += '```bash\n'
                for var_name in vars_list:
                    readme_content += f'export {var_name}=your_value_here\n'
                readme_content += '```\n\n'

        readme_content += f'''## 包含的配置

- **Skills**: {len(self.selected_configs.get('skills', {}))} 个
- **MCP Servers**: {len(self.selected_configs.get('mcp_servers', {}))} 个
- **Commands**: {len(self.selected_configs.get('commands', {}))} 个
- **Hooks**: {len(self.selected_configs.get('hooks', {}))} 个

## 注意事项

- ⚠️ 敏感信息已被替换为环境变量占位符
- ⚠️ 使用前请设置所需的环境变量
- ⚠️ 建议检查生成的配置文件是否符合需求
'''
        with open(self.output_dir / 'README.md', 'w') as f:
            f.write(readme_content)

    def _generate_env_example(self, sensitive_vars):
        """Generate .env.example file."""
        if not sensitive_vars:
            return

        # Get unique variable names
        unique_vars = {}
        for var in sensitive_vars:
            name = var['name']
            if name not in unique_vars:
                unique_vars[name] = var

        content = '# Environment Variables Example\n'
        content = '# Copy this file to .env and fill in your values\n\n'

        for var_name in sorted(unique_vars.keys()):
            content += f'{var_name}=\n'

        with open(self.output_dir / '.env.example', 'w') as f:
            f.write(content)

    def validate_export(self):
        """Validate the generated export package."""
        print("\n🔍 Validating export package...")

        errors = []

        # Check config.yml exists and is valid YAML
        config_path = self.output_dir / 'config.yml'
        if not config_path.exists():
            errors.append("config.yml not found")
        else:
            try:
                with open(config_path) as f:
                    config_data = yaml.safe_load(f)
                print("  ✓ config.yml is valid YAML")

                # Validate structure
                if 'categories' not in config_data:
                    errors.append("config.yml missing 'categories' section")
                else:
                    print("  ✓ config.yml has categories section")

                    # Validate each category entry
                    for category, items in config_data.get('categories', {}).items():
                        for item in items:
                            # Check required fields
                            required_fields = ['id', 'name', 'description', 'path']
                            for field in required_fields:
                                if field not in item:
                                    errors.append(f"{category}/{item.get('id', 'unknown')}: missing '{field}' field")

                            # Check file exists
                            file_path = self.output_dir / item['path']
                            if not file_path.exists():
                                errors.append(f"{category}/{item.get('id', 'unknown')}: file not found at {item['path']}")

                    print("  ✓ All config entries validated")

            except yaml.YAMLError as e:
                errors.append(f"config.yml is invalid YAML: {e}")

        # Check installer.py exists
        installer_path = self.output_dir / 'installer.py'
        if not installer_path.exists():
            errors.append("installer.py not found")
        else:
            print("  ✓ installer.py exists")

            # Try to import it to check for syntax errors
            try:
                with open(installer_path) as f:
                    code = f.read()
                compile(code, str(installer_path), 'exec')
                print("  ✓ installer.py has valid Python syntax")
            except SyntaxError as e:
                errors.append(f"installer.py has syntax error: {e}")

        # Check README.md exists
        readme_path = self.output_dir / 'README.md'
        if not readme_path.exists():
            errors.append("README.md not found")
        else:
            print("  ✓ README.md exists")

        # Validate directory structure
        expected_dirs = ['skills', 'mcp_servers', 'commands', 'hooks']
        for dir_name in expected_dirs:
            dir_path = self.output_dir / dir_name
            if not dir_path.exists():
                errors.append(f"{dir_name}/ directory not found")
            else:
                print(f"  ✓ {dir_name}/ directory exists")

        # Check that referenced files exist
        config_path = self.output_dir / 'config.yml'
        if config_path.exists():
            with open(config_path) as f:
                config_data = yaml.safe_load(f)

            for category, items in config_data.get('categories', {}).items():
                for item in items:
                    file_path = self.output_dir / item['path']
                    if file_path.exists():
                        # For MCP servers, validate JSON structure
                        if category == 'mcp' and file_path.name == 'mcp-server.json':
                            try:
                                with open(file_path) as f:
                                    mcp_config = json.load(f)
                                if 'name' not in mcp_config:
                                    errors.append(f"{item['id']}: mcp-server.json missing 'name' field")
                                if 'command' not in mcp_config:
                                    errors.append(f"{item['id']}: mcp-server.json missing 'command' field")
                            except json.JSONError as e:
                                errors.append(f"{item['id']}: mcp-server.json is invalid JSON: {e}")

        if errors:
            print("\n❌ Validation failed:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("\n✅ All validation checks passed!")
            return True

    def test_install(self, test_dir=None):
        """Test installation to a temporary directory."""
        import tempfile
        import subprocess

        if test_dir is None:
            test_dir = Path(tempfile.mkdtemp(prefix='claude-config-test-'))
        else:
            test_dir = Path(test_dir)

        print(f"\n🧪 Testing installation to {test_dir}/...")

        try:
            # Create a modified installer that installs to test directory
            test_installer = test_dir / 'test_installer.py'
            with open(self.output_dir / 'installer.py') as f:
                installer_code = f.read()

            # Override the config directory path
            modified_code = installer_code.replace(
                'return Path.home() / \'.claude\'',
                f'return Path("{test_dir}") / ".claude"'
            )
            modified_code = modified_code.replace(
                'return Path(appdata) / \'claude\'',
                f'return Path("{test_dir}") / "claude"'
            )

            with open(test_installer, 'w') as f:
                f.write(modified_code)

            # Copy config.yml to test directory
            shutil.copy2(self.output_dir / 'config.yml', test_dir / 'config.yml')

            # Copy configuration directories
            for dir_name in ['skills', 'mcp_servers', 'commands', 'hooks']:
                src = self.output_dir / dir_name
                if src.exists():
                    dst = test_dir / dir_name
                    shutil.copytree(src, dst)

            # Run the test installer
            result = subprocess.run(
                [sys.executable, str(test_installer)],
                cwd=test_dir,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("  ✓ Test installation succeeded")

                # Verify files were installed
                test_claude_dir = test_dir / '.claude'
                if test_claude_dir.exists():
                    installed_dirs = list(test_claude_dir.glob('*'))
                    print(f"  ✓ Installed {len(installed_dirs)} configuration directories")

                    # List installed configurations
                    for config_dir in installed_dirs:
                        if config_dir.is_dir():
                            config_count = len(list(config_dir.glob('*')))
                            print(f"    - {config_dir.name}: {config_count} file(s)")

                return True
            else:
                print("  ❌ Test installation failed")
                print(f"  Error: {result.stderr}")
                return False

        except Exception as e:
            print(f"  ❌ Test installation error: {e}")
            return False
        finally:
            # Clean up test directory
            if test_dir.exists():
                try:
                    shutil.rmtree(test_dir)
                    print(f"  ✓ Cleaned up test directory")
                except Exception as e:
                    print(f"  ⚠️  Could not clean up test directory: {e}")


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description='Export Claude Code configurations')
    parser.add_argument('--output', '-o', default='claude-config-export',
                       help='Output directory (default: claude-config-export)')
    parser.add_argument('--test', '-t', action='store_true',
                       help='Run test installation after export')
    parser.add_argument('--no-validate', action='store_true',
                       help='Skip validation')

    args = parser.parse_args()

    print("Claude Code Configuration Exporter")
    print("=" * 40)

    exporter = ConfigExporter(output_dir=args.output)

    # Scan configurations
    exporter.scan_configurations()

    # TODO: Add interactive selection logic
    # For now, just export everything found
    print("\n⚠️  Interactive selection not implemented in CLI mode")
    print("   Use /contribute skill in Claude Code for full functionality")

    # Export selected configurations
    if any(exporter.scanned_configs.values()):
        selected = exporter.select_configurations()
        if selected:
            exporter.create_export_package(selected)

        # Validate the export
        if not args.no_validate:
            if exporter.validate_export():
                print("\n✅ Export package is ready to share!")

                # Optionally test installation
                if args.test:
                    print("\nRunning test installation...")
                    if exporter.test_install():
                        print("\n✅ Test installation successful!")
                    else:
                        print("\n❌ Test installation failed")
            else:
                print("\n❌ Export package has errors. Please fix before sharing.")


if __name__ == '__main__':
    main()
