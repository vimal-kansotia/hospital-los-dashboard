"""
Hospital Length of Stay Prediction Dashboard
Main Application Entry Point with Native Navigation
"""

import streamlit as st
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Hospital LOS Prediction",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom dark theme styling
st.markdown("""
<style>
    .stApp {
        background-color: #0F172A;
    }
    [data-testid="stSidebar"] {
        background-color: #1E293B;
    }
    h1, h2, h3, body, p {
        color: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    from utils_preprocessing import load_and_prepare_data
    if os.path.exists('data/LengthOfStay.csv'):
        return load_and_prepare_data('data/LengthOfStay.csv')
    else:
        st.error("❌ Dataset not found! Place 'LengthOfStay.csv' in 'data/' folder")
        st.stop()

@st.cache_resource
def load_model():
    import joblib
    try:
        if os.path.exists('models/best_model.pkl'):
            return joblib.load('models/best_model.pkl')
    except:
        pass
    return None

# Initialize session state so pages can access df and model
if 'df' not in st.session_state:
    st.session_state.df = load_data()

if 'model' not in st.session_state:
    st.session_state.model = load_model()

# Define pages using Streamlit's native navigation
pages = [
    st.Page("pages/overview.py", title="Overview", icon="🏠"),
    st.Page("pages/analytics.py", title="Patient Analytics", icon="📊"),
    st.Page("pages/clinical.py", title="Clinical Insights", icon="🔬"),
    st.Page("pages/ml_lab.py", title="ML Lab", icon="🤖"),
    st.Page("pages/predictions.py", title="Predictions", icon="🎯"),
    st.Page("pages/explainability.py", title="Explainability", icon="🧠"),
    st.Page("pages/explorer.py", title="Data Explorer", icon="📋"),
    st.Page("pages/research.py", title="Research", icon="📚"),
]

pg = st.navigation(pages)

# Run the selected page
pg.run()
