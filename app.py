import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.parse import quote
from datetime import datetime, timedelta, timezone

st.set_page_config(
    page_title="SuryaDrishti",
    page_icon="icon.png",
    layout="wide"
)

st.markdown("""
<div class="main-brand">
    <h1>☀️ SuryaDrishti</h1>
    <p class="brand-subtitle">SPACE WEATHER ALERT SYSTEM</p>
    <p class="brand-tagline">
        AI-Powered Space Weather Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.main-brand {
    text-align: center;
    padding: 12px 0 24px;
}

.main-brand h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 4px;
    color: #F8FAFC;
}

.brand-subtitle {
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 3px;
    color: #8FCBFF;
    margin: 0;
}

.brand-tagline {
    font-size: 0.9rem;
    color: #A8B8CC;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Premium mission-control styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --space-bg: #07111f;
    --space-panel: #0d1b2d;
    --space-panel-2: #10243a;
    --space-line: rgba(112, 171, 220, .22);
    --space-cyan: #55e6f2;
    --space-violet: #a78bfa;
    --space-text: #e8f1fb;
    --space-muted: #9fb4ca;
}
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background:
      radial-gradient(ellipse at 12% 0%, rgba(29, 78, 137, .24), transparent 38%),
      radial-gradient(ellipse at 92% 8%, rgba(103, 58, 183, .18), transparent 30%),
      var(--space-bg);
    color: var(--space-text);
}
[data-testid="stHeader"] {
    background: rgba(7, 17, 31, .72);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1728 0%, #0c1b2e 100%);
    border-right: 1px solid var(--space-line);
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--space-muted);
}
h1, h2, h3 {
    letter-spacing: -.035em;
}
h1 {
    font-weight: 800 !important;
    background: linear-gradient(90deg, #f2fbff 0%, var(--space-cyan) 48%, var(--space-violet) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
h2, h3 {
    color: #e6f4ff;
}
[data-testid="stCaptionContainer"] {
    color: var(--space-muted);
}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(17, 39, 61, .96), rgba(10, 25, 42, .96));
    border: 1px solid var(--space-line);
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, .16);
    transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(85, 230, 242, .62);
    box-shadow: 0 10px 30px rgba(27, 192, 220, .10);
}
[data-testid="stMetricLabel"] {
    color: #a9c0d7 !important;
}
[data-testid="stMetricValue"] {
    color: #f4fbff !important;
    font-weight: 800;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--space-line);
}
div[data-testid="stExpander"] {
    border: 1px solid var(--space-line);
    border-radius: 14px;
    background: rgba(13, 27, 45, .72);
}
.stButton > button, .stLinkButton > a {
    border-radius: 10px;
    border: 1px solid rgba(85, 230, 242, .45);
    background: linear-gradient(100deg, rgba(21, 90, 116, .88), rgba(67, 56, 125, .88));
    color: #f4fbff;
    font-weight: 650;
    transition: transform .18s ease, filter .18s ease;
}
.stButton > button:hover, .stLinkButton > a:hover {
    filter: brightness(1.15);
    transform: translateY(-1px);
    border-color: var(--space-cyan);
    color: white;
}
[data-testid="stTabs"] button[role="tab"] {
    border-radius: 10px 10px 0 0;
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
    border: 1px solid var(--space-line);
    border-radius: 12px;
    overflow: hidden;
}
[data-testid="stPlotlyChart"], [data-testid="stArrowVegaLiteChart"] {
    border: 1px solid rgba(112, 171, 220, .16);
    border-radius: 14px;
    padding: 6px;
    background: rgba(10, 24, 40, .58);
}
hr {
    border-color: var(--space-line);
}
.mission-kicker {
    display: flex;
    align-items: center;
    gap: 9px;
    color: var(--space-cyan);
    text-transform: uppercase;
    letter-spacing: .16em;
    font-size: .72rem;
    font-weight: 800;
    margin: 0 0 .45rem 0;
}
.mission-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 12px rgba(74, 222, 128, .85);
    display: inline-block;
    animation: mission-pulse 2s infinite;
}
@keyframes mission-pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 5px rgba(74, 222, 128, .55); }
    50% { opacity: .65; box-shadow: 0 0 15px rgba(74, 222, 128, .95); }
}
/* Premium animated sidebar controls */
[data-testid="stSidebar"] > div:first-child { padding-top: 1.1rem; }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #eaf7ff !important; letter-spacing: .02em;
}
[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    color: #a9c5dc !important; font-size: .76rem !important; font-weight: 800 !important;
    letter-spacing: .12em; text-transform: uppercase; margin-bottom: .5rem;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] { gap: .45rem; }
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] {
    background: linear-gradient(135deg, rgba(19, 42, 64, .92), rgba(12, 28, 47, .96));
    border: 1px solid rgba(112, 171, 220, .25); border-radius: 12px;
    padding: .55rem .72rem; min-height: 2.6rem;
    transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease, background .2s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]:hover {
    transform: translateY(-2px); border-color: rgba(85, 230, 242, .75);
    box-shadow: 0 6px 18px rgba(35, 199, 225, .12);
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"] {
    background: linear-gradient(110deg, rgba(13, 148, 166, .28), rgba(124, 89, 220, .26));
    border: 1px solid rgba(85, 230, 242, .9);
    box-shadow: 0 0 0 1px rgba(85, 230, 242, .10), 0 7px 22px rgba(27, 192, 220, .13);
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] > div:first-child { display: none; }
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] p {
    color: #dceeff !important; font-weight: 650; margin: 0;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > label,
[data-testid="stSidebar"] [data-testid="stCheckbox"] label { color: #c5d9eb !important; font-weight: 600; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    border-radius: 12px; background: rgba(12, 29, 48, .94);
    border-color: rgba(112, 171, 220, .32);
    transition: border-color .2s ease, box-shadow .2s ease;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: var(--space-cyan); box-shadow: 0 0 0 2px rgba(85, 230, 242, .13);
}
[data-testid="stSidebar"] [data-testid="stCheckbox"] [role="checkbox"] {
    border-radius: 5px; transition: transform .18s ease, box-shadow .18s ease;
}
[data-testid="stSidebar"] [data-testid="stCheckbox"] [role="checkbox"]:hover {
    transform: scale(1.08); box-shadow: 0 0 10px rgba(85, 230, 242, .25);
}
@media (max-width: 640px) {
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] { gap: .3rem; }
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] { padding: .48rem .5rem; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important;
        transition-duration: .01ms !important; scroll-behavior: auto !important; }
}

/* Cinematic glass + 3D motion layer for the whole dashboard */
:root { --glass-edge: rgba(119, 222, 255, .27); }
[data-testid="stAppViewContainer"] { perspective: 1400px; }
[data-testid="stMetric"] {
  position: relative; overflow: hidden; isolation: isolate;
  background: linear-gradient(145deg, rgba(21,48,73,.88), rgba(8,20,36,.94)) !important;
  border: 1px solid rgba(112,210,244,.28) !important;
  border-radius: 18px !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.07), inset 0 -12px 24px rgba(0,0,0,.13), 0 10px 24px rgba(0,0,0,.18), 0 0 0 1px rgba(66,190,235,.035) !important;
  transform: translateZ(0); animation: metric-arrive .65s cubic-bezier(.2,.8,.2,1) both;
}
[data-testid="stMetric"]:before {
  content:""; position:absolute; inset:-1px; z-index:-1; pointer-events:none;
  background: linear-gradient(115deg, transparent 15%, rgba(111,235,255,.10) 45%, transparent 72%);
  transform: translateX(-120%); animation: glass-sweep 7s ease-in-out infinite;
}
[data-testid="stMetric"]:after {
  content:""; position:absolute; left:14px; right:14px; top:0; height:1px;
  background:linear-gradient(90deg,transparent,rgba(155,244,255,.72),transparent); opacity:.8;
}
[data-testid="stMetric"]:hover { transform: translateY(-5px) rotateX(2deg); border-color:rgba(85,230,242,.72)!important; box-shadow:inset 0 1px 0 rgba(255,255,255,.1),0 18px 38px rgba(0,0,0,.28),0 0 25px rgba(41,202,232,.10)!important; }
[data-testid="stExpander"] {
  position:relative; overflow:hidden; border:1px solid rgba(99,202,239,.27)!important;
  border-radius:19px!important; background:linear-gradient(145deg,rgba(13,31,51,.83),rgba(7,18,33,.87))!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.045),0 12px 32px rgba(0,0,0,.15)!important;
  transition:border-color .3s ease, box-shadow .3s ease, transform .3s ease;
}
[data-testid="stExpander"]:hover { border-color:rgba(85,230,242,.52)!important; box-shadow:0 14px 34px rgba(0,0,0,.2),0 0 24px rgba(53,180,220,.06)!important; }
[data-testid="stAlert"] { border-radius:15px!important; border:1px solid rgba(130,207,244,.25)!important; box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 8px 20px rgba(0,0,0,.12); animation:panel-rise .45s ease both; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] { box-shadow:0 0 0 5px rgba(85,230,242,.10),0 0 18px rgba(85,230,242,.30); transition:box-shadow .2s ease,transform .2s ease; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]:hover { transform:scale(1.12); box-shadow:0 0 0 7px rgba(85,230,242,.12),0 0 24px rgba(85,230,242,.42); }
[data-testid="stDataFrame"], [data-testid="stTable"] { box-shadow:0 12px 26px rgba(0,0,0,.16); }
[data-testid="stPlotlyChart"] { box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 12px 28px rgba(0,0,0,.14)!important; transition:transform .25s ease,border-color .25s ease; }
[data-testid="stPlotlyChart"]:hover { transform:translateY(-2px); border-color:rgba(85,230,242,.35)!important; }
.stMarkdown h2, .stMarkdown h3 { text-shadow:0 0 24px rgba(85,230,242,.08); }
@keyframes metric-arrive { from { opacity:0; transform:translateY(9px) rotateX(-3deg); } to { opacity:1; transform:translateY(0) rotateX(0); } }
@keyframes glass-sweep { 0%,65%,100% { transform:translateX(-120%); } 82% { transform:translateX(120%); } }
@keyframes panel-rise { from { opacity:.65; transform:translateY(5px); } to { opacity:1; transform:translateY(0); } }
/* A floating, dimensional simulator viewport with depth layers */
.sim-scene {
  transform-style:preserve-3d; border:1px solid rgba(106,226,255,.42)!important;
  background:radial-gradient(ellipse at 50% 120%,rgba(32,95,151,.28),transparent 48%),radial-gradient(ellipse at 78% 22%,rgba(131,82,255,.16),transparent 34%),linear-gradient(135deg,#050d1b 0%,#0b2038 48%,#100f2c 100%)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.10),inset 0 -25px 55px rgba(0,0,0,.24),0 18px 45px rgba(0,0,0,.25),0 0 35px rgba(53,198,235,.07)!important;
  animation:scene-hover 8s ease-in-out infinite;
}
.sim-scene:before { content:"";position:absolute;inset:0;pointer-events:none;opacity:.24;background-image:radial-gradient(1px 1px at 8% 20%,#d8f6ff 99%,transparent),radial-gradient(1px 1px at 42% 13%,#d8f6ff 99%,transparent),radial-gradient(1px 1px at 67% 32%,#d8f6ff 99%,transparent),radial-gradient(1px 1px at 92% 63%,#d8f6ff 99%,transparent),radial-gradient(1px 1px at 30% 72%,#d8f6ff 99%,transparent);background-size:190px 130px;animation:star-drift 22s linear infinite; }
.sim-topline,.sim-scene-footer { position:relative;z-index:2;text-shadow:0 0 12px rgba(85,230,242,.2); }
.sim-sun { filter:drop-shadow(0 0 8px rgba(255,132,56,.3)); }
.sim-earth { box-shadow:inset -12px -8px 16px rgba(0,0,0,.52),inset 5px 3px 8px rgba(255,255,255,.24),0 0 24px rgba(46,165,255,.42)!important; }
.sim-field { filter:drop-shadow(0 0 4px rgba(85,230,242,.5)); }
.sim-solar-stream { filter:drop-shadow(0 0 7px rgba(255,160,86,.5)); }
@keyframes scene-hover { 0%,100% { transform:perspective(1000px) rotateX(0deg) translateY(0); } 50% { transform:perspective(1000px) rotateX(.6deg) translateY(-2px); } }
@keyframes star-drift { from { background-position:0 0; } to { background-position:190px 130px; } }
@media (prefers-reduced-motion:reduce) { [data-testid="stMetric"],.sim-scene:before,.sim-scene { animation:none!important; } }

/* Space-weather simulator: animated visual stage */
.sim-scene {
  --flare-intensity: .4;
  --field-opacity: .4;
  --flare-width: 116px;
  --flare-height: 25px;
  --sun-glow: 30px;
  --sun-glow-wide: 50px;
  --stream-scale: .7;
  position: relative; overflow: hidden; margin: .65rem 0 1rem;
  min-height: 255px; border-radius: 20px;
  border: 1px solid rgba(85,230,242,.28);
  background: radial-gradient(ellipse at 75% 48%, rgba(26,73,111,.35), transparent 42%),
              radial-gradient(ellipse at 15% 35%, rgba(117,45,71,.22), transparent 32%),
              linear-gradient(125deg,#07111f 0%,#0a1930 55%,#10152f 100%);
  box-shadow: inset 0 0 45px rgba(25,108,157,.10), 0 12px 35px rgba(0,0,0,.18);
}
.sim-topline,.sim-scene-footer { display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; padding:13px 16px; color:#9fc4dc; font-size:.68rem; font-weight:800; letter-spacing:.12em; }
.sim-topline span:first-child { color:#55e6f2; }
.sim-cosmos { position:relative; height:170px; overflow:hidden; }
.sim-sun { position:absolute; left:9%; top:40px; width:68px; height:68px; border-radius:50%; background:radial-gradient(circle at 34% 30%,#fff8c4 0%,#ffd166 20%,#ff8a36 54%,#e94b26 78%,#8b1e32 100%); box-shadow:0 0 var(--sun-glow) rgba(255,125,50,.6),0 0 var(--sun-glow-wide) rgba(255,87,34,.25); animation:sim-sun-pulse 3s ease-in-out infinite; }
.sim-sun-core { position:absolute; inset:-8px; border:1px solid rgba(255,187,95,.35); border-radius:50%; animation:sim-sun-ring 4s linear infinite; }
.sim-flare { position:absolute; width:var(--flare-width); height:var(--flare-height); left:48px; top:12px; transform:rotate(-19deg); transform-origin:left center; border-radius:100%; background:linear-gradient(90deg,rgba(255,213,116,.9),rgba(255,111,55,.55),transparent); filter:blur(2px); animation:sim-flare-wave 2.4s ease-in-out infinite; }
.sim-solar-stream { position:absolute; left:18%; top:67px; width:50%; height:32px; background:linear-gradient(90deg,rgba(255,148,61,.35),rgba(255,116,65,.14),transparent); clip-path:polygon(0 25%,100% 0,100% 100%,0 75%); filter:blur(4px); transform:scaleX(var(--stream-scale)); transform-origin:left center; animation:sim-stream 3.2s ease-in-out infinite; }
.sim-earth-system { position:absolute; right:13%; top:40px; width:100px; height:100px; display:flex; align-items:center; justify-content:center; }
.sim-earth { position:relative; z-index:2; width:68px; height:68px; border-radius:50%; overflow:hidden; background:radial-gradient(circle at 30% 28%,#7ce8ff 0%,#277bb4 30%,#123d78 68%,#07152e 100%); box-shadow:0 0 22px rgba(71,190,255,.48),inset -9px -4px 15px rgba(0,0,0,.55); }
.sim-earth:before { content:""; position:absolute; inset:-20%; background:repeating-linear-gradient(115deg,transparent 0 9px,rgba(95,220,166,.72) 10px 15px,transparent 16px 24px); opacity:.55; animation:sim-earth-turn 8s linear infinite; }
.sim-earth-shine { position:absolute; inset:0; border-radius:50%; border-left:2px solid rgba(190,246,255,.85); }
.sim-field { position:absolute; border:1.5px solid rgba(85,230,242,var(--field-opacity)); border-radius:50%; width:140px; height:76px; box-shadow:0 0 9px rgba(85,230,242,.18); animation:sim-field-breathe 4s ease-in-out infinite; }
.sim-field.field-a { transform:rotate(0deg) scaleY(1); }
.sim-field.field-b { width:158px; height:94px; transform:rotate(48deg); animation-delay:-1.2s; }
.sim-field.field-c { width:158px; height:94px; transform:rotate(-48deg); animation-delay:-2.1s; }
.sim-scene-footer { border-top:1px solid rgba(112,171,220,.13); color:#d5e9f6; letter-spacing:.04em; }
.sim-scene-footer b { color:#55e6f2; }
.sim-note { border:1px solid rgba(85,230,242,.22); border-left:3px solid #55e6f2; background:rgba(13,31,49,.72); padding:12px 14px; border-radius:10px; color:#c7dced; font-size:.9rem; }
.sim-result-label { color:#9fb4ca; font-size:.76rem; font-weight:800; text-transform:uppercase; letter-spacing:.1em; }
@keyframes sim-sun-pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.045)} }
@keyframes sim-sun-ring { 0%{transform:scale(.92);opacity:.8} 100%{transform:scale(1.45);opacity:0} }
@keyframes sim-flare-wave { 0%,100%{opacity:.55;transform:rotate(-19deg) scaleX(.85)} 50%{opacity:1;transform:rotate(-14deg) scaleX(1.12)} }
@keyframes sim-stream { 0%,100%{opacity:.45} 50%{opacity:.9} }
@keyframes sim-earth-turn { from{transform:translateX(-8px)} to{transform:translateX(8px)} }
@keyframes sim-field-breathe { 0%,100%{opacity:.6;filter:brightness(.9)} 50%{opacity:1;filter:brightness(1.45)} }
@media (prefers-reduced-motion: reduce) { .sim-sun,.sim-sun-core,.sim-flare,.sim-solar-stream,.sim-earth:before,.sim-field { animation:none !important; } }

</style>
""", unsafe_allow_html=True)

