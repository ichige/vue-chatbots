import asyncio
import streamlit as st
from llama_index.core import (
    Settings,
    set_global_handler
)
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context

def workflows_run():
    """
    AIへ問い合わせる
    """
    if prompt := st.session_state.input_prompt:
        # ユーザの質問を表示
        with st.chat_message("user"):
            st.markdown(prompt)
        # セッションへ保存
        st.session_state.messages.append({"role": "user", "content": prompt})

        # LLM に問い合わせ
        with st.status("思考中...") as status:
            response = assistant_run(prompt)
            status.update(label="完了", state="complete")

        # 解答を表示
        with st.chat_message("assistant"):
            st.markdown(response)
        # セッションへ保存
        st.session_state.messages.append({"role": "assistant", "content": response})

def assistant_run(query: str):
    """
    Gemini に問い合わせをする
    """
    from llms import (
        chat_agent,
        gemini
    )

    # state
    model = st.session_state.gemini_model
    deep_thinking = st.session_state.deep_thinking_on
    chat_ctx = st.session_state.chat_ctx

    print(f"""
MODEL: {model}
DEEP_THINKING: {deep_thinking}
""")

    # Base Model
    Settings.llm = gemini(model=model, deep_thinking=deep_thinking)
    set_global_handler("simple")

    # Agent
    agent = chat_agent()
    # Chat Context
    ctx = Context.from_dict(workflow=agent, data=chat_ctx)

    # run
    text = asyncio.run(_run(agent, query, ctx))

    # Save Chat Context
    st.session_state.chat_ctx = ctx.to_dict()
    return text

async def _run(agent: FunctionAgent, user_msg: str, ctx: Context) -> str:
    """
    問い合わせ非同期処理
    """
    result = await agent.run(
        user_msg=user_msg,
        ctx=ctx,
        max_iterations=5
    )
    return str(result)
