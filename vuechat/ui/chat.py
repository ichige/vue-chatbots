import streamlit as st
from .dialog import render_confirm_dialog

def render_chat_histories():
    """
    session に保存されているチャット履歴を表示
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"])
            else:
                st.markdown(message["content"]["text"])
                if message["content"]["doc_urls"]:
                    st.divider()
                    st.caption("参考リンク:")
                    for url in message["content"]["doc_urls"]:
                        st.markdown(f"[{url}]({url})")

def render_chat_input():
    """
    チャット入力を表示
    """
    prompt = st.chat_input(
        placeholder="質問を入力してください",
    )
    st.session_state.input_prompt = prompt

def render_reset_btn():
    """
    チャット履歴のリセット
    """
    if len(st.session_state.messages) > 0:
        with st.container(horizontal=True):
            st.space("stretch")
            reset_btn = st.button(
                label="",
                type="secondary",
                icon=":material/delete:",
                on_click=render_confirm_dialog,
                args=["会話をリセットしますか？"]
            )