# Give Plotly charts a consistent dark theme.
px.defaults.template = "plotly_dark"

BASE = "https://services.swpc.noaa.gov"

TXT = {
    "en": {
        "title": "🛰️ Space Weather Alert System",
        "caption": "Early warnings for Telecom & Agriculture | Data: NOAA SWPC",
        "settings": "Settings",
        "view": "View",
        "views": ["Telecom", "Farmer"],
        "demo": "Demo mode (simulated May 2024 storm)",
        "state": "Select your state",
        "radio": "HF Radio Blackout",
        "geo": "Geomagnetic Storm",
        "gnss": "GNSS/GPS Concern",
        "farm": "Farm Equipment",
        "none": "None",
        "night": "Night side: not affected",
        "unavail": "Unavailable",
        "levels": ["Low", "Moderate", "High", "Very high"],
        "geo_names": ["Quiet (below G1)", "G1 Minor", "G2 Moderate",
                      "G3 Strong", "G4 Severe", "G5 Extreme"],
        "sev": ["ALL CLEAR", "WATCH", "WARNING", "SEVERE"],
        "banner_sub": ["No disruption expected", "Minor disturbance possible",
                       "Disruption likely", "Severe disruption: act now"],
        "pause": "⛔ PAUSE",
        "caution": "⚠️ Caution",
        "safe": "✅ Safe",
        "advice": "advice",
        "local": "Location-based concern (simplified model, indicative only)",
        "t_r3": "Strong HF blackout on the sunlit side of Earth. "
                "Switch to satellite or alternate links.",
        "t_r1": "Minor to moderate HF disruption possible. Monitor links.",
        "t_ok": "No HF radio disruption expected.",
        "t_kp": "Geomagnetic storm: GNSS timing sources may be less reliable.",
        "f_pause": "GPS accuracy may drop. Pause auto-steer and precision farming equipment.",
        "f_caution": "GPS accuracy may be reduced. Check equipment before autonomous operation.",
        "f_safe": "GPS conditions normal. Safe to run automated equipment.",
        "check": "✅ What should I do?",
        "crop_h": "🌾 Crop-aware farm advisor",
        "crop": "Crop",
        "task": "Task",
        "crop_pause": "⛔ Postpone {task} of {crop} if it needs precise GPS. "
                      "Use manual mode or wait for the alert to clear.",
        "crop_caution": "⚠️ {task} of {crop}: GPS may be less accurate. "
                        "Check equipment and keep manual control ready.",
        "crop_go": "✅ Good conditions for {task} of {crop} with GPS-guided equipment.",
        "crop_nogps": "ℹ️ {task} of {crop} does not depend much on GPS, so you can continue.",
        "sms_h": "📱 SMS / WhatsApp alert",
        "sms_note": "Copy the message below or share it.",
        "wa": "Share on WhatsApp",
        "map": "🗺️ India GNSS concern map",
        "last24": "Last 24 hours",
        "fc": "🔮 Forecast",
        "fc_official": "NOAA official Kp forecast",
        "fc_exp": "Experimental 3-hour trend (not official)",
        "fc_note": "Simple trend estimate for demonstration, not an official forecast.",
        "fc_storm": "Storm possible: Kp may reach 5 or higher in the next hours.",
        "fc_ok": "Low chance of a major storm in the next 3 hours.",
        "hour": "Hour",
        "est": "Estimated Kp",
        "updated": "Data updated (UTC)",
        "stale": "⚠️ Some data is older than 30 minutes. Values may be outdated.",
        "sim": "Simulated data (demo mode)",
        "why": "🔎 Why this alert?",
        "why_geo": "Geomagnetic: Kp {kp:.1f} → {name}. "
                   "NOAA G-scale: G1 starts at Kp 5, G3 at 7, G5 at 9.",
        "why_radio": "Radio: X-ray flux {flux:.2e} W/m² → R{r}. "
                     "NOAA R-scale: R1 starts at 1e-5 W/m².",
        "why_night": "Radio blackout affects the sunlit side only. "
                     "It is currently night in India, so it is not counted.",
        "why_local": "GNSS concern for {state}: Kp {kp:.1f} × latitude factor {f:.1f} "
                     "= {kpl:.1f}. Simplified model, not a measured GPS error.",
        "why_farm": "Farm equipment is paused at local Kp 7 or higher, "
                    "and caution is advised from 5.",
        "hist": "🕘 Alert history (this session)",
        "hist_empty": "No alerts logged yet.",
        "h_cols": ["Time (UTC)", "State", "Level", "Kp", "Radio"],
    },
    "hi": {
        "title": "🛰️ अंतरिक्ष मौसम चेतावनी प्रणाली",
        "caption": "दूरसंचार और खेती के लिए पहले से चेतावनी | डेटा: NOAA SWPC",
        "settings": "सेटिंग्स",
        "view": "देखें",
        "views": ["दूरसंचार", "किसान"],
        "demo": "डेमो मोड (मई 2024 के तूफ़ान का अनुकरण)",
        "state": "अपना राज्य चुनें",
        "radio": "HF रेडियो बाधा",
        "geo": "भू-चुंबकीय तूफ़ान",
        "gnss": "GNSS/GPS की समस्या",
        "farm": "खेती के उपकरण",
        "none": "कोई नहीं",
        "night": "रात का समय: प्रभावित नहीं",
        "unavail": "उपलब्ध नहीं",
        "levels": ["कम", "मध्यम", "ज़्यादा", "बहुत ज़्यादा"],
        "geo_names": ["शांत (G1 से नीचे)", "G1 हल्का", "G2 मध्यम", "G3 तेज़", "G4 गंभीर", "G5 अत्यधिक"],
        "sev": ["सब सामान्य", "नज़र रखें", "चेतावनी", "गंभीर"],
        "banner_sub": ["किसी परेशानी की आशंका नहीं", "हल्की परेशानी हो सकती है", "परेशानी होने की संभावना", "गंभीर परेशानी: तुरंत कदम उठाएँ"],
        "pause": "⛔ रोकें",
        "caution": "⚠️ सावधानी",
        "safe": "✅ सुरक्षित",
        "advice": "सलाह",
        "local": "आपके स्थान के अनुसार चिंता (सरल अनुमान, केवल जानकारी के लिए)",
        "t_r3": "सूरज की ओर वाले हिस्से में HF रेडियो में गंभीर बाधा हो सकती है। सैटेलाइट या दूसरे संपर्क माध्यम का इस्तेमाल करें।",
        "t_r1": "HF रेडियो में हल्की या मध्यम बाधा हो सकती है। संपर्क पर नज़र रखें।",
        "t_ok": "HF रेडियो में बाधा की आशंका नहीं है।",
        "t_kp": "भू-चुंबकीय तूफ़ान के कारण GNSS समय-संकेत कम भरोसेमंद हो सकते हैं।",
        "f_pause": "GPS की सटीकता कम हो सकती है। ऑटो-स्टीयर और GPS से चलने वाले खेती के उपकरण रोक दें।",
        "f_caution": "GPS की सटीकता कम हो सकती है। अपने आप चलने वाले उपकरण इस्तेमाल करने से पहले जाँच लें।",
        "f_safe": "GPS सामान्य है। अपने आप चलने वाले उपकरण चला सकते हैं।",
        "check": "✅ मुझे क्या करना चाहिए?",
        "crop_h": "🌾 फसल के अनुसार खेती की सलाह",
        "crop": "फसल",
        "task": "काम",
        "crop_pause": "⛔ अगर {crop} की {task} में सही GPS ज़रूरी है, तो अभी यह काम टाल दें। हाथ से काम करें या चेतावनी हटने तक इंतज़ार करें।",
        "crop_caution": "⚠️ {crop} की {task}: GPS कम सटीक हो सकता है। उपकरण जाँचें और ज़रूरत पड़ने पर हाथ से चलाने के लिए तैयार रहें।",
        "crop_go": "✅ GPS वाले उपकरणों से {crop} की {task} करने के लिए हालात ठीक हैं।",
        "crop_nogps": "ℹ️ {crop} की {task} में GPS की ज़्यादा ज़रूरत नहीं है, इसलिए आप काम जारी रख सकते हैं।",
        "sms_h": "📱 SMS / WhatsApp चेतावनी संदेश",
        "sms_note": "नीचे दिया गया संदेश कॉपी करें या साझा करें।",
        "wa": "WhatsApp पर भेजें",
        "map": "🗺️ भारत में GNSS समस्या का नक्शा",
        "last24": "पिछले 24 घंटे",
        "fc": "🔮 अनुमान",
        "fc_official": "NOAA का आधिकारिक Kp अनुमान",
        "fc_exp": "प्रयोग के लिए 3 घंटे का रुझान (आधिकारिक नहीं)",
        "fc_note": "यह प्रदर्शन के लिए बनाया गया सरल अनुमान है, आधिकारिक भविष्यवाणी नहीं।",
        "fc_storm": "तूफ़ान आ सकता है: अगले कुछ घंटों में Kp 5 या उससे ज़्यादा हो सकता है।",
        "fc_ok": "अगले 3 घंटों में बड़े तूफ़ान की संभावना कम है।",
        "hour": "घंटा",
        "est": "अनुमानित Kp",
        "updated": "डेटा अपडेट हुआ (UTC)",
        "stale": "⚠️ कुछ डेटा 30 मिनट से पुराना है। मान बदल चुके हो सकते हैं।",
        "sim": "अनुकरण वाला डेटा (डेमो मोड)",
        "why": "🔎 यह चेतावनी क्यों?",
        "why_geo": "भू-चुंबकीय स्थिति: Kp {kp:.1f} → {name}. NOAA के G-स्तर में G1, Kp 5 से; G3, Kp 7 से; और G5, Kp 9 से शुरू होता है।",
        "why_radio": "रेडियो: X-ray ऊर्जा {flux:.2e} W/m² → R{r}. NOAA का R1 स्तर 1e-5 W/m² से शुरू होता है।",
        "why_night": "रेडियो बाधा केवल पृथ्वी के सूरज की ओर वाले हिस्से को प्रभावित करती है। भारत में अभी रात है, इसलिए इसे नहीं गिना गया।",
        "why_local": "{state} के लिए GNSS चिंता: Kp {kp:.1f} × अक्षांश कारक {f:.1f} = {kpl:.1f}. यह सरल अनुमान है, GPS की मापी गई गलती नहीं।",
        "why_farm": "स्थानीय Kp 7 या उससे ज़्यादा होने पर खेती के उपकरण रोकने की सलाह है। Kp 5 से सावधानी रखें।",
        "hist": "🕘 इस सत्र में चेतावनी का इतिहास",
        "hist_empty": "अभी तक कोई चेतावनी दर्ज नहीं हुई है।",
        "h_cols": ["समय (UTC)", "राज्य", "स्तर", "Kp", "रेडियो"],
    },
}

