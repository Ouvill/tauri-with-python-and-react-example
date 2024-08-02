import PyInstaller.__main__
from pathlib import Path
import subprocess
import re
import sys
import argparse
from typing import Optional

current_script_path = Path(__file__).resolve()
main_file = current_script_path.parent / 'main.py'
project_root = current_script_path.parent.parent.parent
dist_dir = project_root / 'src-tauri' / 'binaries'
app_name = "python-app"

# Rustのターゲットトリプルを取得する
def get_target_triple() -> str:
    result = subprocess.run(["rustc", "-vV"], capture_output=True, text=True)
    output = result.stdout.strip()
    # Process the output as needed
    match = re.search(r'host: (\S+)', output)
    if not match:
        raise ValueError('Failed to determine platform target triple')
    target_triple = match.group(1)
    return target_triple

# OSによって拡張子を取得する.
def get_extension():
    return '.exe' if sys.platform.startswith('win') else ''

# ビルドされたアプリ名を取得する
def get_builded_app_name(base_name: str, target: str, extension: str):
    return f'{base_name}-{target}{extension}'

# PyInstallerの実行
def build(target: Optional[str] = None):
    if target is None:
        target = get_target_triple()

    extension = get_extension()
    builded_name = get_builded_app_name(app_name, target, extension)

    PyInstaller.__main__.run([
        str(main_file),
        "--distpath" , str(dist_dir),
        "--onefile",
        "--name", str(builded_name),
        "--console"
    ])

    print(f"Built {builded_name}")

def main():
    parser = argparse.ArgumentParser(description="Build script for PyInstaller")
    parser.add_argument("--target", help="Specify the target triple (e.g., x86_64-apple-darwin)")
    args = parser.parse_args()

    build(args.target)

if __name__ == '__main__':
  main()
