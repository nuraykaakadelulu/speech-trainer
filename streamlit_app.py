import streamlit as st
import time

st.set_page_config(page_title="AI Speech Fluency Trainer", page_icon="🎙️", layout="centered")

st.title("🎙️ English Speech Fluency & Metric Diagnostic")
st.write("Record your speech on two different topics to get detailed metrics, comparison, and professional improvement advice.")

# Topics
st.markdown("### 📋 Speaking Tasks (1 minute each)")
st.info("**Task 1 (Basic):** Talk about your favorite hobby and why you enjoy it.")
st.warning("**Task 2 (Advanced):** Discuss a significant challenge you faced recently and how it changed your perspective.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Recording 1 (Hobby)")
    audio_file_1 = st.audio_input("Record Audio 1", key="audio_1")

with col2:
    st.markdown("#### Recording 2 (Complex Topic)")
    audio_file_2 = st.audio_input("Record Audio 2", key="audio_2")

# Analysis Button
if st.button("🚀 Run Speech Analysis", type="primary"):
    if not audio_file_1 or not audio_file_2:
        st.error("Please record both audio tasks before running the analysis!")
    else:
        with st.spinner("Analyzing speech rate, pauses, and lexical metrics..."):
            time.sleep(3) # Simulation of processing
            
            # Simulated metrics based on academic framework
            metrics_1 = {
                "Speech Rate (WPM)": 118,
                "Mean Length of Utterance (MLU)": 7.5,
                "Lexical Diversity (TTR)": 0.64,
                "Filled Pauses (um, uh)": 3,
                "Phonation Time Ratio": "80%"
            }
            
            metrics_2 = {
                "Speech Rate (WPM)": 96,
                "Mean Length of Utterance (MLU)": 9.2,
                "Lexical Diversity (TTR)": 0.81,
                "Filled Pauses (um, uh)": 8,
                "Phonation Time Ratio": "66%"
            }

        st.success("✨ Analysis successfully completed!")
        
        # Display comparison
        st.subheader("📊 Speech Metrics Comparison")
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("##### Task 1: Hobby")
            for k, v in metrics_1.items():
                st.metric(label=k, value=v)
                
        with c2:
            st.markdown("##### Task 2: Advanced Topic")
            for k, v in metrics_2.items():
                st.metric(label=k, value=v, delta="-22 WPM (higher cognitive load)" if k == "Speech Rate (WPM)" else None)

        # AI Feedback & Recommendations
        st.subheader("💡 Expert Recommendations & Feedback")
        st.markdown("""
        * **Lexical Sophistication:** Your **TTR (Type-Token Ratio)** increased significantly in the second task, demonstrating a rich and diverse vocabulary choice for advanced topics.
        * **Fluency & Hesitations:** Under increased cognitive pressure in Task 2, the number of filled pauses and silent intervals grew. This is a common adjustment pattern.
        * **Actionable Advice:** To minimize pauses when switching to complex topics, practice utilizing transitional discourse markers (e.g., *«From my perspective...», «Despite the complexity...»*). This grants your cognitive processing extra time without relying on filler words.
        """)