CHK = {
    "en": {
        "telecom": [
            ["Normal operations. No action needed.",
             "Keep monitoring the dashboard."],
            ["Alert the network operations team.",
             "Prepare backup links (satellite or fibre) for HF and timing services.",
             "Check GNSS-based time sync on base stations."],
            ["Switch critical traffic to satellite or fibre links now.",
             "Expect HF radio blackout on the sunlit side: use alternate bands or routes.",
             "Move base-station timing to a backup source."],
        ],
        "farmer": [
            ["GPS is normal. Run automated equipment as planned.",
             "Keep checking before long autonomous jobs."],
            ["Check GPS accuracy before using auto-steer.",
             "Do high-precision jobs (sowing, spraying) with extra care.",
             "Keep a person ready to take manual control."],
            ["Pause auto-steer and GPS-guided machines.",
             "Switch to manual operation or postpone precision jobs.",
             "Wait for the alert to clear, then recalibrate before restarting."],
        ],
    },
    "hi": {
        "telecom": [
            ["सामान्य स्थिति है। किसी कार्रवाई की ज़रूरत नहीं है।", "डैशबोर्ड पर नज़र रखें।"],
            ["नेटवर्क संचालन टीम को सूचना दें।", "HF और समय-संकेत सेवाओं के लिए सैटेलाइट या फाइबर जैसे बैकअप संपर्क तैयार रखें।", "बेस स्टेशन पर GNSS से मिलने वाले समय की जाँच करें।"],
            ["ज़रूरी नेटवर्क ट्रैफ़िक को तुरंत सैटेलाइट या फाइबर पर भेजें।", "सूरज की ओर वाले हिस्से में HF रेडियो बाधित हो सकता है; दूसरे बैंड या रास्ते इस्तेमाल करें।", "बेस स्टेशन का समय बैकअप स्रोत से लें।"],
        ],
        "farmer": [
            ["GPS सामान्य है। खेती के स्वचालित उपकरण योजना के अनुसार चलाएँ।", "लंबे समय तक अपने आप चलने वाले काम से पहले जाँच करते रहें।"],
            ["ऑटो-स्टीयर इस्तेमाल करने से पहले GPS की सटीकता जाँचें।", "बुआई और छिड़काव जैसे सटीक काम सावधानी से करें।", "ज़रूरत पड़ने पर मशीन हाथ से चलाने के लिए किसी व्यक्ति को तैयार रखें।"],
            ["ऑटो-स्टीयर और GPS से चलने वाली मशीनें रोक दें।", "मशीन हाथ से चलाएँ या सटीक काम कुछ समय के लिए टाल दें।", "चेतावनी हटने तक रुकें। दोबारा शुरू करने से पहले मशीन की सेटिंग जाँचें।"],
        ],
    },
}

SMS = {
    "en": [
        "Space weather is normal in {s}. GPS and radio are fine. "
        "Safe to run farm equipment.",
        "Space weather WATCH in {s}: GPS may be less accurate. "
        "Check auto-steer before use.",
        "SPACE WEATHER ALERT in {s}: severe disturbance. "
        "PAUSE GPS-guided equipment and use manual mode.",
    ],
    "hi": [
        "{s} में अंतरिक्ष मौसम सामान्य है। GPS और रेडियो ठीक हैं। खेती के उपकरण सुरक्षित रूप से चला सकते हैं।",
        "{s} में अंतरिक्ष मौसम की चेतावनी: GPS की सटीकता कम हो सकती है। ऑटो-स्टीयर इस्तेमाल करने से पहले जाँच लें।",
        "{s} में अंतरिक्ष मौसम की गंभीर चेतावनी है। GPS से चलने वाले उपकरण रोक दें और मशीन हाथ से चलाएँ।",
    ],
}

STATES = {
    "Jammu & Kashmir": (33.8, 76.6),
    "Himachal Pradesh": (31.9, 77.2),
    "Punjab": (30.9, 75.4),
    "Uttarakhand": (30.1, 79.0),
    "Haryana": (29.1, 76.1),
    "Rajasthan": (26.9, 73.8),
    "Uttar Pradesh": (26.8, 80.9),
    "Assam": (26.2, 92.9),
    "Bihar": (25.6, 85.6),
    "Gujarat": (22.3, 71.6),
    "West Bengal": (23.0, 87.9),
    "Madhya Pradesh": (23.5, 78.6),
    "Jharkhand": (23.6, 85.3),
    "Chhattisgarh": (21.3, 81.8),
    "Odisha": (20.5, 84.4),
    "Maharashtra": (19.5, 76.0),
    "Telangana": (17.9, 79.1),
    "Andhra Pradesh": (15.9, 79.7),
    "Karnataka": (15.3, 75.7),
    "Tamil Nadu": (11.1, 78.6),
    "Kerala": (10.5, 76.3),
}

CROPS = {
    "wheat": ("Wheat", "गेहूँ"),
    "rice": ("Rice", "धान"),
    "sugarcane": ("Sugarcane", "गन्ना"),
    "cotton": ("Cotton", "कपास"),
    "maize": ("Maize", "मक्का"),
}
TASKS = {
    "sowing": ("Sowing", "बुआई", 2),
    "spraying": ("Spraying", "छिड़काव", 2),
    "ploughing": ("Ploughing", "जुताई", 1),
    "harvesting": ("Harvesting", "कटाई", 1),
    "irrigation": ("Irrigation", "सिंचाई", 0),
}

RISK_COLORS = ["#2e9e4f", "#e0a800", "#e8590c", "#c92a2a"]
BANNER_COLORS = ["#1b8a3b", "#b7791f", "#c2410c", "#b91c1c"]


# ---------- Data fetching ----------
@st.cache_data(ttl=300)
def get_xray():
    url = BASE + "/json/goes/primary/xrays-1-day.json"

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    rows = response.json()

    if not isinstance(rows, list) or not rows:
        raise ValueError("NOAA X-ray feed returned no records")

    df = pd.DataFrame(rows)

    required_columns = {"time_tag", "energy", "flux"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "NOAA X-ray feed is missing required columns"
        )

    # Keep the X-ray energy band used by the existing dashboard.
    df = df[df["energy"] == "0.1-0.8nm"].copy()

    if df.empty:
        raise ValueError("No matching NOAA X-ray observations")

    # Normalize timestamps to timezone-aware UTC.
    df["time_tag"] = pd.to_datetime(
        df["time_tag"],
        utc=True,
        errors="coerce"
    )

    # Convert flux to numeric values.
    df["flux"] = pd.to_numeric(
        df["flux"],
        errors="coerce"
    )

    # Remove missing, invalid, infinite, or negative measurements.
    df = df.dropna(subset=["time_tag", "flux"])

    df = df[
        np.isfinite(df["flux"]) &
        (df["flux"] >= 0)
    ].copy()

    # Always put the newest valid observation last.
    df = df.sort_values("time_tag").reset_index(drop=True)

    if df.empty:
        raise ValueError(
            "No valid NOAA X-ray observations remain after validation"
        )

    return df[["time_tag", "flux"]]


