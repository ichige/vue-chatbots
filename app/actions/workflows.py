import streamlit as st

def workflows_run(key: str):
    """
    AIへ問い合わせる
    """
    prompt = st.session_state[key]
    st.session_state.messages.append({"role": "user", "content": prompt})
    # TODO: LLM実行
    response = f"あなたの質問は  でしたね？"
    st.session_state.messages.append({"role": "assistant", "content": response})