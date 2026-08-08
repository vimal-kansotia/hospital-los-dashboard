"""
Model Training Script
Trains Random Forest and other models on hospital LOS data
Run: python train_model.py
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("🏥 HOSPITAL LENGTH OF STAY MODEL TRAINING")
print("=" * 80)

# Check if data exists
if not os.path.exists('data/LengthOfStay.csv'):
    print("❌ Error: data/LengthOfStay.csv not found!")
    print("Please place the dataset in data/ folder and try again.")
    exit(1)

# Load data
print("\n📂 Loading data...")
df = pd.read_csv('data/LengthOfStay.csv')
print(f"✓ Loaded {len(df):,} records with {len(df.columns)} columns")

# Preprocessing
print("\n🔧 Preprocessing...")
df['vdate'] = pd.to_datetime(df['vdate'], format='%m/%d/%Y', errors='coerce')
df['discharged'] = pd.to_datetime(df['discharged'], format='%m/%d/%Y', errors='coerce')
df['rcount'] = df['rcount'].replace('5+', 5).astype(int)

# Feature engineering
df['month_admission'] = df['vdate'].dt.month
df['day_of_week'] = df['vdate'].dt.dayofweek

comorbidity_cols = [
    'dialysisrenalendstage', 'asthma', 'irondef', 'pneum',
    'substancedependence', 'psychologicaldisordermajor',
    'depress', 'psychother', 'fibrosisandother', 'malnutrition',
    'hemo', 'secondarydiagnosisnonicd9'
]
df['comorbidity_score'] = df[comorbidity_cols].sum(axis=1)

print("✓ Data preprocessing complete")

# Prepare features
print("\n🎯 Preparing features...")
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

# Encode categorical
le_gender = LabelEncoder()
le_facility = LabelEncoder()
X['gender'] = le_gender.fit_transform(X['gender'])
X['facid'] = le_facility.fit_transform(X['facid'])

# Fill NaN
for col in X.select_dtypes(include=[np.number]).columns:
    X[col].fillna(X[col].median(), inplace=True)

print(f"✓ Features prepared: {X.shape}")

# Train-test split
print("\n📊 Splitting data (80-20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"✓ Train: {X_train.shape[0]:,} | Test: {X_test.shape[0]:,}")

# Scale features
print("\n📈 Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("✓ Features scaled")

# Train Random Forest
print("\n🤖 Training Random Forest...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=4,
    max_features='sqrt',
    class_weight='balanced',
    n_jobs=-1,
    random_state=42,
    verbose=1
)

model.fit(X_train_scaled, y_train)
print("✓ Random Forest training complete")

# Evaluate
print("\n📊 Evaluating model...")
train_pred = model.predict(X_train_scaled)
test_pred = model.predict(X_test_scaled)

train_acc = accuracy_score(y_train, train_pred)
test_acc = accuracy_score(y_test, test_pred)

print(f"✓ Train Accuracy: {train_acc:.4f} ({train_acc*100:.2f}%)")
print(f"✓ Test Accuracy:  {test_acc:.4f} ({test_acc*100:.2f}%)")

# Cross-validation
print("\n🔄 Cross-validation (5-fold)...")
cv_scores = cross_val_score(
    model, X_train_scaled, y_train,
    cv=StratifiedKFold(n_splits=5, random_state=42, shuffle=True),
    scoring='accuracy',
    n_jobs=-1
)
print(f"✓ CV Scores: {cv_scores}")
print(f"✓ CV Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# Classification report
print("\n📋 Classification Report (Test Set):")
print(classification_report(y_test, test_pred))

# Confusion matrix
print("\n🎯 Confusion Matrix:")
cm = confusion_matrix(y_test, test_pred)
print(cm)

# Feature importance
print("\n🌟 Top 10 Feature Importance:")
importances = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False).head(10)

for idx, row in importances.iterrows():
    print(f"  {row['Feature']:<30} : {row['Importance']:.4f}")

# Create models directory
os.makedirs('models', exist_ok=True)

# Save model
print("\n💾 Saving model...")
joblib.dump(model, 'models/best_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(le_gender, 'models/encoder_gender.pkl')
joblib.dump(le_facility, 'models/encoder_facility.pkl')
print("✓ Model saved to models/best_model.pkl")
print("✓ Scaler saved to models/scaler.pkl")
print("✓ Encoders saved")

# Summary
print("\n" + "=" * 80)
print("✅ TRAINING COMPLETE!")
print("=" * 80)
print(f"""
Summary:
  • Model Type: Random Forest Classifier
  • Test Accuracy: {test_acc*100:.2f}%
  • Cross-Val Accuracy: {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%
  • Training Samples: {X_train.shape[0]:,}
  • Test Samples: {X_test.shape[0]:,}
  • Features: {len(feature_cols)}
  • Classes: 4 (1-3, 4-6, 7-10, 11+ days)
  
Files saved:
  ✓ models/best_model.pkl
  ✓ models/scaler.pkl
  ✓ models/encoder_gender.pkl
  ✓ models/encoder_facility.pkl

Next step: Run 'streamlit run app.py' to launch dashboard!
""")
print("=" * 80)
