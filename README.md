# ⛏️ Froth Flotation Recovery Predictor

**Real-time ML predictions for optimizing iron ore recovery in froth flotation plants**

## 🎯 Overview

This project provides a production-ready machine learning solution for predicting iron ore concentrate recovery based on process parameters. The model predicts iron concentrate percentage (%) based on 21 operational parameters including pH, density, chemical dosing, air flows, and column levels.

### Key Features

- **⚡ Real-time Predictions**: Get instant predictions from plant parameters
- **📊 Batch Processing**: Analyze 100s of samples at once
- **🔧 Parameter Optimization**: Explore how different parameters affect recovery
- **📈 Interactive Dashboard**: Web-based UI for easy access
- **🚀 Cloud Deployed**: Available on Streamlit Cloud for 24/7 access

---

## 🌐 Live Demo

**🚀 Access the app here**: <https://flotation-recovery-predictor-zqghhtovnz7eppw9fnggh3.streamlit.app/>

(Replace `YOUR_USERNAME` with your actual GitHub username after deployment)

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **Algorithm** | Random Forest (Regularized) |
| **Test R²** | 0.288 (29% variance explained) |
| **Test RMSE** | ±0.92% |
| **Test MAE** | ±0.72% |
| **Cross-Val R²** | 0.259 ± 0.019 |
| **Training Samples** | 3,158 |
| **Test Samples** | 790 |
| **Features** | 21 parameters |

### Model Accuracy

- **Real-world accuracy:**±0.92% typical error
- **Confidence range**: ±1.8% (95% CI)
- **Use case**: Decision support + expert judgment

---

## 📁 Project Structure

```
flotation-recovery-predictor/
├── streamlit_app.py                  # Main web application
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── STREAMLIT_DEPLOYMENT_GUIDE.md     # Deployment instructions
├── Froth_Flotation_Recovery_Model.ipynb  # Training notebook
├── models/                           # Trained models
│   ├── random_forest_model_*.pkl     # Prediction model
│   ├── feature_scaler_*.pkl          # Feature scaler
│   ├── model_metadata_*.pkl          # Model metrics
│   └── model_info_*.json             # Human-readable info
├── .streamlit/
│   └── config.toml                   # Streamlit configuration
└── .gitignore                        # Git ignore rules
```

---

## 🚀 Quick Start

### Option 1: Use Live App (Easiest)

1. Click the link above
2. Select prediction mode from sidebar
3. Enter parameters
4. Get instant predictions ⚡

### Option 2: Run Locally

```bash
# Clone repository
git clone https://github.com/24f2001499/flotation-recovery-predictor
cd flotation-recovery-predictor

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

App opens at: `http://localhost:8501`

---

## 📋 Using the App

### 🎯 Single Prediction Mode

- Enter process parameters using interactive sliders
- Get instant prediction with confidence interval
- See color-coded result (excellent/good/suboptimal)

**Example:**

```
pH: 10.0
Density: 1.75
Starch Flow: 2500 mL/min
Amina Flow: 450 mL/min
↓
Predicted Iron Concentrate: 65.49%
Confidence Range: 64.57% - 66.41%
```

### 📈 Batch Analysis Mode

- Upload CSV with multiple samples
- Get predictions for all samples
- Download results
- See statistical summary

**CSV Format Example:**

```
% Iron Feed,% Silica Feed,Ore Pulp pH,Ore Pulp Density,...
67.5,2.1,10.0,1.75,...
68.0,2.2,9.9,1.78,...
...
```

### 🔧 Parameter Optimization Mode

- Select a parameter to vary
- See how it affects recovery
- Find optimal values
- Interactive sensitivity analysis

### ℹ️ Model Information

- View detailed model metrics
- See feature descriptions
- Read deployment info
- Check limitations & best practices

---

## 🔧 Technical Details

### Features (21 total)

**Feed Quality (2):**

- % Iron Feed
- % Silica Feed

**Process Control (19):**

