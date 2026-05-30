import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime, timedelta

st.set_page_config(
    page_title="ExamZen · AI Study Coach",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
:root {
    --bg:#0a0e1a; --surface:#111827; --card:#161d2e; --border:#1f2d45;
    --accent1:#38bdf8; --accent2:#818cf8; --accent3:#34d399; --accent4:#fb923c;
    --text:#e2e8f0; --muted:#64748b;
}
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif;background-color:var(--bg)!important;color:var(--text)!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:1.5rem!important;max-width:1100px;}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border);}
[data-testid="stSidebar"] *{color:var(--text)!important;}
textarea,input[type="text"],input[type="password"]{background:var(--card)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:8px!important;}
.stButton>button{background:linear-gradient(135deg,var(--accent1),var(--accent2))!important;color:#0a0e1a!important;font-weight:700!important;border:none!important;border-radius:8px!important;padding:.55rem 1.4rem!important;}
.ez-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1rem;}
.ez-card-accent{border-left:3px solid var(--accent1);}
.feature-badge{display:inline-block;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:.18rem .6rem;border-radius:20px;margin-bottom:.6rem;}
.badge-blue{background:rgba(56,189,248,.15);color:var(--accent1);border:1px solid rgba(56,189,248,.3);}
.badge-violet{background:rgba(129,140,248,.15);color:var(--accent2);border:1px solid rgba(129,140,248,.3);}
.badge-green{background:rgba(52,211,153,.15);color:var(--accent3);border:1px solid rgba(52,211,153,.3);}
.badge-amber{background:rgba(251,146,60,.15);color:var(--accent4);border:1px solid rgba(251,146,60,.3);}
.page-title{font-size:1.8rem;font-weight:700;line-height:1.2;margin-bottom:.25rem;}
.page-sub{color:var(--muted);font-size:.95rem;margin-bottom:1.5rem;font-style:italic;}
.chat-bubble-user{background:rgba(56,189,248,.08);border:1px solid rgba(56,189,248,.2);border-radius:12px 12px 2px 12px;padding:.75rem 1rem;margin:.5rem 0;text-align:right;font-size:.9rem;}
.chat-bubble-ai{background:var(--card);border:1px solid var(--border);border-radius:12px 12px 12px 2px;padding:.75rem 1rem;margin:.5rem 0;font-size:.92rem;line-height:1.65;}
.chat-label{font-size:.7rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;margin-bottom:.3rem;}
.chat-label-user{color:var(--accent1);text-align:right;}
.chat-label-ai{color:var(--accent3);}
.divider{border-top:1px solid var(--border);margin:1.25rem 0;}
table{width:100%!important;border-collapse:collapse!important;}
th{background:rgba(56,189,248,.1)!important;color:var(--accent1)!important;font-weight:600!important;font-size:.8rem!important;text-transform:uppercase;padding:.6rem .8rem!important;border-bottom:1px solid var(--border)!important;}
td{padding:.55rem .8rem!important;border-bottom:1px solid var(--border)!important;font-size:.88rem!important;vertical-align:top;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_client():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        return None

def call_gemini(model, system, user, temperature=0.7):
    try:
        prompt = f"{system}\n\n{user}"
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=2048,
            )
        )
        return response.text
    except Exception as e:
        raise e

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mistake_log" not in st.session_state:
    st.session_state.mistake_log = []
