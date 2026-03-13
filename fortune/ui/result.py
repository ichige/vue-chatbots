import streamlit as st
import time

def render_result():
    """
    診断結果をタイプライター的に表示
    """
    st.write_stream(_stream_data)

def _stream_data():
    """
    診断結果を1文字ずつ出力
    """
    result = st.session_state.result
    for char in result:
        yield char
        time.sleep(0.02)
