import PyInstaller.__main__
from pathlib import Path
import subprocess
import re
import sys

current_script_path = Path(__file__).resolve()
main_file = current_script_path.parent / 'main.py'
project_root = current_script_path.parent.parent.parent
dist_dir = project_root / 'src-tauri' / 'binaries'
app_name = "python-app"

# tauriのsidecarに対応するために、target tripleを取得する
def get_app_name_with_target_triple():
    result = subprocess.run(["rustc", "-vV"], capture_output=True, text=True)
    output = result.stdout.strip()
    # Process the output as needed
    match = re.search(r'host: (\S+)', output)
    if not match:
        raise ValueError('Failed to determine platform target triple')
    target_triple = match.group(1)

    extension = '.exe' if sys.platform.startswith('win') else ''
    return f'{app_name}-{target_triple}{extension}'

# PyInstallerの実行
def build():
    app_name_with_target_triple = get_app_name_with_target_triple()

    PyInstaller.__main__.run([
        str(main_file),
        "--distpath" , str(dist_dir),
        "--onefile",
        "--name", str(app_name_with_target_triple),
        "--console"
    ])

    print(f"Built {app_name_with_target_triple}")