if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = {}

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:.5rem 0 1.2rem'>
        <div style='font-size:2.4rem'>⚛️</div>
        <div style='font-size:1.25rem;font-weight:700'>ExamZen</div>
        <div style='font-size:.75rem;color:#64748b;text-transform:uppercase;letter-spacing:.08em'>AI Study Coach · JEE / NEET</div>
    </div>
    """, unsafe_allow_html=True)
    nav = st.radio("Navigate", [
        "🏠  Home","🧑‍🏫  Mentor","🔬  Correctify",
        "📅  TimeTable","⚡  QuickQuiz","📊  My Progress"
    ], label_visibility="collapsed")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("**Subject Context**")
    subject = st.selectbox("subject", ["Physics","Chemistry","Biology","Mathematics"], label_visibility="collapsed")
    exam = st.selectbox("exam", ["JEE Main","JEE Advanced","NEET UG"], label_visibility="collapsed")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.72rem;color:#475569;text-align:center'>Built for JEE/NEET aspirants 🚀<br>Powered by Gemini</div>", unsafe_allow_html=True)

model = get_client()

def api_missing():
    st.error("API key not found. Add GEMINI_API_KEY in Streamlit secrets.", icon="🔑")

if nav == "🏠  Home":
    st.markdown("<div class='page-title'>Welcome to <span style='color:#38bdf8'>ExamZen</span> ✦</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Your personal AI-powered study companion for JEE and NEET success</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="medium")
    features = [
        ("🧑‍🏫","badge-blue","MENTOR","Chat with your AI tutor. Ask any concept and get clear explanations with real-world analogies tailored to JEE/NEET."),
        ("🔬","badge-violet","CORRECTIFY","Paste a wrong answer. The AI diagnoses your exact conceptual gap and explains where your reasoning broke down."),
        ("📅","badge-green","TIMETABLE","Enter your weak topics and get a smart personalised 7-day revision schedule with daily targets."),
        ("⚡","badge-amber","QUICKQUIZ","Generate instant MCQs on any topic. Get immediate AI feedback on your reasoning."),
    ]
    for i,(icon,badge_cls,title,desc) in enumerate(features):
        col = col1 if i%2==0 else col2
        with col:
            st.markdown(f"<div class='ez-card ez-card-accent'><div style='font-size:1.6rem;margin-bottom:.4rem'>{icon}</div><span class='feature-badge {badge_cls}'>{title}</span><div style='font-size:1rem;font-weight:600;margin-bottom:.35rem'>{title.title()}</div><div style='color:#94a3b8;font-size:.875rem;line-height:1.55'>{desc}</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.info("👈 Pick a feature from the sidebar to get started.", icon="💡")

elif nav == "🧑‍🏫  Mentor":
    st.markdown(f"<div class='page-title'>🧑‍🏫 AI Mentor</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='page-sub'>Ask any {subject} concept and get a clear explanation built for {exam}</div>", unsafe_allow_html=True)
    MENTOR_SYSTEM = f"""You are ExamZen Mentor, an elite {subject} teacher for {exam} preparation.
Rules:
1. Always use at least ONE vivid real-world analogy.
2. Structure every reply with: Core Idea, Real-World Analogy, The Science, Common Exam Traps, Memory Tip.
3. Keep language friendly but precise.
4. Flag HIGH-YIELD concepts for {exam}.
5. Stay strictly on {subject} topics."""
    for msg in st.session_state.chat_history:
        if msg["role"]=="user":
            st.markdown(f"<div class='chat-label chat-label-user'>You</div><div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-label chat-label-ai'>⚛️ ExamZen Mentor</div><div class='chat-bubble-ai'>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    col_inp,col_btn = st.columns([5,1])
    with col_inp:
        user_q = st.text_area("Your question", placeholder="e.g. Why does current lag voltage in an inductor?", height=90, label_visibility="collapsed")
    with col_btn:
        st.write("")
        send = st.button("Ask", use_container_width=True)
    col_clr,_ = st.columns([1,5])
    with col_clr:
        if st.button("Clear Chat"):
            st.session_state.chat_history=[]
            st.rerun()
    if send:
        if not model: api_missing()
        elif not user_q.strip(): st.warning("Please type a question first.", icon="✏️")
        else:
            with st.spinner("Mentor is thinking..."):
                history_text="\n".join(f"{'Student' if m['role']=='user' else 'Mentor'}: {m['content']}" for m in st.session_state.chat_history[-6:])
                full_prompt=(history_text+f"\nStudent: {user_q}").strip()
                try:
                    reply=call_gemini(model,MENTOR_SYSTEM,full_prompt,temperature=0.65)
                    st.session_state.chat_history.append({"role":"user","content":user_q})
                    st.session_state.chat_history.append({"role":"assistant","content":reply})
                    st.rerun()
                except Exception as e: st.error(f"API error: {e}",icon="🔴")

elif nav == "🔬  Correctify":
    st.markdown("<div class='page-title'>🔬 Correctify</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Paste a question and your wrong answer. The AI finds exactly where you went wrong.</div>", unsafe_allow_html=True)
    CORRECTIFY_SYSTEM = f"""You are ExamZen Correctify, a diagnostic tutor for {exam} {subject}.
