import streamlit as st
from .histories import reset_chat_histories

def prepare():
    """
    初期準備
    特にセッションのキーはここで明示的に初期化することで、後方で存在確認が省ける。
    しかしどのキーが存在し、その型まではIDEも把握されないので、アプリが大きくなったら管理クラスが必要になるだろう。
    """
    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    # confirm ダイアログの初期化
    if "confirm" not in st.session_state:
        st.session_state["confirm"] = False
    # chat context
    if "chat_ctx" not in st.session_state:
        st.session_state["chat_ctx"] = {}
    # 質問入力値
    if "input_prompt" in st.session_state:
        st.session_state["input_prompt"] = ""

    # 会話のリセット
    reset_chat_histories()