import streamlit as st

@st.dialog(title="Confirm", icon=":material/info:")
def render_confirm_dialog(message:str):
    """
    確認ダイアログ
    """
    st.write(message)
    with st.container(horizontal=True):
        if st.button(label="OK"):
            st.session_state.confirm = True
            st.rerun()
        if st.button(label="Cancel"):
            st.session_state.confirm = False
            st.rerun()