Given a question and a student's incorrect answer produce:
1. What Went Wrong - the exact mistake in 1-2 sentences.
2. Root Cause - the underlying misconception.
3. Correct Approach - step-by-step correct solution.
4. The Rule to Remember - one memorable principle.
5. Similar Traps - 2 other question types using the same misconception.
6. Difficulty for {exam}: Easy / Medium / High"""
    col_a,col_b=st.columns(2,gap="large")
    with col_a:
        question_text=st.text_area("The Question",placeholder="Paste the full question here...",height=160)
    with col_b:
        student_answer=st.text_area("Your Answer or Working",placeholder="What did you write or calculate?",height=160)
    if st.button("Diagnose My Mistake"):
        if not model: api_missing()
        elif not question_text.strip() or not student_answer.strip(): st.warning("Please fill in both fields.",icon="✏️")
        else:
            with st.spinner("Diagnosing..."):
                try:
                    prompt=f"QUESTION:\n{question_text}\n\nSTUDENT ANSWER:\n{student_answer}"
                    diagnosis=call_gemini(model,CORRECTIFY_SYSTEM,prompt,temperature=0.4)
                    st.success("Diagnosis complete!",icon="✅")
                    st.markdown(f"<div class='ez-card'>{diagnosis}</div>",unsafe_allow_html=True)
                    st.session_state.mistake_log.append({"question":question_text[:80]+"...","diagnosis":diagnosis,"ts":datetime.now().strftime("%d %b, %H:%M"),"subject":subject})
                except Exception as e: st.error(f"API error: {e}",icon="🔴")
    st.markdown("<div class='divider'></div>",unsafe_allow_html=True)
    st.markdown("### Your Mistake Log")
    if not st.session_state.mistake_log:
        st.info("No mistakes logged yet. Every diagnosis you run is saved here.",icon="📝")
    else:
        for entry in reversed(st.session_state.mistake_log):
            with st.expander(f"[{entry['ts']}] {entry['subject']} - {entry['question']}"):
                st.markdown(entry["diagnosis"])
        if st.button("Clear Mistake Log"):
            st.session_state.mistake_log=[]
            st.rerun()

elif nav == "📅  TimeTable":
    st.markdown("<div class='page-title'>📅 Smart TimeTable</div>",unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Tell us your weak spots and get a hyper-targeted 7-day revision plan.</div>",unsafe_allow_html=True)
    TIMETABLE_SYSTEM=f"""You are ExamZen study planner for {exam}. Create a focused 7-day revision schedule.