@st.cache_data(ttl=300)
def get_kp():
    url = BASE + "/json/planetary_k_index_1m.json"

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    rows = response.json()

    if not isinstance(rows, list) or not rows:
        raise ValueError("NOAA Kp feed returned no records")

    df = pd.DataFrame(rows)

    required_columns = {"time_tag", "estimated_kp"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "NOAA Kp feed is missing required columns"
        )

    # Normalize timestamps to timezone-aware UTC.
    df["time_tag"] = pd.to_datetime(
        df["time_tag"],
        utc=True,
        errors="coerce"
    )

    # Convert Kp measurements to numeric values.
    df["estimated_kp"] = pd.to_numeric(
        df["estimated_kp"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["time_tag", "estimated_kp"]
    )

    # Kp must be within its expected 0–9 range.
    df = df[
        np.isfinite(df["estimated_kp"]) &
        df["estimated_kp"].between(0, 9)
    ].copy()

    # Ensure the newest valid observation is last.
    df = df.sort_values("time_tag").reset_index(drop=True)

    if df.empty:
        raise ValueError(
            "No valid NOAA Kp observations remain after validation"
        )

    return df[["time_tag", "estimated_kp"]]


@st.cache_data(ttl=900)
def get_official_forecast():
    r = requests.get(BASE + "/products/noaa-planetary-k-index-forecast.json", timeout=15)
    r.raise_for_status()
    rows = r.json()
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df["time_tag"] = pd.to_datetime(df["time_tag"])
    df["kp"] = df["kp"].astype(float)
    df = df[df["observed"] == "predicted"][["time_tag", "kp"]].head(8)
    if df.empty:
        raise ValueError("No forecast data")
    return df


# ---------- Risk logic ----------
def radio_level(flux):
    if flux >= 2e-3:
        return 5
    if flux >= 1e-3:
        return 4
    if flux >= 1e-4:
        return 3
    if flux >= 5e-5:
        return 2
    if flux >= 1e-5:
        return 1
    return 0


def geo_idx(kp):
    # Official NOAA G-scale. 0 means below G1.
    if kp >= 9:
        return 5
    if kp >= 8:
        return 4
    if kp >= 7:
        return 3
    if kp >= 6:
        return 2
    if kp >= 5:
        return 1
    return 0


def gnss_idx(kp):
    if kp >= 9:
        return 3
    if kp >= 7:
        return 2
    if kp >= 5:
        return 1
    return 0


def lat_factor(lat):
    if lat >= 30:
        return 1.0
    if lat >= 24:
        return 0.9
    if lat >= 16:
        return 0.8
    return 0.7


def forecast_kp(df, hours=3):
    d = df.tail(180)
    if len(d) < 10:
        return None
    y = d["estimated_kp"].astype(float).values
    slope, _ = np.polyfit(np.arange(len(y)), y, 1)
    last = float(y[-1])
    return [min(9.0, max(0.0, last + slope * 60 * h)) for h in range(1, hours + 1)]


def age_minutes(ts):
    now = datetime.now(timezone.utc)
    ts = pd.to_datetime(ts, utc=True)
    return (now - ts.to_pydatetime()).total_seconds() / 60

def g_label(v):
    g = geo_idx(v)
    return "G" + str(g) if g else "G0"


# ---------- Sidebar ----------
lang_choice = st.sidebar.radio("LANGUAGE", ["English", "Hindi"], horizontal=True)
lk = "en" if lang_choice == "English" else "hi"
li = 0 if lk == "en" else 1
t = TXT[lk]

st.markdown(
    '<div class="mission-kicker"><span class="mission-dot"></span>'
    'SPACE WEATHER OPERATIONS · INDIA MONITORING</div>',
    unsafe_allow_html=True,
)
st.caption(t["caption"])

# ---------- Unified 3D mission-console visual system ----------
st.markdown("""
<style>
:root{--mw-cyan:#65f2ff;--mw-blue:#5b8cff;--mw-violet:#a78bfa;--mw-glass:rgba(18,35,68,.62)}
@keyframes mwFloat{0%,100%{transform:translateY(0) perspective(900px) rotateX(0deg)}50%{transform:translateY(-4px) perspective(900px) rotateX(.7deg)}}
@keyframes mwSheen{0%{background-position:-180% 0}100%{background-position:180% 0}}
@keyframes mwGlow{0%,100%{box-shadow:0 12px 30px rgba(0,0,0,.20),inset 0 1px rgba(255,255,255,.12)}50%{box-shadow:0 18px 42px rgba(39,155,255,.20),inset 0 1px rgba(255,255,255,.22)}}
/* Main dashboard status banner: dimensional glass rather than a flat colour block. */
div[data-testid="stMarkdownContainer"] .mw-status-card{position:relative;overflow:hidden;border:1px solid rgba(140,220,255,.42);border-radius:20px;padding:20px 24px;color:#f6fbff;background:linear-gradient(135deg,rgba(12,30,58,.94),rgba(22,61,102,.88));box-shadow:0 18px 34px rgba(0,0,0,.26),inset 0 1px 0 rgba(255,255,255,.24),inset 0 -12px 24px rgba(4,12,30,.20);transform:perspective(1000px) rotateX(1deg);transition:transform .35s ease,box-shadow .35s ease}
div[data-testid="stMarkdownContainer"] .mw-status-card:before{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 20%,rgba(255,255,255,.11) 45%,transparent 65%);background-size:220% 100%;animation:mwSheen 7s linear infinite;pointer-events:none}
div[data-testid="stMarkdownContainer"] .mw-status-card:hover{transform:perspective(1000px) rotateX(0deg) translateY(-4px);box-shadow:0 24px 46px rgba(20,145,255,.24),inset 0 1px 0 rgba(255,255,255,.3)}
/* Native Streamlit metric, alert and expander surfaces share the same depth. */
div[data-testid="stMetric"]{position:relative;border:1px solid rgba(124,190,255,.26);border-radius:17px;padding:13px 15px;background:linear-gradient(145deg,rgba(30,57,94,.70),rgba(11,24,48,.82));box-shadow:0 9px 20px rgba(0,0,0,.18),inset 0 1px 0 rgba(255,255,255,.12);transition:transform .25s ease,box-shadow .25s ease;overflow:hidden}
div[data-testid="stMetric"]:hover{transform:translateY(-5px) perspective(800px) rotateX(2deg);box-shadow:0 18px 28px rgba(37,145,255,.20),inset 0 1px 0 rgba(255,255,255,.22)}
div[data-testid="stAlert"]{border:1px solid rgba(140,205,255,.34)!important;border-radius:16px!important;box-shadow:0 10px 24px rgba(0,0,0,.16),inset 0 1px 0 rgba(255,255,255,.16);transition:transform .25s ease,box-shadow .25s ease}
div[data-testid="stAlert"]:hover{transform:translateY(-3px);box-shadow:0 16px 30px rgba(40,140,255,.17),inset 0 1px 0 rgba(255,255,255,.22)}
div[data-testid="stExpander"]{border:1px solid rgba(125,190,255,.28);border-radius:16px;overflow:hidden;box-shadow:0 10px 25px rgba(0,0,0,.12);transition:box-shadow .25s ease}
div[data-testid="stExpander"]:hover{box-shadow:0 16px 32px rgba(36,130,255,.15)}
.module-ribbon{display:flex;align-items:center;gap:13px;margin:28px 0 16px;padding:13px 17px;border:1px solid rgba(113,205,255,.26);border-radius:15px;background:linear-gradient(105deg,rgba(17,37,69,.82),rgba(28,25,65,.56));box-shadow:0 10px 24px rgba(0,0,0,.13),inset 0 1px rgba(255,255,255,.10)}.module-ribbon>span{display:grid;place-items:center;width:39px;height:39px;flex:0 0 39px;border-radius:12px;background:linear-gradient(145deg,#6ee7f9,#6677ff);color:#06162d;font-weight:900;box-shadow:0 5px 14px rgba(75,160,255,.25)}.module-ribbon b{display:block;color:#e9f6ff;letter-spacing:.12em;font-size:12px}.module-ribbon small{display:block;color:#9fb8d8;margin-top:3px;font-size:11px}.mw-rec-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:10px 0 14px}
.mw-rec-card{position:relative;min-height:154px;overflow:hidden;border:1px solid rgba(135,205,255,.36);border-radius:18px;padding:17px 17px 18px;background:linear-gradient(145deg,rgba(29,57,94,.92),rgba(11,24,48,.94));color:#edf7ff;box-shadow:0 13px 25px rgba(0,0,0,.22),inset 0 1px 0 rgba(255,255,255,.17),inset 0 -10px 18px rgba(0,0,0,.15);transform:perspective(900px) rotateX(1deg);transition:transform .32s ease,box-shadow .32s ease,border-color .32s ease}
.mw-rec-card:before{content:"";position:absolute;inset:0;background:linear-gradient(112deg,transparent 10%,rgba(255,255,255,.10) 45%,transparent 65%);background-size:230% 100%;animation:mwSheen 8s linear infinite;pointer-events:none}
.mw-rec-card:hover{transform:perspective(900px) translateY(-7px) rotateX(0deg) rotateY(-1deg);box-shadow:0 24px 38px rgba(0,0,0,.30),0 0 24px rgba(72,190,255,.16),inset 0 1px 0 rgba(255,255,255,.24);border-color:rgba(111,230,255,.68)}
.mw-rec-card h4{margin:0 0 10px;font-size:14px;letter-spacing:.08em;text-transform:uppercase;color:#8eeeff}
.mw-rec-card p{margin:0;font-size:13px;line-height:1.55;color:#e2edff}
.mw-rec-card .mw-rec-state{display:inline-block;margin-bottom:10px;padding:4px 8px;border-radius:99px;font-size:10px;letter-spacing:.09em;font-weight:800;background:rgba(91,140,255,.20);border:1px solid rgba(135,190,255,.28)}
@media(max-width:700px){.mw-rec-grid{grid-template-columns:1fr}.mw-rec-card{min-height:unset}}
@media(prefers-reduced-motion:reduce){.mw-status-card:before,.mw-rec-card:before{animation:none}div[data-testid="stMetric"],div[data-testid="stAlert"],.mw-rec-card,.mw-status-card{transition:none}}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class=\"mission-kicker\"><span class=\"mission-dot\"></span>MISSION CONTROLS</div>", unsafe_allow_html=True)
st.sidebar.header(t["settings"])
view = st.sidebar.radio(t["view"], [0, 1], format_func=lambda i: t["views"][i], horizontal=True)
state = st.sidebar.selectbox(
    t["state"], list(STATES.keys()), index=list(STATES).index("Uttar Pradesh")
)
demo = st.sidebar.checkbox(t["demo"])

# ---------- MODULE 01 · SIMULATE ----------
st.markdown('<div class="module-ribbon"><span>01</span><div><b>SIMULATE</b><small>Explore hypothetical space-weather scenarios</small></div></div>', unsafe_allow_html=True)
# ---------- Interactive Space Weather Mission Simulator ----------
SIM_TXT = {
    "en": {
        "title": "🧪 SPACE WEATHER MISSION SIMULATOR",
        "caption": "Change the controls to test a hypothetical solar flare and geomagnetic disturbance. This sandbox does not change the live dashboard or send alerts.",
        "flux": "Solar X-ray flux (log₁₀ exponent)",
        "flux_help": "Choose a simulated X-ray flux. The scale is logarithmic because flux values span many orders of magnitude.",
        "kp": "Geomagnetic disturbance (Kp index)",
        "kp_help": "Kp is a geomagnetic activity index from 0 to 9; it is not a direct magnetic-field strength measurement in nT.",
        "visual": "SIMULATION ACTIVE",
        "hypothetical": "HYPOTHETICAL CONDITIONS",
        "flux_unit": "Simulated flux",
        "kp_note": "0 = quiet · 5 = G1 threshold · 9 = extreme Kp value",
        "xray_footer": "X-RAY FLUX",
        "kp_footer": "GEOMAGNETIC Kp",
        "selected": "Selected scenario",
        "baseline_note": "Simulator baseline: X-ray flux 1e-6 W/m² and Kp 2.0. Values are separate from live NOAA data; no alerts are sent.",
        "flux_delta": "orders of magnitude vs baseline",
        "flux_axis": "X-ray flux (W/m²)",
        "radio_axis": "App radio-risk level",
        "kp_axis": "Kp index",
        "geo_axis": "Geomagnetic category index",
        "flux_metric": "Simulated X-ray flux",
        "radio_metric": "Radio-risk level (app rules)",
        "kp_metric": "Simulated Kp",
        "geo_metric": "Geomagnetic category",
        "gnss_metric": "GNSS concern (simplified)",
        "comparison": "BASELINE VS YOUR SCENARIO",
        "metric": "Indicator",
        "baseline": "Baseline",
        "scenario": "Your scenario",
        "xrayrow": "Solar X-ray flux",
        "radiorow": "Radio-risk category",
        "kprow": "Geomagnetic activity (Kp)",
        "georow": "Geomagnetic category",
        "localrow": "Simplified local Kp estimate",
        "gnssrow": "GNSS concern category",
        "radio_chart": "How X-ray flux changes the app's radio-risk category",
        "geo_chart": "How Kp changes the geomagnetic category",
        "recommendation": "WHAT WOULD THE APP RECOMMEND?",
        "warning": "SIMULATION ONLY — these are hypothetical inputs and rule-based estimates, not live NOAA readings, measured GPS errors, or an official warning.",
        "radio_high": "High simulated X-ray flux: the app's rules indicate a stronger HF radio-blackout concern. Telecom operators should review alternate communication paths.",
        "radio_mid": "Elevated simulated X-ray flux: monitor HF radio conditions and communication links.",
        "radio_low": "The selected simulated X-ray flux is below this app's radio-risk thresholds.",
        "geo_high": "Strong simulated geomagnetic disturbance: review GNSS-based timing and navigation dependencies.",
        "geo_mid": "Some geomagnetic activity is simulated: monitor GNSS performance and keep backup procedures available.",
        "geo_low": "The selected Kp-like value is below the app's G1 threshold.",
        "farmer_high": "Farmer view: for GPS-dependent precision work, verify receiver accuracy and keep manual control available. This simulation alone cannot determine whether a real machine is safe.",
        "farmer_mid": "Farmer view: check GPS accuracy before precision work and be ready to switch to manual control.",
        "farmer_low": "Farmer view: no elevated concern is indicated by these simulated rules; follow normal equipment checks.",
        "telecom": "Telecom view: check alternate links and backup timing procedures according to your network's operational policy.",
    },
    "hi": {
        "title": "🧪 अंतरिक्ष मौसम मिशन सिम्युलेटर",
        "caption": "काल्पनिक सौर फ्लेयर और भू-चुंबकीय गड़बड़ी देखने के लिए स्लाइडर बदलें। यह सिमुलेशन लाइव डैशबोर्ड को नहीं बदलता और कोई अलर्ट नहीं भेजता।",
        "flux": "सौर X-ray फ्लक्स (log₁₀ घातांक)",
        "flux_help": "काल्पनिक X-ray फ्लक्स चुनें। मान बहुत अलग-अलग स्तरों पर होते हैं, इसलिए विकल्प क्रमिक पैमाने पर हैं।",
        "kp": "भू-चुंबकीय गतिविधि (Kp सूचकांक)",
        "kp_help": "Kp 0 से 9 तक भू-चुंबकीय गतिविधि का सूचकांक है। यह nT में सीधे चुंबकीय क्षेत्र की ताकत नहीं है।",
        "visual": "सिमुलेशन चालू",
        "hypothetical": "काल्पनिक स्थिति",
        "flux_unit": "काल्पनिक फ्लक्स",
        "kp_note": "0 = शांत · 5 = G1 सीमा · 9 = अत्यधिक Kp मान",
        "xray_footer": "X-RAY फ्लक्स",
        "kp_footer": "भू-चुंबकीय Kp",
        "selected": "चुनी गई स्थिति",
        "baseline_note": "सिमुलेशन का सामान्य आधार: X-ray फ्लक्स 1e-6 W/m² और Kp 2.0। ये मान लाइव NOAA डेटा से अलग हैं; कोई अलर्ट नहीं भेजा जाता।",
        "flux_delta": "सामान्य आधार से परिमाण का अंतर",
        "flux_axis": "X-ray फ्लक्स (W/m²)",
        "radio_axis": "ऐप का रेडियो जोखिम स्तर",
        "kp_axis": "Kp सूचकांक",
        "geo_axis": "भू-चुंबकीय श्रेणी सूचकांक",
        "flux_metric": "काल्पनिक X-ray फ्लक्स",
        "radio_metric": "रेडियो जोखिम स्तर (ऐप के नियम)",
        "kp_metric": "काल्पनिक Kp",
        "geo_metric": "भू-चुंबकीय श्रेणी",
        "gnss_metric": "GNSS चिंता (सरल अनुमान)",
        "comparison": "सामान्य स्थिति बनाम आपका सिमुलेशन",
        "metric": "संकेतक",
        "baseline": "सामान्य आधार",
        "scenario": "आपकी स्थिति",
        "xrayrow": "सौर X-ray फ्लक्स",
        "radiorow": "रेडियो जोखिम श्रेणी",
        "kprow": "भू-चुंबकीय गतिविधि (Kp)",
        "georow": "भू-चुंबकीय श्रेणी",
        "localrow": "सरल स्थानीय Kp अनुमान",
        "gnssrow": "GNSS चिंता श्रेणी",
        "radio_chart": "X-ray फ्लक्स बदलने पर रेडियो जोखिम कैसे बदलता है",
        "geo_chart": "Kp बदलने पर भू-चुंबकीय श्रेणी कैसे बदलती है",
        "recommendation": "ऐप क्या सलाह देगा?",
        "warning": "केवल सिमुलेशन — ये काल्पनिक मान और नियम-आधारित अनुमान हैं, लाइव NOAA माप, वास्तविक GPS त्रुटि या आधिकारिक चेतावनी नहीं।",
        "radio_high": "काल्पनिक X-ray फ्लक्स अधिक है: ऐप के नियमों में HF रेडियो व्यवधान की चिंता बढ़ती है। दूरसंचार टीम वैकल्पिक संचार मार्ग जाँचे।",
        "radio_mid": "काल्पनिक X-ray फ्लक्स बढ़ा हुआ है: HF रेडियो स्थिति और संचार लिंक पर नज़र रखें।",
        "radio_low": "चुना गया काल्पनिक X-ray फ्लक्स इस ऐप की रेडियो जोखिम सीमाओं से नीचे है।",
        "geo_high": "काल्पनिक भू-चुंबकीय गड़बड़ी तेज़ है: GNSS आधारित समय और नेविगेशन की निर्भरता जाँचें।",
        "geo_mid": "कुछ भू-चुंबकीय गतिविधि दिखाई गई है: GNSS प्रदर्शन पर नज़र रखें और बैकअप प्रक्रिया तैयार रखें।",
        "geo_low": "चुना गया Kp मान ऐप की G1 सीमा से नीचे है।",
        "farmer_high": "किसान मोड: GPS पर निर्भर सटीक काम से पहले रिसीवर की सटीकता जाँचें और मशीन को हाथ से चलाने की तैयारी रखें। केवल यह सिमुलेशन असली मशीन की सुरक्षा तय नहीं कर सकता।",
        "farmer_mid": "किसान मोड: सटीक खेती के काम से पहले GPS जाँचें और हाथ से नियंत्रण के लिए तैयार रहें।",
        "farmer_low": "किसान मोड: इन काल्पनिक नियमों से बढ़ी हुई चिंता नहीं दिखती। सामान्य उपकरण जाँच जारी रखें।",
        "telecom": "दूरसंचार मोड: अपने नेटवर्क की प्रक्रिया के अनुसार वैकल्पिक लिंक और बैकअप टाइमिंग जाँचें।",
    }
}
_sim = SIM_TXT[lk]

with st.expander(_sim["title"], expanded=True):
    st.caption(_sim["caption"])
    st.markdown(
        '<div class="sim-note">⚠️ ' + _sim["warning"] + '</div>',
        unsafe_allow_html=True,
    )

    sim_left, sim_right = st.columns([1, 1], gap="large")
    with sim_left:
        sim_log_flux = st.slider(
            _sim["flux"], min_value=-8.0, max_value=-2.0, value=-6.0,
            step=0.1, format="%.1f", help=_sim["flux_help"],
            key="mission_sim_xray_log",
        )
        sim_flux = 10.0 ** float(sim_log_flux)
        st.caption(f"{_sim['flux_unit']}: {sim_flux:.2e} W/m²")
    with sim_right:
        sim_kp = st.slider(
            _sim["kp"], min_value=0.0, max_value=9.0, value=2.0,
            step=0.5, help=_sim["kp_help"], key="mission_sim_kp",
        )
        st.caption(_sim["kp_note"])

    sim_lat, sim_lon = STATES[state]
    sim_factor = lat_factor(sim_lat)
    sim_local_kp = sim_kp * sim_factor
    sim_radio = radio_level(float(sim_flux))
    sim_geo = geo_idx(float(sim_kp))
    sim_gnss = gnss_idx(float(sim_local_kp))
    sim_base_flux = 1e-6
    sim_base_kp = 2.0
    sim_base_radio = radio_level(sim_base_flux)
    sim_base_geo = geo_idx(sim_base_kp)
    sim_base_local = sim_base_kp * sim_factor
    sim_base_gnss = gnss_idx(sim_base_local)
    flare_intensity = max(0.0, min(1.0, (np.log10(float(sim_flux)) + 8.0) / 6.0))
    field_opacity = 0.22 + (float(sim_kp) / 9.0) * 0.72
    flare_width = 80.0 + 90.0 * flare_intensity
    flare_height = 18.0 + 18.0 * flare_intensity
    sun_glow = 15.0 + 36.0 * flare_intensity
    sun_glow_wide = 25.0 + 55.0 * flare_intensity
    stream_scale = 0.5 + flare_intensity

    st.markdown(
        f'''<div class="sim-scene" style="--flare-intensity:{flare_intensity:.3f};--field-opacity:{field_opacity:.3f};--flare-width:{flare_width:.1f}px;--flare-height:{flare_height:.1f}px;--sun-glow:{sun_glow:.1f}px;--sun-glow-wide:{sun_glow_wide:.1f}px;--stream-scale:{stream_scale:.3f};">
          <div class="sim-topline"><span>● {_sim["visual"]}</span><span>{_sim["hypothetical"]}</span></div>
          <div class="sim-cosmos">
            <div class="sim-sun"><div class="sim-sun-core"></div><div class="sim-flare"></div></div>
            <div class="sim-solar-stream"></div>
            <div class="sim-earth-system"><div class="sim-field field-a"></div><div class="sim-field field-b"></div><div class="sim-field field-c"></div><div class="sim-earth"><div class="sim-earth-shine"></div></div></div>
          </div>
          <div class="sim-scene-footer"><span>☀ {_sim["xray_footer"]}: <b>{float(sim_flux):.2e} W/m²</b></span><span>◉ {_sim["kp_footer"]}: <b>{float(sim_kp):.1f} / 9</b></span></div>
        </div>''',
        unsafe_allow_html=True,
    )

    st.markdown("#### " + _sim["comparison"])
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(_sim["flux_metric"], f"{float(sim_flux):.2e} W/m²", f"{np.log10(float(sim_flux) / sim_base_flux):+.1f} {_sim['flux_delta']}")
    m2.metric(_sim["radio_metric"], f"R{sim_radio}", f"{_sim['baseline']} R{sim_base_radio}", delta_color="off")
    m3.metric(_sim["geo_metric"], g_label(sim_kp), f"Kp {sim_kp:.1f} · {_sim['baseline']} {g_label(sim_base_kp)}", delta_color="off")
    m4.metric(_sim["gnss_metric"], t["levels"][sim_gnss], f"{_sim['localrow']}: {sim_local_kp:.1f}", delta_color="off")

    sim_table = pd.DataFrame([
        {_sim["metric"]: _sim["xrayrow"], _sim["baseline"]: f"{sim_base_flux:.1e} W/m²", _sim["scenario"]: f"{float(sim_flux):.1e} W/m²"},
        {_sim["metric"]: _sim["radiorow"], _sim["baseline"]: f"R{sim_base_radio}", _sim["scenario"]: f"R{sim_radio}"},
        {_sim["metric"]: _sim["kprow"], _sim["baseline"]: f"{sim_base_kp:.1f}", _sim["scenario"]: f"{float(sim_kp):.1f}"},
        {_sim["metric"]: _sim["georow"], _sim["baseline"]: g_label(sim_base_kp), _sim["scenario"]: g_label(sim_kp)},
        {_sim["metric"]: _sim["localrow"], _sim["baseline"]: f"{sim_base_local:.1f}", _sim["scenario"]: f"{sim_local_kp:.1f}"},
        {_sim["metric"]: _sim["gnssrow"], _sim["baseline"]: t["levels"][sim_base_gnss], _sim["scenario"]: t["levels"][sim_gnss]},
    ])
    st.dataframe(sim_table, hide_index=True, width="stretch")

    chart_left, chart_right = st.columns(2, gap="large")
    flux_curve = np.logspace(-8, -2, 100)
    radio_curve_df = pd.DataFrame({
        _sim["flux_axis"]: flux_curve,
        _sim["radio_axis"]: [radio_level(float(value)) for value in flux_curve],
    })
    radio_fig = px.line(radio_curve_df, x=_sim["flux_axis"], y=_sim["radio_axis"], log_x=True, title=_sim["radio_chart"])
    radio_fig.add_scatter(x=[float(sim_flux)], y=[sim_radio], mode="markers", name=_sim["selected"], marker={"size": 12, "color": "#ff9b54"})
    radio_fig.update_yaxes(dtick=1, range=[-0.2, 5.3])
    radio_fig.update_layout(margin=dict(l=8, r=8, t=55, b=8), height=310)
    chart_left.plotly_chart(radio_fig, use_container_width=True, key="mission_sim_radio_curve")

    kp_curve = np.arange(0, 9.01, 0.25)
    geo_curve_df = pd.DataFrame({
        _sim["kp_axis"]: kp_curve,
        _sim["geo_axis"]: [geo_idx(float(value)) for value in kp_curve],
    })
    geo_fig = px.line(geo_curve_df, x=_sim["kp_axis"], y=_sim["geo_axis"], title=_sim["geo_chart"])
    geo_fig.add_scatter(x=[float(sim_kp)], y=[sim_geo], mode="markers", name=_sim["selected"], marker={"size": 12, "color": "#55e6f2"})
    geo_fig.update_xaxes(dtick=1, range=[0, 9])
    geo_fig.update_yaxes(dtick=1, range=[-0.2, 5.3])
    geo_fig.update_layout(margin=dict(l=8, r=8, t=55, b=8), height=310)
    chart_right.plotly_chart(geo_fig, use_container_width=True, key="mission_sim_geo_curve")

    st.markdown("#### " + _sim["recommendation"])
    radio_advice = _sim["radio_high"] if sim_radio >= 3 else (_sim["radio_mid"] if sim_radio >= 1 else _sim["radio_low"])
    geo_advice = _sim["geo_high"] if sim_local_kp >= 5 else (_sim["geo_mid"] if sim_local_kp >= 3 else _sim["geo_low"])
    if view == 1:
        action_advice = _sim["farmer_high"] if sim_local_kp >= 7 else (_sim["farmer_mid"] if sim_local_kp >= 5 else _sim["farmer_low"])
        action_title = "FARMER ACTION PLAN"
    else:
        action_advice = _sim["telecom"]
        action_title = "TELECOM ACTION PLAN"
    def _card_state(high, medium):
        return "ELEVATED CONCERN" if high else ("MONITOR" if medium else "LOW CONCERN")
    recommendation_html = f'''<div class="mw-rec-grid">
      <article class="mw-rec-card"><span class="mw-rec-state">{_card_state(sim_radio >= 3, sim_radio >= 1)}</span><h4>◉ RADIO / X-RAY</h4><p>{radio_advice}</p></article>
      <article class="mw-rec-card"><span class="mw-rec-state">{_card_state(sim_local_kp >= 5, sim_local_kp >= 3)}</span><h4>⌁ GEOMAGNETIC / GNSS</h4><p>{geo_advice}</p></article>
      <article class="mw-rec-card"><span class="mw-rec-state">SCENARIO GUIDANCE</span><h4>✦ {action_title}</h4><p>{action_advice}</p></article>
    </div>'''
    st.markdown(recommendation_html, unsafe_allow_html=True)
    st.caption(_sim["baseline_note"])

# ---------- End interactive simulator ----------


# ---------- Simulated IoT Monitoring Module ----------

iot_enabled = st.sidebar.checkbox(
    "📡 Enable IoT Simulation Mode",
    value=False,
)

iot_disconnected = False

if iot_enabled:
    iot_disconnected = st.sidebar.checkbox(
        "🔌 Simulate IoT Device Disconnection",
        value=False,
    )


@st.fragment(run_every="5s")
def render_iot_simulator(enabled, disconnected):
    if not enabled:
        return

    st.subheader("📡 IoT Sensor Monitoring")
    st.caption(
        "SIMULATION ONLY — these readings are generated by Python, "
        "not measured by a physical sensor."
    )

    # Initialize session history
    if "iot_history" not in st.session_state:
        st.session_state.iot_history = []

    if disconnected:
        st.error(
            "🔴 Simulated IoT device disconnected. "
            "No new sensor readings are being generated."
        )
    else:
        # Generate illustrative three-axis magnetic field readings.
        # These values are synthetic and do not represent real conditions.
        bx = 20.0 + float(np.random.normal(0, 0.05))
        by = 15.0 + float(np.random.normal(0, 0.05))
        bz = 35.0 + float(np.random.normal(0, 0.05))

        magnitude = float(np.sqrt(bx**2 + by**2 + bz**2))

        reading = {
            "Time (UTC)": datetime.now(timezone.utc),
            "Bx (µT)": round(bx, 3),
            "By (µT)": round(by, 3),
            "Bz (µT)": round(bz, 3),
            "Magnitude (µT)": round(magnitude, 3),
        }

        st.session_state.iot_history.append(reading)

        # Keep only the latest 120 simulated readings.
        st.session_state.iot_history = (
            st.session_state.iot_history[-120:]
        )

        st.success("🟢 Simulated IoT device connected")

    history = st.session_state.iot_history

    if history:
        history_df = pd.DataFrame(history)

        latest = history_df.iloc[-1]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Magnetic Field Magnitude",
            f"{latest['Magnitude (µT)']:.3f} µT",
        )

        c2.metric(
            "Latest Bx Reading",
            f"{latest['Bx (µT)']:.3f} µT",
        )

        c3.metric(
            "Latest Bz Reading",
            f"{latest['Bz (µT)']:.3f} µT",
        )

        st.markdown("#### 📈 Simulated Sensor History")

        chart_df = history_df.set_index("Time (UTC)")

        st.line_chart(
            chart_df[["Magnitude (µT)"]]
        )

        st.markdown("#### Recent Sensor Readings")

        st.dataframe(
            history_df.tail(10).iloc[::-1],
            hide_index=True,
            width="stretch",
        )
    else:
        st.info(
            "No simulated readings have been collected yet."
        )


# Display the IoT panel without replacing the existing dashboard.
render_iot_simulator(iot_enabled, iot_disconnected)

# ---------- End of Simulated IoT Module ----------

# ---------- MODULE 02 · LIVE SITUATIONAL AWARENESS ----------
st.markdown('<div class="module-ribbon"><span>02</span><div><b>LIVE MONITORING & ADVISORY</b><small>Official observations · current risk · operational guidance · map and forecast</small></div></div>', unsafe_allow_html=True)
# ---------- Data (each feed fails on its own) ----------
xray_df = None
kp_df = None
flux = None
kp = None

if demo:
    flux, kp = 8.7e-4, 9.0
    times = pd.date_range(end=pd.Timestamp.now(), periods=60, freq="min")
    xray_df = pd.DataFrame({
        "time_tag": times,
        "flux": [1e-6 * (1.12 ** i) for i in range(60)],
    })
    kp_df = pd.DataFrame({
        "time_tag": times,
        "estimated_kp": [3 + i * 0.1 for i in range(60)],
    })
else:
    try:
        xray_df = get_xray()
        flux = float(xray_df["flux"].iloc[-1])
    except Exception:
        xray_df = None
    try:
        kp_df = get_kp()
        kp = float(kp_df["estimated_kp"].iloc[-1])
    except Exception:
        kp_df = None
    if xray_df is None and kp_df is None:
        st.error("Could not fetch live data from NOAA. "
                 "Check your internet and try again, or use Demo mode.")
        st.stop()

flux_v = flux if flux is not None else 0.0
kp_v = kp if kp is not None else 0.0

# ---------- Data freshness ----------
if demo:
    st.caption("ℹ️ " + t["sim"])
else:
    parts = []
    stale = False
    if xray_df is not None:
        ts = xray_df["time_tag"].iloc[-1]
        parts.append("X-ray " + ts.strftime("%H:%M"))
        stale = stale or age_minutes(ts) > 30
    if kp_df is not None:
        ts = kp_df["time_tag"].iloc[-1]
        parts.append("Kp " + ts.strftime("%H:%M"))
        stale = stale or age_minutes(ts) > 30
    st.caption("🕒 " + t["updated"] + ": " + " · ".join(parts))
    if stale:
        st.warning(t["stale"])

# ---------- Location-based concern ----------
lat, lon = STATES[state]
ist_hour = (datetime.now(timezone.utc) + timedelta(hours=5.5)).hour
daytime = demo or (6 <= ist_hour < 18)
r_global = radio_level(flux_v)
r_loc = r_global if daytime else 0
factor = lat_factor(lat)
kp_loc = kp_v * factor
g_now = geo_idx(kp_v)
c_idx = gnss_idx(kp_loc)
pause = kp_loc >= 7
caution = kp_loc >= 5

# ---------- MODULE 02 add-on · Solar flare + GNSS degradation monitor ----------
st.markdown("""
<style>
.sd-feature-card{position:relative;overflow:hidden;border:1px solid rgba(85,230,242,.25);border-radius:18px;padding:18px 20px;margin:10px 0 14px;background:linear-gradient(125deg,rgba(10,32,55,.94),rgba(17,38,70,.82));box-shadow:0 12px 28px rgba(0,0,0,.18),inset 0 1px rgba(255,255,255,.08);transition:transform .25s ease,box-shadow .25s ease}
.sd-feature-card:hover{transform:translateY(-3px);box-shadow:0 18px 34px rgba(25,165,220,.18)}
.sd-feature-card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,#55e6f2,#6677ff);box-shadow:0 0 18px rgba(85,230,242,.45)}
.sd-feature-title{font-size:17px;font-weight:800;color:#eff8ff;margin-bottom:5px}.sd-feature-sub{font-size:12px;color:#a8bfd7;line-height:1.5}
.sd-live-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#59f3bc;box-shadow:0 0 12px #59f3bc;margin-right:8px;animation:sdPulse 1.8s infinite}
.sd-flare-dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:#ff9366;box-shadow:0 0 14px #ff754d;margin-right:8px;animation:sdPulse 1.2s infinite}
@keyframes sdPulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.45;transform:scale(.82)}}
@media(prefers-reduced-motion:reduce){.sd-live-dot,.sd-flare-dot{animation:none}.sd-feature-card{transition:none}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="sd-feature-card"><div class="sd-feature-title"><span class="sd-live-dot"></span>Solar Flare & Radio-Blackout Monitor</div><div class="sd-feature-sub">Uses the latest available NOAA X-ray flux reading. Flare class and radio-blackout risk are separate indicators; this is monitoring, not a guarantee of impact at a specific location.</div></div>', unsafe_allow_html=True)

def _solar_class(flux_value):
    if flux_value >= 1e-4:
        return "X-class", 4
    if flux_value >= 1e-5:
        return "M-class", 3
    if flux_value >= 1e-6:
        return "C-class", 2
    if flux_value >= 1e-7:
        return "B-class", 1
    return "A-class / below", 0

solar_class, solar_class_idx = _solar_class(max(float(flux_v), 0.0))
flare_cols = st.columns(4)
flare_cols[0].metric("Latest X-ray flux", f"{flux_v:.2e} W/m²", help="Latest value returned by the app's NOAA X-ray feed; if unavailable, the dashboard uses its existing fallback value.")
flare_cols[1].metric("X-ray flare class", solar_class, help="Simplified A/B/C/M/X classification from X-ray flux thresholds.")
flare_cols[2].metric("App radio-risk category", f"R{r_global}", help="The app's rule-based radio-risk category; the official NOAA R scale has its own operational definitions.")
flare_cols[3].metric("Geomagnetic level", g_label(kp_v), f"Kp {kp_v:.1f}")
if solar_class_idx >= 3:
    st.warning("Elevated X-ray flux detected by the current feed. Review the radio-risk card and current official space-weather bulletins; this app's class estimate is not a standalone official alert.")
else:
    st.caption("No M/X-class threshold is indicated by the current X-ray value in this simplified classification. Continue monitoring live data and data freshness.")

with st.expander("☀️ Test a simulated solar-flare event", expanded=False):
    st.caption("DEMO ONLY — these controls do not change the live readings, send messages, or represent a real observed flare.")
    sim_flare_on = st.checkbox("Enable simulated solar flare", key="sd_sim_flare_on")
    sim_flare_flux = st.select_slider("Simulated X-ray flux (W/m²)", options=[1e-7, 1e-6, 1e-5, 1e-4, 1e-3], value=1e-4, format_func=lambda x: f"{x:.0e}", key="sd_sim_flare_flux")
    if sim_flare_on:
        sim_class, _ = _solar_class(float(sim_flare_flux))
        sim_radio = radio_level(float(sim_flare_flux))
        st.error(f"SIMULATED EVENT · {sim_class} solar X-ray level · app radio-risk R{sim_radio}")
        st.write("Recommended demo response: review HF radio links, verify backup communication paths, and acknowledge the simulated event.")
        if st.button("Acknowledge simulated flare", key="sd_ack_flare"):
            st.session_state.setdefault("sd_audit_log", []).append({"Time (UTC)": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), "Event": "Simulated solar flare", "Evidence": f"Flux {sim_flare_flux:.0e} W/m²; {sim_class}; R{sim_radio}", "Action": "Acknowledged"})
            st.success("Simulated event acknowledged and added to this session's audit trail.")

st.markdown('<div class="sd-feature-card"><div class="sd-feature-title"><span class="sd-live-dot"></span>GNSS Degradation Monitoring</div><div class="sd-feature-sub">The current app does not connect to a physical GNSS receiver. Use this clearly labelled test panel to simulate a receiver position error and check the response threshold. Actual degradation requires real receiver/reference measurements.</div></div>', unsafe_allow_html=True)
gnss_col1, gnss_col2 = st.columns(2)
with gnss_col1:
    gnss_error_m = st.slider("Simulated GNSS position error (metres)", min_value=0.0, max_value=50.0, value=2.0, step=0.5, key="sd_gnss_error_m")
with gnss_col2:
    gnss_limit_m = st.slider("Configured error limit (metres)", min_value=1.0, max_value=20.0, value=5.0, step=0.5, key="sd_gnss_limit_m")
gnss_exceeded = gnss_error_m > gnss_limit_m
gnss_status = "OPERATOR_REVIEW" if gnss_exceeded else "NORMAL · SIMULATED"
gnss_m1, gnss_m2, gnss_m3 = st.columns(3)
gnss_m1.metric("Receiver error", f"{gnss_error_m:.1f} m")
gnss_m2.metric("Configured limit", f"{gnss_limit_m:.1f} m")
gnss_m3.metric("Demo controller", "OPERATOR_REVIEW" if gnss_exceeded else "MONITORING")
if gnss_exceeded:
    st.error("GNSS DEGRADATION SIMULATION: receiver error exceeds the configured limit. Ask the operator to review positioning and switch to manual control where appropriate.")
else:
    st.success("No threshold breach in this simulated receiver input. This does not confirm that a real GNSS receiver is healthy.")
if st.button("Record GNSS test event in audit trail", key="sd_record_gnss"):
    st.session_state.setdefault("sd_audit_log", []).append({"Time (UTC)": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), "Event": "Simulated GNSS receiver check", "Evidence": f"Error {gnss_error_m:.1f} m; configured limit {gnss_limit_m:.1f} m", "Action": gnss_status})
    st.success("GNSS test event recorded in this session's audit trail.")

