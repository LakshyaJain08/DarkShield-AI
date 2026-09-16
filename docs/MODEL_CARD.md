# 📄 DarkShield AI — Machine Learning Model Card

**Model Family:** DarkShield-Ecom-v2  
**Developed by:** DarkShield AI Research & Engineering  
**Document Format:** Model Card (following Mitchell et al. guidelines)  
**Date:** September 2026  

---

## 1. Model Overview & Details

DarkShield AI provides an ensemble of four distinct machine learning and deep learning models tuned for detecting deceptive user interface patterns (dark patterns) in e-commerce text:

| Model Identifier | Architecture Type | Input Representation | Number of Parameters / Weights | Checkpoint Artifact |
| :--- | :--- | :--- | :---: | :--- |
| **`logistic_regression`** | Generalized Linear Model ($L_2$ Regularized) | Sparse TF-IDF Vector (Dim = 1000) | 1,001 | `models/logistic_regression.pkl` |
| **`svm`** | Support Vector Classifier (Linear Kernel, Calibrated) | Sparse TF-IDF Vector (Dim = 1000) | 1,001 + Platt Calibration | `models/svm.pkl` |
| **`lstm`** | Recurrent Neural Network (LSTM + Linear Projections) | Dense Projection (Dim = 32) | ~41,200 | `models/lstm.pth` |
| **`gru`** | Gated Recurrent Unit (GRU + Linear Projections) | Dense Projection (Dim = 64) | ~89,600 | `models/gru.pth` |

---

## 2. Intended Use & Scope

### Primary Intended Uses:
- Automated auditing of e-commerce web pages to identify misleading time-pressure countdowns, false scarcity notifications, confirmshaming, and artificial social proof.
- High-throughput scanning via browser extensions to provide real-time consumer warnings during online checkout flows.
- Transparent explainability through SHAP feature attributions, showing consumers and regulators the specific phrases triggering detection.

### Out-of-Scope & Prohibited Uses:
- Automated legal determinations or unilateral penalty imposition without human review.
- Classification of non-English text (current tokenizers are calibrated on English e-commerce corpora).
- Standalone verification of non-textual UI elements (e.g., hidden colors, contrast trickery without text).

---

## 3. Training & Validation Data

- **Corpus Source:** `ec-darkpattern` dataset (containing labeled e-commerce snippets collected from retail platforms).
- **Total Corpus Size:** $2,363$ observations.
- **Data Splitting Strategy:**
  - **Training Split:** $80\%$ ($1,884$ observations), stratified by class label.
  - **Hold-out Test Split:** $20\%$ ($472$ observations), completely isolated prior to text preprocessing and hyperparameter tuning.
- **Label Distribution (Train Split):**
  - Class `0` (Not Dark Pattern): $948$ samples ($50.3\%$)
  - Class `1` (Dark Pattern): $936$ samples ($49.7\%$)
- **Data Cleaning & Normalization:** Lowercasing, removal of external URLs, stripping of non-alphanumeric punctuation, and collapsing of excessive whitespace.

---

## 4. Hyperparameter Optimization & Search Space

All models underwent systematic tuning using 5-fold cross-validation or validation loss monitoring:

```text
Logistic Regression Grid Search:
├── C ∈ [0.01, 0.1, 1.0, 5.0, 10.0]
├── penalty ∈ ['l2']
└── solver ∈ ['lbfgs', 'liblinear']
──> Optimal: {'C': 10.0, 'penalty': 'l2', 'solver': 'lbfgs'}

SVM Grid Search:
├── C ∈ [0.1, 1.0, 5.0, 10.0]
├── kernel ∈ ['linear', 'rbf']
└── probability ∈ [True]
──> Optimal: {'C': 1.0, 'kernel': 'linear', 'probability': True}

LSTM Architecture Exploration:
├── hidden_dim ∈ [32, 64, 128]
├── learning_rate ∈ [0.001, 0.0005]
└── batch_size ∈ [32, 64]
──> Optimal: {'hidden_dim': 32, 'learning_rate': 0.001, 'batch_size': 32, 'epochs': 15}

GRU Architecture Exploration:
├── hidden_dim ∈ [32, 64, 128]
├── learning_rate ∈ [0.001, 0.0005]
└── batch_size ∈ [32, 64]
──> Optimal: {'hidden_dim': 64, 'learning_rate': 0.001, 'batch_size': 32, 'epochs': 15}
```

---

## 5. Performance Evaluation Benchmark

Evaluated on the completely unseen hold-out test set ($N=472$):

| Architecture | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 92.80% | 94.69% | 90.68% | 0.9264 | 0.9750 | **~0.8 ms** |
| **SVM (Linear Kernel)** | 93.64% | 96.40% | 90.68% | 0.9345 | 0.9709 | **~1.2 ms** |
| **LSTM (Deep Sequence)** | **95.13%** | 96.92% | **93.22%** | **0.9503** | 0.9707 | ~8.5 ms |
| **GRU (Deep Sequence)** | **95.13%** | **97.76%** | 92.37% | 0.9499 | **0.9774** | ~7.2 ms |

### Key Trade-offs:
- **Production Extension Deployment:** Logistic Regression and Linear SVM provide sub-millisecond inference speeds with minimal memory footprint, making them ideal for client-side or edge deployment.
- **Deep Sequence Precision:** GRU achieves the lowest false positive rate (Precision = **97.76%**), making it the preferred model for high-stakes regulatory auditing.

---

## 6. Model Interpretability & Explainability (XAI)

DarkShield AI integrates SHAP to deliver local token attributions:
- For linear models, exact token contribution is derived via weight-feature dot product $w_i \cdot x_i$.
- For deep models, `shap.DeepExplainer` computes gradient-based backpropagation across the hidden state trajectory.
- Only words physically present in the input text ($X[0] > 0$) are ranked to prevent misleading zero-value attributions.

---

## 7. Ethical Considerations, Fairness & Caveats

1. **Context Dependency:** A phrase like *"only 2 left"* can represent legitimate inventory management or deceptive artificial scarcity. DarkShield AI flags potential dark patterns as probabilistic risk indicators rather than definitive fraudulent intent.
2. **Dynamic Web Layouts:** Some dark patterns rely on low-contrast text or hidden cancellation links (Obstruction). While textual DOM extraction captures wording, purely visual tricks require multi-modal computer vision models in future iterations.
3. **Consumer Empowerment:** The model is explicitly designed to empower consumers with transparent information, evening the information asymmetry between online retailers and shoppers.
