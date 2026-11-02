import streamlit as st
import re

st.set_page_config(page_title="AI Speech Fluency Trainer", page_icon="🎙️", layout="centered")

st.title("🎙️ AI English Speech Fluency & Metric Diagnostic")
st.write("Complete the speaking tasks below. Tap the microphone icon on your tablet keyboard to dictate your speech, then click calculate!")

# Topics
st.markdown("### 📋 Speaking Tasks (1 minute each)")
st.info("**Task 1:** Talk about your favorite hobby and why you enjoy it.")
st.warning("**Task 2:** Discuss the impact of Artificial Intelligence on modern life.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Task 1: Hobby")
    transcript_1 = st.text_area(
        "Enter or dictate transcript for Task 1:", 
        key="t1", 
        placeholder="Tap the text box, press the mic icon on your keyboard, and speak your answer..."
    )

with col2:
    st.markdown("#### Task 2: Artificial Intelligence")
    transcript_2 = st.text_area(
        "Enter or dictate transcript for Task 2:", 
        key="t2", 
        placeholder="Tap the text box, press the mic icon on your keyboard, and speak your answer..."
    )

# Real mathematical calculation function
def calculate_metrics(text):
    if not text.strip():
        return 0, 0, 0, 0
    
    # Extract words using regex
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    unique_words = len(set(words))
    
    # Type-Token Ratio (TTR) - Lexical Diversity
    ttr = unique_words / total_words if total_words > 0 else 0
    
    # Mean Length of Utterance (MLU) - Sentence complexity
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    total_sentences = len(sentences) if len(sentences) > 0 else 1
    mlu = total_words / total_sentences
    
    return total_words, unique_words, round(ttr, 2), round(mlu, 1)

# Analysis Button
if st.button("🚀 Calculate Real Linguistic Metrics", type="primary"):
    if not transcript_1.strip() or not transcript_2.strip():
        st.error("Please provide transcripts for both tasks to run the analysis!")
    else:
        # Calculate real metrics based on actual input
        w1, u1, ttr1, mlu1 = calculate_metrics(transcript_1)
        w2, u2, ttr2, mlu2 = calculate_metrics(transcript_2)

        st.success("✨ Real metrics successfully calculated from your text!")
        
        # Display comparison dashboard
        st.subheader("📊 Speech Metrics Comparison")
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("##### Task 1: Hobby")
            st.metric("Total Words", w1)
            st.metric("Unique Words", u1)
            st.metric("Lexical Diversity (TTR)", ttr1)
            st.metric("Avg Sentence Length (MLU)", mlu1)
                
        with c2:
            st.markdown("##### Task 2: AI Impact")
            st.metric("Total Words", w2, delta=w2 - w1)
            st.metric("Unique Words", u2, delta=u2 - u1)
            st.metric("Lexical Diversity (TTR)", ttr2, delta=round(ttr2 - ttr1, 2))
            st.metric("Avg Sentence Length (MLU)", mlu2, delta=round(mlu2 - mlu1, 1))

        # Dynamic expert feedback based on math results
        st.subheader("💡 Expert Recommendations & Feedback")
        
        ttr_diff = round(ttr2 - ttr1, 2)
        if ttr_diff > 0:
            feedback_ttr = f"Your lexical diversity (TTR) increased by {ttr_diff} in the complex topic, showing advanced vocabulary usage!"
        elif ttr_diff < 0:
            feedback_ttr = f"Your TTR decreased slightly by {abs(ttr_diff)} in the second task. Try incorporating more diverse academic vocabulary."
        else:
            feedback_ttr = "Your lexical diversity remained stable across both tasks."

        st.markdown(f"""
        * **Lexical Sophistication (TTR):** {feedback_ttr} (Task 1: {ttr1} vs Task 2: {ttr2}).
        * **Structural Complexity (MLU):** Your average sentence length changed from {mlu1} to {mlu2} words per sentence.
        * **Actionable Advice:** When discussing complex concepts like Artificial Intelligence, balance your sentence structures and use advanced cohesive devices to ensure smooth delivery.
        """)