if st.session_state.get("sd_audit_log"):
    with st.expander("🧾 Demo audit trail", expanded=False):
        st.dataframe(pd.DataFrame(st.session_state.sd_audit_log[::-1]), hide_index=True, width="stretch")

r_sev = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 3}[r_loc]
sev = max(c_idx, r_sev)
tier = 2 if (pause or sev >= 3) else (1 if sev >= 1 else 0)



# ---------- Alert history ----------
if "hist" not in st.session_state:
    st.session_state.hist = []
hkey = (state, sev, demo)
if st.session_state.get("last_hkey") != hkey:
    st.session_state.last_hkey = hkey
    if sev >= 1:
        cols = t["h_cols"]
        st.session_state.hist.append({
            cols[0]: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
            cols[1]: state,
            cols[2]: t["sev"][sev] + (" (demo)" if demo else ""),
            cols[3]: round(kp_v, 1),
            cols[4]: ("R" + str(r_loc)) if r_loc else "-",
        })

# ---------- Banner ----------
glow = "animation: pulse 2s infinite;" if sev >= 2 else ""
banner_html = """
<style>
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.45); }
  70% { box-shadow: 0 0 0 18px rgba(255,255,255,0); }
  100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
}
</style>
<div class="mw-status-card" style="border-color:__BG__;__GLOW__">
  <div style="font-size:12px;letter-spacing:.12em;opacity:.88;">◉ LIVE STATUS · __STATE__</div>
  <div style="font-size:clamp(23px,3vw,31px);font-weight:850;letter-spacing:-.02em;margin:6px 0 4px;">__SEV__</div>
  <div style="font-size:15px;opacity:.92;">__SUB__</div>
</div>
"""
banner_html = (
    banner_html.replace("__BG__", BANNER_COLORS[sev])
    .replace("__GLOW__", glow)
    .replace("__STATE__", state)
    .replace("__SEV__", t["sev"][sev])
    .replace("__SUB__", t["banner_sub"][sev])
)
st.markdown(banner_html, unsafe_allow_html=True)
st.write("")

