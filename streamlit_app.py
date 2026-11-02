import streamlit as st
import streamlit.components.v1 as components
import re

st.set_page_config(page_title="AI Speech Fluency Trainer", page_icon="🎙️", layout="centered")

st.title("🎙️ AI English Speech Fluency & Metric Diagnostic")
st.write("Use the live stopwatches below to time your speech, dictate the text via your keyboard mic, and calculate real metrics.")

# Topics
st.markdown("### 📋 Speaking Tasks (1 minute each)")
st.info("**Task 1:** Talk about your favorite hobby and why you enjoy it.")
st.warning("**Task 2:** Discuss the impact of Artificial Intelligence on modern life.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Task 1: Hobby")
    
    # Live Stopwatch HTML component for Task 1
    components.html("""
    <div style="font-family: sans-serif; text-align: center; padding: 12px; background: #f0f2f6; border-radius: 10px; border: 1px solid #dcdcdc;">
        <div id="timer1" style="font-size: 28px; font-weight: bold; color: #262730; margin-bottom: 8px;">00:00</div>
        <button onclick="startTimer1()" style="padding: 6px 14px; background: #ff4b4b; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;">⏱️ Start Stopwatch</button>
        <button onclick="resetTimer1()" style="padding: 6px 14px; background: #717171; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; margin-left: 5px;">🔄 Reset</button>
        <script>
            let t1_interval, s1 = 0;
            function startTimer1() {
                clearInterval(t1_interval);
                s1 = 0;
                t1_interval = setInterval(() => {
                    s1++;
                    let m = Math.floor(s1 / 60), s = s1 % 60;
                    document.getElementById('timer1').innerText = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
                }, 1000);
            }
            function resetTimer1() {
                clearInterval(t1_interval);
                s1 = 0;
                document.getElementById('timer1').innerText = "00:00";
            }
        </script>
    </div>
    """, height=110)
    
    transcript_1 = st.text_area(
        "Dictate transcript for Task 1:", 
        key="t1", 
        placeholder="Tap here, press the keyboard mic icon, and speak..."
    )

with col2:
    st.markdown("#### Task 2: Artificial Intelligence")
    
    # Live Stopwatch HTML component for Task 2
    components.html("""
    <div style="font-family: sans-serif; text-align: center; padding: 12px; background: #f0f2f6; border-radius: 10px; border: 1px solid #dcdcdc;">
        <div id="timer2" style="font-size: 28px; font-weight: bold; color: #262730; margin-bottom: 8px;">00:00</div>
        <button onclick="startTimer2()" style="padding: 6px 14px; background: #ff4b4b; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;">⏱️ Start Stopwatch</button>
        <button onclick="resetTimer2()" style="padding: 6px 14px; background: #717171; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; margin-left: 5px;">🔄 Reset</button>
        <script>
            let t2_interval, s2 = 0;
            function startTimer2() {
                clearInterval(t2_interval);
                s2 = 0;
                t2_interval = setInterval(() => {
                    s2++;
                    let m = Math.floor(s2 / 60), s = s2 % 60;
                    document.getElementById('timer2').innerText = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
                }, 1000);
            }
            function resetTimer2() {
                clearInterval(t2_interval);
                s2 = 0;
                document.getElementById('timer2').innerText = "00:00";
            }
        </script>
    </div>
    """, height=110)

    transcript_2 = st.text_area(
        "Dictate transcript for Task 2:", 
        key="t2", 
        placeholder="Tap here, press the keyboard mic icon, and speak..."
    )

# Real mathematical calculation function
def calculate_metrics(text, duration_seconds=60):
    if not text.strip():
        return 0, 0, 0, 0, 0
    
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    unique_words = len(set(words))
    
    minutes = duration_seconds / 60.0
    wpm = round(total_words / minutes) if minutes > 0 else 0
    
    ttr = unique_words / total_words if total_words > 0 else 0
    
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
