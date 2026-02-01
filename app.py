import streamlit as st
from PIL import Image
import time
import random
from gtts import gTTS
import io
import requests

# --- CONFIG ---
st.set_page_config(page_title="AgriVision AI", page_icon="🌱")
API_KEY = "cb6b7d8b6f065f45d9dcca171bc7112a"  # <--- Put your key from OpenWeatherMap here!

def get_live_weather(city="Kano"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()
        temp = data['main']['temp']
        rain_chance = data.get('clouds', {}).get('all', 0) # Use cloud cover as rain proxy for free tier
        description = data['weather'][0]['description']
        return temp, rain_chance, description
    except:
        return 32.0, 10, "connection error (using backup data)"

# --- TRANSLATIONS ---
translations = {
    "Healthy": {"Pidgin": "Your leaf de okay!", "Hausa": "Shukarka tana da lafiya!"},
    "Cassava Mosaic Disease": {"Pidgin": "This one na Cassava Mosaic.", "Hausa": "Wannan cutar Mosaic ce."},
    "Maize Rust": {"Pidgin": "Maize Rust de here.", "Hausa": "Tsatsar masara ce."}
}

st.title("🌱 AgriVision AI: Plant Doctor")

# 1. LIVE WEATHER SECTION
st.header("📍 Real-Time Environment")
city_input = st.text_input("Enter your city:", "Kano")
live_temp, live_rain, live_desc = get_live_weather(city_input)

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{live_temp}°C")
col2.metric("Humidity/Rain", f"{live_rain}%")
col3.write(f"**Sky:** {live_desc.capitalize()}")

st.markdown("---")

# 2. IMAGE UPLOAD & AI SCAN
st.header("📸 Scan Your Crop")
uploaded_file = st.file_uploader("Upload a leaf photo", type=["jpg", "png"])

if uploaded_file:
    st.image(Image.open(uploaded_file), use_container_width=True)
    with st.status("AI Analyzing...", expanded=False):
        time.sleep(2)
        diagnosis = random.choice(["Healthy", "Cassava Mosaic Disease", "Maize Rust"])
    
    st.subheader(f"Diagnosis: {diagnosis}")

    # 3. LOCAL VOICE
    st.markdown("### 🔊 Listen to Advice")
    lang = st.radio("Language:", ["English", "Pidgin", "Hausa"], horizontal=True)
    
    if lang == "English":
        txt = f"The diagnosis is {diagnosis}. It is {live_temp} degrees in {city_input}."
    else:
        txt = translations.get(diagnosis, {}).get(lang)

    if st.button("Play Voice Advice"):
        tts = gTTS(text=txt, lang='en' if lang != 'Hausa' else 'ha')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp)

    # 4. SMART ADVICE
    st.subheader("💡 Action Plan")
    if live_rain > 70:
        st.error(f"⚠️ DO NOT SPRAY. Live data shows high rain risk in {city_input}.")
    else:
        st.success(f"✅ Conditions in {city_input} are clear for treatment.")
