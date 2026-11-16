import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="AI Speaking, Vocabulary & Fluency Tutor",
    page_icon="🎓",
    layout="centered",
)

# Настраиваем ключ (работает со всеми форматами: и AIza..., и AQ...)
if "GEMINI_API_KEY" in st.secrets:
  genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🎓 AI Speaking, Vocabulary & Fluency Tutor")
st.write(
    "Practice speaking, ask for vocabulary alternatives, check your phrasing,"
    " or request feedback!"
)

SYSTEM_PROMPT = """
You are an expert, encouraging, and interactive English Language Coach and Teacher for high school students. 
Your goal is to help students improve their speaking fluency, lexical diversity (expanding vocabulary), and structural accuracy.

Rules for your responses:
1. Always keep a warm, supportive, and engaging tone. Avoid dry or robotic textbook answers.
2. If the user writes a practice sentence or a speaking snippet, evaluate it: point out strong vocabulary (lexical diversity), gently correct any grammar mistakes, and suggest a more natural/advanced alternative phrasing.
3. Always end your response with a short, engaging follow-up question or a quick speaking challenge to keep the student practicing.
4. Use structured bullet points for readability.
"""

# Используем стандартную модель через проверенный интерфейс чата
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=SYSTEM_PROMPT,
)

if "chat" not in st.session_state:
  st.session_state.chat = model.start_chat(history=[])

# Отображаем историю
for message in st.session_state.chat.history:
  role = "user" if message.role == "user" else "assistant"
  with st.chat_message(role):
    st.markdown(message.parts[0].text)

if user_input := st.chat_input(
    "Type your sentence, question, or speaking practice here..."
):
  with st.chat_message("user"):
    st.markdown(user_input)

  with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
      response = st.session_state.chat.send_message(user_input)
      st.markdown(response.text)
