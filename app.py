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

# Custom CSS for styling - Clean sidebar design
st.markdown("""
<style>
    .stApp {
        background-color: #0F172A;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1E293B;
    }
    
    /* Hide default radio styling */
    [data-testid="stSidebar"] .stRadio > label {
        display: none;
    }
    
    /* Custom navigation buttons */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 8px;
        display: flex;
        flex-direction: column;
    }
    
    [data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {
        background-color: transparent;
        padding: 12px 16px;
        border-radius: 6px;
        border: none;
        color: #94A3B8;
        font-weight: 500;
        font-size: 15px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 0;
        width: 100%;
        text-align: left;
    }
    
    [data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:hover {
        background-color: rgba(30, 58, 138, 0.3);
        color: #E2E8F0;
    }
    
    [data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] input:checked + div {
        background-color: rgba(30, 58, 138, 0.5);
        color: #F8FAFC;
    }
    
    /* Sidebar heading */
    [data-testid="stSidebar"] h2 {
        color: #F8FAFC;
        margin-bottom: 16px;
        font-size: 18px;
        font-weight: 700;
    }
    
    [data-testid="stSidebar"] p {
        color: #94A3B8;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Main content styling */
    h1, h2, h3 {
        color: #F8FAFC;
    }
    
    body, p {
        color: #E2E8F0;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #1E40AF;
        box-shadow: 0 0 20px rgba(30, 58, 138, 0.4);
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #1E3A8A;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #F8FAFC;
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
    
    /* Divider */
    .stDivider {
        border-color: #475569;
    }
</style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
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
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
    
    with col1:
        st.markdown("## 🏥")
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <h1 style='margin: 0; font-size: 2.5rem;'>Hospital Length of Stay Prediction</h1>
            <p style='color: #94A3B8; margin-top: 10px; font-size: 1rem;'>
                ML-Powered Predictive Analytics Dashboard
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("## 📊")
    
    st.divider()
    
    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.markdown("## Hospital LOS")
        st.markdown("---")
        
        # Navigation Pages
        page_options = {
            "Home": "overview",
            "Patient Analytics": "analytics",
            "Clinical Insights": "clinical",
            "ML Lab": "ml_lab",
            "Predictions": "predictions",
            "Explainability": "explainability",
            "Data Explorer": "explorer",
            "Research": "research"
        }
        
        selected_page = st.radio(
            "Navigate to:",
            options=list(page_options.keys()),
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # About Section
        st.markdown("### About")
        st.markdown("""
**Master's in Big Data Analytics**  
St. Xavier's College, Mumbai

**Project:** Hospital Length of Stay Prediction

**Dataset:** 100K+ patient records with clinical vitals, demographics, and comorbidities
        """)
    
    # ==================== PAGE ROUTING ====================
    page_module = page_options[selected_page]
    
    try:
        if page_module == "overview":
            from overview import show
            show(st.session_state.df)
        elif page_module == "analytics":
            from analytics import show
            show(st.session_state.df)
        elif page_module == "clinical":
            from clinical import show
            show(st.session_state.df)
        elif page_module == "ml_lab":
            from ml_lab import show
            show(st.session_state.df, st.session_state.model)
        elif page_module == "predictions":
            from predictions import show
            show(st.session_state.df, st.session_state.model)
        elif page_module == "explainability":
            from explainability import show
            show(st.session_state.df, st.session_state.model)
        elif page_module == "explorer":
            from explorer import show
            show(st.session_state.df)
        elif page_module == "research":
            from research import show
            show(st.session_state.df, st.session_state.model)
    except ImportError as e:
        st.error(f"❌ Module not found: {e}")
        st.info(f"Attempted to load page: {page_module}")
    except Exception as e:
        st.error(f"⚠️ Error loading page: {e}")

if __name__ == "__main__":
    main()
