import streamlit as st

def render_sidebar():
    """
    サイドバーの描画
    """
    with st.sidebar:
        st.write(":material/settings: Configure")
        app_run = st.session_state.app_run
        app_mode = st.radio(
            label="相性診断コンテンツ",
            options=["犬", "お菓子", "料理"],
            index=0,
            key="app_mode",
            disabled=(app_run == True),
        )