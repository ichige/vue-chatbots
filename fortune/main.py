import streamlit as st
from agent import agent_workflow_run

st.title("ワンコ 占い :dog:")

#
# session の初期化
#

# AgentWorkflow の再実行フラグ
if "workflow_run" not in st.session_state:
    st.session_state.workflow_run = False
# QAの履歴
if "additional_messages" not in st.session_state:
    st.session_state.additional_messages = []
    print("init additional_messages")

# 占うボタン押下で AgentWorkflow をキック
if st.button(label="占う"):
    agent_workflow_run()

# rerun で AgentWorkflow をキック
if st.session_state.workflow_run:
    agent_workflow_run()