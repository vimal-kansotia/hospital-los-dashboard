"""
Hospital Length of Stay Prediction Dashboard
Main Application Entry Point
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Hospital LOS Prediction",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0F172A;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E293B;
    }
    
    /* Card styling */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #F8FAFC;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F8FAFC;
    }
    
    /* Text */
    body, p {
        color: #E2E8F0;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #1E40AF;
        box-shadow: 0 0 20px rgba(30, 58, 138, 0.4);
    }
    
    /* Metric containers */
    [data-testid="metric-container"] {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #1E3A8A;
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background-color: #0F172A;
        color: #F8FAFC;
        border: 1px solid #475569;
        border-radius: 6px;
    }
    
    /* Sliders */
    .stSlider>div>div>div>input {
        background-color: #1E3A8A;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        color: #94A3B8;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    """Load and prepare the dataset."""
    from utils_preprocessing import load_and_prepare_data
    
    # Try to load from data folder
    if os.path.exists('data/LengthOfStay.csv'):
        df = load_and_prepare_data('data/LengthOfStay.csv')
    else:
        st.error("❌ Dataset not found! Place 'LengthOfStay.csv' in 'data/' folder")
        st.stop()
    
    return df

# Load model if available
@st.cache_resource
def load_model():
    """Load pre-trained ML model."""
    import joblib
    
    try:
        if os.path.exists('models/best_model.pkl'):
            model = joblib.load('models/best_model.pkl')
            return model
    except:
        pass
    
    return None

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = load_data()

if 'model' not in st.session_state:
    st.session_state.model = load_model()

if 'last_prediction' not in st.session_state:
    st.session_state.last_prediction = None

# Main App
def main():
    # Header
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    
    with col1:
        st.markdown("## 🏥")
    
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <h1 style='margin: 0;'>Hospital Length of Stay Prediction</h1>
            <p style='color: #94A3B8; margin-top: 5px;'>
                ML-Powered Predictive Analytics Dashboard
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("## 📊")
    
    st.divider()
    
    # Sidebar Navigation
    st.sidebar.markdown("## 📍 Navigation")
    st.sidebar.markdown("---")
    
    page_options = {
        "🏠 Overview": "overview",
        "📊 Patient Analytics": "analytics",
        "🔬 Clinical Insights": "clinical",
        "🤖 ML Lab": "ml_lab",
        "🎯 Predictions": "predictions",
        "🧠 Explainability": "explainability",
        "📋 Data Explorer": "explorer",
        "📚 Research": "research"
    }
    
    selected_page = st.sidebar.radio(
        "Select a page:",
        options=list(page_options.keys()),
        index=0
    )
    
    st.sidebar.markdown("---")
    
    # Dataset info in sidebar
    st.sidebar.markdown("### 📈 Dataset Info")
    st.sidebar.metric("Total Patients", f"{len(st.session_state.df):,}")
    st.sidebar.metric("Total Features", len(st.session_state.df.columns))
    st.sidebar.metric("Date Range", f"{st.session_state.df['vdate'].min().strftime('%m/%d/%Y')} - {st.session_state.df['vdate'].max().strftime('%m/%d/%Y')}")
    st.sidebar.metric("Avg LOS", f"{st.session_state.df['lengthofstay'].mean():.2f} days")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.markdown("""
    **Master's in Big Data Analytics**  
    St. Xavier's College, Mumbai
    
    **Project:** Predicting Hospital Length of Stay
    
    **Data:** 100K+ patient records with clinical vitals, demographics, and comorbidities
    """)
    
    # Route to selected page
    page_module = page_options[selected_page]
    
    if page_module == "overview":
        from pages.overview import show
        show(st.session_state.df)
    
    elif page_module == "analytics":
        from pages.analytics import show
        show(st.session_state.df)
    
    elif page_module == "clinical":
        from pages.clinical import show
        show(st.session_state.df)
    
    elif page_module == "ml_lab":
        from pages.ml_lab import show
        show(st.session_state.df, st.session_state.model)
    
    elif page_module == "predictions":
        from pages.predictions import show
        show(st.session_state.df, st.session_state.model)
    
    elif page_module == "explainability":
        from pages.explainability import show
        show(st.session_state.df, st.session_state.model)
    
    elif page_module == "explorer":
        from pages.explorer import show
        show(st.session_state.df)
    
    elif page_module == "research":
        from pages.research import show
        show(st.session_state.df, st.session_state.model)

if __name__ == "__main__":
    main()
