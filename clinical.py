"""
Page 3: Clinical Insights
Vitals and correlation analysis with direct inline scatter rendering
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils_visualizations import (
    box_plot_clinical_variable,
    correlation_heatmap
)
from utils_preprocessing import get_clinical_stats, get_correlation_matrix

def show(df):
    st.markdown("# 🔬 Clinical Insights")
    st.markdown("*Explore relationships between clinical variables and length of stay*")
    st.divider()
    
    # Clinical variable list
    clinical_variables = [
        'bmi', 'glucose', 'pulse', 'hematocrit', 'creatinine',
        'bloodureanitro', 'sodium', 'neutrophils', 'respiration'
    ]
    
    # Control Bar
    st.markdown("## 🎮 Analysis Controls")
    
    control_col1, control_col2, control_col3 = st.columns(3)
    
    with control_col1:
        primary_var = st.selectbox(
            "Primary Variable",
            options=clinical_variables,
            index=1,
            key="primary_clinical_var"
        )
    
    with control_col2:
        secondary_var = st.selectbox(
            "Secondary Variable",
            options=clinical_variables,
            index=0,
            key="secondary_clinical_var"
        )
    
    with control_col3:
        plot_type = st.selectbox(
            "Plot Type",
            options=['Box Plot', 'Violin Plot', 'Histogram'],
            key="clinical_plot_type"
        )
    
    st.divider()
    
    # Dynamic Plot Analysis based on user selection
    st.markdown(f"## 📊 {primary_var.title()} by Length of Stay Category")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        
        for los_cat in ['1-3 days', '4-6 days', '7-10 days', '11+ days']:
            data = df[df['los_category'] == los_cat][primary_var]
            
            if plot_type == 'Box Plot':
                fig.add_trace(go.Box(
                    y=data,
                    name=los_cat,
                    boxmean='sd',
                    hovertemplate='<b>%{fullData.name}</b><br>Value: %{y:.2f}<extra></extra>'
                ))
            elif plot_type == 'Violin Plot':
                fig.add_trace(go.Violin(
                    y=data,
                    name=los_cat,
                    box_visible=True,
                    meanline_visible=True,
                    hovertemplate='<b>%{fullData.name}</b><br>Value: %{y:.2f}<extra></extra>'
                ))
            else:
                pass
        
        if plot_type == 'Histogram':
            fig = px.histogram(
                df, 
                x=primary_var, 
                color='los_category', 
                barmode='group',
                marginal='rug',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig.update_layout(
                title=f'{primary_var.title()} Distribution Histogram',
                xaxis_title=primary_var.title(),
                yaxis_title='Count',
                template='plotly_dark',
                height=450
            )
        else:
            fig.update_layout(
                title=f'{primary_var.title()} Distribution by LOS Category ({plot_type})',
                yaxis_title=primary_var.title(),
                template='plotly_dark',
                height=450,
                hovermode='closest'
            )
        
        st.plotly_chart(fig, use_container_width=True, key="clinical_dynamic_plot")
    
    with col2:
        # Statistical summary
        stats = get_clinical_stats(df)
        var_stats = stats[primary_var]
        
        stats_text = f"""
        ### Statistical Summary: {primary_var.title()}
        
        | Metric | Value |
        |--------|-------|
        | Mean | {var_stats['mean']:.2f} |
        | Median | {var_stats['median']:.2f} |
        | Std Dev | {var_stats['std']:.2f} |
        | Min | {var_stats['min']:.2f} |
        | Max | {var_stats['max']:.2f} |
        | Q1 (25%) | {var_stats['q1']:.2f} |
        | Q3 (75%) | {var_stats['q3']:.2f} |
        
        **Interpretation:**
        - Range: {var_stats['min']:.1f} to {var_stats['max']:.1f}
        - Interquartile Range: {var_stats['q3'] - var_stats['q1']:.2f}
        - Data spread: σ = {var_stats['std']:.2f}
        """
        
        st.markdown(stats_text)
    
    st.divider()
    
    # Correlation Matrix
    st.markdown("## 🔗 Correlation Matrix")
    
    corr_matrix = get_correlation_matrix(df)
    fig_corr = correlation_heatmap(corr_matrix, title='Feature Correlation Matrix')
    st.plotly_chart(fig_corr, use_container_width=True, key="correlation_matrix")
    
    # Correlation insights
    st.markdown("### 💡 Key Correlations with Length of Stay")
    los_corr = corr_matrix['lengthofstay'].sort_values(ascending=False)
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.markdown("**Positive Correlations** (increase LOS):")
        for var, corr_val in los_corr[1:4].items():
            st.markdown(f"- **{var.title()}**: {corr_val:.3f}")
    
    with insight_col2:
        st.markdown("**Negative Correlations** (decrease LOS):")
        for var, corr_val in los_corr[-3:].items():
            st.markdown(f"- **{var.title()}**: {corr_val:.3f}")
    
    st.divider()
    
    # Direct Inline Scatter Plot (Guaranteed to update instantly with any primary/secondary selection)
    st.markdown(f"## 🔍 {primary_var.title()} vs {secondary_var.title()}")
    
    sample_df = df.sample(min(2000, len(df)))
    scatter_fig = px.scatter(
        sample_df,
        x=primary_var,
        y=secondary_var,
        color='lengthofstay',
        color_continuous_scale='Viridis',
        opacity=0.7,
        title=f'{primary_var.title()} vs {secondary_var.title()} (Colored by Length of Stay)'
    )
    scatter_fig.update_layout(
        template='plotly_dark',
        height=500,
        xaxis_title=primary_var.title(),
        yaxis_title=secondary_var.title()
    )
    
    st.plotly_chart(scatter_fig, use_container_width=True, key=f"dynamic_scatter_{primary_var}_{secondary_var}")
    
    st.divider()
    
    # Clinical Variable Comparison Table
    st.markdown("## 📋 All Clinical Variables Summary")
    
    stats_all = get_clinical_stats(df)
    summary_data = []
    
    for var, var_stats in stats_all.items():
        summary_data.append({
            'Variable': var.title(),
            'Mean': f"{var_stats['mean']:.2f}",
            'Median': f"{var_stats['median']:.2f}",
            'Std Dev': f"{var_stats['std']:.2f}",
            'Min': f"{var_stats['min']:.2f}",
            'Max': f"{var_stats['max']:.2f}"
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Comorbidity Impact on Clinical Variables
    st.markdown("## 🏥 Comorbidity Impact Analysis")
    
    comorbidity_col1, comorbidity_col2 = st.columns(2)
    
    with comorbidity_col1:
        st.markdown("### High Comorbidity Patients")
        high_comorbid = df[df['comorbidity_score'] >= df['comorbidity_score'].median()]
        
        stats_high = {
            'Glucose': high_comorbid['glucose'].mean(),
            'Creatinine': high_comorbid['creatinine'].mean(),
            'BMI': high_comorbid['bmi'].mean(),
            'Avg LOS': high_comorbid['lengthofstay'].mean()
        }
        
        for key, val in stats_high.items():
            st.metric(key, f"{val:.2f}")
    
    with comorbidity_col2:
        st.markdown("### Low Comorbidity Patients")
        low_comorbid = df[df['comorbidity_score'] < df['comorbidity_score'].median()]
        
        stats_low = {
            'Glucose': low_comorbid['glucose'].mean(),
            'Creatinine': low_comorbid['creatinine'].mean(),
            'BMI': low_comorbid['bmi'].mean(),
            'Avg LOS': low_comorbid['lengthofstay'].mean()
        }
        
        for key, val in stats_low.items():
            st.metric(key, f"{val:.2f}")
