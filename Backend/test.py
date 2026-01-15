import tensorflow as tf
import numpy as np
import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
model = tf.keras.models.load_model(str(BASE_DIR / "models" / "phishing_model_2026.h5"))
print("Model loaded! Testing prediction...")
# Create dummy data (adjust the number 30 to your feature count)
dummy_input = np.random.rand(1, 30) 
pred = model.predict(dummy_input)
print("Prediction successful:", pred)
