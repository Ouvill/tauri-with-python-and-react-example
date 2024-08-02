# Tauri + React + Typescript

プロジェクトの作成。今回作成するプロジェクト名は`tauri-with-python-and-react`とする。

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
