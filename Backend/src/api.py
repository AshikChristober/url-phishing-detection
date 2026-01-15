import os

# ---- SYSTEM SETTINGS ----
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import pickle
import pandas as pd
import numpy as np
from tensorflow import keras

from src.extractor import get_url_features

# ---- APP INIT ----
app = FastAPI(title="Phishing Detection API 2026")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

model = None
scaler = None
encoder = None

# ---- CLASS MAP (IMPORTANT) ----
CLASS_MAP = {
    0: "BENIGN",
    1: "Malware",
    2: "PHISHING",
    3: "DEFACEMENT"
}

# ---- LOAD ARTIFACTS ----
try:
    model = keras.models.load_model(
        BASE_DIR / "models" / "phishing_model_2026.h5",
        compile=False
    )

    with open(BASE_DIR / "pkl_files" / "scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    with open(BASE_DIR / "pkl_files" / "encoder.pkl", "rb") as f:
        encoder = pickle.load(f)

    print("✅ Model, scaler, and encoder loaded successfully!")

except Exception as e:
    print("❌ Error loading artifacts:", e)

# ---- REQUEST MODEL ----
class URLRequest(BaseModel):
    url: str

# ---- PREDICT ----
@app.post("/predict")
async def predict_url(request: URLRequest):
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        url = request.url

        features = get_url_features(url)
        df = pd.DataFrame([features], columns=scaler.feature_names_in_)
        scaled = scaler.transform(df)

        probs = model.predict(scaled, verbose=0)[0]

        confidences = {
            CLASS_MAP[i]: f"{float(prob) * 100:.2f}%"
            for i, prob in enumerate(probs)
        }

        final_prediction = CLASS_MAP[int(np.argmax(probs))]

        return {
            "url": url,
            "final_prediction": final_prediction,
            "confidences": confidences,
            "status": "Success"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