Output a valid Markdown table with these columns:
Day | Date | Topic | Subtopics to Cover | Resources | Goal | Evening Revision
Rules:
- Weaker topics get more days and repetitions.
- Revisit Day 1 topics on Day 3 and Day 5.
- Add one practice test on Day 7.
- After the table add a 3-point Strategy Note."""
    col1,col2=st.columns([3,2],gap="large")
    with col1:
        weak_topics=st.text_area("Your Weak Topics",placeholder="e.g. Rotational Dynamics, Electrochemistry, Limits",height=120)
        daily_hours=st.slider("Study hours per day",2,12,6)
    with col2:
        start_date=st.date_input("Start date",datetime.today())
        study_goal=st.text_input("Your Goal",placeholder="e.g. Score 95% in JEE Main")
    if st.button("Generate My 7-Day Plan"):
        if not model: api_missing()
        elif not weak_topics.strip(): st.warning("Please enter at least one weak topic.",icon="📌")
        else:
            with st.spinner("Building your personalised plan..."):
                try:
                    dates=[(start_date+timedelta(days=i)).strftime("%a %d %b") for i in range(7)]
                    prompt=f"Weak topics: {weak_topics}\nDaily hours: {daily_hours}\nGoal: {study_goal or 'Maximise score in '+exam}\nDates: {', '.join(dates)}\nSubject: {subject}"
                    plan=call_gemini(model,TIMETABLE_SYSTEM,prompt,temperature=0.5)
                    st.success("Your plan is ready!",icon="🗓️")
                    st.markdown(plan)
                    st.download_button("Download as Markdown",data=plan,file_name="examzen_timetable.md",mime="text/markdown")
                except Exception as e: st.error(f"API error: {e}",icon="🔴")

elif nav == "⚡  QuickQuiz":
    st.markdown("<div class='page-title'>⚡ QuickQuiz</div>",unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Generate sharp MCQs on any topic. Get instant AI feedback.</div>",unsafe_allow_html=True)
    QUIZ_GEN_SYSTEM=f"""You are an expert {exam} question-setter for {subject}.
Generate exactly {{n}} multiple-choice questions on the topic provided.
Return ONLY a JSON array with no extra text. Schema:
[{{"q":"question","options":{{"A":"...","B":"...","C":"...","D":"..."}},"answer":"A","explanation":"explanation","difficulty":"Easy|Medium|Hard","topic_tag":"subtopic"}}]"""
    FEEDBACK_SYSTEM=f"""You are a {exam} coach for {subject}.
