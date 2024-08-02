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
