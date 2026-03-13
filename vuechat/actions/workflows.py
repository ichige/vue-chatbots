import asyncio
import streamlit as st
import time
from streamlit.elements.lib.mutable_status_container import StatusContainer
from llama_index.core import (
    Settings,
    set_global_handler
)
from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    AgentStream,
    FunctionAgent,
    ToolCall,
    ToolCallResult
)
from llama_index.core.workflow import Context
from llms import (
    chat_agent,
    gemini,
    ChatResponse
)

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
            response = assistant_run(prompt, status)
            status.update(label="完了", state="complete")

        def response_generator():
            """
            Response を1行ずつ出力する
            """
            for line in response.text.splitlines(keepends=True):
                yield line
                time.sleep(0.05)

        # 解答を表示
        with st.chat_message("assistant"):
            st.write_stream(stream=response_generator)

        # 参考リンク
        if response.doc_urls:
            st.divider()
            st.caption("参考リンク:")
            for url in response.doc_urls:
                st.markdown(f"[{url}]({url})")

        # セッションへ保存
        st.session_state.messages.append({"role": "assistant", "content": { "text": response.text, "doc_urls": response.doc_urls }})

def assistant_run(query: str, status: StatusContainer) -> ChatResponse:
    """
    Gemini に問い合わせをする
    """
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
    result = asyncio.run(_run(agent, query, ctx, status))

    # Save Chat Context
    st.session_state.chat_ctx = ctx.to_dict()

    # 結果が構造化ではない場合、ChatResponse とならない場合もある。
    model = result.get_pydantic_model(ChatResponse)

    try:
        assert isinstance(model, ChatResponse)
        return model
    except Exception as e:
        return ChatResponse(text=str(result), doc_urls=[])


async def _run(agent: FunctionAgent, user_msg: str, ctx: Context, status: StatusContainer) -> AgentOutput:
    """
    問い合わせ非同期処理
    """
    handler = agent.run(
        user_msg=user_msg,
        ctx=ctx,
        max_iterations=5
    )

    # Streamを実況する
    async for event in handler.stream_events():
        if isinstance(event, ToolCall):
            status.update(label=f"{event.tool_name} calling...", state="running")
        if isinstance(event, ToolCallResult):
            status.update(label=f"{event.tool_name} returning...", state="running")
        if isinstance(event, AgentInput):
            status.update(label=f"{event.current_agent_name} input...", state="running")
        if isinstance(event, AgentOutput):
            status.update(label=f"{event.current_agent_name} output...", state="running")
        if isinstance(event, AgentStream):
            status.update(label="streaming now...", state="running")

    result: AgentOutput = await handler
    return result
