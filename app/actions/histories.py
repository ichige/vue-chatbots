import streamlit as st

def reset_chat_histories():
    """
     チャット履歴のリセット
    """
    if st.session_state.confirm:
        st.session_state.messages = []
        st.session_state.confirm = False
