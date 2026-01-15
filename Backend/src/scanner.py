import tensorflow as tf
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from urllib.parse import urlparse
from extractor import get_url_features 

# --- 1. SET UP AUTOMATIC PATHS ---
BASE_DIR = Path(__file__).resolve().parent.parent

# FIXED PATHS: Pointing to the new folders where train.py saves them
MODEL_PATH = BASE_DIR / "models" / "phishing_model_2026.h5"
SCALER_PATH = BASE_DIR / "pkl_files" / "scaler.pkl"
ENCODER_PATH = BASE_DIR / "pkl_files" / "encoder.pkl"

# --- 2. LOAD EVERYTHING ---
if not MODEL_PATH.exists():
    print(f"ERROR: Model not found at {MODEL_PATH}")
    exit()

model = tf.keras.models.load_model(str(MODEL_PATH))

with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

# Load the encoder to ensure labels match training exactly
with open(ENCODER_PATH, 'rb') as f:
    encoder = pickle.load(f)

# --- 3. GET USER INPUT ---
print("\n--- Deep Learning URL Shield ---")
user_url = input("Paste URL to scan: ").strip()

if not user_url.startswith('http'):
    test_url = "https://" + user_url
else:
    test_url = user_url

# --- 4. PROCESS ---
raw_features = get_url_features(test_url)
feature_names = scaler.feature_names_in_
features_df = pd.DataFrame([raw_features], columns=feature_names)
scaled_features = scaler.transform(features_df)

# 🛡️ THE HEURISTIC BYPASS
parsed = urlparse(test_url)
domain = (parsed.netloc or parsed.path.split('/')[0]).lower()
trusted_domains = ['google.com', 'wikipedia.org', 'microsoft.com', 'apple.com', 'github.com']

is_trusted = any(trusted in domain for trusted in trusted_domains)

if is_trusted:
    print("\n[HEURISTIC] Verified Trusted Domain.")
    label_name = "BENIGN"
    confidence = 100.0
    result_idx = 0 
else:
    # --- 5. PREDICT ---
    prediction = model.predict(scaled_features, verbose=0)
    result_idx = np.argmax(prediction)
    confidence = np.max(prediction) * 100

    # --- 6. MAPPING ---
    # We use the encoder to get the original label (0, 1, 2, or 3)
    raw_label = encoder.inverse_transform([result_idx])[0]
    
    # Map the numeric label to a readable name
    target_map = {0: "BENIGN", 1: "DEFACEMENT", 2: "PHISHING", 3: "MALWARE"}
    label_name = target_map.get(int(raw_label), "UNKNOWN")

    # --- 7. LOGIC GUARDRAILS ---
    if label_name == "PHISHING" and confidence < 90:
        if test_url.count('/') <= 3 and '?' not in test_url:
            label_name = "BENIGN (Low Suspicion)"
    elif confidence < 70 and label_name == "PHISHING":
        label_name = "BENIGN (Low Confidence)"

# --- 8. FINAL OUTPUT ---
print("\n" + "="*40)
print(f"ANALYZING: {test_url}")
print("-" * 40)
print(f"DETECTION RESULT : {label_name}")
print(f"CONFIDENCE SCORE : {confidence:.2f}%")
print(f"RAW INDEX        : {result_idx}") 
print("="*40)