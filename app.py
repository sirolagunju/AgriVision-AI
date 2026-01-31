import streamlit as st
from PIL import Image
import time
import random

# Page Config
st.set_page_config(page_title="AgriVision AI", page_icon="🌱")

st.title("🌱 AgriVision AI: Plant Doctor")
st.markdown("---")

# 1. Sidebar for Weather (Hyper-local simulation)
st.sidebar.header("📍 Location: Kano, Nigeria")
temp = st.sidebar.slider("Current Temperature (°C)", 20, 45, 32)
rain_chance = st.sidebar.slider("Rain Probability (%)", 0, 100, 10)

# 2. Image Upload Section
st.header("📸 Scan Your Crop")
uploaded_file = st.file_uploader("Upload a photo of a leaf (Cassava, Maize, Tomato)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # 3. Simulate AI Processing
    with st.status("AI is analyzing leaf patterns...", expanded=True) as status:
        st.write("Detecting leaf edges...")
        time.sleep(1)
        st.write("Checking for fungal spores...")
        time.sleep(1)
        st.write("Comparing with 10,000+ disease signatures...")
        time.sleep(1)
        status.update(label="Analysis Complete!", state="complete", expanded=False)

    # 4. Logic for Diagnosis (Simulation)
    # In a real app, this is where the AI model would return a result
    diseases = ["Healthy", "Cassava Mosaic Disease", "Maize Rust", "Tomato Early Blight"]
    diagnosis = random.choice(diseases)

    # 5. Result Display
    st.subheader(f"Diagnosis: {diagnosis}")
    
    if diagnosis == "Healthy":
        st.success("Your crop looks great! No action needed.")
    else:
        st.error(f"Alert: {diagnosis} detected.")
        
        # Smart Advice based on Weather
        st.subheader("💡 Expert Advice")
        if rain_chance > 60:
            st.warning("⚠️ DO NOT SPRAY TODAY. High chance of rain will wash away treatments.")
        elif temp > 35:
            st.info("🕒 Apply treatment in the evening. It's too hot for the plant right now.")
        else:
            st.success("✅ Weather is optimal for treatment. Apply recommended fungicide.")

else:
    st.info("Please upload a leaf image to start the diagnosis.")

st.markdown("---")
st.caption("AgriVision AI v1.0 | Empowering Nigerian Farmers")
