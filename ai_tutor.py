from google import genai
from google.genai import types
import os
import streamlit as st

st.set_page_config(
    page_title="AI Speaking Tutor", page_icon="🎓", layout="centered"
)

if "GEMINI_API_KEY" not in st.secrets:
  st.error("GEMINI_API_KEY is missing in Streamlit Secrets!")
  st.stop()

# Передаем ключ в среду
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# Инициализируем клиент в режиме Vertex AI для ключей AQ...
# Если потребуется проект, можно указать project="твой-проект" и location="us-central1"
try:
  client = genai.Client(vertexai=True)
except Exception:
  client = genai.Client()

st.title("🎓 AI Speaking, Vocabulary & Fluency Tutor")
st.write(
    "Practice speaking, learn new vocabulary, improve your grammar and"
    " become more fluent in English!"
)

SYSTEM_PROMPT = """
You are an expert, friendly and encouraging English Language Coach for high school students. 
Your goal is to help students improve their speaking fluency, vocabulary, and grammar.
Rules:
1. Be friendly and supportive.
2. Gently correct grammar mistakes.
3. Suggest advanced vocabulary.
4. Always finish with a short follow-up question.
5. Use clear bullet points.
"""

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if user_input := st.chat_input(
    "Type your sentence, question, or speaking practice here..."
):
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  with st.chat_message("assistant"):
    with st.spinner("Your AI tutor is thinking..."):
      try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nStudent says: {user_input}"
        response = client.models.generate_content(
            model="gemini-1.5-flash", contents=full_prompt
        )
        answer = response.text
      except Exception as e:
        answer = (
            "✨ That's a great sentence! To sound even more natural, try"
            f" incorporating richer vocabulary. (Note: {e})"
        )

      st.markdown(answer)
      st.session_state.messages.append(
          {"role": "assistant", "content": answer}
      )

with st.sidebar:
  st.header("🎓 Speaking Tutor")
  st.write("Your personal English learning assistant.")
  st.divider()
  if st.button("🗑️ Clear conversation"):
    st.session_state.messages = []
    st.rerun()
  st.caption("Powered by Google Gemini AI")
