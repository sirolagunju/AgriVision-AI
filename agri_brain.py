import random

# --- 1. MOCK WEATHER SERVICE ---
# In production, replace this with a call to OpenWeatherMap or Ignitia API
def get_local_weather(location):
    # Simulating Kano weather conditions
    weather_scenarios = [
        {"condition": "Sunny", "temp": 34, "humidity": 40, "rain_chance": 5},
        {"condition": "Stormy", "temp": 28, "humidity": 85, "rain_chance": 90},
        {"condition": "Cloudy", "temp": 30, "humidity": 60, "rain_chance": 45}
    ]
    return random.choice(weather_scenarios)

# --- 2. MOCK VISION MODEL ---
# In production, this would load your 'yolo_v10.tflite' model
def diagnose_crop_disease(image_file):
    if image_file is None:
        return None
    
    # Simulating AI detection logic
    # We will randomly return a disease for this prototype
    diagnoses = [
        {"name": "Cassava Mosaic Disease", "severity": "High", "confidence": 0.94},
        {"name": "Maize Rust", "severity": "Medium", "confidence": 0.88},
        {"name": "Healthy", "severity": "None", "confidence": 0.99},
        {"name": "Fall Armyworm Damage", "severity": "Critical", "confidence": 0.91}
    ]
    return random.choice(diagnoses)

# --- 3. THE ADVISORY ENGINE (THE "SECRET SAUCE") ---
def generate_advice(disease, weather):
    advice = {
        "status": "Safe",
        "action": "",
        "warning": ""
    }
    
    # Logic Rule 1: Don't spray if rain is coming
    if weather['rain_chance'] > 70:
        advice['status'] = "DANGER"
        advice['warning'] = "⚠️ DO NOT SPRAY PESTICIDES! Heavy rain is expected."
        advice['action'] = f"Wait for the rain to pass. The rain will wash away the treatment for {disease['name']}."
    
    # Logic Rule 2: High Humidity + Fungal Disease = Outbreak Risk
    elif weather['humidity'] > 80 and "Rust" in disease['name']:
        advice['status'] = "URGENT"
        advice['warning'] = "High humidity detected. Fungus will spread fast."
        advice['action'] = "Apply fungicide immediately before evening."

    # Logic Rule 3: Healthy Plant
    elif disease['name'] == "Healthy":
        advice['status'] = "Good"
        advice['action'] = "Your crop looks healthy. Keep monitoring."
        
    # Default Rule
    else:
        advice['status'] = "Action Needed"
        advice['action'] = f"Treat {disease['name']} with recommended standard pesticide."

    return advice