# ---------- Separate hazard cards ----------
st.caption(t["local"])
c1, c2, c3, c4 = st.columns(4)

if flux is None:
    c1.metric(t["radio"], t["unavail"])
else:
    c1.metric(
        t["radio"],
        ("R" + str(r_loc)) if r_loc else t["none"],
        ("X-ray {:.2e} W/m²".format(flux)) if daytime else t["night"],
        delta_color="off",
    )

if kp is None:
    c2.metric(t["geo"], t["unavail"])
    c3.metric(t["gnss"], t["unavail"])
    c4.metric(t["farm"], t["unavail"])
else:
    c2.metric(t["geo"], "G" + str(g_now), "Kp {:.1f}".format(kp), delta_color="off")
    c3.metric(
        t["gnss"],
        t["levels"][c_idx],
        "Kp {:.1f} → {:.1f}".format(kp, kp_loc),
        delta_color="off",
    )
    c4.metric(
        t["farm"],
        t["pause"] if pause else (t["caution"] if caution else t["safe"]),
    )

# ---------- Why this alert? ----------
with st.expander(t["why"]):
    if kp is not None:
        st.markdown("- " + t["why_geo"].format(kp=kp, name=t["geo_names"][g_now]))
    if flux is not None:
        st.markdown("- " + t["why_radio"].format(flux=flux, r=r_global))
        if not daytime:
            st.markdown("- " + t["why_night"])
    if kp is not None:
        st.markdown("- " + t["why_local"].format(state=state, kp=kp, f=factor, kpl=kp_loc))
        st.markdown("- " + t["why_farm"])

