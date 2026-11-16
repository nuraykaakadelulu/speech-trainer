from google import genai
from google.genai import types
import streamlit as st

st.set_page_config(
    page_title="AI Speaking & Fluency Tutor", page_icon="🎓", layout="centered"
)
st.title("🎓 AI Speaking, Vocabulary & Fluency Tutor")
st.write(
    "Practice speaking, ask for vocabulary alternatives, check your phrasing,"
    " or request feedback!"
)

try:
  client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

  # Расширенный промпт: теперь ИИ оценивает беглость, лексику и помогает с разговорной практикой
  SYSTEM_PROMPT = """
    You are an expert, encouraging, and interactive English Language Coach and Teacher for high school students. 
    Your goal is to help students improve their speaking fluency, lexical diversity (expanding vocabulary), and structural accuracy.
    
    Rules for your responses:
    1. Always keep a warm, supportive, and engaging tone. Avoid dry or robotic textbook answers.
    2. If the user writes a practice sentence or a speaking snippet, evaluate it: point out strong vocabulary (lexical diversity), gently correct any grammar mistakes, and suggest a more natural/advanced alternative phrasing.
    3. Always end your response with a short, engaging follow-up question or a quick speaking challenge to keep the student practicing.
    4. Use structured bullet points for readability.
    """

  if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

  for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  if user_input := st.chat_input(
      "Type your sentence, question, or speaking practice here..."
  ):
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
      st.markdown(user_input)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[msg["content"] for msg in st.session_state.chat_history],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT, temperature=0.7
        ),
    )

    ai_reply = response.text
    st.session_state.chat_history.append(
        {"role": "assistant", "content": ai_reply}
    )
    with st.chat_message("assistant"):
      st.markdown(ai_reply)

except Exception as e:
  st.error(
      "Please configure your GEMINI_API_KEY in Streamlit Secrets to start the"
      " chat."
  )
