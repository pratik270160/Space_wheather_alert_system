import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Space Weather Alert System", layout="wide")
st.title("🛰️ Space Weather Alert System")
st.caption("Early warnings for Telecom & Agriculture | Data: NOAA SWPC")

BASE = "https://services.swpc.noaa.gov"

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

def radio_level(flux):
    if flux >= 2e-3: return 5
    if flux >= 1e-3: return 4
    if flux >= 1e-4: return 3
    if flux >= 5e-5: return 2
    if flux >= 1e-5: return 1
    return 0

def gnss_level(kp):
    if kp >= 9: return "Severe"
    if kp >= 7: return "High"
    if kp >= 5: return "Moderate"
    return "Normal"

# Sidebar
st.sidebar.header("Settings")
view = st.sidebar.radio("View", ["Telecom", "Farmer"])
demo = st.sidebar.checkbox("Demo mode (simulate May 2024 storm)")

# Data
try:
    if demo:
        flux, kp = 8.7e-4, 9.0
        xray_df = pd.DataFrame({"time_tag": pd.date_range(end=pd.Timestamp.now(), periods=60, freq="min"),
                                "flux": [1e-6 * (1.12 ** i) for i in range(60)]})
        kp_df = pd.DataFrame({"time_tag": xray_df["time_tag"],
                              "estimated_kp": [3 + i * 0.1 for i in range(60)]})
    else:
        xray_df, kp_df = get_xray(), get_kp()
        flux = float(xray_df["flux"].iloc[-1])
        kp = float(kp_df["estimated_kp"].iloc[-1])
except Exception as e:
    st.error(f"Could not fetch live data: {e}")
    st.stop()

r_lvl = radio_level(flux)
g_lvl = gnss_level(kp)

c1, c2, c3 = st.columns(3)
c1.metric("HF Radio Blackout", f"R{r_lvl}" if r_lvl else "None", f"X-ray flux {flux:.2e} W/m²")
c2.metric("GNSS Degradation Risk", g_lvl, f"Kp index {kp:.1f}")
pause = kp >= 7
c3.metric("Farm Equipment Sync", "⛔ PAUSE" if pause else ("⚠️ Caution" if kp >= 5 else "✅ Safe"))

st.subheader(f"{view} advice")
if view == "Telecom":
    if r_lvl >= 3: st.error("Strong HF blackout on the sunlit side of Earth. Switch to satellite or alternate links.")
    elif r_lvl >= 1: st.warning("Minor to moderate HF disruption possible. Monitor links.")
    else: st.success("No HF radio disruption expected.")
    if kp >= 5: st.warning("Geomagnetic storm: GNSS timing sources may be less reliable.")
else:
    if pause: st.error("GPS accuracy may drop. Pause auto-steer and precision farming equipment.")
    elif kp >= 5: st.warning("GPS accuracy may be reduced. Check equipment before autonomous operation.")
    else: st.success("GPS conditions normal. Safe to run automated equipment.")

st.subheader("Last 24 hours")
a, b = st.columns(2)
a.line_chart(xray_df.set_index("time_tag")["flux"])
b.line_chart(kp_df.set_index("time_tag")["estimated_kp"])