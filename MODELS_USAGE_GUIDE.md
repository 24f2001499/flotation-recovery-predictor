# Saved Models - Usage Guide

## 📁 Saved Files Location

```
d:\tanmay\Meta_project\models\
```

## 📦 What Was Saved

| File | Type | Purpose | Size |
|------|------|---------|------|
| `random_forest_model_*.pkl` | Binary (Pickle/Joblib) | Main prediction model | ~5-10 MB |
| `linear_regression_model_*.pkl` | Binary (Pickle) | Baseline model | ~1 KB |
| `feature_scaler_*.pkl` | Binary (Pickle) | Feature normalization | ~5 KB |
| `model_metadata_*.pkl` | Binary (Pickle) | Model metrics & features | ~10 KB |
| `model_info_*.json` | JSON (Text) | Human-readable metadata | ~1 KB |

**Timestamp Format:** `YYYYMMDD_HHMMSS` (e.g., `20260410_010319`)

---

## 🚀 Quick Start: Using Saved Models

### Option 1: Load Latest Models Automatically

```python
import joblib
import pickle
import glob
import os

models_dir = r'd:\tanmay\Meta_project\models'

# Find latest files
rf_files = glob.glob(os.path.join(models_dir, 'random_forest_model_*.pkl'))
scaler_files = glob.glob(os.path.join(models_dir, 'feature_scaler_*.pkl'))

# Load most recent
rf_model = joblib.load(max(rf_files, key=os.path.getctime))
scaler = pickle.load(open(max(scaler_files, key=os.path.getctime), 'rb'))
```

### Option 2: Load Specific Model by Timestamp

```python
import joblib
import pickle

timestamp = '20260410_010319'
models_dir = r'd:\tanmay\Meta_project\models'

rf_model = joblib.load(os.path.join(models_dir, f'random_forest_model_{timestamp}.pkl'))
scaler = pickle.load(open(os.path.join(models_dir, f'feature_scaler_{timestamp}.pkl'), 'rb'))
metadata = pickle.load(open(os.path.join(models_dir, f'model_metadata_{timestamp}.pkl'), 'rb'))
```

---

## 🔮 Making Predictions

### Step 1: Prepare New Data

```python
import pandas as pd

# Create DataFrame with 21 features (same as training)
new_data = pd.DataFrame({
    'Ore Pulp pH': [10.0],
    'Ore Pulp Density': [1.75],
    'Starch Flow': [2500.0],
    # ... all 21 features ...
})
```

### Step 2: Scale the Data

```python
# Feature names from metadata
features = metadata['all_features']
new_data_scaled = scaler.transform(new_data[features])
```

### Step 3: Make Prediction

```python
prediction = rf_model.predict(new_data_scaled)[0]
print(f"Predicted Iron Concentrate: {prediction:.2f}%")
print(f"Confidence: R² = 0.29 (±0.09% typical error)")
print(f"Recommended Range: {prediction-0.5:.2f}% - {prediction+0.5:.2f}%")
```

---

## 📊 Model Information

### Performance Metrics

```
Train R²:              0.5303 (on 3,158 training samples)
Test R²:               0.2879 (on 790 test samples) ← USE THIS
Cross-Val R²:          0.2591 ± 0.0188 (5-fold CV)
Test RMSE:             0.9190%
Test MAE:              0.7176%
```

### Model Configuration

```
Algorithm:             Random Forest (100 trees)
Max Depth:             8 (regularized to prevent overfitting)
Min Samples Split:     10
Min Samples Leaf:      4
Features:              21 industrial parameters
Training Samples:      3,158
Test Samples:          790
```

### Feature List (21 total)

**Feed Quality (2):**

- % Iron Feed
- % Silica Feed

**Control Parameters (19):**

- Ore Pulp pH
- Ore Pulp Density
- Ore Pulp Flow
- Starch Flow
- Amina Flow
- Flotation Column 01-07 Air Flow (7 features)
- Flotation Column 01-07 Level (7 features)

**Target Variable:**

- % Iron Concentrate (what we predict)

---

## ⚠️ Important Notes

### Model Accuracy

- **Real-world accuracy: ±0.92% (RMSE)**
- Predictions should be used as **decision support only**
- Combine with expert judgment and validation trials
- Expected uncertainty: ±0.5-1.0% range

### When to Retrain

- Monthly: Check prediction accuracy against actual production
- Quarterly: Retrain with accumulated new data
- When: Significant process changes occur
- If: Predictions consistently diverge from reality

### Limitations

- Model explains only 29% of variance (71% by unmeasured factors)
- Requires complete data for all 21 features
- Features must be scaled with included scaler
- Not suitable for ore types outside training distribution

---

## 🔄 Workflow Integration

### For Real-Time Predictions

1. **Collect** plant data (21 parameters)
2. **Format** as pandas DataFrame
3. **Scale** using saved scaler
4. **Predict** using saved model
5. **Validate** result is in expected range
6. **Alert** operator if anomaly detected
7. **Log** prediction for future retraining

### For Batch Processing

```python
# Process multiple records
for idx, row in new_data.iterrows():
    scaled = scaler.transform(row.values.reshape(1, -1))
    prediction = rf_model.predict(scaled)[0]
    results.append(prediction)
```

---

## 📝 JSON Metadata Example

```json
{
    "timestamp": "20260410_010319",
    "model_type": "Random Forest (Regularized)",
    "features": 21,
    "training_samples": 3158,
    "test_samples": 790,
    "performance": {
        "train_r2": 0.5303,
        "test_r2": 0.2878,
        "rmse": 0.9190,
        "mae": 0.7176,
        "cv_mean_r2": 0.2591,
        "cv_std_r2": 0.0188
    },
    "files": {
        "linear_regression_model": "linear_regression_model_20260410_010319.pkl",
        "random_forest_model": "random_forest_model_20260410_010319.pkl",
        "scaler": "feature_scaler_20260410_010319.pkl",
        "metadata": "model_metadata_20260410_010319.pkl"
    }
}
```

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| `FileNotFoundError` | Ensure model files exist in `d:\tanmay\Meta_project\models\` |
| `ValueError: wrong number of features` | Check DataFrame has all 21 required features |
| `KeyError on column name` | Verify feature names match exactly (case-sensitive) |
| `Predictions seem wrong` | Verify data was scaled using the saved scaler |
| `Models won't load` | Regenerate models by running notebook training cells |

---

## 📞 Support

- **Notebook Location:** `d:\tanmay\Meta_project\Froth_Flotation_Recovery_Model.ipynb`
- **Models Location:** `d:\tanmay\Meta_project\models\`
- **Training Data:** `d:\tanmay\Meta_project\Data for FlotationNet.../Data/Data.csv`
- **Metadata:** See `model_info_*.json` files

---

Generated: April 10, 2026
Model Version: 20260410_010319
