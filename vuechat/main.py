import streamlit as st
from actions import (
    prepare,
    workflows_run
)
from ui import (
    render_chat_histories,
    render_chat_input,
    render_sidebar,
    render_reset_btn,
)

st.title(":green[Vue.js] :orange[C]hatbot :cow:")

# アプリの準備
prepare()

# sidebar
render_sidebar()

# チャット履歴を表示
render_chat_histories()

# ユーザの質問欄を表示
render_chat_input()

# LLM問い合わせ処理
workflows_run()

# リセットボタンを表示
render_reset_btn()