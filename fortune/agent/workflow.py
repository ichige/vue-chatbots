import asyncio
import streamlit as st
from workflows import (
    Workflow,
    step
)
from workflows.events import (
    InputRequiredEvent,
    StartEvent,
    StopEvent
)

from llama_index.core.llms import ChatMessage
from .agents import function_agent
from .exceptions import InputRequiredException
from ui.dialog import render_input_dialog

class FortuneFlow(Workflow):
    """
    占い Workflow
    """

    @step
    async def fortune_telling(self, event: StartEvent) -> StopEvent|InputRequiredEvent:
        """
        LLMに問い合わせを実行する
        """
        agent = function_agent()
        # QAの履歴を追加する。
        user_massage = st.session_state.user_massage
        chat_histories = [
            ChatMessage(
                role="user",
                content=user_massage
            )
        ]
        additional_messages = st.session_state.additional_messages
        for message in additional_messages:
            chat_histories.append(ChatMessage(
                role="assistant",
                content=message.get("assistant"),
            ))
            chat_histories.append(ChatMessage(
                role="user",
                content=message.get("user"),
            ))

        try:
            handler = agent.run(chat_history=chat_histories)
            async for _event in handler.stream_events():
                # tool で発生したエラーイベントの購読
                if hasattr(_event, "tool_output") and _event.tool_output.is_error:
                    print(f"エラー発生やで？ {_event.tool_output.tool_name}")
                    # ask_user 関数がコールされた場合は例外を投げて、render_dialog ステップへ遷移させる。
                    if _event.tool_output.tool_name == 'ask_user':
                        raise _event.tool_output.exception

            result = await handler
            return StopEvent(result=str(result))
        except Exception as e:
            if isinstance(e, InputRequiredException):
                # noinspection PyArgumentList
                return InputRequiredEvent(**e.to_dict())
            raise e

    @step
    async def render_dialog(self, event: InputRequiredEvent) -> StopEvent:
        """
        入力ダイアログの表示
        """
        render_input_dialog(**event.to_dict())
        return StopEvent(result="")

async def main() -> str:
    """
    LLM問い合わせ実行非同期処理
    """
    w = FortuneFlow()
    result = await w.run()
    return result

def agent_workflow_run():
    """
    AgentWorkflow を非同期実行する
    """
    st.session_state.app_run = True
    result = asyncio.run(main())
    if result:
        # セッションの初期化
        st.session_state.additional_messages = []
        st.session_state.workflow_run = False
        # 結果の表示
        st.session_state.result = result
        st.rerun()