Given an MCQ and the student answer provide:
1. Correct or Incorrect
2. Why the correct answer is right
3. Why the wrong choice is a trap if wrong
4. One key insight to remember
Keep under 150 words."""
    col_q,col_s=st.columns([3,1])
    with col_q:
        quiz_topic=st.text_input("Topic for quiz",placeholder="e.g. Magnetic Force on Moving Charge")
    with col_s:
        n_questions=st.selectbox("Questions",[3,5,10],index=1)
    if st.button("Generate Quiz"):
        if not model: api_missing()
        elif not quiz_topic.strip(): st.warning("Enter a topic first.",icon="📚")
        else:
            with st.spinner("Generating questions..."):
                try:
                    system=QUIZ_GEN_SYSTEM.replace("{n}",str(n_questions))
                    raw=call_gemini(model,system,quiz_topic,temperature=0.75)
                    raw=raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
                    questions=json.loads(raw)
                    st.session_state.quiz_state={"questions":questions,"answers":{},"feedback":{},"submitted":set()}
                except json.JSONDecodeError: st.error("Could not parse quiz. Try again.",icon="🔴")
                except Exception as e: st.error(f"API error: {e}",icon="🔴")
    qs=st.session_state.quiz_state
    if qs and "questions" in qs:
        st.markdown("<div class='divider'></div>",unsafe_allow_html=True)
        correct_count=0
        for i,q in enumerate(qs["questions"]):
            diff_color={"Easy":"#34d399","Medium":"#fb923c","Hard":"#f87171"}.get(q.get("difficulty","Medium"),"#94a3b8")
            st.markdown(f"<div style='font-size:.72rem;font-weight:700;color:{diff_color};text-transform:uppercase'>{q.get('difficulty','?')} · {q.get('topic_tag','')}</div>",unsafe_allow_html=True)
            st.markdown(f"**Q{i+1}.** {q['q']}")
            opts=q["options"]
            chosen=st.radio(f"q{i}",list(opts.keys()),format_func=lambda k,o=opts:f"{k}) {o[k]}",key=f"quiz_radio_{i}",label_visibility="collapsed")
            qs["answers"][i]=chosen
            if st.button(f"Check Answer",key=f"check_{i}"):
                qs["submitted"].add(i)
                with st.spinner("Analysing..."):
                    try:
                        fb_prompt=f"Question: {q['q']}\nOptions: {q['options']}\nCorrect: {q['answer']}\nStudent chose: {chosen}\nExplanation: {q['explanation']}"
                        fb=call_gemini(model,FEEDBACK_SYSTEM,fb_prompt,temperature=0.4)
                        qs["feedback"][i]=fb
                    except Exception as e: qs["feedback"][i]=f"Error: {e}"
            if i in qs["submitted"]:
                is_correct=qs["answers"].get(i)==q["answer"]
                if is_correct:
                    st.success(qs["feedback"].get(i,""),icon="✅")
                    correct_count+=1
                else:
                    st.error(qs["feedback"].get(i,""),icon="❌")
            st.markdown("<div class='divider'></div>",unsafe_allow_html=True)
        if len(qs["submitted"])==len(qs["questions"]):
            pct=int(correct_count/len(qs["questions"])*100)
            if pct>=80: st.success(f"Score: {correct_count}/{len(qs['questions'])} ({pct}%) — Excellent!",icon="🏆")
            elif pct>=50: st.warning(f"Score: {correct_count}/{len(qs['questions'])} ({pct}%) — Keep revising!",icon="📈")
            else: st.error(f"Score: {correct_count}/{len(qs['questions'])} ({pct}%) — Review with Mentor.",icon="⚠️")

elif nav == "📊  My Progress":
    st.markdown("<div class='page-title'>📊 My Progress</div>",unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Track your mistake patterns and revision activity.</div>",unsafe_allow_html=True)
    col1,col2,col3=st.columns(3)
    total_mistakes=len(st.session_state.mistake_log)
    total_chats=len([m for m in st.session_state.chat_history if m["role"]=="user"])
    quiz_done=len(st.session_state.quiz_state.get("submitted",set()))
    for col,label,val,color in [(col1,"Mistakes Diagnosed",total_mistakes,"#f87171"),(col2,"Mentor Questions Asked",total_chats,"#38bdf8"),(col3,"Quiz Qs Attempted",quiz_done,"#34d399")]:
        col.markdown(f"<div class='ez-card' style='text-align:center'><div style='font-size:2rem;font-weight:700;color:{color}'>{val}</div><div style='font-size:.8rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.07em;margin-top:.2rem'>{label}</div></div>",unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>",unsafe_allow_html=True)
    if st.session_state.mistake_log:
        st.markdown("#### Mistakes by Subject")
        subject_counts={}
        for entry in st.session_state.mistake_log:
            s=entry.get("subject","Unknown")
            subject_counts[s]=subject_counts.get(s,0)+1
        for subj,cnt in subject_counts.items():
            bar_pct=int(cnt/total_mistakes*100)
            st.markdown(f"<div style='margin:.4rem 0'><span style='font-size:.85rem;width:90px;display:inline-block'>{subj}</span><span style='display:inline-block;background:#38bdf8;height:10px;border-radius:5px;width:{bar_pct}%;max-width:60%;vertical-align:middle;margin:0 .5rem'></span><span style='font-size:.8rem;color:#94a3b8'>{cnt} mistake{'s' if cnt>1 else ''}</span></div>",unsafe_allow_html=True)
    else:
        st.info("Use Correctify to diagnose mistakes and they will appear here.",icon="🔬")
    st.markdown("<div class='divider'></div>",unsafe_allow_html=True)
    st.markdown("#### Recent Mentor Questions")
    user_msgs=[m["content"] for m in st.session_state.chat_history if m["role"]=="user"]
    if user_msgs:
        for q in user_msgs[-5:][::-1]:
            st.markdown(f"<div class='ez-card' style='padding:.6rem 1rem;font-size:.87rem'>🔹 {q}</div>",unsafe_allow_html=True)
    else:
        st.info("Ask your first question in Mentor to see history here.",icon="🧑‍🏫")
