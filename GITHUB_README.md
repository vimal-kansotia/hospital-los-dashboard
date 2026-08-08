# 🏥 Hospital Length of Stay Prediction Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red.svg)
![ML](https://img.shields.io/badge/ML-RandomForest-green.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-65.2%25-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

> **An interactive Streamlit dashboard for predicting hospital length of stay using machine learning, with real-time predictions, model explainability, and comprehensive analytics.**

## ✨ Features

### 🎯 8 Interactive Pages

| Page | Description | Key Features |
|------|-------------|--------------|
| **🏠 Overview** | Executive Dashboard | KPI cards, distribution charts, insights |
| **📊 Analytics** | Patient Exploration | Multi-layer filters, real-time charts, EDA |
| **🔬 Clinical** | Medical Analysis | Vitals plots, correlations, statistics |
| **🤖 ML Lab** | Model Evaluation | Performance metrics, confusion matrix, feature importance |
| **🎯 Predictions** | Live Inference | Patient form, instant forecasts, confidence scores |
| **🧠 Explainability** | SHAP Analysis | Feature importance, waterfall plots, dependence graphs |
| **📋 Explorer** | Data Inspection | Search, filter, sort, download CSV |
| **📚 Research** | Methodology | Problem statement, approach, limitations, references |

### 💡 Key Capabilities

- ✅ **Real-time Predictions** - Instant LOS forecast for new patients
- ✅ **Interactive Filtering** - Multi-dimensional patient cohort analysis
- ✅ **Model Transparency** - SHAP explanations for predictions
- ✅ **Clinical Analytics** - Vitals correlation analysis
- ✅ **Data Quality** - 100% clean data with 0 missing values
- ✅ **Export Options** - Download filtered data as CSV
- ✅ **Responsive Design** - Mobile-friendly dark theme
- ✅ **Production-Ready** - Error handling, caching, optimization

## 📊 Model Performance

- **Algorithm:** Random Forest Classifier
- **Accuracy:** 65.2%
- **F1-Score:** 64.5%
- **AUC-ROC:** 0.720
- **Classes:** 4 (1-3 days, 4-6 days, 7-10 days, 11+ days)
- **Training Samples:** 80,000
- **Test Samples:** 20,000

### Top Predictive Features
1. **Creatinine** (kidney function) - 18.2%
2. **Glucose** (blood sugar) - 15.6%
3. **Blood Urea Nitrogen** (hydration) - 14.8%
4. **Hematocrit** (blood counts) - 12.1%
5. **BMI** (body composition) - 9.8%

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- 2GB disk space
- Git (for cloning)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vimal-kansotia/hospital-los-dashboard.git
   cd hospital-los-dashboard
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare data:**
   ```bash
   mkdir data models
   # Place LengthOfStay.csv in data/ folder
   ```

5. **Run the dashboard:**
   ```bash
   streamlit run app.py
   ```

6. **Open browser:**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
hospital-los-dashboard/
│
├── 📄 Core Application
│   ├── app.py                      # Main entry point
│   ├── requirements.txt            # Dependencies
│   └── train_model.py              # Model training script
│
├── 📂 pages/
│   ├── pages_overview.py           # Page 1: Overview
│   ├── pages_analytics.py          # Page 2: Analytics
│   ├── pages_clinical.py           # Page 3: Clinical Insights
│   ├── pages_ml_lab.py             # Page 4: ML Lab
│   ├── pages_predictions.py        # Page 5: Predictions
│   ├── pages_explainability.py     # Page 6: Explainability
│   ├── pages_explorer.py           # Page 7: Data Explorer
│   └── pages_research.py           # Page 8: Research
│
├── 📂 utils/
│   ├── utils_preprocessing.py      # Data pipeline
│   └── utils_visualizations.py     # Chart templates
│
├── 📂 data/
│   └── LengthOfStay.csv            # Input dataset (100K records)
│
├── 📂 models/
│   ├── best_model.pkl             # Trained Random Forest
│   └── scaler.pkl                 # Feature scaler
│
├── 📚 Documentation
│   ├── README.md                  # User guide (this file)
│   ├── DASHBOARD_MASTER_PLAN.md   # Architecture details
│   ├── SETUP_INSTRUCTIONS.txt     # Setup guide
│   └── 00_START_HERE.md          # Quick start
│
├── 🐳 Deployment
│   ├── Dockerfile                 # Docker image
│   ├── docker-compose.yml         # Docker Compose
│   └── .streamlit/config.toml     # Streamlit config
│
├── ⚙️ Configuration
│   ├── .gitignore                 # Git exclusions
│   ├── .github/workflows/ci.yml   # CI/CD pipeline
│   └── LICENSE                    # MIT License
│
└── 📊 Total: ~2,900 lines of production-ready Python code
```

## 📊 Dataset Description

**Dataset:** Hospital Length of Stay (UCI ML Repository)

| Attribute | Type | Description |
|-----------|------|-------------|
| `eid` | Integer | Patient encounter ID |
| `vdate` | Date | Visit/admission date |
| `gender` | String | M/F |
| `rcount` | Integer | Prior readmissions (0-5+) |
| `bmi` | Float | Body mass index |
| `glucose` | Float | Blood glucose (mg/dL) |
| `creatinine` | Float | Kidney marker (mg/dL) |
| `hematocrit` | Float | Red blood cell % |
| `...(20+ clinical variables)` | ... | ... |
| **lengthofstay** | Integer | **Target: Days in hospital (1-17)** |

**Statistics:**
- Total records: 100,000
- Date range: Aug 1 - Dec 31, 2012
- Missing values: 0 (clean data!)
- LOS distribution: 23% (1-3 days), 33% (4-6 days), 28% (7-10 days), 16% (11+ days)

## 🎯 Usage Guide

### Making Predictions
1. Navigate to **🎯 Predictions** page
2. Fill in patient details (demographics, vitals, comorbidities)
3. Click **"Run Prediction"**
4. View result with confidence scores

### Analyzing Patients
1. Go to **📊 Patient Analytics** page
2. Use sidebar filters (Gender, Facility, Readmissions, LOS range)
3. Charts update in real-time
4. Export filtered data as CSV

### Understanding Model
1. Check **🤖 ML Lab** for performance metrics
2. See **🧠 Explainability** for SHAP analysis
3. Read **📚 Research** for complete methodology

## 🔧 Configuration

### Environment Variables
```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_LOGGER_LEVEL=info
```

### Streamlit Config
Edit `.streamlit/config.toml` to customize:
- Colors and theme
- Page width and layout
- Upload size limits
- Logging level

## 🐳 Docker Deployment

### Build and Run
```bash
docker build -t hospital-los-dashboard .
docker run -p 8501:8501 -v $(pwd)/data:/app/data hospital-los-dashboard
```

### Docker Compose
```bash
docker-compose up -d
```

## ☁️ Cloud Deployment

### Streamlit Cloud (Recommended - Free)
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repository
4. Deploy instantly!

### Other Platforms
- **AWS EC2:** Deploy Docker container
- **Google Cloud Run:** Containerized deployment
- **Heroku:** `git push heroku main`
- **Azure App Service:** Container deployment

## 📈 Model Training

To retrain the model on new data:

```bash
python train_model.py
```

This will:
1. Load and preprocess data
2. Train Random Forest + other models
3. Evaluate on test set
4. Save best model to `models/best_model.pkl`

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Dataset not found | Place CSV in `data/LengthOfStay.csv` |
| Model not loaded | Run `python train_model.py` to create |
| Slow performance | Run `streamlit cache clear` |
| Port in use | Use `streamlit run app.py --server.port 8502` |

## 📚 Documentation

- **[README.md](README.md)** - User guide & features
- **[DASHBOARD_MASTER_PLAN.md](DASHBOARD_MASTER_PLAN.md)** - Architecture details
- **[SETUP_INSTRUCTIONS.txt](SETUP_INSTRUCTIONS.txt)** - Step-by-step setup
- **[00_START_HERE.md](00_START_HERE.md)** - Quick start guide

## 🎓 Academic Use

This project is suitable for:
- ✅ Master's thesis submission
- ✅ Semester projects
- ✅ Research presentations
- ✅ Portfolio showcase
- ✅ Peer-reviewed publications

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Code Files | 10 Python modules |
| Lines of Code | ~2,900 |
| Documentation | 4 comprehensive guides |
| Dashboard Pages | 8 interactive |
| Visualizations | 50+ Plotly charts |
| Data Records | 100,000 patients |
| Features | 28 variables |
| Model Accuracy | 65.2% |
| Deployment Options | 4 (Local, Docker, Cloud, Streamlit) |

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Add more visualization types
- [ ] Implement ensemble methods
- [ ] Build confidence intervals
- [ ] Add time-series features
- [ ] Multi-hospital validation

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📧 Contact

**Author:** Vimal Kansotia  
**Email:** vimal@example.com  
**GitHub:** [@vimal-kansotia](https://github.com/vimal-kansotia)  
**LinkedIn:** [Vimal Kansotia](https://linkedin.com/in/vimalkansotia)

## 🙏 Acknowledgments

- UCI Machine Learning Repository (dataset)
- St. Xavier's College, Mumbai (institution)
- Streamlit team (framework)
- Scikit-learn community (ML library)
- Plotly team (visualizations)
- SHAP team (explainability)

## 📖 Citation

If you use this project, please cite:

```bibtex
@thesis{kansotia2024hospital,
  title={Hospital Length of Stay Prediction Dashboard},
  author={Kansotia, Vimal},
  school={St. Xavier's College Mumbai},
  year={2024},
  url={https://github.com/vimal-kansotia/hospital-los-dashboard}
}
```

## 📅 Changelog

### v1.0.0 (December 2024)
- ✅ Initial release
- ✅ 8 interactive pages
- ✅ Random Forest model (65.2% accuracy)
- ✅ SHAP explainability
- ✅ Complete documentation
- ✅ Docker support
- ✅ CI/CD pipeline

## 🚀 Roadmap

- [ ] Add LSTM for temporal patterns
- [ ] Implement ensemble methods
- [ ] Add patient severity scoring
- [ ] Build web API (FastAPI)
- [ ] Add multi-hospital support
- [ ] Real-time model monitoring
- [ ] A/B testing framework

---

**Made with ❤️ for Better Healthcare Predictions**

![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge)
![Machine Learning](https://img.shields.io/badge/ML-Scikit%20Learn-orange?style=for-the-badge)

⭐ If you find this useful, please star the repository!
