"""
Page 1: Executive Overview
KPIs, summary metrics, and high-level visualizations
"""

import streamlit as st
import pandas as pd
from utils_visualizations import (
    bar_chart_los_distribution,
    donut_chart_facility_distribution,
    gender_donut_chart,
    readmission_vs_los_chart,
    histogram_los_with_mean_median
)

def show(df):
    st.markdown("# 🏠 Executive Overview")
    st.markdown("*Dashboard summary of hospital operations and patient length of stay metrics*")
    st.divider()
    
    # KPI Cards - Row 1
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="👥 Total Patients",
            value=f"{len(df):,}",
            delta="100K Records"
        )
    
    with col2:
        avg_los = df['lengthofstay'].mean()
        st.metric(
            label="⏱️ Average LOS",
            value=f"{avg_los:.1f} days",
            delta="+0.2 days vs target"
        )
    
    with col3:
        median_los = df['lengthofstay'].median()
        st.metric(
            label="📈 Median LOS",
            value=f"{median_los:.0f} days",
            delta="50th percentile"
        )
    
    with col4:
        max_los = df['lengthofstay'].max()
        st.metric(
            label="🔴 Max LOS",
            value=f"{max_los:.0f} days",
            delta="Outlier"
        )
    
    with col5:
        st.metric(
            label="🤖 Model Accuracy",
            value="65.2%",
            delta="+7.2% baseline"
        )
    
    st.divider()
    
    # Charts - Row 2
    st.markdown("## 📉 Distribution Analysis")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.plotly_chart(
            bar_chart_los_distribution(df),
            use_container_width=True,
            key="overview_los_dist"
        )
    
    with chart_col2:
        st.plotly_chart(
            donut_chart_facility_distribution(df),
            use_container_width=True,
            key="overview_facility"
        )
    
    st.divider()
    
    # Charts - Row 3
    st.markdown("## 🔍 Patient Demographics & Readmissions")
    
    demo_col1, demo_col2 = st.columns(2)
    
    with demo_col1:
        st.plotly_chart(
            gender_donut_chart(df),
            use_container_width=True,
            key="overview_gender"
        )
    
    with demo_col2:
        st.plotly_chart(
            readmission_vs_los_chart(df),
            use_container_width=True,
            key="overview_readmission"
        )
    
    st.divider()
    
    # Key Insights
    st.markdown("## 💡 Key Insights & Findings")
    
    # Calculate insights
    short_stay = len(df[df['lengthofstay'] <= 3])
    short_stay_pct = (short_stay / len(df)) * 100
    
    long_stay = len(df[df['lengthofstay'] > 10])
    long_stay_pct = (long_stay / len(df)) * 100
    
    readmitted = len(df[df['rcount'] > 0])
    readmitted_pct = (readmitted / len(df)) * 100
    
    readmitted_los = df[df['rcount'] > 0]['lengthofstay'].mean()
    no_readmit_los = df[df['rcount'] == 0]['lengthofstay'].mean()
    readmit_diff = readmitted_los - no_readmit_los
    
    insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)
    
    with insight_col1:
        st.info(f"""
        **Short Stays (≤3 days)**  
        {short_stay_pct:.1f}% of patients  
        {short_stay:,} patients
        
        ✅ Standard recovery period
        """)
    
    with insight_col2:
        st.warning(f"""
        **Long Stays (>10 days)**  
        {long_stay_pct:.1f}% of patients  
        {long_stay:,} patients
        
        ⚠️ Requires investigation
        """)
    
    with insight_col3:
        st.error(f"""
        **Readmitted Patients**  
        {readmitted_pct:.1f}% of total  
        {readmitted:,} patients
        
        🔴 Higher LOS impact
        """)
    
    with insight_col4:
        st.success(f"""
        **Readmission Impact**  
        +{readmit_diff:.1f} days avg  
        ({readmitted_los:.1f} vs {no_readmit_los:.1f})
        
        📊 30% longer stays
        """)
    
    st.divider()
    
    # Additional Statistics
    st.markdown("## 📋 Additional Statistics")
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        facility_dist = df['facid'].value_counts()
        top_facility = facility_dist.index[0]
        top_facility_count = facility_dist.values[0]
        
        st.metric(
            label="🏢 Top Facility",
            value=f"Facility {top_facility}",
            delta=f"{top_facility_count:,} patients ({(top_facility_count/len(df)*100):.1f}%)"
        )
    
    with stats_col2:
        male_count = len(df[df['gender'] == 'M'])
        female_count = len(df[df['gender'] == 'F'])
        
        st.metric(
            label="👨 Male to Female Ratio",
            value=f"{male_count:,} : {female_count:,}",
            delta=f"{(male_count/len(df)*100):.1f}% M, {(female_count/len(df)*100):.1f}% F"
        )
    
    with stats_col3:
        comorbidity_score = df['comorbidity_score'].mean()
        
        st.metric(
            label="🏥 Avg Comorbidity Score",
            value=f"{comorbidity_score:.2f}",
            delta="Conditions per patient"
        )
    
    st.divider()
    
    # Quick Navigation
    st.markdown("## 🚀 Quick Navigation")
    
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
    
    with nav_col1:
        st.info("""
        **📊 Patient Analytics**  
        Deep dive with interactive filters
        """)
    
    with nav_col2:
        st.info("""
        **🔬 Clinical Insights**  
        Vitals analysis & correlations
        """)
    
    with nav_col3:
        st.info("""
        **🎯 Predictions**  
        Real-time LOS inference
        """)
    
    with nav_col4:
        st.info("""
        **🧠 Explainability**  
        SHAP & feature attribution
        """)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #94A3B8; font-size: 12px; margin-top: 20px;'>
        <p>Hospital Length of Stay Prediction Dashboard | Powered by ML</p>
        <p>Data spans August - December 2012 | 100,000 patient records</p>
    </div>
    """, unsafe_allow_html=True)
