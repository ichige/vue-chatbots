import streamlit as st

@st.dialog("AIからの質問")
def render_input_dialog(**kwargs) -> None:
    """
    AIからの質問をを入力させるダイアログを表示
    """
    st.write(kwargs.get("message", "message"))
    name = st.text_input(
        label=kwargs.get("label", "label"),
        placeholder=kwargs.get("placeholder", "")
    )
    if st.button("送信"):
        print(name)
        if name:
             # QA 履歴に書き込み
            st.session_state.additional_messages.append(f"""
            ** QA **
Q. {kwargs.get("message", "message")}
A. {name}
            """.strip())
        # Workflow 再起動フラグ
        st.session_state.workflow_run = True
        # dialog から抜けるには rerun が必要。
        st.rerun()