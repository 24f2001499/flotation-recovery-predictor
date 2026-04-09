"""
Quick model retraining script - Syncs models to sklearn 1.3.2
Skips all EDA, comparisons, and analysis. Just trains and saves.
Expected runtime: 5-7 minutes
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import pickle
from datetime import datetime
import os

print("="*60)
print("QUICK MODEL RETRAIN (sklearn 1.3.2)")
print("="*60)

# Step 1: Load and preprocess data
print("\n[1/5] Loading data...")
df = pd.read_csv("Data/Data.csv")
print(f"  Loaded {len(df)} rows from CSV")

# Remove NaN rows (99.6% of data)
df_clean = df.dropna()
print(f"  After removing NaN: {len(df_clean)} rows")

# Features (exclude target)
X = df_clean.iloc[:, :-1]
y = df_clean.iloc[:, -1]

print(f"  Features: {X.shape[1]}, Target: {y.shape[0]} samples")

# Step 2: Split data
print("\n[2/5] Train-test split (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"  Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

# Step 3: Scale features
print("\n[3/5] Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("  StandardScaler fitted and applied")

# Step 4: Train model
print("\n[4/5] Training Random Forest (100 trees, max_depth=8)...")
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=8,
    min_samples_split=10,
    min_samples_leaf=4,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train_scaled, y_train)

# Evaluate
train_r2 = rf_model.score(X_train_scaled, y_train)
test_r2 = rf_model.score(X_test_scaled, y_test)
print(f"  Train R²: {train_r2:.4f}")
print(f"  Test R²:  {test_r2:.4f}")

# Step 5: Save models
print("\n[5/5] Saving models...")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
models_dir = "models"
os.makedirs(models_dir, exist_ok=True)

# Save Random Forest
rf_path = f"{models_dir}/random_forest_model_{timestamp}.pkl"
joblib.dump(rf_model, rf_path)
print(f"  ✓ Saved RF: {rf_path}")

# Save Scaler
scaler_path = f"{models_dir}/feature_scaler_{timestamp}.pkl"
joblib.dump(scaler, scaler_path)
print(f"  ✓ Saved Scaler: {scaler_path}")

# Save Metadata
metadata = {
    "model_type": "RandomForestRegressor",
    "timestamp": timestamp,
    "sklearn_version": "1.3.2",
    "train_r2": float(train_r2),
    "test_r2": float(test_r2),
    "n_estimators": 100,
    "max_depth": 8,
    "n_features": X.shape[1],
    "train_samples": X_train.shape[0],
    "test_samples": X_test.shape[0]
}
metadata_path = f"{models_dir}/model_metadata_{timestamp}.pkl"
pickle.dump(metadata, open(metadata_path, 'wb'))
print(f"  ✓ Saved Metadata: {metadata_path}")

print("\n" + "="*60)
print("SUCCESS - Models retrained with sklearn 1.3.2")
print("="*60)
print(f"\nNew files saved with timestamp: {timestamp}")
print("Ready for Streamlit deployment!")
