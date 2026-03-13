# Vue Chatbots

- [Streamlit](https://streamlit.io/)  
- [LlamaIndex](https://www.llamaindex.ai/)

Streamlit + LlamaIndex で、AI を利用した簡易的なアプリを作っています。  
何かしらの参考になれば幸いです。

## Vue Document Chat

しばらく前に vue.js の案件で開発していた際に、gemini または Copilot あたりに質問すると、古い情報ばかり拾ってきて話にならなかったという経緯があり、だったら自前で RAG を用意してやろうという事でこちらのアプリを作ったまでです。  
※ 無料版だから余計に嘘が多いのでしょうけど…。

結果として〇〇専用エージェントを自前で用意するのは、悪くないなという印象です。  
ただし、より精度を上げるためには良質なサンプルコードなども大量に必要であり、AI を利用しつつベストプラクティスとなるコードを大量に生産し、さらにそれを RAG として利用することで AI の推論の精度を上げていくといったサイクルが必要になるかと。  
これを実践できる開発会社、または個人は非常に強くなるかもしれません。  
※ Self-Improving RAG(自己改善型RAG)を目指すと良い結果が訪れるかも？

### 実装についてのポイント

RAG となるデータベースさえ用意できていれば、LlamaIndex の提供している高レベルAPIにて実装すれば、そこそこ満足する仕上がりになるような気がします。  
とはいえ、Streamlit というUIで表示する際は、アプリっぽい演出なども必要なのかと思われます。

- LLM への問い合わせを stream 実行させ、現在の状況を Streamlit 上に表示させ「思考してる感」を演出。
- あえて tool calling や Structured Output なども実装。
- RAG から参考にした文献のURLを別途表示。

といった小技も効かせています。  
基本的にはオーソドックスなチャットアプリになるので、LlamaIndex との相性も悪くないです。

当然ですが、RAG となるデータの鮮度を保つ必要があります。  
※ これもある程度自動化できそうな気がしている。

## Fortune(占い？)アプリ

<video src="https://github.com/user-attachments/assets/7e610716-f464-472b-9228-dc3a961f605a" controls></video>

エージェントを構成する際に、以下のポイントが重要になってきます。

- AI に自律的に思考させる。
- AI の要請にたいして人間が実行許可を与える(Human in the loop)。

LlamaIndex は Human in the loop(以下 HITL) に対応しており、実装自体は難しくありません。  
しかしながら、Streamlit の設計思想がこの HITL と相反するものであり、現時点では完全な実装が不可能という状況です。  

> Gemini 曰く「Streamlit はスクリプトを上から下まで再実行する（Rerun）というステートレスな設計思想であるため、AI が思考を中断して『人間の入力を待機（Block）』し、そこから『思考を再開』するというステートフルな HITL の制御フローを維持するのが極めて困難です。」とのこと。

しかしアプリの要件と設計次第では、Streamlit でも疑似的な HITL も実装出来そうな？モヤっとしたアイディアが頭浮かんで来たため、このアプリを作る次第になりました。  
※ 単純に HITL を実装して動かしてみたいなら marimo を使うと苦労しません。

### なぜ占い(診断)アプリなのか？

HITL が何故必要かと言えば、最終的に人間の判断を必要とする処理だから…といった要件が主流になるかと思われます。  
抽象的にこのフローを捉えると、人間が判定・入力した結果をLLMに渡すことで、引き続きAIに思考を委ねるといった事が目的になるわけです。  
そのサンプルケースとして以下のような事を考えたまでです。

- AI にお題に合わせて人間への質問を作らせる。
- tool calling を経由して人間の回答を待つ。
- 人間が回答した結果を LLM に渡し、必要であれば再度質問させる。
- お題の解決に必要な情報がそろったら診断結果を出す。

まず、AI にお題から質問を作ってもらうことで、AI の自律的な思考を優先させます。  
質問を必ず tool calling を経由して実行させます。これによりアプリ側はLLMからの回答をユーザへの質問であると判断できます。  
ユーザが質問に回答するという行為は HITL とも言えますが、実際のところはチャットに律儀に返答しただけとも言えます。  
ユーザの返答をAIに伝えることで、AIはお題の解決に臨みますが、まだ解決が出来ないと判断すれば再質問してきます。  
診断可能となると、最終的に診断結果を回答する(tool calling は利用しない)という流れになります。

といった流れをアプリにするために、「占い」でいいかと思ったわけですが、Gemini に「占い」を頼んだところ諸事情で断られたので、「診断」という言い方に変わりました。  
こういったセーフティフィルタ的な実装は、いついかなるタイミングで実装されるのか不明ですが、プロンプトの調整でなんとかなる場合もあるようです。

### 実装のポイント

Streamlit 設計思想のおかけで、何かしら入力を受け付ける際は、必ず LLM との通信も完全に停止させる必要があります。  
通常のチャットであれば...

- ユーザの入力
- AI の回答
- ユーザの入力
- AI の回答
- ...ループ

といった整然としたフローの繰り返しとなるため、履歴さえ保存していれば引き続きチャットを再開するのは容易です。  
疑似的な HIHL では...

- アプリからお題を提供
- AI が tool calling を使って質問を投げてくる
- ここで AI エージェントを強制停止して、ユーザに質問を投げて入力を求める。
- ユーザの回答を使って、AI に再度お題を提供
- 情報が足りなければ、AIは再度tool calling を使って質問を投げてくる
- ここで AI エージェントを強制停止して、ユーザに質問を投げて入力を求める。
- ユーザの回答を使って、AI に再度お題を提供
- 情報が足りるとAIはお題に対する回答を生成して返す。
- 診断結果をユーザに表示する。

これも整然とした流れではあるものの、いくつかの問題点が出てきます。

- AI は tool calling 経由での人間の回答を直接受け取れない。
- LlamaIndex の処理フローを強制的に停止すること、そもそも tool calling がチャットではないため履歴管理の対象にならない。
- 結果として自前で履歴管理しつつ、AI に質問内容をその解答を伝える必要が生じる。

まず第1に、tool calling の途中で のAI エージェントのフローを強制停止するのも割と難儀である。  
通常の tool calling では、ここでレスポンスを返すことで AI は思考を続けてくれるわけですが、AIに「ちょっと待ってください！」と返したところで、待ってくれるわけではありません。  
したがって tool calling の関数 `ask_user` ではいきなり例外を投げます。  

```python
# fortune/agent/functions.py
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
```

LlamaIndex は tool calling からの例外をキャッチして、まるで何事もなかったかのようにスルーしてしまいます。  
これは LlamaIndex の堅牢性の一つなので、むしろ歓迎すべき機能ですが、このケースではこれが足かせになります。
そのためにイベントループの中で無理矢理この例外への参照を試みます。

```python
# fortune/agent/workflow.py
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
```

ポイントは `_event` が ToolCallResult の場合に `tool_output` というプロパティが定義されており、この `tool_output` が ToolOutput モデルであるという事です。  
この ToolOutput モデルには `is_error` や `exception` というプロパティがあり、この値から投げられた例外クラスの参照が可能になっています。  
これを解析するのはなかなか厄介でしたが、わかってしまえばあとは stream から例外を投げてエラーを発生させフローを強制停止、InputRequiredEvent を返して次のステップへ遷移させます。  
※ APIリファレンスなどでも詳しく書かれてないようなので、本家のAIチャットに相談しつつ、ソースコードの解析が必要です。  
あとはダイアログでユーザの入力を待つだけです。

続いて入力結果をどうやってAIに伝えるか？です。  
これを解決するために、tool calling での質問と回答を疑似的にチャット履歴として AI に伝えるという手段を取っています。  

```python
# fortune/agent/workflow.py

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
```

「お題」を履歴の先頭に配置して、tool calling の質問と回答を生成します。  
要するに内部的にはチャットしているのとほぼ同じと言えますが、今回のケースではこれで正解かと思います。

少々ややこしいですが、tool calling からの疑似的な HITL は、なんとかなりました。 

### LLMのスペック

このアプリにおいて、LLMとのチャットの内容は単純ではあるのですが、ユーザへの質問を tool calling 経由で実行させる事、履歴からすでに質問した内容を読み取らせて「質問への回答済」であることを理解させる事の２点に関しては、軽量レベルのモデルでは不可能なようでした。  
軽量モデルでは文脈が長くなるほど、命令を無視しやすくなるという傾向があるため、期待した結果にはなりませんでした。  
gemini-3.1-flash-lite-preview 以上で、ようやく期待した結果となり、そこそこ安定して動作します。  
それでも時々質問を tool calling ではなくチャットのレスポンスとして返すこともしばしば発生するので、本番運用？するのであれば、そこそこのモデルを選択しつつ、保険として回答結果がそれらしいものかどうかを再度AIに問い合わせるなど、より繊細な処理フリーも必要になるかと思います。  
※ Self-Correction（自己修正）、Output Validation と呼ばれる構成。

## Streamlit の所感

アプリの基本設計の思想がかえって潔く、小さい使い捨てアプリを大量かつスピーディに作成するのに向いていると思いました。  
非エンジニア系の営業職さんから、AIを使って何かしたいというアイディアがあれば、即座に対応できそうな気がします。  
非常ににシンプルであるので、道具(データや実行環境)さえ揃ってしまえば、それこそバイブコーディングだけで完成品に近いものが作成出来そうです。  

基本思想としてコードの上から下まで再実行するという動きなるため、ステートの管理がキモになります。  
もう少し高度なアプリを作成する場合は、ステート管理クラスを用意して、ステート(フラグ)に対して1つの動作が動き、処理が完了したら別のステートへ遷移させるという流れ(ステートマシン)を作れば、保守性が保たれる気がしました。

とはいえ、web socket を使っているのであれば、Human in the loop へのネイティブな対応を期待したいところです。

## Environment

wsl2 + uv で仮想環境を構築しています。  
問題がなければ Python3.14.x を利用しますが、AI 関連では 3.14 対応が少々遅いようなので注意して下さい。

```bash
# 初期化
uv init
# venv の作成
uv venv --python 3.14
# パッケージのインストール
uv sync
```

### LLM

メインとなる LLM として Gemini を採用しています。  
気軽に無料枠を試せるという点もありますが、AI 関連の開発をするのに料金体系が優しめであるという理由での選定です。  
アプリでは `.env` で API キーを参照しています。

```dotenv
GOOGLE_API_KEY="Google AI Studio で発行できる API キーを指定"
```

ローカルPC上の Ollama でも色々と試してみましたが、Tool Calling などでの実行確実性が低いため、Gemini 等のAIサービスを使う方が圧倒的に安定します。  
※ 利用するモデルにも依存する。

### その他構成

Vue.js のドキュメントを Tool Calling 経由で RAG として提供する土台として、Qdarnt を採用しています。  
web アプリのダッシュボードがついているので、登録されたデータの中身を見るのに便利です。  
その際に embedding では Ollama を利用して必要以上の課金を抑えています。

- [Ollama](https://docs.ollama.com/)
- [Qdrant](https://qdrant.tech/documentation/)

## アプリの起動

Streamlit のアプリ起動は以下の手順です。

```bash
# vue document chat
uv run --env-file .env streamlit run vuechat/main.py
# fortune app
uv run --env-file .env streamlit run fortune/main.py
```
