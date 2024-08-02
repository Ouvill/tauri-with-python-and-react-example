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

HERE = Path(__file__).parent.absolute()
path_to_main = HERE / "main.py"

def build():
    PyInstaller.__main__.run([
        str(path_to_main),
        "--onefile",
        "--name", "myapp",
        "--console"
    ])
```

poetryにビルドスクリプトを追加する。

`pyproject.toml`

```toml
[tool.poetry.scripts]
build = "src_python.pyinstaller:build"
```

ビルドスクリプトを実行する。

```bash
poetry run build
```

ビルドが成功すると、`dist`フォルダーに`myapp`という実行ファイルが生成される。
