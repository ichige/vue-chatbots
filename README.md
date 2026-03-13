# Vue Chatbots

> - [Streamlit](https://streamlit.io/)  
> - [LlamaIndex](https://www.llamaindex.ai/)

Streamlit + LlamaIndex で、AI を利用した簡易的なアプリを作っています。  
何かしらの参考になれば幸いです。

## Virtual Environment

wsl2 + uv で仮想環境を構築しています。  
問題がなければ Python3.14.x を利用しますが、AI 関連では 3.14 対応が少々遅いようなので注意して下さい。

```bash
# 初期化
uv init
# venv の作成
uv venv --python 3.14
# パッケージのインストール
uv sync
```

## アプリの起動

```bash
# vue document chat
uv run --env-file .env streamlit run vuechat/main.py
# fortune app
uv run --env-file .env streamlit run fortune/main.py
```
