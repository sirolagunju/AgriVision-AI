import streamlit as st
import agri_brain as brain
from PIL import Image

# --- APP CONFIGURATION ---
st.set_page_config(page_title="AgriVision AI", page_icon="🌱")

# --- SIDEBAR (Language & Location) ---
st.sidebar.title("⚙️ Settings")
language = st.sidebar.selectbox("Language", ["English", "Hausa", "Yoruba", "Pidgin"])
location = st.sidebar.text_input("Farm Location", "Kano, Nigeria")

# --- MAIN HEADER ---
st.title("🌱 AgriVision AI")
st.write("Scan your crop. Check the weather. Save your harvest.")
st.markdown("---")

# --- SECTION 1: WEATHER INTELLIGENCE ---
st.header(f"1. Weather in {location}")
if st.button("Check Local Weather"):
    weather = brain.get_local_weather(location)
    
    # Display Weather Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Condition", weather['condition'])
    col2.metric("Temperature", f"{weather['temp']}°C")
    col3.metric("Rain Chance", f"{weather['rain_chance']}%")
    
    # Store weather in session state for the advisory engine
    st.session_state['weather'] = weather

# --- SECTION 2: CROP VISION ---
st.header("2. Crop Diagnosis")
uploaded_file = st.file_uploader("Take a photo or upload an image of the leaf...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Leaf Image', use_column_width=True)
    
    st.write("Analyzing...")
    
    # Get AI Diagnosis
    diagnosis = brain.diagnose_crop_disease(uploaded_file)
    
    if diagnosis:
        st.success(f"**Diagnosis:** {diagnosis['name']}")
        st.info(f"**Confidence:** {int(diagnosis['confidence']*100)}%")
        
        # --- SECTION 3: INTEGRATED ADVISORY ---
        st.header("3. AI Agronomist Advice")
        
        # Check if we have weather data, if not, fetch default
        if 'weather' not in st.session_state:
            st.session_state['weather'] = brain.get_local_weather(location)
            
        final_advice = brain.generate_advice(diagnosis, st.session_state['weather'])
        
        # Display Recommendation
        if final_advice['status'] == "DANGER":
            st.error(final_advice['warning'])
            st.error(f"**Action Plan:** {final_advice['action']}")
        elif final_advice['status'] == "URGENT":
            st.warning(final_advice['warning'])
            st.warning(f"**Action Plan:** {final_advice['action']}")
        else:
            st.success(f"**Action Plan:** {final_advice['action']}")

# --- FOOTER ---
st.markdown("---")
st.caption("AgriVision AI Prototype v1.0 | Offline-First Architecture")
