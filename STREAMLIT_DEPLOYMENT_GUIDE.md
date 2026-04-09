# 🚀 Streamlit Cloud Deployment Guide

## Quick Start: Deploy to Streamlit Cloud in 5 Minutes

### Step 1: Prepare GitHub Repository

1. **Create a GitHub account** (if you don't have one): <https://github.com>
2. **Create a new repository**:
   - Go to <https://github.com/new>
   - Name it: `flotation-recovery-predictor`
   - Make it **PUBLIC** (for Streamlit Cloud)
   - Check "Add a README file"
   - Click "Create repository"

3. **Upload files to GitHub**:

   ```bash
   cd d:\tanmay\Meta_project
   git init
   git add .
   git commit -m "Initial commit: Streamlit app for flotation recovery"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/flotation-recovery-predictor.git
   git push -u origin main
   ```

   **Or manually**: Upload these files through GitHub web interface:
   - `streamlit_app.py` (main app file)
   - `requirements.txt` (dependencies)
   - `models/random_forest_model_*.pkl` (model file)
   - `models/feature_scaler_*.pkl` (scaler file)
   - `models/model_metadata_*.pkl` (metadata)
   - `.streamlit/config.toml` (configuration)
   - `README.md`

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: <https://share.streamlit.io/>
2. **Sign in with GitHub** (creates account automatically)
3. **Click "New app"** button
4. **Fill deployment form**:
   - **Repository**: Select `YOUR_USERNAME/flotation-recovery-predictor`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. **Click "Deploy!"**
6. **Wait** 2-3 minutes for deployment to complete
7. **Your app is now live!** 🎉

**Your public URL will be**: `https://share.streamlit.io/YOUR_USERNAME/flotation-recovery-predictor`

---

## Directory Structure

```
flotation-recovery-predictor/
├── streamlit_app.py           # Main application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── models/                     # Machine learning models
│   ├── random_forest_model_20260410_010319.pkl
│   ├── feature_scaler_20260410_010319.pkl
│   ├── model_metadata_20260410_010319.pkl
│   └── model_info_20260410_010319.json
└── .streamlit/
    └── config.toml            # Streamlit configuration
```

---

## 📋 Complete File Checklist

Before deploying, make sure you have:

✅ **streamlit_app.py** - Main application file
✅ **requirements.txt** - Python dependencies  
✅ **.streamlit/config.toml** - Configuration (optional but recommended)
✅ **models/** directory with:

- `random_forest_model_*.pkl`
- `feature_scaler_*.pkl`
- `model_metadata_*.pkl`
- `model_info_*.json`
✅ **README.md** - Project description
✅ **.gitignore** - (Optional) Exclude large files

---

## Dependencies

The `requirements.txt` includes:

```
streamlit==1.28.1        # Web framework
pandas==2.1.3            # Data manipulation
numpy==1.26.2            # Numerical computing
scikit-learn==1.3.2      # Machine learning
joblib==1.3.2            # Model serialization
plotly==5.18.0           # Interactive visualizations
matplotlib==3.8.2        # Static plotting
seaborn==0.13.0          # Statistical visualization
```

---

## 🎯 Features of the Streamlit App

### 📊 Single Prediction Mode

- Interactive sliders for all 21 features
- Real-time predictions with uncertainty estimates
- Color-coded result (excellent/good/below baseline)
- Confidence ranges

### 📈 Batch Analysis Mode

- Upload CSV files with multiple samples
- Process 100s of predictions at once
- Statistical summary (mean, min, max, std)
- Download results as CSV

### 🔧 Parameter Optimization Mode

- Explore how parameters affect predictions
- Interactive parameter sensitivity analysis
- Visualize optimization curves
- Find optimal operating conditions

### ℹ️ Model Information Mode

- Model performance metrics
- Feature importance information
- Dataset statistics
- Deployment & usage documentation

---

## 🚀 Local Testing (Before Deployment)

### Test locally first

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

The app will open at: `http://localhost:8501`

**Browser should display:**

1. Header: "⛏️ Froth Flotation Recovery Predictor"
2. Sidebar with navigation modes
3. Model info card showing it's loaded ✅

---

## 🔧 Troubleshooting

### Issue: "Models directory not found"

**Solution**: Upload `models/` folder to GitHub with all `.pkl` files

### Issue: "Module not found" (streamlit, pandas, etc)

**Solution**: Ensure `requirements.txt` is in repository root with correct versions

### Issue: App takes 30+ seconds to load

**Solution**: Model loading is cached (`@st.cache_resource`), first load is slowest

### Issue: "No module named X"

**Solution**: Add package to `requirements.txt` and redeploy

### Issue: Deployment fails with "memory exceeded"

**Solution**: Streamlit Cloud provides 1GB RAM - should be sufficient. Check for file size limits.

---

## 📊 Performance & Limits

| Metric | Value |
|--------|-------|
| **Free Tier** | 3 apps |
| **Storage** | 1 GB |
| **Memory** | 1 GB during runtime |
| **File Upload** | 200 MB |
| **Concurrent Users** | Unlimited |
| **Uptime** | 24/7 |

---

## 🔐 Security Notes

1. **Model files are public** (on GitHub) - OK, they don't contain sensitive data
2. **No user data is stored** - App runs stateless
3. **Predictions are not logged** - Your data stays with you
4. **HTTPS enabled** - Streamlit Cloud provides SSL/TLS

---

## 💡 How to Update the App

### After updating streamlit_app.py

```bash
git add streamlit_app.py
git commit -m "Update: New feature added"
git push origin main
```

Streamlit Cloud auto-detects changes and redeploys in 1-2 minutes! 🚀

### After retraining the model

1. Run training notebook to generate new models
2. Save models to `models/` directory
3. Upload `.pkl` files to GitHub
4. Redeploy (Streamlit Cloud will reload automatically)

---

## 📞 Support & Resources

- **Streamlit Docs**: <https://docs.streamlit.io/>
- **Streamlit Cloud Docs**: <https://docs.streamlit.io/streamlit_community_cloud/get_started>
- **Deploy Guide**: <https://docs.streamlit.io/streamlit_community_cloud/deploy_your_app>
- **GitHub Desktop**: <https://desktop.github.com/> (easier than command line)

---

## 📝 README.md Template

```markdown
# Froth Flotation Recovery Predictor

🎯 ML-powered real-time predictions for iron ore recovery optimization

## Features

- **Single Prediction**: Make predictions from plant parameters
- **Batch Analysis**: Process multiple samples at once
- **Optimization**: Explore parameter sensitivity
- **Model Info**: View detailed model metrics

## Quick Links

- 🚀 **Live App**: https://share.streamlit.io/YOUR_USERNAME/flotation-recovery-predictor
- 📊 **Notebook**: [Link to Jupyter notebook]
- 📈 **Performance**: 29% variance explained (Test R² = 0.288)

## Usage

1. Select prediction mode from sidebar
2. Enter or upload process parameters
3. Get real-time predictions with confidence intervals

## Model Details

- **Algorithm**: Random Forest (100 trees, max_depth=8)
- **Features**: 21 industrial parameters
- **Training Data**: 3,158 samples
- **Test Accuracy**: ±0.92% RMSE

## Deployment

Deployed on Streamlit Cloud. Auto-deploys on GitHub push.

## License

MIT License
```

---

## Next Steps

1. ✅ Create GitHub account & repository
2. ✅ Upload all files to GitHub
3. ✅ Connect to Streamlit Cloud
4. ✅ Deploy app
5. ✅ Share public URL with team
6. ✅ Monitor & maintain app

**Your app will be live in <5 minutes!** 🎉

---

## Questions?

Check Streamlit Cloud docs or GitHub Issues for help!

**Happy deploying! 🚀**
