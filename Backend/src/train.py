from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import pickle 
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping

# --- 1. DIRECTORY CONFIGURATION (FIXED) ---
# This script is in /src, so we go up to the project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "Dataset" / "master_dataset.csv"

# Output Paths (Automatically putting them in the right folders)
MODEL_OUT = BASE_DIR / "models" / "phishing_model_2026.h5"
SCALER_OUT = BASE_DIR / "pkl_files" / "scaler.pkl"
ENCODER_OUT = BASE_DIR / "pkl_files" / "encoder.pkl"
RESULT_OUT = BASE_DIR / "results" / "confusion_matrix.png"

# --- 2. DATA LOADING & BALANCING ---
print(f"Loading data from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

df_0 = df[df['label'] == 0]
df_1 = df[df['label'] == 1]
df_2 = df[df['label'] == 2]
df_3 = df[df['label'] == 3]

df_0_downsampled = resample(df_0, replace=False, n_samples=100000, random_state=42)
df_balanced = pd.concat([df_0_downsampled, df_1, df_2, df_3])

X = df_balanced.drop(['label'], axis=1)
y = df_balanced['label']

# --- 3. PREPROCESSING ---
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
class_names = [str(c) for c in encoder.classes_]

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

scaler = RobustScaler() 
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# --- 4. MODEL BUILDING ---
weights = compute_class_weight('balanced', classes=np.unique(y_encoded), y=y_encoded)
class_weight_dict = dict(enumerate(weights))

model = Sequential([
    Dense(256, activation='relu', input_shape=(X_train.shape[1],)),
    BatchNormalization(),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# --- 5. TRAINING ---
print("Training started...")
model.fit(X_train, y_train, epochs=50, batch_size=128, 
          validation_split=0.2, class_weight=class_weight_dict, 
          callbacks=[early_stop], verbose=1)

# --- 6. EVALUATION ---
y_pred = np.argmax(model.predict(X_test), axis=1)
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.savefig(RESULT_OUT)

# --- 7. SAVING ARTIFACTS (CRITICAL FIX) ---
# We save to the organized folders, NOT the src folder
model.save(str(MODEL_OUT))
with open(SCALER_OUT, 'wb') as f:
    pickle.dump(scaler, f)
with open(ENCODER_OUT, 'wb') as f:
    pickle.dump(encoder, f)

print(f"\nSUCCESS! Files synced in models/ and pkl_files/")