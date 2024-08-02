# Tauri + React + Typescript

プロジェクトの作成。今回作成するプロジェクト名は`tauri-with-python-and-react`とする。

tauriのsidecarにpythonを追加する。

```bash
$ pnpm create tauri-app
✔ Project name · tauri-with-python-and-react
✔ Choose which language to use for your frontend · TypeScript / JavaScript - (pnpm, yarn, npm, bun)
✔ Choose your package manager · pnpm
✔ Choose your UI template · React - (https://react.dev/)
✔ Choose your UI flavor · TypeScript

Template created! To get started run:
  cd tauri-with-python-and-react
  pnpm install
  pnpm tauri dev
```

プロジェクトフォルダーに移動

cd `tauri-with-python-and-react`

依存パッケージのダウンロード

```bash
pnpm install
```

tauriの起動

```bash
pnpm tauri dev
```

pythonのプロジェクトを追加する。pythonのプロジェクト管理にはpoetryを採用する。

```bash
poetry new src-python
```

`src-python/src_python/main.py`を以下のように作成

```python
print("Hello from Python!")
```

pythonをビルドするためにpyinstallerをインストール。

互換性の問題を回避するためにpythonのバージョンを`pyproject.toml`に記述する。

```toml
[tool.poetry.dependencies]
python = ">=3.12,<3.13"
```

pyinstallerのビルドスクリプトを作成する。

`src-python/src_python/pyinstaller.py`

```python
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
```

poetryにビルドスクリプトを追加する。

`pyproject.toml`

```toml
[tool.poetry.scripts]
build = "src_python.pyinstaller:build"
```

ビルド

```bash
poetry run build
```

ビルドが成功すると、`src-tauri/binaries`フォルダーに`python-app-x86_64-unknown-linux-gnu`のようなファイルが作成される。windowsやmacは別の名前になる。
