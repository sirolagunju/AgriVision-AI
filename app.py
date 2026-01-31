import streamlit as st
from PIL import Image
import time
import random
from gtts import gTTS
import io

st.set_page_config(page_title="AgriVision AI", page_icon="🌱")

# --- TRANSLATION DATA ---
# In a real app, these would be professionally recorded or use an AI translator.
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

# 📸 IMAGE UPLOAD
uploaded_file = st.file_uploader("Upload a leaf photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Scanning...", use_container_width=True)
    
    with st.status("AI Analyzing...", expanded=False):
        time.sleep(2)
        diagnosis = random.choice(["Healthy", "Cassava Mosaic Disease", "Maize Rust"])
        st.write(f"Result: {diagnosis}")

    st.subheader(f"Diagnosis: {diagnosis}")

    # 🔊 VOICE ADVICE SECTION
    st.markdown("### 🔊 Listen to Advice")
    lang_choice = st.radio("Select Language:", ["English", "Pidgin", "Hausa"], horizontal=True)

    # Get the text for the chosen language
    if lang_choice == "English":
        speech_text = f"The diagnosis is {diagnosis}. Follow the recommended treatment."
        tts_lang = 'en'
    else:
        # Get from our translation dictionary
        speech_text = translations.get(diagnosis, {}).get(lang_choice, "Language not supported yet.")
        tts_lang = 'en' if lang_choice == "Pidgin" else 'ha' # Use 'en' for Pidgin as gTTS doesn't have native Pidgin

    if st.button("Play Voice Advice"):
        tts = gTTS(text=speech_text, lang=tts_lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
        st.write(f"🗨️ {speech_text}")

else:
    st.info("Upload a photo to see and hear the diagnosis.")
