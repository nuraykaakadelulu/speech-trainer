
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AI Speaking Tutor",
    page_icon="🎓",
    layout="centered"
)

SYSTEM_PROMPT = """
You are an expert, encouraging and interactive English Language Coach
for high school students.

Rules:
1. Always be warm, supportive and engaging.
2. Correct grammar mistakes gently.
3. Explain strong vocabulary and suggest advanced alternatives.
4. Help students improve speaking fluency and accuracy.
5. Always finish with a short follow-up question or speaking challenge.
6. Use structured bullet points.
"""

st.title("🎓 AI Speaking, Vocabulary & Fluency Tutor")

st.write(
    "Practice speaking, ask for vocabulary alternatives, "
    "check your phrasing, or request feedback!"
)

# Get API key
if "GEMINI_API_KEY" not in st.secrets:
    st.error("GEMINI_API_KEY is missing!")
    st.stop()

# Create and cache Gemini client
@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)

client = get_client(st.secrets["GEMINI_API_KEY"])

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input(
    "Type your sentence, question, or speaking practice here..."
):

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                # Convert conversation history
                history = [
                    types.Content(
                        role="user" if m["role"] == "user" else "model",
                        parts=[types.Part(text=m["content"])]
                    )
                    for m in st.session_state.messages
                ]

                # Generate AI response
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=history,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    )
                )

                answer = response.text

                if not answer:
                    raise ValueError("Gemini returned an empty response.")

                st.markdown(answer)

                # Save AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Gemini error: {e}")
