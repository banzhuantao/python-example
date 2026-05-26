import streamlit as st
# import os
# from openai import OpenAI
import ollama

# 或者直接访问响应对象的字段
# print(response.message.content)

# Streamlit应用配置：设置页面标题、图标、布局和侧边栏状态
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🍑",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={}
)

# 设置应用主标题
st.title("AI智能伴侣")

# 设置应用Logo
st.logo("resource/logo.jpg")

client = ollama.Client(host="http://localhost:11434")

# 系统提示词
system_prompt = "你是一个可爱的智能助手，请你使用可爱的语气回答我的问题。"

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示聊天记录
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 创建聊天输入框
prompt = st.chat_input("请输入你的问题：")
if prompt:
    st.chat_message("user").write(prompt)
    # 保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat(
        model='deepseek-r1:1.5b',
        messages=[
            {'role': 'system', 'content': system_prompt},
            *st.session_state.messages
        ],
        stream=False,
    )
    st.chat_message("assistant").write(response.message.content)
    st.session_state.messages.append({"role": "assistant", "content": response.message.content})

    # 打印响应内容
    # print(response['message']['content'])
    print(st.session_state.messages)
