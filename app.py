# 以下を「app.py」に書き込み
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
import secret_keys  # 外部ファイルにAPI keyを保存

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
os.environ["OPENAI_API_KEY"] = st.secrets.OpenAIAPI.openai_api_key

chat = ChatOpenAI(model="gpt-3.5-turbo")

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
            SystemMessage(
                content="あなたは優秀なアシスタントAIです。"
                )
        ]

# LLMとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = HumanMessage(
        content=st.session_state["user_input"]
    )

    messages.append(user_message)
    response = chat(messages)
    messages.append(response)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("LangChainを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message.type == "ai":
            speaker="🤖"

        st.write(speaker + ": " + message.content)
