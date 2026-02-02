import streamlit as st
from PIL import Image
import time
import random
from gtts import gTTS
import io
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AgriVision AI Pro", page_icon="🌿", layout="centered")

# --- 2. CUSTOM STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F1; }
    h1, h2, h3 { color: #2E7D32; font-family: 'Helvetica', sans-serif; }
    .metric-card { background-color: #FFFFFF; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
    .stButton>button { background-color: #2E7D32; color: white; border-radius: 20px; border: none; width: 100%; }
    .stButton>button:hover { background-color: #1B5E20; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & API ---
API_KEY = "cb6b7d8b6f065f45d9dcca171bc7112a"# <--- RE-PASTE YOUR KEY HERE!

disease_db = {
    "Healthy": {
        "desc": "Your crop is in excellent condition.",
        "treatment": "Continue current irrigation and fertilizer schedule.",
        "chemical": "N/A",
        "pidgin": "Your farm dey bam! No wahala here.",
        "hausa": "Shukarka tana da lafiya. Ci gaba da kula da ita."
    },
    "Cassava Mosaic Disease": {
        "desc": "Viral infection causing yellow twisted leaves.",
        "treatment": "Uproot infected plants immediately to stop spread.",
        "chemical": "No chemical cure. Plant resistant varieties like TME 419.",
        "pidgin": "This one na Mosaic Virus. Pull the bad ones commot quick quick!",
        "hausa": "Wannan cutar Mosaic ce. Cire masu cutar ku kona su."
    },
    "Maize Rust": {
        "desc": "Fungal infection showing brown powdery pustules.",
        "treatment": "Apply fungicide if infection covers >10% of leaf.",
        "chemical": "Recommended: Mancozeb 80% WP or Strobilurin.",
        "pidgin": "Na Rust disease be this. You need spray Mancozeb medicine.",
        "hausa": "Wannan tsatsa ce. Yi amfani da maganin Mancozeb."
    }
}

def get_live_weather(city="Kano"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()
        return data['main']['temp'], data['clouds']['all'], data['weather'][0]['description']
    except:
        return 32.5, 20, "sunny intervals (Simulated)"

# --- 4. THE APP INTERFACE ---
st.title("🌿 AgriVision AI")
st.caption("Precision Agriculture System v2.0")

# Weather Section
st.subheader("📍 Field Conditions")
col1, col2 = st.columns([3, 1])
with col1:
    city = st.text_input("Farm Location", "Kano", label_visibility="collapsed")
with col2:
    if st.button("Update"):
        st.rerun()

temp, rain, desc = get_live_weather(city)

st.markdown(f"""
<div style="display: flex; gap: 10px; margin-bottom: 20px;">
    <div class="metric-card" style="flex: 1;">
        <span style="font-size: 24px;">🌡️</span>
        <div style="font-weight: bold;">{temp}°C</div>
        <div style="font-size: 12px; color: #666;">Temperature</div>
    </div>
    <div class="metric-card" style="flex: 1;">
        <span style="font-size: 24px;">💧</span>
        <div style="font-weight: bold;">{rain}%</div>
        <div style="font-size: 12px; color: #666;">Rain Chance</div>
    </div>
    <div class="metric-card" style="flex: 1;">
        <span style="font-size: 24px;">☁️</span>
        <div style="font-weight: bold;">{desc}</div>
        <div style="font-size: 12px; color: #666;">Condition</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Scan Section
st.markdown("---")
st.header("📸 AI Crop Doctor")
uploaded_file = st.file_uploader("Upload Leaf Image", type=["jpg", "png"])

if uploaded_file:
    st.image(Image.open(uploaded_file), caption="Analyzing Specimen...", use_container_width=True)
    
    if st.button("Start Diagnosis"):
        # Fake Loading
        progress_text = "Initializing Neural Network..."
        my_bar = st.progress(0, text=progress_text)
        for percent in [20, 40, 60, 80, 100]:
            time.sleep(0.2)
            my_bar.progress(percent, text="Scanning...")
            
        diagnosis = random.choice(list(disease_db.keys()))
        info = disease_db[diagnosis]
        
        st.success(f"**DIAGNOSIS: {diagnosis.upper()}**")
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["💊 Treatment", "🔊 Voice Advice", "🛒 Marketplace"])
        
        with tab1:
            st.info(f"**Treatment:** {info['treatment']}")
            st.warning(f"**Chemical:** {info['chemical']}")
            if rain > 50:
                st.error("🚨 CRITICAL: High rain chance. DO NOT SPRAY TODAY.")
            else:
                st.success("✅ Weather is clear for treatment.")

        with tab2:
            st.write("Listen in local language:")
            lang = st.radio("Select:", ["Pidgin", "Hausa"], horizontal=True)
            
            # --- THE FIXED AUDIO SECTION ---
            if st.button("▶️ Play Audio"):
                try:
                    with st.spinner("Generating Voice Note..."):
                        # Select language code
                        lang_code = 'en' if lang == "Pidgin" else 'ha'
                        text_to_speak = info[lang.lower()]
                        
                        # Create audio
                        tts = gTTS(text=text_to_speak, lang=lang_code)
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        
                        # THE MAGIC FIX: Rewind the file pointer
                        fp.seek(0)
                        
                        st.audio(fp, format='audio/mp3')
                        st.caption(f"Playing: '{text_to_speak}'")
                        
                except Exception as e:
                    st.error(f"Voice Error: {e}")

        with tab3:
            st.write("Partner Suppliers:")
            st.button("🛒 Buy Recommended Fungicide (Demo)")

else:
    st.info("👆 Upload a photo to begin.")
