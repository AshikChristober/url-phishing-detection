import pickle
import numpy as np
from extractor import get_url_features

# 1. Load your scaler
try:
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    print("✅ Scaler loaded successfully.")
except:
    print("❌ Could not find scaler.pkl")

# 2. Test Google (Should be Benign) and a Fake Phish
urls = ["https://google.com", "http://urgent-action-required-login.xyz"]

for url in urls:
    print(f"\n--- Testing URL: {url} ---")
    raw = get_url_features(url)
    
    # Convert to 2D array for the scaler
    raw_array = np.array(raw).reshape(1, -1)
    
    # Scale the features
    scaled = scaler.transform(raw_array)
    
    print(f"Raw Features (First 5): {raw[:5]}")
    print(f"Scaled Features (First 5): {scaled[0][:5]}")
    
    # Check for "Extreme" values
    if np.any(np.abs(scaled) > 10):
        print("⚠️ WARNING: Your Scaler is producing extreme outliers. This is why the model is failing.")
