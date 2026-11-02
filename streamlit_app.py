import streamlit as st
import streamlit.components.v1 as components
import re

st.set_page_config(page_title="AI Speech Fluency Trainer", page_icon="🎙️", layout="centered")

st.title("🎙️ AI English Speech Fluency & Metric Diagnostic")
st.write("Use the live stopwatches (with 1-minute alarm) to time your speech, dictate or paste your transcript, and get advanced linguistic metrics.")

# Topics
st.markdown("### 📋 Speaking Tasks (1 minute each)")
st.info("**Task 1:** Talk about your favorite hobby and why you enjoy it.")
st.warning("**Task 2:** Discuss the impact of Artificial Intelligence on modern life.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Task 1: Hobby")
    components.html("""
    <div style="font-family: sans-serif; text-align: center; padding: 10px; background: #f0f2f6; border-radius: 10px; border: 1px solid #dcdcdc;">
        <div id="timer1" style="font-size: 26px; font-weight: bold; color: #262730; margin-bottom: 6px;">00:00</div>
        <button onclick="startTimer1()" style="padding: 5px 12px; background: #ff4b4b; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px;">⏱️ Start 1-Min Timer</button>
        <button onclick="resetTimer1()" style="padding: 5px 12px; background: #717171; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px; margin-left: 4px;">🔄 Reset</button>
        <script>
            let t1_interval, s1 = 0;
            function playBeep() {
                let ctx = new (window.AudioContext || window.webkitAudioContext)();
                let osc = ctx.createOscillator();
                let gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.value = 587.33; // D5 note
                gain.gain.setValueAtTime(0.1, ctx.currentTime);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.5);
            }
            function startTimer1() {
                clearInterval(t1_interval);
                s1 = 0;
                document.getElementById('timer1').style.color = '#262730';
                t1_interval = setInterval(() => {
                    s1++;
                    let m = Math.floor(s1 / 60), s = s1 % 60;
                    document.getElementById('timer1').innerText = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
                    if (s1 === 60) {
                        playBeep();
                        document.getElementById('timer1').style.color = '#ff4b4b';
                    }
                }, 1000);
            }
            function resetTimer1() {
                clearInterval(t1_interval);
                s1 = 0;
                document.getElementById('timer1').innerText = "00:00";
                document.getElementById('timer1').style.color = '#262730';
            }
        </script>
    </div>
    """, height=105)
    
    transcript_1 = st.text_area(
        "Paste or dictate transcript for Task 1:", 
        key="t1", 
        placeholder="Paste your text here or tap the keyboard mic icon to dictate..."
    )

with col2:
    st.markdown("#### Task 2: Artificial Intelligence")
    components.html("""
    <div style="font-family: sans-serif; text-align: center; padding: 10px; background: #f0f2f6; border-radius: 10px; border: 1px solid #dcdcdc;">
        <div id="timer2" style="font-size: 26px; font-weight: bold; color: #262730; margin-bottom: 6px;">00:00</div>
        <button onclick="startTimer2()" style="padding: 5px 12px; background: #ff4b4b; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px;">⏱️ Start 1-Min Timer</button>
        <button onclick="resetTimer2()" style="padding: 5px 12px; background: #717171; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px; margin-left: 4px;">🔄 Reset</button>
        <script>
            let t2_interval, s2 = 0;
            function playBeep2() {
                let ctx = new (window.AudioContext || window.webkitAudioContext)();
                let osc = ctx.createOscillator();
                let gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.value = 587.33;
                gain.gain.setValueAtTime(0.1, ctx.currentTime);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.5);
            }
            function startTimer2() {
                clearInterval(t2_interval);
                s2 = 0;
                document.getElementById('timer2').style.color = '#262730';
                t2_interval = setInterval(() => {
                    s2++;
                    let m = Math.floor(s2 / 60), s = s2 % 60;
                    document.getElementById('timer2').innerText = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
                    if (s2 === 60) {
                        playBeep2();
                        document.getElementById('timer2').style.color = '#ff4b4b';
                    }
                }, 1000);
            }
            function resetTimer2() {
                clearInterval(t2_interval);
                s2 = 0;
                document.getElementById('timer2').innerText = "00:00";
                document.getElementById('timer2').style.color = '#262730';
            }
        </script>
    </div>
    """, height=105)

    transcript_2 = st.text_area(
        "Paste or dictate transcript for Task 2:", 
        key="t2", 
        placeholder="Paste your text here or tap the keyboard mic icon to dictate..."
    )

