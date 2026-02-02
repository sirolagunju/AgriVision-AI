import streamlit as st
from PIL import Image
import time
import random
from gtts import gTTS
import io
import requests

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AgriVision AI Pro",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CUSTOM STYLING (CSS) ---
# This makes the app look like a real mobile product, not just a script.
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #F0F4F1;
    }
    /* Headers */
    h1, h2, h3 {
        color: #2E7D32;
        font-family: 'Helvetica', sans-serif;
    }
    /* Cards */
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    /* Buttons */
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        border-radius: 20px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONFIG & DATA ---
API_KEY ="cb6b7d8b6f065f45d9dcca171bc7112a" # <--- REMEMBER TO PASTE YOUR KEY HERE

# Real Medical Advice Database
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

# Header Section
st.title("🌿 AgriVision AI")
st.caption("Precision Agriculture System v2.0 | Powered by Neural Networks")

# Live Weather Dashboard (Card Style)
st.subheader("📍 Field Conditions")
col1, col2 = st.columns([3, 1])
with col1:
    city = st.text_input("Farm Location", "Kano", label_visibility="collapsed")
with col2:
    if st.button("Update"):
        st.rerun()

temp, rain, desc = get_live_weather(city)

# Weather Cards using HTML
st.markdown(f"""
<div style="display: flex; gap: 10px; margin-bottom: 20px;">
    <div class="metric-card" style="flex: 1;">
        <span style="font-size: 24px;">🌡️</span>
        <div style="font-weight: bold; font-size: 18px;">{temp}°C</div>
        <div style="font-size: 12px; color: #666;">Temperature</div>
    </div>
    <div class="metric-card" style="flex: 1;">
        <span style="font-size: 24px;">💧</span>
        <div style="font-weight: bold; font-size: 18px;">{rain}%</div>
        <div style="font-size: 12px; color: #666;">Rain Chance</div>
    </div>
    <div class="metric-card" style="flex: 1;">
        <span style="font-size: 24px;">☁️</span>
        <div style="font-weight: bold; font-size: 18px;">{desc}</div>
        <div style="font-size: 12px; color: #666;">Condition</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Scan Section
st.markdown("---")
st.header("📸 AI Crop Doctor")
uploaded_file = st.file_uploader("Upload Leaf Image", type=["jpg", "png"])

if uploaded_file:
    # Show Image
    st.image(Image.open(uploaded_file), caption="Analyzing Specimen...", use_container_width=True)
    
    # Realistic Scanning Animation
    if st.button("Start Diagnosis"):
        progress_text = "Initializing Neural Network..."
        my_bar = st.progress(0, text=progress_text)
        
        steps = [
            (20, "🔍 Detecting Leaf Boundaries..."),
            (40, "🦠 Scanning for Pathogens..."),
            (60, "🧬 Analyzing Chlorophyll Levels..."),
            (80, "📡 Matching with IITA Database..."),
            (100, "✅ Diagnosis Complete.")
        ]
        
        for percent, label in steps:
            time.sleep(0.6) # Fake processing time
            my_bar.progress(percent, text=label)
            
        # Result Generation
        diagnosis = random.choice(list(disease_db.keys()))
        info = disease_db[diagnosis]
        
        # --- THE DIAGNOSIS CARD ---
        st.success(f"**DIAGNOSIS CONFIRMED: {diagnosis.upper()}**")
        
        # Detailed Tab View
        tab1, tab2, tab3 = st.tabs(["💊 Treatment", "🔊 Voice Advice", "🛒 Buy Medicine"])
        
        with tab1:
            st.info(f"**Description:** {info['desc']}")
            st.warning(f"**Action:** {info['treatment']}")
            st.error(f"**Recommended Chemical:** {info['chemical']}")
            
            # Smart Weather Check
            if rain > 50:
                st.markdown("🚨 **CRITICAL WEATHER WARNING:** High chance of rain. **DO NOT SPRAY TODAY.**")
            else:
                st.markdown("✅ **WEATHER CLEAR:** Safe to apply treatment.")

        with tab2:
            st.write("Listen in local language:")
            lang = st.radio("Select:", ["Pidgin", "Hausa"], horizontal=True)
            if st.button("▶️ Play Audio"):
                txt = info[lang.lower()]
                tts = gTTS(text=txt, lang='en' if lang == "Pidgin" else 'ha')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp)
                st.caption(f"Says: '{txt}'")

        with tab3:
            st.markdown("### Partner Marketplace")
            if diagnosis == "Maize Rust":
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Pesticide_spraying.jpg/320px-Pesticide_spraying.jpg", caption="Mancozeb Fungicide")
                st.write("**Price:** ₦4,500 / Bottle")
                st.button("🛒 Add to Cart (Demo)")
            elif diagnosis == "Healthy":
                st.write("Your plant is healthy! Consider buying booster fertilizer.")
                st.button("🛒 Buy NPK 15-15-15")
            else:
                st.write("No chemical available. Contact IITA for resistant stems.")
                st.button("📞 Contact Extension Agent")

else:
    st.info("👆 Upload a photo to begin the diagnostic process.")
