import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# .env の読み込み
load_dotenv()

# OpenAI APIキーを環境変数から取得
api_key = os.getenv("OPENAI_API_KEY")

# LangChainのLLMモデル設定
llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")

# --- Streamlit Webアプリ ---
st.title("💬 LLMアプリ")
st.write("テキストを入力し、専門家の種類を選択すると、その専門家になりきった回答が返ってきます。")

# ラジオボタンで専門家を選択
role = st.radio("専門家を選んでください:", ["医者", "歴史学者"])

# 入力フォーム
user_input = st.text_input("質問を入力してください:")

def get_llm_response(user_text, role):
    """ユーザーの入力と専門家の役割を受け取り、LLMからの回答を返す"""
    if role == "医者":
        system_message = SystemMessage(content="あなたは優秀な医者です。専門的かつわかりやすく回答してください。")
    elif role == "歴史学者":
        system_message = SystemMessage(content="あなたは知識豊富な歴史学者です。歴史的な背景も交えて説明してください。")
    else:
        system_message = SystemMessage(content="あなたは親切なアシスタントです。")

    messages = [
        system_message,
        HumanMessage(content=user_text)
    ]

    response = llm.invoke(messages)
    return response.content

# 送信ボタンが押されたら処理
if st.button("送信"):
    if user_input.strip():
        answer = get_llm_response(user_input, role)
        st.write("### 回答:")
        st.write(answer)
    else:
        st.warning("テキストを入力してください。")
