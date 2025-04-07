import streamlit as st
from openai import OpenAI

# --------------------- 应用界面 ---------------------
st.title("📄 Document question answering (DeepSeek)")
st.write("Upload a document below and ask a question – DeepSeek will answer!")

# 初始化客户端
client = OpenAI(
    api_key="sk-c958fbee89374324ab74f6b56301322f",
    base_url="https://api.deepseek.com/v1"
)

# --------------------- 核心逻辑 ---------------------
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)",
    type=("txt", "md")
)

question = st.text_area(
    "Ask a question about the document:",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file
)

if uploaded_file and question:
    try:
        # 读取文档内容
        document = uploaded_file.read().decode()
        
        # 构建消息
        messages = [{
            "role": "user",
            "content": f"Document Content:\n{document}\n\n---\n\nQuestion: {question}"
        }]

        # 流式调用
        with st.spinner("DeepSeek is thinking..."):
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=True,
            )
            st.write_stream(stream)

    except Exception as e:
        st.error(f"❌ 发生错误: {str(e)}")