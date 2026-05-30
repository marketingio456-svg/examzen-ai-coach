"""
AI Study Coach for JEE/NEET Aspirants — v2 Mobile-First (Fixed Implementation)
======================================================================
==
Fully mobile-optimised. No sidebar dependency.
Powered by Google Gemini 2.5 Flash.
"""
import streamlit as st
import os
from google import genai
from google.genai import types
# ─── PAGE CONFIG
─────────────────────────────────────────────────────────
─────
st.set
_page
_
config(
page
title="ExamZen AI · JEE/NEET Coach"
,
_
page
icon="⚡"
,
_
layout="centered"
,
initial
sidebar
_
_
state="collapsed"
,
)
# ─── MASTER CSS
─────────────────────────────────────────────────────────
──────
st.markdown("""
<style>
@import
url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&f
amily=Outfit:wght@300;400;500;600;700;800;900&display=swap');
/* ════════════════════════════════════════
ROOT VARIABLES
════════════════════════════════════════ */
:root {
--bg: #070B14;
--surface: #0E1420;
--card: #131929;
--border: #1E2D45;
--border2: #243550;
--accent: #00D4FF;
--accent2: #7B61FF;
--green: #00FF88;
--orange: #FF6B35;
--pink: #FF3CAC;
--text: #E8EDF5;
--muted: #6B7FA3;
--muted2: #4A5568;
}
/* ════════════════════════════════════════
GLOBAL RESET & BASE
════════════════════════════════════════ */
*
,
*::before,
*::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"], .stApp {
font-family: 'Space Grotesk'
, sans-serif !important;
background: var(--bg) !important;
color: var(--text) !important;
}
/* Animated mesh background */
.stApp::before {
content: '';
position: fixed;
inset: 0;
background:
radial-gradient(ellipse 80% 50% at 20% 10%, rgba(0,212,255,0.06) 0%, transparent 60%),
radial-gradient(ellipse 60% 40% at 80% 80%, rgba(123,97,255,0.07) 0%, transparent
60%),
radial-gradient(ellipse 50% 60% at 50% 50%, rgba(0,255,136,0.03) 0%, transparent 70%);
pointer-events: none;
z-index: 0;
}
/* ════════════════════════════════════════
HIDE STREAMLIT CHROME
════════════════════════════════════════ */
#MainMenu, footer, header,
section[data-testid="stSidebar"],
.stDeployButton,
[data-testid="collapsedControl"] { display: none !important; }
.block-container {
padding: 0 1rem 6rem 1rem !important;
max-width: 520px !important;
margin: 0 auto !important;
}
/* ════════════════════════════════════════
KEYFRAME ANIMATIONS
════════════════════════════════════════ */
@keyframes fadeUp {
from { opacity: 0; transform: translateY(24px); }
to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
from { opacity: 0; }
to { opacity: 1; }
}
@keyframes glow {
0%, 100% { box-shadow: 0 0 20px rgba(0,212,255,0.15); }
50% { box-shadow: 0 0 35px rgba(0,212,255,0.3), 0 0 60px rgba(0,212,255,0.1); }
}
@keyframes pulse {
0%, 100% { opacity: 1; transform: scale(1); }
50% { opacity: 0.7; transform: scale(0.97); }
}
@keyframes dotPulse {
0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
40% { transform: scale(1.0); opacity: 1; }
}
/* ════════════════════════════════════════
TOP HEADER BAR
════════════════════════════════════════ */
.top-bar {
position: sticky;
top: 0;
z-index: 999;
background: rgba(7,11,20,0.92);
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
border-bottom: 1px solid var(--border);
padding: 0.9rem 1.2rem;
margin: 0 -1rem 1.5rem -1rem;
display: flex;
align-items: center;
justify-content: space-between;
animation: fadeIn 0.4s ease;
}
.top-bar-logo {
font-family: 'Outfit'
, sans-serif;
font-size: 1.25rem;
font-weight: 800;
background: linear-gradient(135deg, var(--accent), var(--accent2));
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
letter-spacing: -0.02em;
}
.top-bar-badge {
background: rgba(0,212,255,0.1);
border: 1px solid rgba(0,212,255,0.25);
color: var(--accent);
font-size: 0.68rem;
font-weight: 600;
letter-spacing: 0.08em;
text-transform: uppercase;
padding: 0.25rem 0.6rem;
border-radius: 20px;
}
/* ════════════════════════════════════════
BOTTOM NAV BAR OVERLAY STRUCTURING
════════════════════════════════════════ */
.bottom-nav {
position: fixed;
bottom: 0;
left: 0;
right: 0;
z-index: 1000;
background: rgba(13,18,30,0.97);
backdrop-filter: blur(24px);
-webkit-backdrop-filter: blur(24px);
border-top: 1px solid var(--border);
padding: 0.6rem 0.5rem;
display: flex;
justify-content: space-around;
align-items: center;
animation: fadeIn 0.5s ease;
pointer-events: none; /* Let clicks pass through cleanly to Streamlit buttons below */
}
.nav-item {
display: flex;
flex-direction: column;
align-items: center;
gap: 0.2rem;
padding: 0.4rem 0.8rem;
border-radius: 12px;
min-width: 60px;
color: var(--muted);
}
.nav-item.active {
background: rgba(0,212,255,0.1);
color: var(--accent);
}
.nav-icon { font-size: 1.3rem; line-height: 1; }
.nav-label {
font-size: 0.62rem;
font-weight: 600;
letter-spacing: 0.04em;
text-transform: uppercase;
}
/* Click Layer Container */
.nav-trigger-container {
position: fixed;
bottom: 0;
left: 0;
right: 0;
z-index: 1001;
height: 64px;
display: flex;
justify-content: space-around;
align-items: center;
padding: 0 0.5rem;
}
.nav-trigger-container .stButton,
.nav-trigger-container .stButton > button {
height: 100% !important;
width: 100% !important;
background: transparent !important;
border: none !important;
box-shadow: none !important;
color: transparent !important;
border-radius: 0px !important;
margin: 0 !important;
padding: 0 !important;
}
/* ════════════════════════════════════════
HERO SECTION
════════════════════════════════════════ */
.hero {
text-align: center;
padding: 2rem 0.5rem 1.5rem;
animation: fadeUp 0.6s ease;
}
.hero-eyebrow {
display: inline-flex;
align-items: center;
gap: 0.4rem;
background: rgba(0,255,136,0.08);
border: 1px solid rgba(0,255,136,0.2);
color: var(--green);
font-size: 0.72rem;
font-weight: 600;
letter-spacing: 0.1em;
text-transform: uppercase;
padding: 0.3rem 0.8rem;
border-radius: 20px;
margin-bottom: 1rem;
}
.hero-dot {
width: 6px; height: 6px;
background: var(--green);
border-radius: 50%;
animation: pulse 2s infinite;
}
.hero-title {
font-family: 'Outfit'
, sans-serif;
font-size: 2.4rem;
font-weight: 900;
line-height: 1.1;
letter-spacing: -0.03em;
color: #FFFFFF;
margin-bottom: 0.8rem;
}
.hero-title span {
background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
}
.hero-sub {
font-size: 0.92rem;
color: var(--muted);
line-height: 1.65;
max-width: 320px;
margin: 0 auto 1.5rem;
font-weight: 300;
}
.hero-stats {
display: flex;
justify-content: center;
gap: 1.5rem;
margin-top: 1.2rem;
}
.stat-item {
text-align: center;
}
.stat-number {
font-family: 'Outfit'
, sans-serif;
font-size: 1.4rem;
font-weight: 800;
color: #FFFFFF;
line-height: 1;
}
.stat-label {
font-size: 0.68rem;
color: var(--muted);
text-transform: uppercase;
letter-spacing: 0.06em;
margin-top: 0.2rem;
}
/* ════════════════════════════════════════
FEATURE CARDS (Home)
════════════════════════════════════════ */
.feature-grid { display: flex; flex-direction: column; gap: 0.9rem; margin: 1.2rem 0; }
.fcard {
background: var(--card);
border: 1px solid var(--border);
border-radius: 16px;
padding: 1.2rem 1.3rem;
display: flex;
align-items: flex-start;
gap: 1rem;
transition: all 0.25s ease;
animation: fadeUp 0.5s ease both;
position: relative;
overflow: hidden;
}
.fcard:nth-child(1) { animation-delay: 0.1s; border-left: 3px solid var(--accent); }
.fcard:nth-child(2) { animation-delay: 0.2s; border-left: 3px solid var(--accent2); }
.fcard:nth-child(3) { animation-delay: 0.3s; border-left: 3px solid var(--green); }
.fcard-icon {
width: 48px; height: 48px;
border-radius: 12px;
display: flex; align-items: center; justify-content: center;
font-size: 1.4rem;
flex-shrink: 0;
}
.fcard:nth-child(1) .fcard-icon { background: rgba(0,212,255,0.1); }
.fcard:nth-child(2) .fcard-icon { background: rgba(123,97,255,0.1); }
.fcard:nth-child(3) .fcard-icon { background: rgba(0,255,136,0.1); }
.fcard-body { flex: 1; }
.fcard-tag {
font-size: 0.65rem;
font-weight: 700;
letter-spacing: 0.1em;
text-transform: uppercase;
margin-bottom: 0.3rem;
}
.fcard:nth-child(1) .fcard-tag { color: var(--accent); }
.fcard:nth-child(2) .fcard-tag { color: var(--accent2); }
.fcard:nth-child(3) .fcard-tag { color: var(--green); }
.fcard-title {
font-family: 'Outfit'
, sans-serif;
font-size: 1rem;
font-weight: 700;
color: #FFFFFF;
margin-bottom: 0.3rem;
}
.fcard-desc { font-size: 0.8rem; color: var(--muted); line-height: 1.55; }
.fcard-arrow { color: var(--muted2); font-size: 1rem; align-self: center; }
/* ════════════════════════════════════════
PAGE HEADERS
════════════════════════════════════════ */
.page-header {
padding: 1.5rem 0 1rem;
animation: fadeUp 0.4s ease;
}
.page-eyebrow {
font-size: 0.7rem;
font-weight: 700;
letter-spacing: 0.12em;
text-transform: uppercase;
color: var(--accent);
margin-bottom: 0.4rem;
}
.page-title {
font-family: 'Outfit'
, sans-serif;
font-size: 1.8rem;
font-weight: 800;
color: #FFFFFF;
letter-spacing: -0.02em;
line-height: 1.2;
}
.page-sub { font-size: 0.85rem; color: var(--muted); margin-top: 0.4rem; line-height: 1.55; }
/* ════════════════════════════════════════
CHAT MESSAGES
════════════════════════════════════════ */
.chat-wrap { display: flex; flex-direction: column; gap: 0.8rem; margin: 1rem 0; }
.msg-user {
display: flex;
justify-content: flex-end;
animation: fadeUp 0.3s ease;
margin-bottom: 0.6rem;
}
.msg-user-bubble {
background: linear-gradient(135deg, var(--accent2), #5B4BD0);
color: #FFFFFF;
border-radius: 18px 18px 4px 18px;
padding: 0.75rem 1rem;
max-width: 85%;
font-size: 0.88rem;
line-height: 1.55;
box-shadow: 0 4px 20px rgba(123,97,255,0.25);
}
.msg-ai {
display: flex;
gap: 0.6rem;
align-items: flex-start;
animation: fadeUp 0.3s ease;
margin-bottom: 0.6rem;
}
.msg-ai-avatar {
width: 32px; height: 32px;
background: linear-gradient(135deg, var(--accent), var(--accent2));
border-radius: 10px;
display: flex; align-items: center; justify-content: center;
font-size: 0.9rem;
flex-shrink: 0;
animation: glow 3s infinite;
}
.msg-ai-bubble {
background: var(--card);
border: 1px solid var(--border);
color: var(--text);
border-radius: 4px 18px 18px 18px;
padding: 0.9rem 1rem;
max-width: 88%;
font-size: 0.88rem;
line-height: 1.65;
}
/* Typing indicator */
.typing-indicator {
display: flex;
gap: 0.25rem;
padding: 0.6rem 0.8rem;
background: var(--card);
border: 1px solid var(--border);
border-radius: 4px 18px 18px 18px;
width: fit-content;
}
.typing-dot {
width: 7px; height: 7px;
background: var(--accent);
border-radius: 50%;
animation: dotPulse 1.4s infinite ease-in-out;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
/* ════════════════════════════════════════
INPUT AREA
════════════════════════════════════════ */
.stTextArea textarea {
background: var(--card) !important;
border: 1px solid var(--border) !important;
border-radius: 14px !important;
color: var(--text) !important;
font-family: 'Space Grotesk'
, sans-serif !important;
font-size: 0.9rem !important;
line-height: 1.55 !important;
padding: 0.9rem 1rem !important;
resize: none !important;
}
.stTextArea textarea:focus {
border-color: var(--accent) !important;
box-shadow: 0 0 0 3px rgba(0,212,255,0.1) !important;
}
.stTextInput input {
background: var(--card) !important;
border: 1px solid var(--border) !important;
border-radius: 12px !important;
color: var(--text) !important;
font-family: 'Space Grotesk'
, sans-serif !important;
font-size: 0.9rem !important;
padding: 0.75rem 1rem !important;
}
/* Chat input */
.stChatInputContainer,
[data-testid="stChatInput"] {
background: var(--card) !important;
border: 1px solid var(--border2) !important;
border-radius: 16px !important;
}
.stChatInput textarea {
background: transparent !important;
color: var(--text) !important;
font-family: 'Space Grotesk'
, sans-serif !important;
}
/* ════════════════════════════════════════
BUTTONS
════════════════════════════════════════ */
.stButton > button {
background: linear-gradient(135deg, var(--accent), #00A8CC) !important;
color: #000000 !important;
font-family: 'Outfit'
, sans-serif !important;
font-weight: 700 !important;
font-size: 0.88rem !important;
letter-spacing: 0.04em !important;
border: none !important;
border-radius: 12px !important;
padding: 0.7rem 1.5rem !important;
transition: all 0.2s ease !important;
box-shadow: 0 4px 20px rgba(0,212,255,0.25) !important;
width: 100% !important;
}
.stButton > button:hover {
transform: translateY(-2px) !important;
box-shadow: 0 8px 30px rgba(0,212,255,0.35) !important;
}
/* ════════════════════════════════════════
SELECT / DROPDOWN
════════════════════════════════════════ */
.stSelectbox > div > div {
background: var(--card) !important;
border: 1px solid var(--border) !important;
border-radius: 12px !important;
color: var(--text) !important;
}
.stSelectbox label {
color: var(--muted) !important;
font-size: 0.8rem !important;
font-weight: 600 !important;
letter-spacing: 0.04em !important;
}
/* ════════════════════════════════════════
RESULT BOXES
════════════════════════════════════════ */
.result-box {
background: var(--card);
border: 1px solid var(--border);
border-top: 3px solid var(--green);
border-radius: 16px;
padding: 1.3rem;
margin-top: 1.2rem;
animation: fadeUp 0.4s ease;
font-size: 0.88rem;
line-height: 1.75;
color: var(--text);
}
.result-label {
font-size: 0.68rem;
font-weight: 700;
letter-spacing: 0.1em;
text-transform: uppercase;
color: var(--green);
margin-bottom: 0.8rem;
display: flex;
align-items: center;
gap: 0.4rem;
}
.result-label::before {
content: '';
display: inline-block;
width: 6px; height: 6px;
background: var(--green);
border-radius: 50%;
animation: pulse 2s infinite;
}
.error-box {
background: rgba(255,59,59,0.06);
border: 1px solid rgba(255,59,59,0.2);
border-radius: 12px;
padding: 0.9rem 1rem;
font-size: 0.85rem;
color: #FF6B6B;
margin-top: 0.8rem;
animation: fadeUp 0.3s ease;
}
.info-box {
background: rgba(0,212,255,0.05);
border: 1px solid rgba(0,212,255,0.15);
border-radius: 12px;
padding: 0.9rem 1rem;
font-size: 0.85rem;
color: var(--muted);
margin: 0.8rem 0;
line-height: 1.6;
}
.info-box b { color: var(--text); }
.sdiv {
border: none;
border-top: 1px solid var(--border);
margin: 1.2rem 0;
}
.chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.6rem 0 1rem; }
.chip {
background: rgba(0,212,255,0.07);
border: 1px solid rgba(0,212,255,0.18);
color: var(--accent);
font-size: 0.73rem;
font-weight: 500;
padding: 0.25rem 0.65rem;
border-radius: 20px;
}
.stTextArea label, .stTextInput label, .stNumberInput label {
color: var(--muted) !important;
font-size: 0.8rem !important;
font-weight: 600 !important;
text-transform: uppercase !important;
}
.stNumberInput input {
background: var(--card) !important;
border: 1px solid var(--border) !important;
border-radius: 12px !important;
color: var(--text) !important;
}
.stDownloadButton > button {
background: transparent !important;
color: var(--accent) !important;
border: 1px solid rgba(0,212,255,0.3) !important;
box-shadow: none !important;
font-size: 0.83rem !important;
}
.stDownloadButton > button:hover {
background: rgba(0,212,255,0.08) !important;
border-color: var(--accent) !important;
}
[data-testid="stChatMessage"] {
background: transparent !important;
border: none !important;
padding: 0 !important;
}
</style>
"""
, unsafe
allow
_
_
html=True)
# ─── GEMINI CLIENT
─────────────────────────────────────────────────────────
────
@st.cache
_
resource(show
_
def get
_
client():
try:
spinner=False)
# Access secret variable securely using correct modern structures
api
_
key = st.secrets.get("GEMINI
API
_
_
KEY") or os.environ.get("GEMINI
API
_
_
if not api
_
key:
return None
return genai.Client(api
_
key=api
_
key)
except Exception:
return None
KEY")
def call
_gemini(client, prompt: str, system: str, temperature: float = 0.7) -> str:
try:
response = client.models.generate
_
content(
model="gemini-1.5-flash"
,
contents=prompt,
config=types.GenerateContentConfig(
system
_
instruction=system,
temperature=temperature,
max
_
output
tokens=2048,
_
),
)
return response.text
except Exception as e:
return f"⚠ Error parsing request: {str(e)}"
# ─── SYSTEM PROMPTS
─────────────────────────────────────────────────────────
───
MENTOR
_
You are 'Arya'
Style rules:
SYSTEM = """
— an elite JEE/NEET mentor with 15+ years of IIT coaching.
- Start EVERY answer with a vivid real-world analogy in bold.
- Structure: 🌍 Analogy → 📖 Concept → 📐 Formula → 🎯 Exam Tip
- Use markdown formatting: bold, bullet points, code blocks for formulas.
- Be warm, encouraging, exam-focused.
- Only answer JEE/NEET subjects: Physics, Chemistry, Biology, Math.
- End every response with: 🎯 **Exam Tip:** [one high-yield tip]
"""
CORRECTIFY
SYSTEM = """
_
You are 'CorrectifyAI'
— a JEE/NEET error diagnostician.
For every mistake submitted:
1. 🔴 **Root Error**
— exact conceptual gap or formula mistake
2. ❌ **Why It's Wrong**
— clear logical explanation
3. ✅ **Correct Approach**
— step-by-step solution
4. 📚 **Topic to Revise**
— specific NCERT chapter / JEE syllabus topic
5. 🧠
**Memory Hook**
— one trick/mnemonic to prevent this again
Use bold headers, be direct but kind.
"""
TIMETABLE
SYSTEM = """
_
You are 'PlannerAI'
— a JEE/NEET revision schedule expert.
Create a detailed 7-day timetable:
- Weak topics appear MORE often (spaced repetition)
- Each day: morning slot (30 min revision) + main slot + evening problems (60 min)
- Alternate subjects to prevent burnout
- Sunday = light revision + rest
- Include book references: NCERT, HC Verma, DC Pandey, MS Chouhan, etc.
- Use ### Day 1, ### Day 2 ... headers
- End with 💡 3 Power Tips for execution
Format cleanly with markdown.
"""
# ─── SESSION STATE
─────────────────────────────────────────────────────────
────
if "page" not in st.session
state:
_
st.session
_
state.page = "home"
if "mentor
_
messages" not in st.session
_
st.session
state.mentor
_
_
messages = []
if "mistake
_
log" not in st.session
state:
_
st.session
state.mistake
_
_
log = []
state:
# ─── TOP BAR
─────────────────────────────────────────────────────────
──────────
client = get
_
client()
api
_
status = "⚡ Live" if client else "🔴 No Key"
st.markdown(f"""
<div class='top-bar'>
<div class='top-bar-logo'>⚡ ExamZen</div>
<div class='top-bar-badge'>{api
_
status}</div>
</div>
"""
, unsafe
allow
_
_
html=True)
# ─── FIXED VISUAL NAVIGATION NAV OVERLAY
───────────────────────────────────────
pages = [
("home"
"🏠"
,
,
("mentor"
"󰳓"
,
,
("correctify"
"🔍"
,
,
("timetable"
,
"📅"
,
"Home"),
"Mentor"),
"Fix"),
"Plan"),
]
nav
html = "<div class='bottom-nav'>"
_
for pid, icon, label in pages:
active = "active" if st.session
_
state.page == pid else ""
nav
html += f"""
_
<div class='nav-item {active}'>
<span class='nav-icon'>{icon}</span>
<span class='nav-label'>{label}</span>
</div>"""
html += "</div>"
nav
st.
_
