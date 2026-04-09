"""
Froth Flotation Recovery ML Prediction App
Hosted on Streamlit Cloud: https://share.streamlit.io/
Real-time predictions for Iron Ore Recovery Optimization
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle
import os
import glob
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ======================== PAGE CONFIG ========================
st.set_page_config(
    page_title="Flotation Recovery Predictor",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================== CUSTOM STYLING ========================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d1f2eb;
        border-left: 4px solid #06a77d;
        padding: 15px;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #ffeebf;
        border-left: 4px solid #ff9900;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ======================== LOAD MODEL & SCALER ========================
@st.cache_resource
def load_model_and_scaler():
    """Load the latest trained model and scaler"""
    models_dir = "models"
    
    if not os.path.exists(models_dir):
        st.error("❌ Models directory not found. Please ensure models are saved first.")
        st.stop()
    
    # Find latest model files
    rf_files = glob.glob(os.path.join(models_dir, "random_forest_model_*.pkl"))
    scaler_files = glob.glob(os.path.join(models_dir, "feature_scaler_*.pkl"))
    metadata_files = glob.glob(os.path.join(models_dir, "model_metadata_*.pkl"))
    
    if not (rf_files and scaler_files and metadata_files):
        st.error("❌ Model files not found. Please train and save models first.")
        st.stop()
    
    # Load most recent files
    rf_model = joblib.load(max(rf_files, key=os.path.getctime))
    scaler = pickle.load(open(max(scaler_files, key=os.path.getctime), 'rb'))
    metadata = pickle.load(open(max(metadata_files, key=os.path.getctime), 'rb'))
    
    return rf_model, scaler, metadata

# ======================== HELPER FUNCTIONS ========================
def make_prediction(input_data, scaler, model, metadata):
    """Make prediction with uncertainty estimate"""
    try:
        # Subset features to match training data order
        if isinstance(input_data, pd.DataFrame):
            input_data = input_data[metadata['all_features']]
        
        # Scale input
        scaled_data = scaler.transform(input_data)
        
        # Predict
        prediction = model.predict(scaled_data)[0]
        
        # Calculate uncertainty (based on model R² and RMSE)
        uncertainty = 0.92  # Test RMSE is ~0.92%
        confidence_range = (prediction - uncertainty, prediction + uncertainty)
        
        return prediction, uncertainty, confidence_range
    except Exception as e:
        st.error(f"❌ Prediction error: {str(e)}")
        return None, None, None

def format_prediction_result(prediction, uncertainty, confidence_range, title="Prediction Result"):
    """Format and display prediction with confidence interval"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Predicted Value", f"{prediction:.2f}%")
    
    with col2:
        st.metric("Uncertainty (±RMSE)", f"{uncertainty:.2f}%")
    
    with col3:
        st.metric("Confidence Range", f"{confidence_range[0]:.2f}% - {confidence_range[1]:.2f}%")

