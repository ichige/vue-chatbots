import streamlit as st

def render_sidebar():
    st.sidebar.title(":material/settings: Configure")
    with st.sidebar:
        # Gemini のモデル選択
        # 一部モデルに deep thinking が利用できる。
        gemini_model = st.selectbox(
            label="Select gemini models",
            options=[
                "gemini-3.1-pro-preview",
                "gemini-3.1-flash-lite-preview",
                "gemini-flash-latest",
                "gemini-flash-lite-latest",
                "gemini-2.5-pro",
            ],
            key="gemini_model",
            index=3,
        )

        # deep thinking
        deep_thinking = st.toggle(
            label="Deep Thinking",
            key="deep_thinking_on",
            disabled=(gemini_model not in ["gemini-3.1-pro-preview", "gemini-3.1-flash-lite-preview"])
        )