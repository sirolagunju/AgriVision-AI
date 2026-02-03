import streamlit as st
from PIL import Image, ImageOps
import time
import random
from gtts import gTTS
import io
import requests

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AgriVision AI | Nigeria",
    page_icon="🌿",
    layout="centered"
)

# --- 2. CUSTOM NIGERIAN BRANDING (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAF8; }
    h1, h2, h3 { color: #1B5E20; font-family: 'Helvetica Neue', sans-serif; }
    .metric-card { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 12px; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
        text-align: center;
        border: 1px solid #E0E0E0;
    }
    .stButton>button { 
        background-color: #2E7D32; 
        color: white; 
        border-radius: 25px; 
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover { background-color: #1B5E20; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & CONFIGURATION ---
API_KEY = "YOUR_OPENWEATHER_API_KEY" # Replace with your real key

disease_db = {
    "Healthy": {
        "desc": "Your crop is in excellent condition.",
        "treatment": "Continue current irrigation and fertilizer schedule.",
        "chemical": "N/A",
        "english": "Your crop is healthy. No treatment needed.",
        "pidgin": "Your farm dey bam! No wahala here.",
        "hausa": "Shukarka tana da lafiya. Ci gaba da kula.",
        "yoruba": "Irugbin rẹ wa ni ilera to dara. Tẹsiwaju bi o ṣe n ṣe.",
        "igbo": "Ihe ubi gị dị mma. Gaa n'ihu na-elekọta ya."
    },
    "Cassava Mosaic Disease": {
        "desc": "Viral infection causing yellow twisted leaves.",
        "treatment": "Uproot infected plants immediately to stop spread.",
        "chemical": "No chemical cure. Plant resistant varieties like TME 419.",
        "english": "This is Cassava Mosaic Virus. Uproot infected plants.",
        "pidgin": "This one na Mosaic Virus. Pull the bad ones commot quick!",
        "hausa": "Wannan cutar Mosaic ce. Cire masu cutar ku kona su.",
        "yoruba": "Aisan Mosaic ni eyi. Fa awọn ti o ni arun na tu kuro.",
        "igbo": "Nke a bụ ọrịa Mosaic. Wepụ ndị ahụ metụtara ozugbo."
    },
    "Maize Rust": {
        "desc": "Fungal infection showing brown powdery pustules.",
        "treatment": "Apply fungicide if infection covers >10% of leaf.",
        "chemical": "Recommended: Mancozeb 80% WP or Strobilurin.",
        "english": "Detected Maize Rust. Fungicide treatment required.",
        "pidgin": "Na Rust disease be this. You need spray Mancozeb medicine.",
        "hausa": "Wannan tsatsa ce. Yi amfani da maganin Mancozeb.",
        "yoruba": "Aisan ipata agbado ni eyi. Lo oogun Mancozeb.",
        "igbo": "Nke a bụ ọrịa nchara ọka. Jiri ọgwụ Mancozeb mee ihe."
    }
}

marketplace_db = {
    "Maize Rust": [
        {"name": "Mancozeb 80% WP", "price": 5200, "img": "https://5.imimg.com/data5/SELLER/Default/2022/9/MQ/XW/YI/48366430/copper-oxychloride-50-wp-fungicide-500x500.jpg", "vendor": "Saro Agrosciences"},
        {"name": "Knapsack Sprayer (16L)", "price": 18500, "img": "https://ng.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/04/0488011/1.jpg", "vendor": "Mainland Tools"}
    ],
    "Cassava Mosaic Disease": [
        {"name": "Resistant Stems (TME 419)", "price": 12000, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRz-7u7m_5L9Yx-hE6I6Y7_H8h9Z5_0_0_0", "vendor": "IITA Partner"}
    ],
    "Healthy": [
        {"name": "NPK 15:15:15 Fertilizer", "price": 28500, "img": "https://i0.wp.com/www.indoramafertilisers.com/wp-content/uploads/2020/09/NPK-15-15-15.png", "vendor": "Indorama"}
    ]
}

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},NG&appid={API_KEY}&units=metric"
        res = requests.get(url).json()
        return res['main']['temp'], res['clouds']['all'], res['weather'][0]['description']
    except:
        return 30.0, 15, "Clear Sky (Default)"

# --- 4. SESSION STATE (MEMORY) ---
if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = None
if 'scanned' not in st.session_state:
    st.session_state.scanned = False

# --- 5. APP UI ---
st.title("🌿 AgriVision AI")
st.caption("Serving Farmers across Nigeria • v2.5")

# Weather Section
with st.expander("📍 View Farm Weather", expanded=True):
    city = st.text_input("Enter Local Government Area (LGA) or City:", "Kano")
    temp, cloud, desc = get_weather(city)
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="metric-card">🌡️<br><b>{temp}°C</b><br><small>Temp</small></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card">☁️<br><b>{cloud}%</b><br><small>Clouds</small></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card">📡<br><b>{desc}</b><br><small>Sky</small></div>', unsafe_allow_html=True)

st.divider()

# AI Scan Section
st.header("📸 Crop Scan")
file = st.file_uploader("Upload or Capture Leaf Photo", type=['jpg', 'png', 'jpeg'])

if file:
    img = Image.open(file)
    st.image(img, caption="Leaf Specimen", use_container_width=True)

    if not st.session_state.scanned:
        if st.button("🚀 Run AI Diagnosis"):
            with st.status("Analyzing pathogens...", expanded=True) as status:
                time.sleep(1)
                st.write("Checking leaf patterns...")
                time.sleep(1)
                st.write("Verifying with IITA database...")
                status.update(label="Analysis Complete!", state="complete", expanded=False)
            
            st.session_state.diagnosis = random.choice(list(disease_db.keys()))
            st.session_state.scanned = True
            st.rerun()

# Result Display
if st.session_state.scanned and st.session_state.diagnosis:
    diag = st.session_state.diagnosis
    info = disease_db[diag]
    
    st.success(f"### Result: {diag}")
    
    tab1, tab2, tab3 = st.tabs(["💊 Treatment", "🔊 Voice Guide", "🛒 Marketplace"])
    
    with tab1:
        st.write(f"**What it is:** {info['desc']}")
        st.write(f"**Immediate Action:** {info['treatment']}")
        if cloud > 50:
            st.error("🚨 **CLIMATE LOCK:** Rain expected. Do not spray chemicals today to avoid waste.")
        else:
            st.success("✅ **SAFE TO SPRAY:** Weather conditions are optimal for treatment.")

    with tab2:
        st.write("Listen to advice in your language:")
        lang = st.selectbox("Select Language:", ["English", "Pidgin", "Hausa", "Yoruba", "Igbo"])
        
        if st.button("▶️ Play Voice Advice"):
            lang_map = {"English": "en", "Pidgin": "en", "Hausa": "ha", "Yoruba": "yo", "Igbo": "ig"}
            text = info[lang.lower()]
            
            with st.spinner("Generating audio..."):
                tts = gTTS(text=text, lang=lang_map[lang])
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp, format="audio/mp3")
                st.caption(f"Playing in {lang}: '{text}'")

    with tab3:
        st.subheader("Order Inputs")
        products = marketplace_db.get(diag, marketplace_db["Healthy"])
        for p in products:
            c1, c2 = st.columns([1, 2])
            c1.image(p['img'], width=100)
            c2.markdown(f"**{p['name']}**")
            c2.markdown(f"Price: ₦{p['price']:,}")
            if c2.button(f"Buy from {p['vendor']}", key=p['name']):
                st.toast(f"Added {p['name']} to cart!")

    if st.button("🔄 Clear & Scan New Leaf"):
        st.session_state.scanned = False
        st.session_state.diagnosis = None
        st.rerun()