# ---------- Advice + checklist ----------
st.subheader(t["views"][view] + " " + t["advice"])
if view == 0:
    if r_loc >= 3:
        st.error(t["t_r3"])
    elif r_loc >= 1:
        st.warning(t["t_r1"])
    else:
        st.success(t["t_ok"])
    if kp_loc >= 5:
        st.warning(t["t_kp"])
    role = "telecom"
else:
    if pause:
        st.error(t["f_pause"])
    elif caution:
        st.warning(t["f_caution"])
    else:
        st.success(t["f_safe"])
    role = "farmer"

st.markdown("**" + t["check"] + "**")
for item in CHK[lk][role][tier]:
    st.markdown("- " + item)

# ---------- Crop-aware advisor (farmer view) ----------
if view == 1:
    st.subheader(t["crop_h"])
    cc1, cc2 = st.columns(2)
    crop_key = cc1.selectbox(t["crop"], list(CROPS.keys()), format_func=lambda k: CROPS[k][li])
    task_key = cc2.selectbox(t["task"], list(TASKS.keys()), format_func=lambda k: TASKS[k][li])
    need = TASKS[task_key][2]
    names = {"crop": CROPS[crop_key][li], "task": TASKS[task_key][li]}
    if need == 0:
        st.info(t["crop_nogps"].format(**names))
    elif (need == 2 and kp_loc >= 5) or (need == 1 and kp_loc >= 7):
        st.error(t["crop_pause"].format(**names))
    elif kp_loc >= 5:
        st.warning(t["crop_caution"].format(**names))
    else:
        st.success(t["crop_go"].format(**names))

# ---------- SMS / WhatsApp alert ----------
st.subheader(t["sms_h"])
st.caption(t["sms_note"])
tab_en, tab_hi = st.tabs(["English", "Hindi"])
for tab, key in ((tab_en, "en"), (tab_hi, "hi")):
    with tab:
        msg = SMS[key][tier].format(s=state)
        st.code(msg, language=None)
        st.link_button(TXT[key]["wa"], "https://wa.me/?text=" + quote(msg))

# ---------- India map ----------
st.subheader(t["map"])
rows = []
for name, (la, lo) in STATES.items():
    k = kp_v * lat_factor(la)
    rows.append({
        "state": name,
        "lat": la,
        "lon": lo,
        "risk": t["levels"][gnss_idx(k)],
        "kp_local": round(k, 1),
    })
map_df = pd.DataFrame(rows)
fig = px.scatter_map(
    map_df,
    lat="lat",
    lon="lon",
    color="risk",
    hover_name="state",
    hover_data={"lat": False, "lon": False, "kp_local": True},
    color_discrete_map={t["levels"][i]: RISK_COLORS[i] for i in range(4)},
    category_orders={"risk": t["levels"]},
    zoom=3.4,
    center={"lat": 23.0, "lon": 80.0},
    height=480,
    map_style="carto-darkmatter",
)
fig.update_traces(marker=dict(size=18))
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), legend_title_text="")
st.plotly_chart(fig, width="stretch")

# ---------- Forecast: official first, experimental second ----------
st.subheader(t["fc"])
if not demo:
    try:
        off = get_official_forecast()
        st.markdown("**" + t["fc_official"] + "**")
        off_show = pd.DataFrame({
            "UTC": off["time_tag"].dt.strftime("%m-%d %H:%M"),
            "Kp": off["kp"].round(1),
            "G": [g_label(v) for v in off["kp"]],
        })
        st.dataframe(off_show, hide_index=True, width="stretch")
        if off["kp"].max() >= 5:
            st.warning(t["fc_storm"])
    except Exception:
        st.info("NOAA official forecast: " + t["unavail"])

if kp_df is not None:
    fc = forecast_kp(kp_df)
    if fc:
        st.markdown("**" + t["fc_exp"] + "**")
        fc_df = pd.DataFrame({
            t["hour"]: ["+" + str(h) + "h" for h in range(1, 4)],
            t["est"]: [round(v, 1) for v in fc],
            "G": [g_label(v) for v in fc],
        })
        st.dataframe(fc_df, hide_index=True, width="stretch")
        st.caption(t["fc_note"])

# ---------- Charts ----------
st.subheader(t["last24"])
a, b = st.columns(2)
if xray_df is not None:
    a.line_chart(xray_df.set_index("time_tag")["flux"])
else:
    a.info(t["radio"] + ": " + t["unavail"])
if kp_df is not None:
    b.line_chart(kp_df.set_index("time_tag")["estimated_kp"])
else:
    b.info(t["geo"] + ": " + t["unavail"])

# ---------- MODULE 03 · AI ALERT COPILOT + PREDICTIVE INTELLIGENCE ----------
st.markdown('<div class="module-ribbon"><span>03</span><div><b>SOLAR SHIELD AI & PREDICTIVE INTELLIGENCE</b><small>Evidence summary · recommended response · experimental machine-learning forecast</small></div></div>', unsafe_allow_html=True)
st.markdown("""
<style>
.ai-hero{position:relative;overflow:hidden;border:1px solid rgba(124,110,255,.35);border-radius:22px;padding:24px 26px;margin:18px 0 22px;background:radial-gradient(circle at 85% 20%,rgba(78,91,255,.25),transparent 32%),linear-gradient(120deg,rgba(12,24,47,.98),rgba(28,18,57,.94));box-shadow:0 18px 50px rgba(0,0,0,.22);transition:transform .25s ease,box-shadow .25s ease}
.ai-hero:hover{transform:translateY(-2px);box-shadow:0 22px 48px rgba(40,120,255,.17)}
.ai-hero:after{content:"";position:absolute;width:230px;height:230px;right:-55px;top:-115px;border:1px solid rgba(121,210,255,.26);border-radius:50%;box-shadow:0 0 0 22px rgba(121,210,255,.035),0 0 0 48px rgba(121,210,255,.025);animation:orbitPulse 7s ease-in-out infinite}
.ai-kicker{font-size:11px;letter-spacing:.19em;font-weight:800;color:#a5b4fc}.ai-title{font-size:clamp(24px,3vw,38px);font-weight:850;line-height:1.1;margin:8px 0;color:#f2f5ff}.ai-copy{color:#b9c6e8;max-width:850px;font-size:14px}.ai-live{display:inline-block;width:8px;height:8px;border-radius:50%;background:#61f4c0;box-shadow:0 0 14px #61f4c0;margin-right:8px;animation:livePulse 1.8s infinite}
@keyframes orbitPulse{0%,100%{transform:scale(.96) rotate(0deg);opacity:.65}50%{transform:scale(1.05) rotate(12deg);opacity:1}}@keyframes livePulse{0%,100%{opacity:1}50%{opacity:.35}}
@media(prefers-reduced-motion:reduce){.ai-hero:after,.ai-live,.ai-hero{animation:none;transition:none}}
</style>
<div class="ai-hero"><div class="ai-kicker"><span class="ai-live"></span>EXPLAINABLE ALERT ASSISTANT</div><div class="ai-title"></div><div class="ai-copy">Summarizes the current app evidence into a structured situation report and recommended actions. This version uses transparent rules and safe fallback logic; it does not call an external LLM or require an API key. GNSS receiver values remain simulated unless a real receiver feed is connected.</div></div>
""", unsafe_allow_html=True)
# Solar Shield AI
# Build an explainable copilot report from current readings plus the GNSS test panel.
solar_class_now, _ = _solar_class(max(float(flux_v), 0.0))
copilot_findings = []
copilot_actions = []
if flux_v >= 1e-4:
    copilot_findings.append(f"X-ray flux is {flux_v:.2e} W/m² ({solar_class_now} threshold in the app's simplified classification).")
    copilot_actions.append("Review current NOAA radio-blackout alerts and verify alternate HF/communications paths.")
