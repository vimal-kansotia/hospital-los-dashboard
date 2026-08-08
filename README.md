# 🏥 Hospital Length of Stay Prediction Dashboard

**A production-grade interactive Streamlit dashboard for predicting and analyzing patient hospital stays using machine learning.**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red.svg)
![ML](https://img.shields.io/badge/ML-RandomForest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🎯 Project Overview

This dashboard predicts hospital length of stay (LOS) using a Random Forest machine learning model trained on 100,000 patient records. It includes interactive visualizations, SHAP explainability, and comprehensive research documentation.

**Key Metrics:**
- **Accuracy**: 65.2%
- **Dataset**: 100,000 patient records (Aug-Dec 2012)
- **Features**: 28 (demographics, vitals, comorbidities)
- **Target**: LOS 1-17 days (4 classes)

---

## 📋 Features

### 8 Interactive Pages:

1. **🏠 Overview** - Executive dashboard with KPIs
2. **📊 Patient Analytics** - Interactive EDA with filters
3. **🔬 Clinical Insights** - Vitals analysis & correlations
4. **🤖 ML Lab** - Model comparison & performance
5. **🎯 Predictions** - Live patient inference
6. **🧠 Explainability** - SHAP & feature attribution
7. **📋 Data Explorer** - Raw data inspection
8. **📚 Research** - Complete methodology

### Dashboard Capabilities:

✅ **Real-time Predictions** - Instant LOS forecast for new patients  
✅ **Interactive Filtering** - Multi-layer patient cohort analysis  
✅ **Model Transparency** - SHAP explanations for every prediction  
✅ **Clinical Analytics** - Vitals correlation analysis  
✅ **Data Quality** - 100% clean data, 0 missing values  
✅ **Export Options** - Download filtered data as CSV  
✅ **Responsive Design** - Mobile-friendly dark theme  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- ~2GB free disk space

### Installation

1. **Clone or download the repository:**
   ```bash
   cd hospital-los-dashboard
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required directories:**
   ```bash
   mkdir data models
   ```

5. **Place the dataset:**
   - Copy `LengthOfStay.csv` to the `data/` folder

6. **Train the model (or use pre-trained):**
   ```bash
   python train_model.py
   ```
   This creates `models/best_model.pkl`

7. **Run the dashboard:**
   ```bash
   streamlit run app.py
   ```

8. **Open in browser:**
   - Navigate to `http://localhost:8501`

---

## 📁 Project Structure

```
hospital-length-of-stay-analytics/
│
├── 📄 app.py                           # Main Streamlit app
│
├── 📂 pages/
│   ├── overview.py                     # Page 1: Overview
│   ├── analytics.py                    # Page 2: Patient Analytics
│   ├── clinical.py                     # Page 3: Clinical Insights
│   ├── ml_lab.py                       # Page 4: ML Lab
│   ├── predictions.py                  # Page 5: Predictions
│   ├── explainability.py               # Page 6: Explainability
│   ├── explorer.py                     # Page 7: Data Explorer
│   └── research.py                     # Page 8: Research
│
├── 📂 utils/
│   ├── preprocessing.py                # Data pipeline
│   └── visualizations.py               # Chart templates
│
├── 📂 data/
│   └── LengthOfStay.csv                # Raw dataset (100K records)
│
├── 📂 models/
│   ├── best_model.pkl                  # Trained Random Forest
│   └── preprocessing_pipeline.pkl      # Fitted scaler
│
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
└── MASTER_PLAN.md                      # Architecture documentation

```

---

## 🎨 Dashboard Pages Guide

### Page 1: 🏠 Overview (Executive Dashboard)
**What you'll see:**
- 5 KPI cards (Patients, Avg LOS, Median, Max, Model Accuracy)
- Distribution charts (LOS by day, Facility breakdown)
- Gender & readmission analysis
- Key insights summary

**Use case:** Quick scan for hospital managers & examiners

---

### Page 2: 📊 Patient Analytics (Interactive EDA)
**What you'll see:**
- Sidebar filters (Gender, Facility, Readmissions, LOS range)
- 4-panel visualization grid
- Real-time chart updates as you filter
- Comorbidity prevalence analysis
- Downloadable filtered data

**Use case:** Deep exploration of patient cohorts

---

### Page 3: 🔬 Clinical Insights (Vitals Analysis)
**What you'll see:**
- Box plots by LOS category
- Correlation heatmap (all vitals)
- Scatter plot analysis
- Statistical summary tables
- Comorbidity impact analysis

**Use case:** Understand clinical drivers of LOS

---

### Page 4: 🤖 ML Lab (Model Performance)
**What you'll see:**
- Model comparison table (RF, XGBoost, LightGBM, LR)
- Confusion matrix heatmap
- Classification report by class
- Feature importance rankings
- Training progress charts

**Use case:** Model validation & selection

---

### Page 5: 🎯 Predictions (Live Inference)
**What you'll see:**
- Patient input form (demographics, vitals, comorbidities)
- Large prediction result card
- Probability bar chart (all 4 LOS classes)
- Clinical interpretation text
- Similar patients comparison

**Use case:** Real-time prediction for clinicians

---

### Page 6: 🧠 Explainability (SHAP)
**What you'll see:**
- Global feature importance
- SHAP waterfall explanation
- Feature dependence plots
- Local interpretation for individuals
- Model fairness assessment

**Use case:** Transparency & model debugging

---

### Page 7: 📋 Data Explorer (Raw Data)
**What you'll see:**
- Data quality metrics
- Search & filter functionality
- Sortable data table with pagination
- Column information
- Export as CSV

**Use case:** Data inspection & verification

---

### Page 8: 📚 Research (Methodology)
**What you'll see:**
- Problem statement
- Dataset description
- Complete methodology breakdown
- Key findings & limitations
- Future improvements
- References & citations

**Use case:** Academic submission & documentation

---

## 🎯 Using the Dashboard

### Basic Workflow:

1. **Start on Overview** → Get quick summary of all metrics
2. **Explore Patient Analytics** → Filter by demographic groups
3. **Check Clinical Insights** → Understand vitals correlations
4. **Review ML Lab** → Validate model performance
5. **Make Predictions** → Input patient data, get LOS forecast
6. **Understand Explanations** → See why model made that prediction
7. **Inspect Raw Data** → Verify underlying records
8. **Read Research** → Understand methodology & limitations

### Common Tasks:

**Q: How do I filter patients?**
A: Go to "Patient Analytics" page → Use sidebar filters (Gender, Facility, Readmissions, LOS range) → Charts update in real-time

**Q: How do I make a prediction?**
A: Go to "Predictions" page → Fill in patient form → Click "Run Prediction" → See result with confidence scores

**Q: How does the model decide?**
A: Go to "Explainability" page → See global feature importance and local SHAP values for individual predictions

**Q: Can I download the data?**
A: Yes! On "Data Explorer" page, use search/filters → Click "Download as CSV"

---

## 📊 Data Description

**Dataset:** Hospital Length of Stay (UCI ML Repository)

| Attribute | Type | Description |
|-----------|------|-------------|
| eid | Integer | Patient encounter ID |
| vdate | Date | Visit/admission date |
| gender | String | M/F |
| rcount | Integer | Prior readmissions (0-5) |
| bmi | Float | Body mass index |
| glucose | Float | Blood glucose (mg/dL) |
| creatinine | Float | Kidney marker (mg/dL) |
| hematocrit | Float | Red blood cell % |
| pulse | Integer | Heart rate (bpm) |
| ...(20+ more clinical variables) | ... | ... |
| lengthofstay | Integer | **Target: Days in hospital (1-17)** |

**Statistics:**
- Total records: 100,000
- Date range: Aug 1 - Dec 31, 2012
- Missing values: 0 (clean data!)
- LOS distribution: 1-3 days (23%), 4-6 days (33%), 7-10 days (28%), 11+ days (16%)

---

## 🤖 Machine Learning Model

**Algorithm:** Random Forest Classifier

**Performance:**
- **Test Accuracy:** 65.2%
- **Macro F1-Score:** 64.5%
- **AUC-ROC:** 0.720
- **Classes:** 4 (1-3 days, 4-6 days, 7-10 days, 11+ days)

**Top Predictive Features:**
1. Creatinine (kidney function) - 18.2%
2. Glucose (metabolic state) - 15.6%
3. Blood Urea Nitrogen (hydration) - 14.8%
4. Hematocrit (blood counts) - 12.1%
5. BMI (body composition) - 9.8%

**Hyperparameters:**
```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    class_weight='balanced',
    random_state=42
)
```

---

## 🔧 Troubleshooting

### Issue: "Dataset not found!"
**Solution:** Place `LengthOfStay.csv` in `data/` folder and restart

### Issue: "Model not loaded"
**Solution:** Run `python train_model.py` to create `models/best_model.pkl`

### Issue: Slow performance
**Solution:** 
- Clear Streamlit cache: `streamlit cache clear`
- Reduce dataset size in preprocessing.py
- Run on faster machine

### Issue: Port already in use
**Solution:** Run on different port:
```bash
streamlit run app.py --server.port 8502
```

---

## 📦 Dependencies

- **streamlit** (1.40): Interactive UI framework
- **pandas** (2.1.4): Data manipulation
- **scikit-learn** (1.3.2): ML models & metrics
- **xgboost** (2.0.3): Gradient boosting
- **plotly** (5.18.0): Interactive visualizations
- **shap** (0.44.1): Model explainability
- **joblib** (1.3.2): Model serialization

See `requirements.txt` for full list.

---

## 🚀 Deployment

### Local Deployment (Development)
```bash
streamlit run app.py
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect GitHub repo
4. Select `app.py` as main file
5. Deploy!

### Docker Deployment
```bash
docker build -t los-dashboard .
docker run -p 8501:8501 los-dashboard
```

### Cloud Platforms
- **Heroku**: `git push heroku main`
- **AWS EC2**: Deploy using Docker
- **Google Cloud Run**: Containerized deployment

---

## 📈 Model Training (Optional)

To retrain the model on new data:

```bash
python train_model.py --data data/LengthOfStay.csv --output models/best_model.pkl
```

This will:
1. Load and preprocess data
2. Train Random Forest + XGBoost + LightGBM
3. Evaluate on test set
4. Save best model
5. Print performance metrics

---

## 📝 Academic Use

This dashboard is suitable for:
- ✅ Master's thesis submission
- ✅ PhD research projects
- ✅ Conference presentations
- ✅ Peer-reviewed publications
- ✅ Industrial portfolio

**Citation:**
```
Vimal Kansotia. "Hospital Length of Stay Prediction Dashboard." 
Master's Thesis, St. Xavier's College Mumbai, 2024.
(https://github.com/vimal-kansotia/hospital-length-of-stay-analytics/tree/main)
```

---

## 📄 License

MIT License - Feel free to use, modify, and distribute

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add more visualization types
- [ ] Implement ensemble methods
- [ ] Build confidence intervals
- [ ] Add time-series features
- [ ] Multi-hospital validation

---

## 📧 Contact & Support

**Author:** Vimal Kansotia  
**Email:** kansotiavimal4@gmail.com  
**GitHub:** (https://github.com/vimal-kansotia/hospital-length-of-stay-analytics/tree/main)  

For issues, please create a GitHub issue or email.

---

## 🙏 Acknowledgments

- UCI Machine Learning Repository (dataset)
- St. Xavier's College, Mumbai (institution)
- Streamlit team (framework)
- Scikit-learn community (models)

---

**Happy analyzing! 🚀**

*Last updated: December 2024*