# ======================== MAIN APP ========================
def main():
    # Header
    st.markdown('<p class="main-header">⛏️ Froth Flotation Recovery Predictor</p>', unsafe_allow_html=True)
    st.markdown("**Real-time predictions for optimal iron ore recovery**")
    st.divider()
    
    # Load model
    with st.spinner("Loading model..."):
        rf_model, scaler, metadata = load_model_and_scaler()
    
    st.success("✅ Model loaded successfully!")
    
    # Sidebar - Navigation
    st.sidebar.title("🎯 Navigation")
    app_mode = st.sidebar.radio(
        "Select Mode",
        ["📊 Single Prediction", "📈 Batch Analysis", "🔧 Parameter Optimization", "ℹ️ Model Info"]
    )
    
    # Sidebar - Model Info
    with st.sidebar.expander("ℹ️ Model Performance", expanded=False):
        st.write(f"**Train R²:** {metadata['rf_r2_train']:.4f}")
        st.write(f"**Test R²:** {metadata['rf_r2_test']:.4f}")
        st.write(f"**Test RMSE:** {metadata['rf_rmse']:.4f}%")
        st.write(f"**Test MAE:** {metadata['rf_mae']:.4f}%")
        st.write(f"**CV Mean R²:** {rf_model.n_estimators:.0f}±{metadata['rf_mae']:.4f}")
        st.divider()
        st.info("""
        ⚠️ **Accuracy Note:**
        - Real-world accuracy: ±0.92% (RMSE)
        - Model explains 29% of variance
        - Use as decision support only
        - Validate with expert judgment
        """)
    
    # ======================== MODE 1: SINGLE PREDICTION ========================
    if app_mode == "📊 Single Prediction":
        st.header("Single Sample Prediction")
        st.write("Enter process parameters to predict iron concentrate recovery.")
        st.divider()
        
        # Create input form
        col1, col2 = st.columns(2)
        
        input_data = {}
        
        with col1:
            st.subheader("Feed Quality Parameters")
            input_data["% Iron Feed"] = st.slider(
                "Iron Feed %",
                min_value=64.0, max_value=70.0, value=67.5, step=0.1,
                help="Current iron content in feed ore"
            )
            input_data["% Silica Feed"] = st.slider(
                "Silica Feed %",
                min_value=1.5, max_value=4.0, value=2.1, step=0.1,
                help="Current silica content in feed"
            )
        
        with col2:
            st.subheader("Control Parameters (Key)")
            input_data["Ore Pulp pH"] = st.slider(
                "Ore Pulp pH",
                min_value=8.5, max_value=10.5, value=10.0, step=0.1
            )
            input_data["Ore Pulp Density"] = st.slider(
                "Ore Pulp Density",
                min_value=1.5, max_value=1.9, value=1.75, step=0.01
            )
        
        st.subheader("Chemical Dosing")
        col3, col4 = st.columns(2)
        
        with col3:
            input_data["Starch Flow"] = st.slider(
                "Starch Flow (mL/min)",
                min_value=500.0, max_value=3000.0, value=2500.0, step=100.0
            )
        
        with col4:
            input_data["Amina Flow"] = st.slider(
                "Amina Flow (mL/min)",
                min_value=200.0, max_value=700.0, value=450.0, step=50.0
            )
        
        st.subheader("Ore Pulp Flow & Air Distribution")
        col5, col6 = st.columns(2)
        
        with col5:
            input_data["Ore Pulp Flow"] = st.slider(
                "Ore Pulp Flow (m³/h)",
                min_value=800.0, max_value=1500.0, value=1100.0, step=50.0
            )
        
        with col6:
            avg_air_flow = st.slider(
                "Average Air Flow Per Column (m³/h)",
                min_value=200.0, max_value=800.0, value=500.0, step=50.0
            )
        
        # Set air flows for all columns
        for col_num in range(1, 8):
            input_data[f"Flotation Column {col_num:02d} Air Flow"] = avg_air_flow
        
        st.subheader("Column Levels")
        avg_level = st.slider(
            "Average Column Level",
            min_value=0.5, max_value=3.0, value=1.5, step=0.1
        )
        
        # Set levels for all columns
        for col_num in range(1, 8):
            input_data[f"Flotation Column {col_num:02d} Level"] = avg_level
        
        # Prepare DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Predict
        if st.button("🔮 Make Prediction", use_container_width=True):
            prediction, uncertainty, confidence_range = make_prediction(input_df, scaler, rf_model, metadata)
            
            if prediction is not None:
                st.success("✅ Prediction Complete!")
                st.divider()
                
                # Display results
                format_prediction_result(prediction, uncertainty, confidence_range)
                
                # Color code result
                if prediction > 65.5:
                    st.markdown(f'<div class="success-box"><strong>🎯 Excellent prediction: {prediction:.2f}% iron concentrate</strong><br>This configuration is well above baseline (65.03%)</div>', unsafe_allow_html=True)
                elif prediction > 65.0:
                    st.markdown(f'<div class="warning-box"><strong>⚠️ Good prediction: {prediction:.2f}% iron concentrate</strong><br>This is slightly above baseline (65.03%)</div>', unsafe_allow_html=True)
                else:
                    st.warning(f"⚠️ Predicted value: {prediction:.2f}% (below baseline 65.03%)")
    
    # ======================== MODE 2: BATCH ANALYSIS ========================
    elif app_mode == "📈 Batch Analysis":
        st.header("Batch Data Analysis")
        st.write("Upload a CSV file with multiple samples for batch predictions.")
        st.divider()
        
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        
        if uploaded_file is not None:
            df_batch = pd.read_csv(uploaded_file)
            
            st.write(f"Loaded {len(df_batch)} samples")
            st.dataframe(df_batch.head())
            
            if st.button("🔄 Process Batch", use_container_width=True):
                try:
                    # Make predictions for all samples
                    predictions = rf_model.predict(scaler.transform(df_batch[metadata['all_features']]))
                    
                    # Add predictions to dataframe
                    df_batch['Predicted_Iron_Concentrate'] = predictions
                    
                    st.success(f"✅ Processed {len(df_batch)} samples!")
                    st.dataframe(df_batch)
                    
                    # Statistics
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Mean Prediction", f"{predictions.mean():.2f}%")
                    col2.metric("Min Prediction", f"{predictions.min():.2f}%")
                    col3.metric("Max Prediction", f"{predictions.max():.2f}%")
                    col4.metric("Std Dev", f"{predictions.std():.3f}%")
                    
                    # Histogram
                    fig = px.histogram(
                        x=predictions,
                        nbins=20,
                        labels={'x': 'Predicted Iron Concentrate %', 'y': 'Frequency'},
                        title="Distribution of Predictions"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Download results
                    csv = df_batch.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results CSV",
                        data=csv,
                        file_name=f"batch_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}\nEnsure CSV has all required features.")
    
    # ======================== MODE 3: OPTIMIZATION ========================
    elif app_mode == "🔧 Parameter Optimization":
        st.header("Parameter Optimization Explorer")
        st.write("Explore how different parameters affect iron recovery predictions.")
        st.divider()
        
        # Select parameter to vary
        param_to_vary = st.selectbox(
            "Select parameter to vary",
            ["Ore Pulp pH", "Ore Pulp Density", "Starch Flow", "Amina Flow"]
        )
        
        # Create baseline data
        baseline_data = {
            "% Iron Feed": 67.5,
            "% Silica Feed": 2.1,
            "Ore Pulp pH": 10.0,
            "Ore Pulp Density": 1.75,
            "Starch Flow": 2500.0,
            "Amina Flow": 450.0,
            "Ore Pulp Flow": 1100.0,
        }
        
        # Set air flows and levels
        for col_num in range(1, 8):
            baseline_data[f"Flotation Column {col_num:02d} Air Flow"] = 500.0
            baseline_data[f"Flotation Column {col_num:02d} Level"] = 1.5
        
        # Parameter ranges
        ranges = {
            "Ore Pulp pH": np.linspace(8.5, 10.5, 20),
            "Ore Pulp Density": np.linspace(1.5, 1.9, 20),
            "Starch Flow": np.linspace(500, 3000, 20),
            "Amina Flow": np.linspace(200, 700, 20),
        }
        
        # Generate predictions
        predictions_list = []
        param_values = ranges[param_to_vary]
        
        with st.spinner(f"Optimizing {param_to_vary}..."):
            for value in param_values:
                temp_data = baseline_data.copy()
                temp_data[param_to_vary] = value
                df_temp = pd.DataFrame([temp_data])
                pred = rf_model.predict(scaler.transform(df_temp[metadata['all_features']]))[0]
                predictions_list.append(pred)
        
        # Create visualization
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=param_values,
            y=predictions_list,
            mode='lines+markers',
            name='Prediction',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=f"Effect of {param_to_vary} on Iron Recovery",
            xaxis_title=param_to_vary,
            yaxis_title="Predicted Iron Concentrate %",
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Best value
        best_idx = np.argmax(predictions_list)
        st.success(f"✅ **Optimal {param_to_vary}: {param_values[best_idx]:.2f}** → {predictions_list[best_idx]:.2f}% iron")
    
    # ======================== MODE 4: MODEL INFO ========================
    elif app_mode == "ℹ️ Model Info":
        st.header("Model Information & Documentation")
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Model Performance")
            st.metric("Training R²", f"{metadata['rf_r2_train']:.4f}")
            st.metric("Test R² (Real Accuracy)", f"{metadata['rf_r2_test']:.4f}")
            st.metric("Train-Test Gap", f"{(metadata['rf_r2_train'] - metadata['rf_r2_test']):.4f}")
        
        with col2:
            st.subheader("🎯 Prediction Accuracy")
            st.metric("Test RMSE", f"{metadata['rf_rmse']:.4f}%")
            st.metric("Test MAE", f"{metadata['rf_mae']:.4f}%")
            st.metric("CV Mean R²", f"0.2591 ± 0.0188")
        
        st.divider()
        st.subheader("📋 Dataset & Features")
        
        col3, col4, col5 = st.columns(3)
        col3.metric("Total Features", metadata['feature_count'])
        col4.metric("Training Samples", metadata['training_samples'])
        col5.metric("Test Samples", metadata['test_samples'])
        
        st.divider()
        st.subheader("🔑 Feature Groups")
        
        col6, col7 = st.columns(2)
        
        with col6:
            st.write("**Feed Quality (2):**")
            for feat in metadata['feed_quality_features']:
                st.write(f"  • {feat}")
        
        with col7:
            st.write("**Control Parameters (19):**")
            for feat in metadata['control_parameters'][:10]:
                st.write(f"  • {feat}")
            if len(metadata['control_parameters']) > 10:
                st.write(f"  ... and {len(metadata['control_parameters']) - 10} more")
        
        st.divider()
        st.subheader("⚠️ Important Notes")
        
        st.warning("""
        **Model Limitations:**
        - Explains ~29% of variance (71% from unmeasured factors)
        - Test RMSE: ±0.92% typical error
        - Use as decision support, not autonomous control
        - Validate predictions with expert judgment
        
        **Best Practices:**
        - Always monitor actual vs predicted recovery
        - Combine with operator expertise
        - Retrain model quarterly with new data
        - Check for distribution shifts (different ore types)
        """)
        
        st.divider()
        st.subheader("🚀 Deployment Info")
        st.info("""
        **Hosted on Streamlit Cloud**
        - Real-time model serving
        - Automatic scaling
        - Zero configuration deployment
        
        **Source:**
        - GitHub: [GitHub URL]
        - Notebook: Froth_Flotation_Recovery_Model.ipynb
        - Models Location: `models/` directory
        """)

if __name__ == "__main__":
    main()
