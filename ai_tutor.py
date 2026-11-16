import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AI Speaking Tutor",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI Speaking, Vocabulary & Fluency Tutor")

st.write(
    "Practice speaking, ask for vocabulary alternatives, "
    "check your phrasing, or request feedback!"
)

SYSTEM_PROMPT = """
You are an expert, encouraging, and interactive English Language Coach
and Teacher for high school students.

Rules:
1. Always use a warm, supportive and engaging tone.
2. Correct grammar mistakes gently.
3. Explain strong vocabulary and suggest advanced alternatives.
4. Help students improve speaking fluency and accuracy.
5. Always finish with a short follow-up question or speaking challenge.
6. Use structured bullet points.
"""

# Check API key
if "GEMINI_API_KEY" not in st.secrets:
    st.error("GEMINI_API_KEY is missing in Streamlit Secrets!")
    st.stop()

# Connect to Gemini
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# Create chat session
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )

# Display chat history
for message in st.session_state.chat.get_history():
    role = "user" if message.role == "user" else "assistant"

    with st.chat_message(role):
        if message.parts:
            st.markdown(message.parts[0].text or "")

# User input
if user_input := st.chat_input(
    "Type your sentence, question, or speaking practice here..."
):
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(
                    user_input
                )
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
