import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="Space Weather Alert System", layout="wide")
BASE = "https://services.swpc.noaa.gov"

TXT = {
    "en": {
        "title": "🛰️ Space Weather Alert System",
        "caption": "Early warnings for Telecom & Agriculture | Data: NOAA SWPC",
        "settings": "Settings", "view": "View", "views": ["Telecom", "Farmer"],
        "demo": "Demo mode (simulate May 2024 storm)", "state": "Select your state",
        "radio": "HF Radio Blackout", "gnss": "GNSS/GPS Risk", "farm": "Farm Equipment",
        "none": "None", "night": "Night side: not affected",
        "levels": ["Normal", "Moderate", "High", "Severe"],
        "pause": "⛔ PAUSE", "caution": "⚠️ Caution", "safe": "✅ Safe",
        "advice": "advice", "local": "Location-based risk (simplified model, indicative only)",
        "t_r3": "Strong HF blackout on the sunlit side of Earth. Switch to satellite or alternate links.",
        "t_r1": "Minor to moderate HF disruption possible. Monitor links.",
        "t_ok": "No HF radio disruption expected.",
        "t_kp": "Geomagnetic storm: GNSS timing sources may be less reliable.",
        "f_pause": "GPS accuracy may drop. Pause auto-steer and precision farming equipment.",
        "f_caution": "GPS accuracy may be reduced. Check equipment before autonomous operation.",
        "f_safe": "GPS conditions normal. Safe to run automated equipment.",
        "last24": "Last 24 hours", "fc": "Next 3 hours forecast",
        "fc_note": "Simple trend estimate, not an official forecast.",
        "fc_storm": "Storm possible: Kp may reach 5 or higher in the next hours.",
        "fc_ok": "Low chance of a major storm in the next 3 hours.",
        "official": "NOAA official forecast", "hour": "Hour", "est": "Estimated Kp",
    },
    "hi": {
        "title": "🛰️ अंतरिक्ष मौसम चेतावनी प्रणाली",
        "caption": "दूरसंचार और कृषि के लिए पूर्व चेतावनी | डेटा: NOAA SWPC",
        "settings": "सेटिंग्स", "view": "दृश्य", "views": ["दूरसंचार", "किसान"],
        "demo": "डेमो मोड (मई 2024 तूफ़ान का अनुकरण)", "state": "अपना राज्य चुनें",
        "radio": "HF रेडियो ब्लैकआउट", "gnss": "GNSS/GPS जोखिम", "farm": "खेती के उपकरण",
        "none": "कोई नहीं", "night": "रात का समय: प्रभावित नहीं",
        "levels": ["सामान्य", "मध्यम", "उच्च", "गंभीर"],
        "pause": "⛔ रोकें", "caution": "⚠️ सावधानी", "safe": "✅ सुरक्षित",
        "advice": "सलाह", "local": "स्थान-आधारित जोखिम (सरल मॉडल, केवल संकेतात्मक)",
        "t_r3": "तेज़ HF ब्लैकआउट। सैटेलाइट या वैकल्पिक लिंक पर जाएँ।",
        "t_r1": "हल्का HF व्यवधान संभव। लिंक की निगरानी करें।",
        "t_ok": "HF रेडियो में व्यवधान की आशंका नहीं।",
        "t_kp": "भू-चुंबकीय तूफ़ान: GNSS टाइमिंग कम भरोसेमंद हो सकती है।",
        "f_pause": "GPS की सटीकता घट सकती है। ऑटो-स्टीयर और सटीक खेती के उपकरण रोकें।",
        "f_caution": "GPS की सटीकता कम हो सकती है। स्वचालित काम से पहले उपकरण जाँचें।",
        "f_safe": "GPS सामान्य है। स्वचालित उपकरण सुरक्षित रूप से चलाएँ।",
        "last24": "पिछले 24 घंटे", "fc": "अगले 3 घंटे का पूर्वानुमान",
        "fc_note": "यह सरल ट्रेंड अनुमान है, आधिकारिक पूर्वानुमान नहीं।",
        "fc_storm": "तूफ़ान की संभावना: अगले घंटों में Kp 5 या उससे अधिक हो सकता है।",
        "fc_ok": "अगले 3 घंटों में बड़े तूफ़ान की आशंका कम है।",
        "official": "NOAA का आधिकारिक पूर्वानुमान", "hour": "घंटा", "est": "अनुमानित Kp",
    },
}

STATES = {
    "Jammu & Kashmir": 34, "Himachal Pradesh": 31.5, "Punjab": 31, "Uttarakhand": 30,
    "Haryana": 29, "Rajasthan": 27, "Uttar Pradesh": 27, "Assam": 26, "Bihar": 25.5,
    "Gujarat": 23, "West Bengal": 23, "Madhya Pradesh": 23.5, "Jharkhand": 23.5,
    "Chhattisgarh": 21.5, "Odisha": 20.5, "Maharashtra": 19, "Telangana": 17.5,
    "Andhra Pradesh": 16, "Karnataka": 15, "Tamil Nadu": 11, "Kerala": 10,
}


@st.cache_data(ttl=300)
def get_xray():
    r = requests.get(f"{BASE}/json/goes/primary/xrays-1-day.json", timeout=15)
    df = pd.DataFrame(r.json())
    df = df[df["energy"] == "0.1-0.8nm"].copy()
    df["time_tag"] = pd.to_datetime(df["time_tag"])
    return df[["time_tag", "flux"]]


