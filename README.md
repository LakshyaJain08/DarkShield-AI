# 🛡️ DarkShield AI: End-to-End MLOps Dark Pattern Detection

An industry-grade Machine Learning and Web Intelligence platform designed to autonomously detect, classify, and explain deceptive UX/UI dark patterns on e-commerce websites.

---

## 🏛️ Repository Architecture (Matching Enterprise MLOps Standard)

```text
├── .github/
│   └── workflows/ci.yaml            # Continuous Integration pipeline
├── data/
│   ├── raw/dataset.tsv              # Original raw data (immutable)
│   ├── processed/train.csv, test.csv# Stratified train/test splits
│   └── external/                    # Lexicons and auxiliary sources
├── docs/                            # 📚 Comprehensive Documentation Suite
│   ├── PRD.md                       # Product Requirements Document
│   ├── ARCHITECTURE.md              # System & ML Architecture Blueprint
│   ├── UI_UX_DESIGN.md              # Sentinel Amber UI/UX Design System
│   ├── DEVELOPMENT_PLAN.md          # Engineering Roadmap & Milestones
│   ├── REQUIREMENTS.md              # Software, Hardware & Environment Specs
│   ├── MODEL_CARD.md                # ML Model Card (LR, SVM, LSTM, GRU)
│   ├── DATA_DICTIONARY.md           # Dataset Schema & Dark Pattern Taxonomy
│   └── API_REFERENCE.md             # FastAPI Endpoint Specifications
├── notebooks/
│   ├── end_to_end_dark_pattern_ml.ipynb # Master End-to-End ML Lifecycle Notebook
│   ├── 01_eda.ipynb                 # In-depth Exploratory Data Analysis
│   ├── 02_data_preparation.ipynb    # Data Ingestion & Transformation experimentation
│   └── 03_model_experimentation.ipynb # Multi-model hyperparameter tuning & evaluation
├── src/
│   ├── components/                  # Reusable ML components
│   │   ├── data_ingestion.py        # Data loading and stratified splitting
│   │   ├── data_validation.py       # Enterprise schema validation & null checks
│   │   ├── data_transformation.py   # Text cleaning & train-only vectorizer fitting
│   │   ├── feature_engineering.py   # TF-IDF, sequence models (LSTM, GRU)
│   │   ├── model_trainer.py         # Systematic 5-fold CV hyperparameter tuning
│   │   ├── model_evaluation.py      # Metrics (F1, AUC, Confusion Matrices, ROC)
│   │   └── model_pusher.py          # Deploys best models directly to backend/models/
│   ├── pipelines/                   # Orchestration pipelines
│   │   ├── training_pipeline.py     # Master end-to-end training pipeline
│   │   ├── inference_pipeline.py    # Production model loader & prediction
│   │   └── prediction_pipeline.py   # Explainable inference with SHAP attributions
│   ├── utils/                       # Common utilities
│   │   ├── common.py                # Artifact persistence (pickle, PyTorch, JSON)
│   │   ├── config_loader.py         # YAML configuration and schema parsers
│   │   └── logger.py                # Enterprise logging to console and log files
│   └── config/                      # Configuration schemas
│       ├── config.yaml              # Hyperparameters, split ratios, paths
│       └── schema.yaml              # Column types, constraints, allowed labels
├── tests/                           # Automated unit & integration tests
│   ├── test_data_validation.py      # Schema and edge case tests
│   └── test_model_inference.py      # Model prediction & SHAP attribution tests
├── models/                          # Stored best models & vectorizer
│   ├── logistic_regression.pkl
│   ├── svm.pkl
│   ├── lstm.pth
│   ├── gru.pth
│   └── vectorizer.pkl
├── outputs/                         # Evaluation artifacts & plots
│   ├── metrics.json                 # Model comparison metrics
│   ├── confusion_matrices.png       # 2x2 confusion matrix grid
│   ├── roc_curves.png               # Comparative ROC curves
│   └── logs/                        # Timestamped execution logs
├── app/                             # API serving layer
│   ├── api.py                       # FastAPI model serving endpoints
│   └── schemas.py                   # Pydantic request/response schemas
├── backend/                         # Live Web Application Backend (FastAPI + Playwright)
├── frontend/                        # Sentinel Amber React Web UI
├── extension/                       # Manifest V3 Chrome Extension
├── Dockerfile                       # Production containerization
├── requirements.txt                 # Project dependencies
└── setup.py                         # Package installation configuration
```

---

## 🚀 Quickstart Guide

### 1. Environment Setup
```bash
# Activate virtual environment
.\backend\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Run the Full MLOps Training Pipeline
To execute the complete pipeline (Ingestion ➔ Validation ➔ Transformation ➔ Hyperparameter Tuning ➔ Evaluation ➔ Model Pusher):
```bash
python -m src.pipelines.training_pipeline
```
*The best models will be tuned and pushed automatically to `backend/models/` for immediate website prediction.*

### 3. Run the Interactive Jupyter Notebook
Launch Jupyter to explore the master end-to-end notebook:
```bash
jupyter notebook notebooks/end_to_end_dark_pattern_ml.ipynb
```

---

## 🏆 Model Performance Benchmark (Holdout Test Set)

| Model Architecture | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** (GridSearch Tuned: C=10.0, l2) | 92.80% | 94.69% | 90.68% | 0.9264 | 0.9750 |
| **SVM (Linear Kernel)** (GridSearch Tuned: C=1.0) | 93.64% | 96.40% | 90.68% | 0.9345 | 0.9709 |
| **LSTM (Deep Sequence)** (Tuned: hidden=32, lr=0.001) | **95.13%** | 96.92% | **93.22%** | **0.9503** | 0.9707 |
| **GRU (Deep Sequence)** (Tuned: hidden=64, lr=0.001) | **95.13%** | **97.76%** | 92.37% | 0.9499 | **0.9774** |

---

## 🧪 Testing
Run the automated test suite:
```bash
pytest tests/
```

---

## 📚 Project Documentation Suite (`docs/`)

Detailed design, engineering, and academic specifications are available in the [`docs/`](docs/) directory:

- [**PRD.md**](docs/PRD.md): Product Requirements Document, user personas, taxonomy definitions, and success metrics.
- [**ARCHITECTURE.md**](docs/ARCHITECTURE.md): System blueprint, decoupled MLOps architecture, neural design, and sequence diagrams.
- [**UI_UX_DESIGN.md**](docs/UI_UX_DESIGN.md): Sentinel Amber design system, design tokens, typography, and component specifications.
- [**DEVELOPMENT_PLAN.md**](docs/DEVELOPMENT_PLAN.md): Engineering roadmap, sprint milestones, CI/CD, and retraining runbooks.
- [**REQUIREMENTS.md**](docs/REQUIREMENTS.md): Hardware, software, dependency matrix, and step-by-step setup guide.
- [**MODEL_CARD.md**](docs/MODEL_CARD.md): Industry-standard ML model card covering LR, SVM, LSTM, GRU, metrics, and ethics.
- [**DATA_DICTIONARY.md**](docs/DATA_DICTIONARY.md): Complete dataset schema, field definitions, category descriptions, and preprocessing specs.
- [**API_REFERENCE.md**](docs/API_REFERENCE.md): REST API contracts for `/analyze/url`, `/analyze/all`, and `/predict`.

