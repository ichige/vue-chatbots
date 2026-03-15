import streamlit as st

app_modes = [
    {
        "value": "犬",
        "title": ":dog: ワンコ相性診断",
        "prompt": "私と相性の良さそうな犬種を選んでください。"
    },
    {
        "value": "お菓子",
        "title": ":chocolate_bar: お菓子相性診断",
        "prompt": "私と相性の良さそうな市販のお菓子を選んでください。"
    },
    {
        "value": "料理",
        "title": ":pizza: お料理相性診断",
        "prompt": "私と今日の健康と相性の良さそうな料理を選んでください。"
    }
]

def render_title():
    """
    動的にタイトルを変更する
    """
    app_mode = st.session_state.app_mode
    target = next((mode for mode in app_modes if mode["value"] == app_mode))
    # prompt を保存しておく。
    st.session_state.user_massage = target["prompt"]

    # 描画
    st.title(target["title"])