# Advanced mathematical calculation function
def calculate_advanced_metrics(text, duration_seconds=60):
    if not text.strip():
        return 0, 0, 0, 0, 0, 0, 0
    
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    unique_words = len(set(words))
    
    minutes = duration_seconds / 60.0
    wpm = round(total_words / minutes) if minutes > 0 else 0
    
    ttr = unique_words / total_words if total_words > 0 else 0
    
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    total_sentences = len(sentences) if len(sentences) > 0 else 1
    mlu = total_words / total_sentences
    
    long_words = [w for w in words if len(w) > 6]
    long_word_ratio = len(long_words) / total_words if total_words > 0 else 0
    
    return total_words, wpm, unique_words, round(ttr, 2), round(mlu, 1), round(long_word_ratio * 100, 1), total_sentences

# Analysis Button
if st.button("🚀 Calculate Advanced Linguistic Metrics", type="primary"):
    if not transcript_1.strip() or not transcript_2.strip():
        st.error("Please provide transcripts for both tasks to run the analysis!")
    else:
        w1, wpm1, u1, ttr1, mlu1, lwr1, s1 = calculate_advanced_metrics(transcript_1)
        w2, wpm2, u2, ttr2, mlu2, lwr2, s2 = calculate_advanced_metrics(transcript_2)

        st.success("✨ Advanced metrics successfully calculated!")
        
        # Display comparison dashboard
        st.subheader("📊 Extended Speech Metrics Comparison")
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("##### Task 1: Hobby")
            st.metric("Speech Rate", f"{wpm1} WPM")
            st.metric("Total Words", w1)
            st.metric("Unique Words", u1)
            st.metric("Lexical Diversity (TTR)", ttr1)
            st.metric("Avg Sentence Length (MLU)", mlu1)
            st.metric("Advanced Words (>6 letters)", f"{lwr1}%")
            st.metric("Total Sentences", s1)
                
        with c2:
            st.markdown("##### Task 2: AI Impact")
            st.metric("Speech Rate", f"{wpm2} WPM", delta=wpm2 - wpm1)
            st.metric("Total Words", w2, delta=w2 - w1)
            st.metric("Unique Words", u2, delta=u2 - u1)
            st.metric("Lexical Diversity (TTR)", ttr2, delta=round(ttr2 - ttr1, 2))
            st.metric("Avg Sentence Length (MLU)", mlu2, delta=round(mlu2 - mlu1, 1))
            st.metric("Advanced Words (>6 letters)", f"{lwr2}%", delta=round(lwr2 - lwr1, 1))
            st.metric("Total Sentences", s2, delta=s2 - s1)

        # Smart Conditional Recommendations
        st.subheader("💡 Smart Expert Recommendations & Video Categories")
        
        recommendations = []
        
        if ttr2 < 0.5 or ttr2 < ttr1:
            recommendations.append("📚 **Vocabulary Focus:** Lexical diversity decreased in Task 2. *Recommended action:* Watch our **Vocabulary Video Lessons** to expand your thematic academic word stock.")
        else:
            recommendations.append("📚 **Vocabulary Focus:** Great job maintaining a rich and diverse vocabulary profile!")

        if mlu2 < 6.0:
            recommendations.append("✍️ **Grammar & Syntax Focus:** Sentence structures are relatively short. *Recommended action:* Check out our **Grammar & Sentence Structure Video Lessons** to practice complex subordinate clauses.")
        else:
            recommendations.append("✍️ **Grammar & Syntax Focus:** Solid syntactic complexity with well-developed clauses.")

        if wpm2 < 90:
            recommendations.append("🗣️ **General Speaking Fluency:** Speech tempo slowed down in Task 2, indicating potential hesitation under cognitive load. *Recommended action:* Review our **General Speaking Skills Video Lessons**.")
        else:
            recommendations.append("🗣️ **General Speaking Fluency:** Confident and steady speaking pace demonstrated across tasks!")

        for rec in recommendations:
            st.markdown(f"- {rec}")
