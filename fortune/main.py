import streamlit as st
from agent import agent_workflow_run
from ui import (
    render_result,
    render_sidebar,
    render_title,
)


#
# session の初期化
#

# 診断中フラグ
if "app_run" not in st.session_state:
    st.session_state.app_run = False
# AgentWorkflow の再実行フラグ
if "workflow_run" not in st.session_state:
    st.session_state.workflow_run = False
# QAの履歴
if "additional_messages" not in st.session_state:
    st.session_state.additional_messages = []
# 診断コンテンツの選択値
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "犬"
# LLMへの問い合わせ prompt
if "user_massage" not in st.session_state:
    st.session_state.user_massage = ""
# LLM への問い合わせ結果
if "result" not in st.session_state:
    st.session_state.result = None

# サイドバー
render_sidebar()

# title
render_title()

# 診断ボタン押下で AgentWorkflow をキック
if not st.session_state.app_run:
    if st.button(label="診断"):
        agent_workflow_run()

# rerun で AgentWorkflow をキック
if st.session_state.workflow_run:
    agent_workflow_run()

# 結果表示
if st.session_state.result:
    render_result()
    st.session_state.result = None

# リセットボタン
if st.session_state.app_run:
    if st.button(label="リセット"):
        st.session_state.app_run = False
        st.rerun()