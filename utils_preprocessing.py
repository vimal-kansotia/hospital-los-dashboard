"""
Data Preprocessing Pipeline
Handles data cleaning, feature engineering, and transformations
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def load_and_prepare_data(csv_path):
    """
    Load and prepare the hospital dataset.
    Returns clean dataframe ready for analysis and modeling.
    """
    # Load data
    df = pd.read_csv(csv_path)
    
    # Date conversions
    df['vdate'] = pd.to_datetime(df['vdate'], format='%m/%d/%Y')
    df['discharged'] = pd.to_datetime(df['discharged'], format='%m/%d/%Y')
    
    # Convert rcount to numeric (5+ → 5)
    df['rcount'] = df['rcount'].replace('5+', 5).astype(int)
    
    # Feature engineering
    df['los_calculated'] = (df['discharged'] - df['vdate']).dt.days
    df['month_admission'] = df['vdate'].dt.month
    df['day_of_week'] = df['vdate'].dt.dayofweek
    
    # Calculate comorbidity score
    comorbidity_cols = [
        'dialysisrenalendstage', 'asthma', 'irondef', 'pneum',
        'substancedependence', 'psychologicaldisordermajor',
        'depress', 'psychother', 'fibrosisandother', 'malnutrition',
        'hemo', 'secondarydiagnosisnonicd9'
    ]
    df['comorbidity_score'] = df[comorbidity_cols].sum(axis=1)
    
    # Create LOS category for analysis (1-3, 4-6, 7-10, 11+)
    df['los_category'] = pd.cut(
        df['lengthofstay'],
        bins=[0, 3, 6, 10, 17],
        labels=['1-3 days', '4-6 days', '7-10 days', '11+ days'],
        include_lowest=True
    )
    
    # Remove duplicates if any
    df = df.drop_duplicates(subset=['eid', 'vdate'], keep='first')
    
    return df


def prepare_ml_features(df):
    """
    Prepare features for machine learning.
    Returns X (features) and y (target).
    """
    # Features for modeling
    feature_cols = [
        'rcount', 'gender', 'dialysisrenalendstage', 'asthma', 'irondef',
        'pneum', 'substancedependence', 'psychologicaldisordermajor',
        'depress', 'psychother', 'fibrosisandother', 'malnutrition', 'hemo',
        'hematocrit', 'neutrophils', 'sodium', 'glucose', 'bloodureanitro',
        'creatinine', 'bmi', 'pulse', 'respiration', 'secondarydiagnosisnonicd9',
        'facid', 'month_admission', 'day_of_week', 'comorbidity_score'
    ]
    
    X = df[feature_cols].copy()
    y = df['lengthofstay'].copy()
    
    # Encode categorical variables
    le_gender = LabelEncoder()
    le_facility = LabelEncoder()
    
    X['gender'] = le_gender.fit_transform(X['gender'])
    X['facid'] = le_facility.fit_transform(X['facid'])
    
    # Handle any NaN values (fill with median)
    for col in X.select_dtypes(include=[np.number]).columns:
        X[col].fillna(X[col].median(), inplace=True)
    
    return X, y, le_gender, le_facility


def scale_features(X_train, X_test=None):
    """
    Scale numeric features using StandardScaler.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
        X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)
        return X_train_scaled, X_test_scaled, scaler
    
    return X_train_scaled, scaler


def get_clinical_stats(df):
    """
    Calculate statistics for clinical variables.
    """
    clinical_cols = [
        'bmi', 'glucose', 'pulse', 'hematocrit', 'creatinine',
        'bloodureanitro', 'sodium', 'neutrophils', 'respiration'
    ]
    
    stats = {}
    for col in clinical_cols:
        stats[col] = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max(),
            'q1': df[col].quantile(0.25),
            'q3': df[col].quantile(0.75)
        }
    
    return stats


def get_demographic_summary(df):
    """
    Get demographic breakdown.
    """
    summary = {
        'total_patients': len(df),
        'gender_split': df['gender'].value_counts().to_dict(),
        'facility_split': df['facid'].value_counts().to_dict(),
        'readmission_dist': df['rcount'].value_counts().sort_index().to_dict(),
        'avg_los': df['lengthofstay'].mean(),
        'median_los': df['lengthofstay'].median(),
        'max_los': df['lengthofstay'].max(),
    }
    return summary


def get_correlation_matrix(df):
    """
    Get correlation matrix for numeric columns.
    """
    numeric_cols = [
        'bmi', 'glucose', 'pulse', 'hematocrit', 'creatinine',
        'bloodureanitro', 'sodium', 'neutrophils', 'respiration',
        'lengthofstay', 'rcount', 'comorbidity_score'
    ]
    
    return df[numeric_cols].corr()


def filter_data(df, gender=None, facility=None, rcount=None, los_range=None):
    """
    Filter dataframe based on multiple criteria.
    """
    df_filtered = df.copy()
    
    if gender:
        df_filtered = df_filtered[df_filtered['gender'].isin(gender)]
    
    if facility:
        df_filtered = df_filtered[df_filtered['facid'].isin(facility)]
    
    if rcount:
        df_filtered = df_filtered[df_filtered['rcount'].isin(rcount)]
    
    if los_range:
        min_los, max_los = los_range
        df_filtered = df_filtered[
            (df_filtered['lengthofstay'] >= min_los) &
            (df_filtered['lengthofstay'] <= max_los)
        ]
    
    return df_filtered


def get_comorbidity_prevalence(df):
    """
    Calculate prevalence of each comorbidity in the dataset.
    """
    comorbidity_cols = [
        'dialysisrenalendstage', 'asthma', 'irondef', 'pneum',
        'substancedependence', 'psychologicaldisordermajor',
        'depress', 'psychother', 'fibrosisandother', 'malnutrition',
        'hemo', 'secondarydiagnosisnonicd9'
    ]
    
    prevalence = {}
    for col in comorbidity_cols:
        count = (df[col] == 1).sum()
        prevalence[col.replace('_', ' ').title()] = {
            'count': count,
            'percentage': (count / len(df)) * 100
        }
    
    return prevalence
