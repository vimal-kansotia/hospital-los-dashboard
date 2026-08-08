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
    /* Main background */
    .stApp {
        background-color: #0F172A;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E293B;
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
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background-color: #0F172A;
        color: #F8FAFC;
        border: 1px solid #475569;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    """Load and prepare the dataset."""
    from utils_preprocessing import load_and_prepare_data
    
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

# Define pages using Streamlit's native navigation (requires page files inside a 'pages' folder)
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

# Run native navigation container (creates the search bar and clean list automatically)
pg = st.navigation(pages)
pg.run()