@st.cache_data(ttl=300)
def get_kp():
    r = requests.get(f"{BASE}/json/planetary_k_index_1m.json", timeout=15)
    df = pd.DataFrame(r.json())
    df["time_tag"] = pd.to_datetime(df["time_tag"])
    return df[["time_tag", "estimated_kp"]]


@st.cache_data(ttl=900)
def get_official_forecast():
    r = requests.get(f"{BASE}/products/noaa-planetary-k-index-forecast.json", timeout=15)
    rows = r.json()
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df["time_tag"] = pd.to_datetime(df["time_tag"])
    df["kp"] = df["kp"].astype(float)
    return df[df["observed"] == "predicted"][["time_tag", "kp"]].head(8)


def radio_level(flux):
    if flux >= 2e-3: return 5
    if flux >= 1e-3: return 4
    if flux >= 1e-4: return 3
    if flux >= 5e-5: return 2
    if flux >= 1e-5: return 1
    return 0


def gnss_idx(kp):
    if kp >= 9: return 3
    if kp >= 7: return 2
    if kp >= 5: return 1
    return 0


def lat_factor(lat):
    if lat >= 30: return 1.0
    if lat >= 24: return 0.9
    if lat >= 16: return 0.8
    return 0.7


def forecast_kp(df, hours=3):
    d = df.tail(180)
    if len(d) < 10:
        return None
    y = d["estimated_kp"].astype(float).values
    slope, _ = np.polyfit(np.arange(len(y)), y, 1)
    last = float(y[-1])
    return [min(9.0, max(0.0, last + slope * 60 * h)) for h in range(1, hours + 1)]


# ---------- Sidebar ----------
lang_choice = st.sidebar.radio("Language / भाषा", ["English", "हिन्दी"])
t = TXT["en"] if lang_choice == "English" else TXT["hi"]

st.title(t["title"])
st.caption(t["caption"])

st.sidebar.header(t["settings"])
view = st.sidebar.radio(t["view"], [0, 1], format_func=lambda i: t["views"][i])
state = st.sidebar.selectbox(t["state"], list(STATES.keys()), index=list(STATES).index("Uttar Pradesh"))
demo = st.sidebar.checkbox(t["demo"])

# ---------- Data ----------
try:
    if demo:
        flux, kp = 8.7e-4, 9.0
        times = pd.date_range(end=pd.Timestamp.now(), periods=60, freq="min")
        xray_df = pd.DataFrame({"time_tag": times, "flux": [1e-6 * (1.12 ** i) for i in range(60)]})
        kp_df = pd.DataFrame({"time_tag": times, "estimated_kp": [3 + i * 0.1 for i in range(60)]})
    else:
        xray_df, kp_df = get_xray(), get_kp()
        flux = float(xray_df["flux"].iloc[-1])
        kp = float(kp_df["estimated_kp"].iloc[-1])
except Exception as e:
    st.error(f"Could not fetch live data: {e}")
    st.stop()

# ---------- Location-based risk ----------
lat = STATES[state]
ist_hour = (datetime.now(timezone.utc) + timedelta(hours=5.5)).hour
daytime = demo or (6 <= ist_hour < 18)
r_global = radio_level(flux)
r_loc = r_global if daytime else 0
kp_loc = kp * lat_factor(lat)
g_idx = gnss_idx(kp_loc)
pause = kp_loc >= 7
caution = kp_loc >= 5

st.subheader(f"📍 {state}")
st.caption(t["local"])
c1, c2, c3 = st.columns(3)
c1.metric(t["radio"], f"R{r_loc}" if r_loc else t["none"],
          f"X-ray flux {flux:.2e} W/m²" if daytime else t["night"], delta_color="off")
c2.metric(t["gnss"], t["levels"][g_idx], f"Kp {kp:.1f} → {kp_loc:.1f}", delta_color="off")
c3.metric(t["farm"], t["pause"] if pause else (t["caution"] if caution else t["safe"]))

# ---------- Advice ----------
st.subheader(f"{t['views'][view]} {t['advice']}")
if view == 0:
    if r_loc >= 3: st.error(t["t_r3"])
    elif r_loc >= 1: st.warning(t["t_r1"])
    else: st.success(t["t_ok"])
    if kp_loc >= 5: st.warning(t["t_kp"])
else:
    if pause: st.error(t["f_pause"])
    elif caution: st.warning(t["f_caution"])
    else: st.success(t["f_safe"])

# ---------- Forecast ----------
st.subheader(f"🔮 {t['fc']}")
fc = forecast_kp(kp_df)
if fc:
    fc_df = pd.DataFrame({t["hour"]: [f"+{h}h" for h in range(1, 4)],
                          t["est"]: [round(v, 1) for v in fc],
                          t["gnss"]: [t["levels"][gnss_idx(v)] for v in fc]})
    st.dataframe(fc_df, hide_index=True, width="stretch")
    if max(fc) >= 5: st.warning(t["fc_storm"])
    else: st.info(t["fc_ok"])
    st.caption(t["fc_note"])

if not demo:
    try:
        off = get_official_forecast()
        st.markdown(f"**{t['official']}**")
        st.dataframe(off.rename(columns={"time_tag": "UTC", "kp": "Kp"}),
                     hide_index=True, width="stretch")
    except Exception:
        pass

# ---------- Charts ----------
st.subheader(t["last24"])
a, b = st.columns(2)
a.line_chart(xray_df.set_index("time_tag")["flux"])
b.line_chart(kp_df.set_index("time_tag")["estimated_kp"])
