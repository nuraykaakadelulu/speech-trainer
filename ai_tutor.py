
import streamlit as st
from google import genai
from google.genai import types

# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="AI Speaking Tutor",
    page_icon="🎓",
    layout="centered"
)

# -----------------------------
# SYSTEM PROMPT
# -----------------------------

SYSTEM_PROMPT = """
You are an expert, friendly and encouraging English Language Coach
for high school students.

Your goal is to help students improve:
- Speaking fluency
- Vocabulary
- Grammar
- Pronunciation knowledge
- Natural English expressions

Rules:
1. Always be friendly and supportive.
2. Correct grammar mistakes gently.
3. Explain mistakes in simple English.
4. Suggest more advanced vocabulary.
5. Give natural alternative expressions.
6. Encourage students to speak more.
7. Always finish with a follow-up question.
8. Use clear bullet points.
9. Adapt your English to the student's level.
"""

# -----------------------------
# TITLE
# -----------------------------

st.title("🎓 AI Speaking, Vocabulary & Fluency Tutor")

st.write(
    "Practice speaking, learn new vocabulary, "
    "improve your grammar and become more fluent in English!"
)

st.divider()

# -----------------------------
# API KEY
# -----------------------------

if "GEMINI_API_KEY" not in st.secrets:
    st.error("GEMINI_API_KEY is missing!")
    st.info("Please add your API key in Streamlit Secrets.")
    st.stop()

API_KEY = st.secrets["GEMINI_API_KEY"]

# -----------------------------
# CHAT HISTORY
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# DISPLAY OLD MESSAGES
# -----------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------

user_input = st.chat_input(
    "Type your sentence, question, or speaking practice here..."
)

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Prepare conversation history
    history = [
        types.Content(
            role="user" if msg["role"] == "user" else "model",
            parts=[types.Part(text=msg["content"])]
        )
        for msg in st.session_state.messages
    ]

    # -----------------------------
    # GEMINI RESPONSE
    # -----------------------------

    with st.chat_message("assistant"):

        try:
            with st.spinner("Your AI tutor is thinking..."):

                # Create a new API client
                client = genai.Client(
                    api_key=API_KEY,
                    http_options=types.HttpOptions(
                        timeout=60000
                    )
                )

                # Main model and alternatives
                models = [
                    "gemini-3.8-flash",
                    "gemini-3.7-flash",
                    "gemini-3.6-flash",
                    "gemini-3.5-flash"
                ]

                response = None
                last_error = None

                # Try available models
                for model_name in models:

                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=history,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                max_output_tokens=700,
                                temperature=0.7
                            )
                        )

                        if response.text:
                            break

                        last_error = RuntimeError(
                            "The model returned an empty response."
                        )
                        response = None

                    except Exception as e:
                        last_error = e
                        response = None

                        error_text = str(e).upper()

                        if (
                            "503" in error_text
                            or "UNAVAILABLE" in error_text
                        ):
                            continue

                        raise

                # Check response
                if response is None or not response.text:
                    raise RuntimeError(
                        f"All models failed. Last error: {last_error}"
                    )

                answer = response.text

                # Display answer
                st.markdown(answer)

                # Save answer
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

        except Exception as e:

            st.error("Sorry! Gemini could not generate a response.")

            st.code(
                f"{type(e).__name__}: {e}"
            )

            st.info(
                "Please check your API key, model availability "
                "and internet connection."
            )

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header("🎓 Speaking Tutor")

    st.write("Your personal English learning assistant.")

    st.divider()

    st.subheader("Practice topics")

    st.write("""
    - 🗣️ Speaking practice
    - 📚 Vocabulary building
    - ✍️ Grammar correction
    - 💬 Natural expressions
    - 🎯 Fluency improvement
    """)

    st.divider()

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by Google Gemini AI")
