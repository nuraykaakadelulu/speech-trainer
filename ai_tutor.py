import os
from google import genai
from google.genai import types
import streamlit as st

st.set_page_config(page_title="AI English Tutor", page_icon="🎓")
st.title("🎓 AI Speaking & Grammar Tutor")
st.write(
    "Ask any questions about grammar, vocabulary, or speaking strategies!"
)

# Подключаем API-ключ из секретов Streamlit
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Инструкция-характер для ИИ-учителя
SYSTEM_PROMPT = """
You are an encouraging, patient, and professional English teacher (CEFR B2-C1 level).
Your task is to help high school students overcome speaking anxiety, expand lexical diversity, and fix grammar mistakes.
Rules:
1. Keep explanations clear, concise, and structured with bullet points.
2. Never just give a dry answer — give 1-2 natural speaking examples and ask a short follow-up question to keep the student practicing.
3. If the student writes a sentence with a mistake, gently correct it and explain why.
"""

# Инициализация истории чата в памяти браузера
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Выводим предыдущие сообщения
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Поле ввода вопроса
if user_input := st.chat_input("Ask your question here..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Формируем запрос с историей и ролью учителя
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[msg["content"] for msg in st.session_state.chat_history],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
        ),
    )

    ai_reply = response.text
    st.session_state.chat_history.append(
        {"role": "assistant", "content": ai_reply}
    )
    with st.chat_message("assistant"):
        st.markdown(ai_reply)
