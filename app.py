import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.parse import quote
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="Space Weather Alert System", page_icon="🛰️", layout="wide")
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
        "caption": "दूरसंचार और कृषि के लिए पूर्व चेतावनी | डेटा: NOAA SWPC",
        "settings": "सेटिंग्स",
        "view": "दृश्य",
        "views": ["दूरसंचार", "किसान"],
        "demo": "डेमो मोड (मई 2024 तूफ़ान का अनुकरण)",
        "state": "अपना राज्य चुनें",
        "radio": "HF रेडियो ब्लैकआउट",
        "geo": "भू-चुंबकीय तूफ़ान",
        "gnss": "GNSS/GPS चिंता",
        "farm": "खेती के उपकरण",
        "none": "कोई नहीं",
        "night": "रात का समय: प्रभावित नहीं",
        "unavail": "उपलब्ध नहीं",
        "levels": ["कम", "मध्यम", "उच्च", "बहुत उच्च"],
        "geo_names": ["शांत (G1 से नीचे)", "G1 हल्का", "G2 मध्यम",
                      "G3 तेज़", "G4 गंभीर", "G5 अत्यधिक"],
        "sev": ["सब सामान्य", "निगरानी", "चेतावनी", "गंभीर"],
        "banner_sub": ["किसी व्यवधान की आशंका नहीं", "हल्की गड़बड़ी संभव",
                       "व्यवधान की संभावना", "गंभीर व्यवधान: तुरंत कदम उठाएँ"],
        "pause": "⛔ रोकें",
        "caution": "⚠️ सावधानी",
        "safe": "✅ सुरक्षित",
        "advice": "सलाह",
        "local": "स्थान-आधारित चिंता (सरल मॉडल, केवल संकेतात्मक)",
        "t_r3": "तेज़ HF ब्लैकआउट। सैटेलाइट या वैकल्पिक लिंक पर जाएँ।",
        "t_r1": "हल्का HF व्यवधान संभव। लिंक की निगरानी करें।",
        "t_ok": "HF रेडियो में व्यवधान की आशंका नहीं।",
        "t_kp": "भू-चुंबकीय तूफ़ान: GNSS टाइमिंग कम भरोसेमंद हो सकती है।",
        "f_pause": "GPS की सटीकता घट सकती है। "
                   "ऑटो-स्टीयर और सटीक खेती के उपकरण रोकें।",
        "f_caution": "GPS की सटीकता कम हो सकती है। "
                     "स्वचालित काम से पहले उपकरण जाँचें।",
        "f_safe": "GPS सामान्य है। स्वचालित उपकरण सुरक्षित रूप से चलाएँ।",
        "check": "✅ मुझे क्या करना चाहिए?",
        "crop_h": "🌾 फसल-आधारित सलाह",
        "crop": "फसल",
        "task": "काम",
        "crop_pause": "⛔ {crop} की {task} में सटीक GPS चाहिए तो उसे टालें। "
                      "हाथ से करें या अलर्ट खत्म होने का इंतज़ार करें।",
        "crop_caution": "⚠️ {crop} की {task}: GPS की सटीकता कम हो सकती है। "
                        "उपकरण जाँचें और हाथ से नियंत्रण तैयार रखें।",
        "crop_go": "✅ {crop} की {task} के लिए GPS वाले उपकरण चलाने की स्थिति अच्छी है।",
        "crop_nogps": "ℹ️ {crop} की {task} GPS पर ज़्यादा निर्भर नहीं है, "
                      "आप जारी रख सकते हैं।",
        "sms_h": "📱 SMS / WhatsApp अलर्ट",
        "sms_note": "नीचे का संदेश कॉपी करें या भेजें।",
        "wa": "WhatsApp पर भेजें",
        "map": "🗺️ भारत GNSS चिंता मानचित्र",
        "last24": "पिछले 24 घंटे",
        "fc": "🔮 पूर्वानुमान",
        "fc_official": "NOAA का आधिकारिक Kp पूर्वानुमान",
        "fc_exp": "प्रयोगात्मक 3 घंटे का ट्रेंड (आधिकारिक नहीं)",
        "fc_note": "यह प्रदर्शन के लिए सरल ट्रेंड अनुमान है, आधिकारिक पूर्वानुमान नहीं।",
        "fc_storm": "तूफ़ान की संभावना: अगले घंटों में Kp 5 या उससे अधिक हो सकता है।",
        "fc_ok": "अगले 3 घंटों में बड़े तूफ़ान की आशंका कम है।",
        "hour": "घंटा",
        "est": "अनुमानित Kp",
        "updated": "डेटा अपडेट (UTC)",
        "stale": "⚠️ कुछ डेटा 30 मिनट से पुराना है। मान पुराने हो सकते हैं।",
        "sim": "नकली डेटा (डेमो मोड)",
        "why": "🔎 यह अलर्ट क्यों?",
        "why_geo": "भू-चुंबकीय: Kp {kp:.1f} → {name}। "
                   "NOAA G-स्केल: G1 Kp 5 से, G3 Kp 7 से, G5 Kp 9 से शुरू होता है।",
        "why_radio": "रेडियो: X-रे फ्लक्स {flux:.2e} W/m² → R{r}। "
                     "NOAA R-स्केल: R1 1e-5 W/m² से शुरू होता है।",
        "why_night": "रेडियो ब्लैकआउट केवल धूप वाले हिस्से को प्रभावित करता है। "
                     "भारत में अभी रात है, इसलिए इसे नहीं गिना गया।",
        "why_local": "{state} के लिए GNSS चिंता: Kp {kp:.1f} × अक्षांश कारक {f:.1f} "
                     "= {kpl:.1f}। यह सरल मॉडल है, मापी गई GPS त्रुटि नहीं।",
        "why_farm": "स्थानीय Kp 7 या उससे ऊपर होने पर उपकरण रोके जाते हैं, "
                    "और 5 से सावधानी की सलाह है।",
        "hist": "🕘 अलर्ट इतिहास (इस सत्र का)",
        "hist_empty": "अभी कोई अलर्ट दर्ज नहीं है।",
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
            ["सामान्य संचालन। किसी कार्रवाई की ज़रूरत नहीं।",
             "डैशबोर्ड पर नज़र रखें।"],
            ["नेटवर्क ऑपरेशन टीम को सूचित करें।",
             "HF और टाइमिंग सेवाओं के लिए बैकअप लिंक (सैटेलाइट या फाइबर) तैयार रखें।",
             "बेस स्टेशनों पर GNSS आधारित टाइम सिंक की जाँच करें।"],
            ["ज़रूरी ट्रैफ़िक तुरंत सैटेलाइट या फाइबर लिंक पर ले जाएँ।",
             "धूप वाले हिस्से में HF रेडियो ब्लैकआउट संभव है: "
             "वैकल्पिक बैंड या रूट इस्तेमाल करें।",
             "बेस स्टेशन की टाइमिंग बैकअप स्रोत पर ले जाएँ।"],
        ],
        "farmer": [
            ["GPS सामान्य है। स्वचालित उपकरण योजना के अनुसार चलाएँ।",
             "लंबे स्वचालित काम से पहले जाँच करते रहें।"],
            ["ऑटो-स्टीयर चलाने से पहले GPS की सटीकता जाँचें।",
             "बुवाई और छिड़काव जैसे सटीक काम अतिरिक्त सावधानी से करें।",
             "हाथ से नियंत्रण लेने के लिए एक व्यक्ति तैयार रखें।"],
            ["ऑटो-स्टीयर और GPS वाली मशीनें रोकें।",
             "हाथ से चलाएँ या सटीक काम टाल दें।",
             "अलर्ट खत्म होने तक रुकें, फिर दोबारा चलाने से पहले कैलिब्रेट करें।"],
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
        "{s} में अंतरिक्ष मौसम सामान्य है। GPS और रेडियो ठीक हैं। "
        "खेती के उपकरण सुरक्षित रूप से चलाएँ।",
        "{s} में अंतरिक्ष मौसम चेतावनी: GPS की सटीकता कम हो सकती है। "
        "ऑटो-स्टीयर चलाने से पहले जाँच लें।",
        "{s} में अंतरिक्ष मौसम अलर्ट: गंभीर गड़बड़ी। "
        "GPS वाले उपकरण रोकें और हाथ से (मैनुअल) चलाएँ।",
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
    "sowing": ("Sowing", "बुवाई", 2),
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
lang_choice = st.sidebar.radio("Language / भाषा", ["English", "हिन्दी"])
lk = "en" if lang_choice == "English" else "hi"
li = 0 if lk == "en" else 1
t = TXT[lk]

st.title(t["title"])
st.caption(t["caption"])

st.sidebar.header(t["settings"])
view = st.sidebar.radio(t["view"], [0, 1], format_func=lambda i: t["views"][i])
state = st.sidebar.selectbox(
    t["state"], list(STATES.keys()), index=list(STATES).index("Uttar Pradesh")
)
demo = st.sidebar.checkbox(t["demo"])

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
<div style="background:__BG__;padding:18px 22px;border-radius:14px;color:white;__GLOW__">
  <div style="font-size:14px;opacity:0.9;">📍 __STATE__</div>
  <div style="font-size:30px;font-weight:700;">__SEV__</div>
  <div style="font-size:15px;">__SUB__</div>
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
tab_hi, tab_en = st.tabs(["हिन्दी", "English"])
for tab, key in ((tab_hi, "hi"), (tab_en, "en")):
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
    map_style="open-street-map",
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

# ---------- Alert history ----------
st.subheader(t["hist"])
if st.session_state.hist:
    st.dataframe(pd.DataFrame(st.session_state.hist[::-1]), hide_index=True, width="stretch")
else:
    st.caption(t["hist_empty"])