- Ore Pulp pH
- Ore Pulp Density
- Ore Pulp Flow
- Starch Flow
- Amina Flow
- Flotation Column 01-07 Air Flow (7)
- Flotation Column 01-07 Level (7)

### Model Architecture

- **Algorithm**: Random Forest Regressor
- **Trees**: 100
- **Max Depth**: 8 (regularized)
- **Min Samples Split**: 10
- **Min Samples Leaf**: 4

### Training Data

- **Total Samples**: 3,948 (after NaN removal)
- **Training**: 3,158 samples (80%)
- **Testing**: 790 samples (20%)
- **Features**: 21 parameters
- **Target**: % Iron Concentrate

---

## ⚠️ Important Notes

### Model Limitations

- ✅ Explains ~29% of variance
- ❌ 71% influenced by unmeasured factors
- ✅ Typical error: ±0.92%
- ⚠️ Use as **decision support only**
- ⚠️ Always validate with expert judgment

### When to Retrain

- 📅 Monthly: Check actual vs predicted
- 🔄 Quarterly: Retrain with new data
- 🚨 When: Process changes significantly
- 📊 If: Predictions diverge from reality

### Best Practices

1. ✅ Start with recommended parameters as baseline
2. ✅ Test in controlled trials first
3. ✅ Monitor actual recovery vs predictions
4. ✅ Combine with operator expertise
5. ✅ Log predictions for future improvement

---

## 🚀 Deployment Instructions

See [STREAMLIT_DEPLOYMENT_GUIDE.md](./STREAMLIT_DEPLOYMENT_GUIDE.md) for complete deployment guide.

**Quick Summary:**

1. Create GitHub account
2. Upload files to GitHub
3. Connect to Streamlit Cloud
4. Click "Deploy"
5. Share public URL

**Complete in <5 minutes!**

---

## 📚 Documentation

- **Deployment Guide**: [STREAMLIT_DEPLOYMENT_GUIDE.md](./STREAMLIT_DEPLOYMENT_GUIDE.md)
- **Model Usage Guide**: [MODELS_USAGE_GUIDE.md](./MODELS_USAGE_GUIDE.md)
- **Analysis & Fixes**: [ANALYSIS_FIXES_SUMMARY.md](./ANALYSIS_FIXES_SUMMARY.md)
- **Training Notebook**: [Froth_Flotation_Recovery_Model.ipynb](./Froth_Flotation_Recovery_Model.ipynb)

---

## 📊 Model Training

The model was trained using:

- **Data Source**: Industrial flotation plant records (1,048,575 hourly measurements)
- **Clean Data**: 3,948 complete records
- **Validation**: 5-fold cross-validation
- **Regularization**: Depth-limited trees + min samples constraints

See notebook for complete training pipeline.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Web Framework** | Streamlit 1.28.1 |
| **ML Model** | Scikit-learn 1.3.2 |
| **Data Processing** | Pandas 2.1.3 |
| **Visualization** | Plotly 5.18.0 |
| **Hosting** | Streamlit Cloud |
| **Version Control** | Git/GitHub |

---

## 📝 Citation

If you use this project, please cite:

```
Flotation Recovery Predictor
Version 1.0 (April 2026)
Machine Learning Model for Froth Flotation Optimization
Dataset: 3,948 plant records | Features: 21 | Algorithm: Random Forest
```

---

## 📞 Support & Contact

- **Issues**: GitHub Issues
- **Streamlit Docs**: <https://docs.streamlit.io/>
- **Streamlit Cloud**: <https://share.streamlit.io/>
- **GitHub**: <https://github.com/>

---

## 📄 License

MIT License - Feel free to use and modify for your needs

---

## 🙏 Acknowledgments

- Built with Streamlit for easy deployment
- Machine learning by Scikit-learn
- Data visualization by Plotly
- Froth flotation domain expertise

---

**🚀 Deploy now and start making predictions! →** [STREAMLIT_DEPLOYMENT_GUIDE.md](./STREAMLIT_DEPLOYMENT_GUIDE.md)

---

### Last Updated

April 10, 2026

### Version

1.0 - Initial Release
