import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AI Speaking Tutor",
    page_icon="🎓",
    layout="centered"
)

SYSTEM_PROMPT = """
You are a friendly and professional English speaking tutor.

Your tasks:
1. Correct grammar mistakes.
2. Explain vocabulary.
3. Suggest more natural and advanced expressions.
4. Improve speaking fluency.
5. Encourage students.
6. Always finish with a follow-up question.
7. Use clear bullet points.
"""

st.title("🎓 AI Speaking, Vocabulary & Fluency Tutor")

st.write(
    "Practice speaking, ask for vocabulary alternatives, "
    "check your phrasing, or request feedback!"
)

if "GEMINI_API_KEY" not in st.secrets:
    st.error("API key is missing. Check Streamlit Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
user_input = st.chat_input(
    "Type your sentence, question, or speaking practice here..."
)

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):

        try:
            with st.spinner("AI is thinking..."):

                # Prepare conversation
                history = [
                    types.Content(
                        role=(
                            "user"
                            if msg["role"] == "user"
                            else "model"
                        ),
                        parts=[
                            types.Part(text=msg["content"])
                        ]
                    )
                    for msg in st.session_state.messages
                ]

                # Create a fresh client for this request
                with genai.Client(
                    api_key=st.secrets["GEMINI_API_KEY"],
                    http_options=types.HttpOptions(
                        timeout=30000,
                        retry_options=types.HttpRetryOptions(
                            attempts=1
                        )
                    )
                ) as client:

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=history,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            max_output_tokens=700,
                            temperature=0.7
                        )
                    )

                answer = response.text

                if not answer:
                    answer = (
                        "I couldn't generate a text response. "
                        "Please try again."
                    )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

        except Exception as e:
            st.error(
                "Sorry! Something went wrong while connecting "
                "to Gemini."
            )
            st.code(f"{type(e).__name__}: {e}")
            st.info(
                "Please check your API key, model access "
                "and internet connection."
            )
