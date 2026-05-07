import streamlit as st
from openai import OpenAI
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import settings

st.set_page_config(page_title="LLM Chat", page_icon="💬", layout="centered")
st.title("💬 LLM 对话")

query_params = st.experimental_get_query_params()
ai_token = query_params.get("token", [""])[0]

with st.sidebar:
    st.subheader("API 配置")
    api_key = st.text_input(
        "API Key",
        value=settings.INSIGHT_ENGINE_API_KEY or "",
        type="password",
        placeholder="请输入 API Key",
    )
    base_url = st.text_input(
        "Base URL",
        value=settings.INSIGHT_ENGINE_BASE_URL or "https://api.openai.com/v1",
        placeholder="https://api.openai.com/v1",
    )
    model_name = st.text_input(
        "Model Name",
        value=settings.INSIGHT_ENGINE_MODEL_NAME or "gpt-3.5-turbo",
        placeholder="gpt-3.5-turbo",
    )

    st.divider()

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful assistant.",
        placeholder="设置系统提示词...",
    )

    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    top_p = st.slider("Top P", 0.0, 1.0, 1.0, 0.05)

    if st.button("清空对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("请输入你的问题...")

if user_input:
    if not api_key:
        st.error("请在侧边栏填写 API Key")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    client = OpenAI(api_key=api_key, base_url=base_url)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                stream = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.messages,
                    ],
                    temperature=temperature,
                    top_p=top_p,
                    stream=True,
                )

                placeholder = st.empty()
                full_response = ""
                for chunk in stream:
                    if chunk.choices and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if delta and delta.content:
                            full_response += delta.content
                            placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)

                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

                escaped_content = json.dumps(full_response, ensure_ascii=False)
                escaped_token = json.dumps(ai_token, ensure_ascii=False)
                st.components.v1.html(f"""
                <div style="display:flex;justify-content:flex-end;margin-top:12px">
                  <button onclick="sendArticle()" style="padding:10px 20px;background:#e6a23c;color:white;border:none;border-radius:6px;cursor:pointer;font-size:14px;font-weight:600">
                    ✉️ 确认收取这篇文章
                  </button>
                </div>
                <script>
                function sendArticle() {{
                  var content = {escaped_content};
                  var token = {escaped_token};
                  if (window.top.opener) {{
                    window.top.opener.postMessage({{
                      type: 'ai_article',
                      token: token,
                      content: content
                    }}, '*');
                  }} else {{
                    alert('未找到父窗口。请从文章编辑页面（localhost:5173）打开此AI助手。');
                  }}
                }}
                </script>
                """, height=60)
            except Exception as e:
                st.error(f"请求失败: {str(e)}")
