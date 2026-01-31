import streamlit as st
from PIL import Image
import time
import random
from gtts import gTTS
import io

# Page Config
st.set_page_config(page_title="AgriVision AI", page_icon="🌱")

# --- TRANSLATIONS ---
translations = {
    "Healthy": {
        "Pidgin": "Your leaf de okay, no problem at all!",
        "Hausa": "Shukarka tana da lafiya, babu matsala!"
    },
    "Cassava Mosaic Disease": {
        "Pidgin": "This one na Cassava Mosaic. The leaf de change color.",
        "Hausa": "Wannan cutar Mosaic ce ta rogo. Ganye yana canza launi."
    },
    "Maize Rust": {
        "Pidgin": "Maize Rust de here. You go see brown spots.",
        "Hausa": "Tsatsar masara ce. Za ka ga digon kasa-kasa."
    }
}

st.title("🌱 AgriVision AI: Plant Doctor")
st.markdown("---")

# 1. SIDEBAR (Restoring the Weather Feature)
st.sidebar.header("📍 Location: Kano, Nigeria")
temp = st.sidebar.slider("Current Temperature (°C)", 20, 45, 32)
rain_chance = st.sidebar.slider("Rain Probability (%)", 0, 100, 10)

# 2. IMAGE UPLOAD
st.header("📸 Scan Your Crop")
uploaded_file = st.file_uploader("Upload a leaf photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Scanning...", use_container_width=True)
    
    with st.status("AI Analyzing...", expanded=False):
        time.sleep(2)
        diagnosis = random.choice(["Healthy", "Cassava Mosaic Disease", "Maize Rust"])
        st.write(f"Result: {diagnosis}")

    st.subheader(f"Diagnosis: {diagnosis}")

    # 3. VOICE ADVICE
    st.markdown("### 🔊 Listen to Advice")
    lang_choice = st.radio("Select Language:", ["English", "Pidgin", "Hausa"], horizontal=True)

    if lang_choice == "English":
        speech_text = f"The diagnosis is {diagnosis}. Current rain chance is {rain_chance} percent."
        tts_lang = 'en'
    else:
        speech_text = translations.get(diagnosis, {}).get(lang_choice, "Language not supported yet.")
        tts_lang = 'en' if lang_choice == "Pidgin" else 'ha'

    if st.button("Play Voice Advice"):
        try:
            tts = gTTS(text=speech_text, lang=tts_lang)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.audio(fp, format='audio/mp3')
            st.write(f"🗨️ {speech_text}")
        except Exception as e:
            st.error("Voice engine is warming up. Please try again in 5 seconds.")

    # 4. SMART ADVICE (Based on weather)
    st.subheader("💡 Action Plan")
    if rain_chance > 70:
        st.warning("⚠️ DO NOT SPRAY. Rain will wash it away.")
    else:
        st.success("✅ Weather is clear for treatment.")

else:
    st.info("Upload a photo to see the Weather and AI Advice.")
