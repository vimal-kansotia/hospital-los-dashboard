"""
Page 2: Patient Analytics
Interactive exploratory data analysis with dynamic filtering
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
from utils_visualizations import (
    gender_donut_chart,
    donut_chart_facility_distribution,
    readmission_vs_los_chart,
    histogram_los_with_mean_median
)
import plotly.graph_objects as go
import plotly.express as px

def show(df):
    st.markdown("# 📊 Patient Analytics")
    st.markdown("*Interactive exploration with dynamic filtering capabilities*")
    st.divider()
    
    # Sidebar Filters
    st.sidebar.markdown("## 🔍 Filters")
    
    # Gender filter
    genders = st.sidebar.multiselect(
        "Gender",
        options=['M', 'F'],
        default=['M', 'F'],
        key="gender_filter"
    )
    
    # Facility filter
    facilities = st.sidebar.multiselect(
        "Facility ID",
        options=sorted(df['facid'].unique()),
        default=sorted(df['facid'].unique()),
        key="facility_filter"
    )
    
    # Readmission filter
    rcount_options = sorted(df['rcount'].unique())
    rcount = st.sidebar.multiselect(
        "Prior Readmissions",
        options=rcount_options,
        default=rcount_options,
        key="rcount_filter"
    )
    
    # LOS range filter
    los_range = st.sidebar.slider(
        "Length of Stay Range",
        min_value=int(df['lengthofstay'].min()),
        max_value=int(df['lengthofstay'].max()),
        value=(int(df['lengthofstay'].min()), int(df['lengthofstay'].max())),
        key="los_filter"
    )
    
    # Apply filters
    df_filtered = df[
        (df['gender'].isin(genders)) &
        (df['facid'].isin(facilities)) &
        (df['rcount'].isin(rcount)) &
        (df['lengthofstay'] >= los_range[0]) &
        (df['lengthofstay'] <= los_range[1])
    ].copy()
    
    # Filter summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Filtered Patients", f"{len(df_filtered):,}")
    with col2:
        st.metric("Records Shown", f"{(len(df_filtered)/len(df)*100):.1f}%")
    with col3:
        if st.button("🔄 Reset Filters"):
            st.rerun()
    
    st.divider()
    
    # Grid of 4 panels
    st.markdown("## 📈 Analysis Panels")
    
    panel_col1, panel_col2 = st.columns(2)
    
    # Panel A: Gender Distribution
    with panel_col1:
        st.subheader("Panel A: Gender Distribution")
        try:
            fig = gender_donut_chart(df_filtered, title="Gender Distribution (Filtered)")
            st.plotly_chart(fig, use_container_width=True, key="panel_a_gender")
        except:
            st.warning("Insufficient data for chart")
    
    # Panel B: Facility Distribution
    with panel_col2:
        st.subheader("Panel B: Facility Distribution")
        try:
            facility_counts = df_filtered['facid'].value_counts()
            fig = go.Figure(data=[
                go.Bar(
                    x=facility_counts.index,
                    y=facility_counts.values,
                    marker=dict(color=facility_counts.values, colorscale='Viridis'),
                    text=facility_counts.values,
                    textposition='auto',
                    hovertemplate='<b>Facility %{x}</b><br>Patients: %{y}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Facility Distribution (Filtered)",
                xaxis_title="Facility",
                yaxis_title="Number of Patients",
                template='plotly_dark',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, key="panel_b_facility")
        except:
            st.warning("Insufficient data for chart")
    
    # Panel C: Readmission Impact
    with panel_col1:
        st.subheader("Panel C: Readmission Impact")
        try:
            fig = readmission_vs_los_chart(df_filtered, title="Readmission vs LOS (Filtered)")
            st.plotly_chart(fig, use_container_width=True, key="panel_c_readmit")
        except:
            st.warning("Insufficient data for chart")
    
    # Panel D: LOS Distribution
    with panel_col2:
        st.subheader("Panel D: LOS Distribution")
        try:
            fig = histogram_los_with_mean_median(df_filtered, title="Length of Stay Distribution (Filtered)")
            st.plotly_chart(fig, use_container_width=True, key="panel_d_los")
        except:
            st.warning("Insufficient data for chart")
    
    st.divider()
    
    # Detailed Statistics
    st.markdown("## 📊 Detailed Statistics")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric(
            "Average LOS",
            f"{df_filtered['lengthofstay'].mean():.2f} days"
        )
    
    with stat_col2:
        st.metric(
            "Median LOS",
            f"{df_filtered['lengthofstay'].median():.0f} days"
        )
    
    with stat_col3:
        st.metric(
            "Std Dev",
            f"{df_filtered['lengthofstay'].std():.2f} days"
        )
    
    with stat_col4:
        st.metric(
            "Max LOS",
            f"{df_filtered['lengthofstay'].max():.0f} days"
        )
    
    st.divider()
    
    # Comorbidity Analysis
    st.markdown("## 🏥 Comorbidity Analysis")
    
    comorbidity_cols = [
        'asthma', 'pneum', 'depress', 'malnutrition',
        'dialysisrenalendstage', 'irondef', 'hemo'
    ]
    
    comorbidity_data = []
    for col in comorbidity_cols:
        if col in df_filtered.columns:
            count = (df_filtered[col] == 1).sum()
            pct = (count / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0
            comorbidity_data.append({
                'Condition': col.replace('_', ' ').title(),
                'Count': count,
                'Percentage': pct
            })
    
    comorbidity_df = pd.DataFrame(comorbidity_data).sort_values('Percentage', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=comorbidity_df['Percentage'],
                y=comorbidity_df['Condition'],
                orientation='h',
                marker=dict(color=comorbidity_df['Percentage'], colorscale='Reds'),
                text=comorbidity_df['Percentage'].round(2),
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>%{x:.2f}%<extra></extra>'
            )
        ])
        fig.update_layout(
            title="Comorbidity Prevalence",
            xaxis_title="Percentage (%)",
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key="comorbidity_chart")
    
    with col2:
        st.dataframe(
            comorbidity_df.rename(columns={'Percentage': 'Prevalence (%)'}),
            use_container_width=True,
            hide_index=True
        )
    
    st.divider()
    
    # Download filtered data
    st.markdown("## 📥 Export Data")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="filtered_patient_data.csv",
            mime="text/csv"
        )
    
    with export_col2:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df_filtered.to_excel(writer, index=False, sheet_name='Patients')
        
        st.download_button(
            label="📊 Download as Excel",
            data=excel_buffer.getvalue(),
            file_name="filtered_patient_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