elif flux_v >= 1e-5:
    copilot_findings.append(f"X-ray flux is elevated at {flux_v:.2e} W/m² ({solar_class_now} threshold).")
    copilot_actions.append("Monitor HF radio links and check official space-weather bulletins.")
else:
    copilot_findings.append(f"Current X-ray flux is {flux_v:.2e} W/m² ({solar_class_now} threshold). No high X-ray threshold is indicated by this simplified rule.")
if kp_v >= 5:
    copilot_findings.append(f"Geomagnetic activity is Kp {kp_v:.1f} ({g_label(kp_v)} threshold or higher).")
    copilot_actions.append("Check GNSS-dependent timing/navigation and keep operational backup procedures available.")
else:
    copilot_findings.append(f"Current Kp is {kp_v:.1f}, below the app's G1 threshold of Kp 5.")
if 'gnss_exceeded' in globals() and gnss_exceeded:
    copilot_findings.append(f"SIMULATED GNSS receiver error {gnss_error_m:.1f} m exceeds configured limit {gnss_limit_m:.1f} m.")
    copilot_actions.append("OPERATOR REVIEW: verify receiver/reference data and consider manual control before precision operations.")
else:
    copilot_findings.append("No GNSS threshold breach is indicated by the current demo input; no physical receiver health check is connected.")
if demo:
    copilot_findings.append("Dashboard is in demo mode; solar/geomagnetic readings are simulated.")
if not copilot_actions:
    copilot_actions.append("Continue monitoring fresh official observations. No elevated action is indicated by these simplified rules.")

copilot_level = "HIGH ATTENTION" if (flux_v >= 1e-4 or kp_v >= 7 or ('gnss_exceeded' in globals() and gnss_exceeded)) else ("WATCH" if (flux_v >= 1e-5 or kp_v >= 5) else "ROUTINE MONITORING")
cc1, cc2 = st.columns([1, 2])
with cc1:
    st.metric("Copilot assessment", copilot_level)
    st.caption("Rule-based fallback is always available. This is decision support, not an official warning.")
with cc2:
    st.markdown("#### Evidence summary")
    for finding in copilot_findings:
        st.markdown(f"- {finding}")
st.markdown("#### Recommended actions")
for action in copilot_actions:
    st.markdown(f"- {action}")
if st.button("Acknowledge current copilot report", key="sd_ack_copilot"):
    st.session_state.setdefault("sd_audit_log", []).append({"Time (UTC)": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), "Event": "Solar Shield AI report", "Evidence": f"Assessment: {copilot_level}; Kp {kp_v:.1f}; X-ray {flux_v:.2e} W/m²", "Action": "Report acknowledged"})
    st.success("Copilot report acknowledged and added to this session's audit trail.")

st.markdown("#### Experimental Kp prediction model")
st.caption("The Random Forest model below remains an experimental historical-data prediction; it is separate from the explainable alert copilot and must not be treated as an official warning.")

# ---------- AI PREDICTION CENTER · OFFICIAL HISTORICAL Kp MODEL ----------
@st.cache_data(ttl=86400, show_spinner=False)
def get_gfz_historical_kp(years=5):
    """Fetch official definitive 3-hour Kp values from GFZ's documented JSON API.

    GFZ's service response shape can vary by API version. This parser supports
    record-oriented JSON and column-oriented JSON while validating timestamps
    and numeric Kp values. It never manufactures observations.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=365 * years)
    url = "https://kp.gfz.de/app/json/"
    params = {
        "start": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "index": "Kp",
        "status": "def",
    }
    response = requests.get(url, params=params, timeout=60, headers={"Accept": "application/json", "User-Agent": "SpaceWeatherAlert/1.0"})
    response.raise_for_status()
    payload = response.json()

    time_names = ("time", "datetime", "timestamp", "date", "time_tag", "starttime", "start_time", "time_utc", "timeUTC")
    value_names = ("Kp", "kp", "value", "index", "Kp_value", "kp_value")
    rows = []

    def is_seq(value):
        return isinstance(value, (list, tuple))

    def add_pair(t, v):
        if not is_seq(t) and not is_seq(v) and t is not None and v is not None:
            rows.append((t, v))

    def walk(obj, depth=0):
        """Recursively recognize common GFZ JSON response layouts."""
        if depth > 8 or obj is None:
            return
        if isinstance(obj, dict):
            lower_map = {str(k).lower(): k for k in obj.keys()}
            tk = next((lower_map[k.lower()] for k in time_names if k.lower() in lower_map), None)
            vk = next((lower_map[k.lower()] for k in value_names if k.lower() in lower_map), None)
            if tk is not None and vk is not None:
                times, values = obj[tk], obj[vk]
                if is_seq(times) and is_seq(values):
                    for t, v in zip(times, values):
                        add_pair(t, v)
                    return
                if not is_seq(times) and not is_seq(values):
                    add_pair(times, values)
                    return
            # Some API versions wrap column arrays in a data/result object.
            for child in obj.values():
                walk(child, depth + 1)
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                if isinstance(item, dict):
                    before = len(rows)
                    walk(item, depth + 1)
                    if len(rows) == before:
                        # Support a single record using less common field names.
                        keys = {str(k).lower(): k for k in item}
                        tk = next((keys[k.lower()] for k in time_names if k.lower() in keys), None)
                        vk = next((keys[k.lower()] for k in value_names if k.lower() in keys), None)
                        if tk is not None and vk is not None:
                            add_pair(item[tk], item[vk])
                elif is_seq(item) and len(item) >= 2:
                    # Common table format: [timestamp, Kp, ...]
                    if isinstance(item[0], str):
                        add_pair(item[0], item[1])
                    else:
                        walk(item, depth + 1)

    walk(payload)
    if not rows:
        preview = repr(payload)
        if len(preview) > 350:
            preview = preview[:350] + "..."
        raise ValueError(f"GFZ Kp API returned no recognizable timestamp/Kp records (response type: {type(payload).__name__}; preview: {preview})")

    df = pd.DataFrame(rows, columns=["time_tag", "kp"])
    df["time_tag"] = pd.to_datetime(df["time_tag"], utc=True, errors="coerce")
    df["kp"] = pd.to_numeric(df["kp"], errors="coerce")
    df = df.dropna(subset=["time_tag", "kp"])
    df = df[np.isfinite(df["kp"]) & df["kp"].between(0, 9)]
    df = df.drop_duplicates("time_tag").sort_values("time_tag").reset_index(drop=True)
    if df.empty:
        raise ValueError("GFZ Kp response contained records, but none passed timestamp and Kp quality checks")
    return df

with st.expander("🧠 Explore the ML forecast, validation and data provenance", expanded=True):
    st.caption("HISTORICAL TRAINING SOURCE: GFZ German Research Centre for Geosciences Kp web service · definitive Kp values · 3-hour cadence · CC BY 4.0. Live dashboard observations remain sourced from NOAA separately.")
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import mean_absolute_error, mean_squared_error

        with st.spinner("Loading official historical Kp records and validating the time series…"):
            hist_kp = get_gfz_historical_kp(years=5)

        # Kp is a 3-hour index. Use past 3, 6, 9, 12, 24 and 48 hours to estimate the next interval.
        hist_kp = hist_kp.sort_values("time_tag").drop_duplicates("time_tag").reset_index(drop=True)
        # GFZ Kp records are nominally 3-hourly. Break sequences across large gaps so
        # lags/targets never silently jump over missing intervals.
        hist_kp["gap_hours"] = hist_kp["time_tag"].diff().dt.total_seconds() / 3600
        hist_kp["segment"] = (hist_kp["gap_hours"].isna() | (hist_kp["gap_hours"] > 3.5)).cumsum()
        lag_steps = [1, 2, 3, 4, 8, 16]
        frames = []
        for _, segment in hist_kp.groupby("segment", sort=False):
            segment = segment.copy()
            for lag in lag_steps:
                segment[f"kp_lag_{lag}"] = segment["kp"].shift(lag)
            segment["target_kp_next_3h"] = segment["kp"].shift(-1)
            frames.append(segment)
        ml_data = pd.concat(frames, ignore_index=True).dropna(subset=[f"kp_lag_{lag}" for lag in lag_steps] + ["target_kp_next_3h"])
        feature_cols = [f"kp_lag_{lag}" for lag in lag_steps]

        if len(ml_data) < 500:
            st.warning(f"The official historical endpoint returned {len(ml_data):,} usable time-ordered training examples after quality checks. At least 500 are required for this prototype; no synthetic records are added and no forecast is shown yet.")
            st.info("Check your internet connection and retry. The source is the official GFZ Kp archive; definitive values may lag recent conditions. If the API format changes, the parser will report the issue rather than fabricate data.")
        else:
            split_at = int(len(ml_data) * 0.8)
            train, test = ml_data.iloc[:split_at], ml_data.iloc[split_at:]
            model = RandomForestRegressor(n_estimators=180, max_depth=10, min_samples_leaf=3, random_state=42, n_jobs=-1)
            model.fit(train[feature_cols], train["target_kp_next_3h"])
            test_pred = np.clip(model.predict(test[feature_cols]), 0, 9)
            mae = float(mean_absolute_error(test["target_kp_next_3h"], test_pred))
            rmse = float(np.sqrt(mean_squared_error(test["target_kp_next_3h"], test_pred)))
            latest_features = ml_data.iloc[[-1]][feature_cols]
            prediction = float(np.clip(model.predict(latest_features)[0], 0, 9))
            latest_time = pd.to_datetime(hist_kp["time_tag"].iloc[-1], utc=True)
            forecast_time = latest_time + pd.Timedelta(hours=3)
            current_kp = float(hist_kp["kp"].iloc[-1])
            delta = prediction - current_kp
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Latest definitive GFZ Kp", f"{current_kp:.1f}")
            m2.metric("ML estimate · +3 hours", f"{prediction:.2f}", f"{delta:+.2f} vs latest")
            m3.metric("Test MAE", f"{mae:.3f}", help="Mean absolute error on the later 20% of the time-ordered dataset; lower is better.")
            m4.metric("Test RMSE", f"{rmse:.3f}", help="Root mean squared error on the later 20% of the time-ordered dataset; lower is better.")
            st.caption(f"Forecast target time: {forecast_time.strftime('%Y-%m-%d %H:%M UTC')} · Latest definitive record: {latest_time.strftime('%Y-%m-%d %H:%M UTC')} · Official historical records: {len(hist_kp):,} · Training examples: {len(train):,} · Test examples: {len(test):,}")
            st.caption("GFZ definitive Kp can lag real time by days to weeks. This forecast is based on the latest available definitive record, not the live NOAA nowcast; compare with current NOAA/GFZ operational forecasts before acting.")

            chart_df = ml_data[["time_tag", "kp", "target_kp_next_3h"]].tail(240).copy()
            chart_df = chart_df.rename(columns={"kp": "Observed GFZ Kp", "target_kp_next_3h": "Next 3-hour Kp target"})
            st.markdown("#### Historical Kp and next-interval targets")
            st.line_chart(chart_df.set_index("time_tag"), height=250)
            st.markdown("#### Model transparency")
            importance = pd.DataFrame({"Feature": feature_cols, "Importance": model.feature_importances_}).sort_values("Importance", ascending=False)
            st.bar_chart(importance.set_index("Feature"), height=190)
            st.caption("Validation uses a chronological split: earlier examples train the model and later examples test it. Consecutive Kp values are correlated, so these metrics are an initial project evaluation—not proof of operational forecasting skill. Source: GFZ Kp index, CC BY 4.0; acknowledge GFZ Helmholtz Centre for Geosciences.")
            if prediction >= 5:
                st.warning("The experimental ML estimate is in the Kp ≥ 5 range. Check current official NOAA/GFZ forecasts and alerts; do not rely on this model alone.")
            else:
                st.info("The experimental ML estimate is below Kp 5 for the next 3-hour interval. Continue monitoring current official products; this is not a guarantee of quiet conditions.")
    except ImportError:
        st.error("The ML library is not installed. In the VS Code terminal run: python -m pip install scikit-learn")
    except Exception as exc:
        st.warning(f"The AI Prediction Center could not retrieve or process the official historical GFZ Kp dataset: {exc}")
        st.caption("The rest of the dashboard remains available. Retry later if the data service is unreachable. No fabricated observations are used.")

# ---------- End AI Prediction Center ----------

# ---------- Alert history ----------
st.subheader(t["hist"])
if st.session_state.hist:
    st.dataframe(pd.DataFrame(st.session_state.hist[::-1]), hide_index=True, width="stretch")
else:
    st.caption(t["hist_empty"])
