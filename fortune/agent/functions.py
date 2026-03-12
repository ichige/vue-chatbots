from pydantic import BaseModel, Field
from llama_index.core.tools import FunctionTool
from .exceptions import InputRequiredException

class AskUserArgs(BaseModel):
    question: str = Field(description="ユーザーに提示する具体的で親身な質問文。1回につき1項目のみ。")
    label: str = Field(description="入力フォームに表示する短いラベル（例: '性格', '住環境'）")

async def ask_user(question: str, label:str = "入力ラベル", **kwargs):
    """
    ユーザーに不足している情報を1つだけ質問し、入力を求めるための『唯一の』手段です。
    テキストで回答を生成する代わりに、この関数を呼び出してください。

    Args:
        question (str): ユーザーに提示する質問文。（例：「休日はどのように過ごすことが多いですか？」）
        label (str): 入力欄のラベル（例：「休日の過ごし方」）
    """
    print("call ask_user")
    # ダイアログの表示のために例外を投げます。
    raise_exception(question, label)

def ask_user_tool() -> FunctionTool:
    """
    ユーザの情報を取得するためのツール
    """
    return FunctionTool.from_defaults(
        async_fn=ask_user,
        fn_schema=AskUserArgs,
        name="ask_user",
        description="ユーザーに不足している情報を1つだけ質問し、入力を求めるための『唯一の』手段です。テキストで回答を生成する代わりに、この関数を呼び出してください。"
    )

def raise_exception(question: str, label: str):
    raise InputRequiredException(
        name="ask_user",
        label=label,
        message=question,
        placeholder=""
    )