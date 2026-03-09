import streamlit as st

st.title("Vue.js Chatbot")

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# チャット履歴を表示
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザの質問待ち
if prompt := st.chat_input("質問を入力してください"):

    st.chat_message("user", avatar="user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"あなたの質問は {prompt} でしたね？"
    with st.chat_message("assistant", avatar="assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})