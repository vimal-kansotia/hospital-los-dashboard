"""
Visualization Utilities
Reusable Plotly chart templates and custom styling
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Color palette
COLORS = {
    'primary': '#1E3A8A',        # Deep Blue
    'success': '#10B981',        # Emerald Green
    'warning': '#FBBF24',        # Amber
    'danger': '#F87171',         # Coral Pink
    'secondary': '#8B5CF6',      # Violet
    'neutral': '#6B7280',        # Gray
}

COLOR_GRADIENT = [
    '#10B981',  # Green (1-3 days)
    '#FBBF24',  # Yellow (4-6 days)
    '#FB923C',  # Orange (7-10 days)
    '#F87171',  # Red (11+ days)
]

PLOTLY_TEMPLATE = 'plotly_dark'


def create_kpi_card_data():
    """Create KPI card data structure."""
    return {
        'label': '',
        'value': '',
        'icon': '',
        'delta': 0,
        'color': COLORS['primary']
    }


def bar_chart_los_distribution(df, title='Length of Stay Distribution'):
    """
    Create bar chart showing LOS distribution by day.
    """
    los_counts = df['lengthofstay'].value_counts().sort_index()
    
    # Color by risk level
    colors = []
    for los in los_counts.index:
        if los <= 3:
            colors.append(COLOR_GRADIENT[0])
        elif los <= 6:
            colors.append(COLOR_GRADIENT[1])
        elif los <= 10:
            colors.append(COLOR_GRADIENT[2])
        else:
            colors.append(COLOR_GRADIENT[3])
    
    fig = go.Figure(data=[
        go.Bar(
            x=los_counts.index,
            y=los_counts.values,
            marker=dict(color=colors, line=dict(color='white', width=1)),
            text=los_counts.values,
            textposition='auto',
            hovertemplate='<b>Days:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        xaxis_title='Length of Stay (Days)',
        yaxis_title='Number of Patients',
        template=PLOTLY_TEMPLATE,
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig


def donut_chart_facility_distribution(df, title='Patient Distribution by Facility'):
    """
    Create donut chart showing facility distribution.
    """
    facility_counts = df['facid'].value_counts()
    
    fig = go.Figure(data=[
        go.Pie(
            labels=facility_counts.index,
            values=facility_counts.values,
            hole=0.4,
            marker=dict(colors=[COLORS['primary'], COLORS['secondary'], 
                               COLORS['success'], COLORS['warning'], COLORS['danger']]),
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Patients: %{value}<br>%{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        template=PLOTLY_TEMPLATE,
        height=400,
        showlegend=True
    )
    
    return fig


def gender_donut_chart(df, title='Gender Distribution'):
    """
    Create donut chart for gender distribution.
    """
    gender_counts = df['gender'].value_counts()
    
    fig = go.Figure(data=[
        go.Pie(
            labels=['Male' if x == 'M' else 'Female' for x in gender_counts.index],
            values=gender_counts.values,
            hole=0.4,
            marker=dict(colors=[COLORS['primary'], COLORS['danger']]),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        template=PLOTLY_TEMPLATE,
        height=400,
        showlegend=True
    )
    
    return fig


def readmission_vs_los_chart(df, title='Impact of Readmissions on Stay Duration'):
    """
    Create bar chart showing readmission impact on LOS.
    """
    readmission_los = df.groupby('rcount')['lengthofstay'].agg(['mean', 'count']).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(
            x=readmission_los['rcount'],
            y=readmission_los['mean'],
            marker=dict(color=readmission_los['mean'], 
                       colorscale='RdYlGn_r', showscale=False),
            text=readmission_los['mean'].round(2),
            textposition='auto',
            hovertemplate='<b>Readmissions:</b> %{x}<br><b>Avg LOS:</b> %{y:.2f} days<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        xaxis_title='Number of Prior Readmissions',
        yaxis_title='Average Length of Stay (Days)',
        template=PLOTLY_TEMPLATE,
        height=400,
        showlegend=False
    )
    
    return fig


def box_plot_clinical_variable(df, variable, title=None):
    """
    Create box plot for a clinical variable by LOS category.
    """
    if title is None:
        title = f'{variable.title()} Distribution by Length of Stay'
    
    fig = go.Figure()
    
    for los_cat in ['1-3 days', '4-6 days', '7-10 days', '11+ days']:
        data = df[df['los_category'] == los_cat][variable]
        fig.add_trace(go.Box(
            y=data,
            name=los_cat,
            marker=dict(color=COLORS['primary']),
            hovertemplate='<b>%{fullData.name}</b><br>Value: %{y}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        yaxis_title=variable.title(),
        template=PLOTLY_TEMPLATE,
        height=400,
        showlegend=True,
        boxmean='sd'
    )
    
    return fig


def correlation_heatmap(correlation_matrix, title='Feature Correlation Matrix'):
    """
    Create correlation heatmap.
    """
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.values.round(2),
        texttemplate='%{text:.2f}',
        textfont={'size': 10},
        hovertemplate='%{x} - %{y}: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        template=PLOTLY_TEMPLATE,
        height=600,
        width=700
    )
    
    return fig


def horizontal_bar_chart_importance(feature_importance, title='Feature Importance'):
    """
    Create horizontal bar chart for feature importance.
    """
    feature_importance = feature_importance.sort_values(ascending=True)
    
    fig = go.Figure(data=[
        go.Bar(
            y=feature_importance.index,
            x=feature_importance.values,
            orientation='h',
            marker=dict(
                color=feature_importance.values,
                colorscale='Viridis',
                showscale=False
            ),
            text=feature_importance.values.round(3),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        xaxis_title='Importance Score',
        yaxis_title='Features',
        template=PLOTLY_TEMPLATE,
        height=500,
        showlegend=False
    )
    
    return fig


def probability_bar_chart(probabilities, title='Prediction Probability Distribution'):
    """
    Create bar chart for prediction probabilities across LOS categories.
    """
    los_categories = ['1-3 days', '4-6 days', '7-10 days', '11+ days']
    
    # Find highest probability
    max_idx = np.argmax(probabilities)
    colors = [COLORS['success'] if i == max_idx else COLORS['neutral'] 
              for i in range(len(probabilities))]
    
    fig = go.Figure(data=[
        go.Bar(
            x=los_categories,
            y=probabilities,
            marker=dict(color=colors),
            text=[f'{p:.1%}' for p in probabilities],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Probability: %{y:.1%}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        yaxis_title='Probability',
        template=PLOTLY_TEMPLATE,
        height=400,
        showlegend=False
    )
    
    return fig


def confusion_matrix_heatmap(confusion_matrix, title='Confusion Matrix'):
    """
    Create confusion matrix heatmap.
    """
    los_labels = ['1-3', '4-6', '7-10', '11+']
    
    fig = go.Figure(data=go.Heatmap(
        z=confusion_matrix,
        x=los_labels,
        y=los_labels,
        colorscale='Blues',
        text=confusion_matrix,
        texttemplate='%{text}',
        textfont={'size': 12},
        hovertemplate='Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        xaxis_title='Predicted',
        yaxis_title='Actual',
        template=PLOTLY_TEMPLATE,
        height=500,
        width=600
    )
    
    return fig


def histogram_los_with_mean_median(df, title='Length of Stay Distribution'):
    """
    Create histogram with mean and median lines.
    """
    mean_val = df['lengthofstay'].mean()
    median_val = df['lengthofstay'].median()
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df['lengthofstay'],
        nbinsx=17,
        marker=dict(color=COLORS['primary'], line=dict(color='white')),
        hovertemplate='<b>Days:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
    ))
    
    fig.add_vline(x=mean_val, line_dash='dash', line_color=COLORS['success'],
                  annotation_text=f'Mean: {mean_val:.2f}', annotation_position='top right')
    fig.add_vline(x=median_val, line_dash='dash', line_color=COLORS['warning'],
                  annotation_text=f'Median: {median_val:.2f}', annotation_position='top left')
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        xaxis_title='Length of Stay (Days)',
        yaxis_title='Number of Patients',
        template=PLOTLY_TEMPLATE,
        height=400,
        showlegend=False
    )
    
    return fig


def scatter_plot_two_variables(df, var1, var2, color_by=None, title=None):
    """
    Create scatter plot for two variables.
    """
    if title is None:
        title = f'{var1.title()} vs {var2.title()}'
    
    fig = px.scatter(
        df,
        x=var1,
        y=var2,
        color=color_by if color_by else None,
        title=title,
        template=PLOTLY_TEMPLATE,
        height=500,
        hover_data={'lengthofstay': True}
    )
    
    fig.update_layout(
        title=dict(font=dict(size=20, color='white'))
    )
    
    return fig
