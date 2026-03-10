import streamlit as st
from actions.prepare import prepare
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

# チャット履歴のリセット

# チャット履歴を表示
render_chat_histories()

# リセットボタンを表示
render_reset_btn()

# ユーザの質問待ち
render_chat_input()