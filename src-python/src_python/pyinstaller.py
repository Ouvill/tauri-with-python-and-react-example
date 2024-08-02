import PyInstaller.__main__
from pathlib import Path
import subprocess
import re
import sys
import argparse
from typing import Optional

# Constants for file paths and application name
CURRENT_SCRIPT_PATH = Path(__file__).resolve()
MAIN_FILE = CURRENT_SCRIPT_PATH.parent / 'main.py'
PROJECT_ROOT = CURRENT_SCRIPT_PATH.parent.parent.parent
DIST_DIR = PROJECT_ROOT / 'src-tauri' / 'binaries'
APP_NAME = "python-app"

def get_target_triple() -> str:
    """
    Get the current platform's target triple using rustc.
    This is necessary for Tauri's sidecar naming convention.
    """
    result = subprocess.run(["rustc", "-vV"], capture_output=True, text=True)
    output = result.stdout.strip()
    match = re.search(r'host: (\S+)', output)
    if not match:
        raise ValueError('Failed to determine platform target triple')
    return match.group(1)

def get_extension() -> str:
    """
    Get the appropriate file extension based on the operating system.
    Windows executables need '.exe', while other platforms don't.
    """
    return '.exe' if sys.platform.startswith('win') else ''


def get_builded_app_name(base_name: str, target: str, extension: str) -> str:
    """
    Generate the final name for the built application.
    This follows Tauri's sidecar naming convention: {name}-{target_triple}{extension}
    """
    return f'{base_name}-{target}{extension}'

# PyInstallerの実行
def build(target: Optional[str] = None):
    """
    Build the Python application using PyInstaller.
    If no target is specified, it uses the current platform's target triple.
    """
    target = target or get_target_triple()
    extension = get_extension()
    builded_name = get_builded_app_name(APP_NAME, target, extension)

    PyInstaller.__main__.run([
        str(MAIN_FILE),
        "--distpath" , str(DIST_DIR),
        "--onefile",
        "--name", str(builded_name),
        "--console"
    ])

    print(f"Built {builded_name}")

def parse_args():
    parser = argparse.ArgumentParser(description="Build script for PyInstaller")
    parser.add_argument("--target", help="Specify the target triple (e.g., x86_64-apple-darwin)")
    return parser.parse_args()

def main():
    """
    Main function to parse command line arguments and start the build process.
    """
    args = parse_args()
    build(args.target)

if __name__ == '__main__':
  main()
