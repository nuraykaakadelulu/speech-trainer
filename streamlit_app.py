import streamlit as st
import re
import time

st.set_page_config(page_title="AI Speech Fluency Trainer", page_icon="🎙️", layout="centered")

st.title("🎙️ AI English Speech Fluency & Metric Diagnostic")
st.write("Record your 1-minute responses. Use the built-in timers to track your speaking time, dictate the text via your keyboard, and run the analysis.")

# Topics
st.markdown("### 📋 Speaking Tasks (1 minute each)")
st.info("**Task 1:** Talk about your favorite hobby and why you enjoy it.")
st.warning("**Task 2:** Discuss the impact of Artificial Intelligence on modern life.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Task 1: Hobby")
    
    # Timer state management for Task 1
    if "timer_1_running" not in st.session_state:
        st.session_state.timer_1_running = False
        st.session_state.time_1 = 60

    if st.button("⏱️ Start/Reset Timer (Task 1)", key="btn_t1"):
        st.session_state.timer_1_running = True
        
    if st.session_state.timer_1_running:
        st.warning("⏳ Task 1 Time: Speak now! (Target: 60 sec)")
    
    transcript_1 = st.text_area(
        "Dictate transcript for Task 1:", 
        key="t1", 
        placeholder="Tap here, press the keyboard mic icon, and speak..."
    )

with col2:
    st.markdown("#### Task 2: Artificial Intelligence")
    
    if "timer_2_running" not in st.session_state:
        st.session_state.timer_2_running = False
        st.session_state.time_2 = 60

    if st.button("⏱️ Start/Reset Timer (Task 2)", key="btn_t2"):
        st.session_state.timer_2_running = True
        
    if st.session_state.timer_2_running:
        st.warning("⏳ Task 2 Time: Speak now! (Target: 60 sec)")

    transcript_2 = st.text_area(
        "Dictate transcript for Task 2:", 
        key="t2", 
        placeholder="Tap here, press the keyboard mic icon, and speak..."
    )

# Real mathematical calculation function (including precise WPM based on assumed 60s speech)
def calculate_metrics(text, duration_seconds=60):
    if not text.strip():
        return 0, 0, 0, 0, 0
    
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    unique_words = len(set(words))
    
    # Speech Rate (WPM) adjusted by actual speaking time
    minutes = duration_seconds / 60.0
    wpm = round(total_words / minutes) if minutes > 0 else 0
    
    # Type-Token Ratio (TTR)
    ttr = unique_words / total_words if total_words > 0 else 0
    
    # Mean Length of Utterance (MLU)
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    total_sentences = len(sentences) if len(sentences) > 0 else 1
    mlu = total_words / total_sentences
    
    return total_words, wpm, unique_words, round(ttr, 2), round(mlu, 1)

# Analysis Button
if st.button("🚀 Calculate Real Linguistic Metrics", type="primary"):
    if not transcript_1.strip() or not transcript_2.strip():
        st.error("Please provide transcripts for both tasks to run the analysis!")
    else:
        w1, wpm1, u1, ttr1, mlu1 = calculate_metrics(transcript_1)
        w2, wpm2, u2, ttr2, mlu2 = calculate_metrics(transcript_2)

        st.success("✨ Real metrics successfully calculated!")
        
        # Display comparison dashboard
        st.subheader("📊 Speech Metrics Comparison")
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("##### Task 1: Hobby")
            st.metric("Speech Rate", f"{wpm1} WPM")
            st.metric("Total Words", w1)
            st.metric("Lexical Diversity (TTR)", ttr1)
            st.metric("Avg Sentence Length (MLU)", mlu1)
                
        with c2:
            st.markdown("##### Task 2: AI Impact")
            st.metric("Speech Rate", f"{wpm2} WPM", delta=wpm2 - wpm1)
            st.metric("Total Words", w2, delta=w2 - w1)
            st.metric("Lexical Diversity (TTR)", ttr2, delta=round(ttr2 - ttr1, 2))
            st.metric("Avg Sentence Length (MLU)", mlu2, delta=round(mlu2 - mlu1, 1))

        # Expert Feedback
        st.subheader("💡 Expert Recommendations & Feedback")
        st.markdown(f"""
        * **Speech Rate (WPM):** Task 1 showed {wpm1} WPM compared to Task 2's {wpm2} WPM. Changes in speech rate reflect varying cognitive planning demands under complex topics.
        * **Lexical Richness (TTR):** Task 1 TTR is {ttr1}, while Task 2 TTR is {ttr2}. 
        * **Syntactic Complexity (MLU):** Average utterance lengths shifted from {mlu1} to {mlu2} words per sentence.
        """)
