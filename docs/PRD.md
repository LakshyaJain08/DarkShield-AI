# 🛡️ DarkShield AI — Product Requirements Document (PRD)

**Document Version:** 2.0.0  
**Status:** Approved  
**Course / Context:** Machine Learning (BCSE209L) — Digital Assignment 2 / Enterprise Prototype  
**Author:** DarkShield AI Engineering Team  
**Last Updated:** September 2026  

---

## 1. Executive Summary & Problem Statement

Modern e-commerce and digital service platforms increasingly employ user-interface manipulation tactics known as **dark patterns**. These deceptive design techniques exploit cognitive biases to steer, deceive, or coerce consumers into decisions they might not otherwise make—such as purchasing unneeded warranties, rushing into checkout under artificial scarcity, or consenting to aggressive data harvesting.

Common examples include:
- **False Urgency:** Countdown timers suggesting imminent expiration of standard pricing.
- **Artificial Scarcity:** "Only 2 left in stock!" indicators fabricated to force immediate buying.
- **Misdirection & Confirmshaming:** Phrasing opt-out buttons with guilt-inducing language ("No thanks, I hate saving money").
- **Social Proof Fabrication:** Notifications claiming hundreds of users recently bought the item without verifiability.

**DarkShield AI** solves this problem by providing an automated, explainable machine-learning system that ingests live e-commerce web pages, extracts text and UI strings, identifies deceptive patterns across multiple model paradigms (Logistic Regression, SVM, LSTM, GRU), and visualizes the exact tokens responsible for the prediction using **SHAP (SHapley Additive exPlanations)**.

---

## 2. Product Objectives & Value Proposition

1. **Autonomous Detection:** Enable instant classification of deceptive UI text from any publicly accessible URL or screenshot.
2. **Transparent Explainability:** Demystify AI decisions by highlighting salient tokens (e.g., *"left in stock"*, *"flash sale"*, *"hurry"*) with quantitative contribution scores.
3. **Multi-Model Intelligence:** Compare linear probabilistic baselines against deep recurrent sequence architectures in parallel.
4. **Seamless Consumer Utility:** Deliver findings via an investigative web intelligence dashboard and a lightweight Manifest V3 Chrome Extension.

---

## 3. Target User Personas

| Persona | Description | Key Need |
| :--- | :--- | :--- |
| **Online Shopper (Consumer)** | Everyday e-commerce consumer navigating retail sites | Quick, non-intrusive alert when countdowns or stock indicators are artificial |
| **Consumer Protection Auditor** | Regulatory or compliance officer auditing commercial sites | Granular audit reports with confidence scores, category breakdowns, and explainable evidence |
| **UI/UX Ethics Researcher** | Academic or designer studying deceptive interfaces | Multi-model performance comparisons, token saliency, and taxonomy distributions |

---

## 4. Deceptive Pattern Taxonomy

DarkShield AI categorizes dark patterns into standard recognized taxonomies:

```
                      ┌────────────────────────────┐
                      │    Deceptive UI Patterns   │
                      └─────────────┬──────────────┘
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
     ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
     │   Urgency   │         │  Scarcity   │         │Misdirection │
     └─────────────┘         └─────────────┘         └─────────────┘
            │                       │                       │
            ▼                       ▼                       ▼
     ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
     │Social Proof │         │ Obstruction │         │  Sneaking   │
     └─────────────┘         └─────────────┘         └─────────────┘
```

1. **Urgency:** Imposes artificial time pressure (e.g., *"Limited time offer"*, *"Offer expires in 05:00"*).
2. **Scarcity:** Signals high demand or limited availability (e.g., *"Only 3 left in stock"*, *"High demand"*).
3. **Misdirection:** Uses visual weight or manipulative language to steer choices (e.g., confirmshaming).
4. **Social Proof:** Displays real or synthetic peer activity (e.g., *"1,142 people added this to cart"*).
5. **Obstruction:** Creates friction when canceling subscriptions or opting out.
6. **Sneaking:** Conceals extra charges (drip pricing) or pre-selects checkboxes.

---

## 5. Scope & Functional Requirements

### 5.1 Web Application Dashboard
- **FR-1.1 Live URL Inspection:** User enters a URL; system uses headless Playwright DOM extraction to gather visible web content.
- **FR-1.2 Model Selection:** User can toggle between Logistic Regression, Linear SVM, LSTM, or GRU.
- **FR-1.3 Multi-Model Benchmark:** "Benchmark All" mode runs all 4 models in parallel and displays a side-by-side comparison table.
- **FR-1.4 Key Indicator Visualization:** Displays the top 5 SHAP token attributions with positive contribution weights.
- **FR-1.5 DOM Text Inspector:** Displays the cleaned, sanitized DOM text analyzed by the engine with one-click copy.
- **FR-1.6 Threat Level Meter:** High-contrast indicator classifying findings into Critical Deception (Confidence $\ge 80\%$), Moderate Concern ($50\% - 79\%$), or Verified Clean ($< 50\%$).

### 5.2 Browser Extension (Manifest V3)
- **FR-2.1 Instant Active Tab Capture:** One-click audit of current tab URL.
- **FR-2.2 Real-Time Badge Feedback:** Displays threat status and confidence percentage in the extension popup.
- **FR-2.3 Salient Token Chips:** Visualizes top detected manipulative words directly inside the popup.

### 5.3 MLOps & Model Pipeline
- **FR-3.1 Data Ingestion:** Stratified 80/20 train/test splitting preserving class proportions.
- **FR-3.2 Schema Validation:** Automated check against required columns (`text`, `label`) and valid binary ranges.
- **FR-3.3 Preprocessing Leakage Prevention:** Vectorizer fit strictly on training split; independent test transform.
- **FR-3.4 Systematic Hyperparameter Tuning:** Automated 5-fold cross-validated grid search for linear models and epoch/hidden-dim search for neural sequence models.
- **FR-3.5 Automated Model Pusher:** Pushes best-performing serialized weights (`.pkl`, `.pth`) directly to the production serving directory.

---

## 6. Non-Functional Requirements (NFRs)

- **NFR-1 Latency:** Linear inference (LR, SVM) must execute in $< 50\text{ ms}$; deep sequence models in $< 200\text{ ms}$.
- **NFR-2 Accuracy & Reliability:** Overall model F1-score must exceed $0.90$ across test split observations.
- **NFR-3 Explainability:** SHAP token attributions must reflect words physically present in the target document.
- **NFR-4 Security & Privacy:** Web scraping occurs in isolated headless browser contexts without persisting user session cookies or personal browsing history.
- **NFR-5 Availability:** FastAPI backend handles concurrent prediction requests via asynchronous event loops.

---

## 7. Success Metrics & Key Performance Indicators (KPIs)

| KPI | Target | Measured Result | Status |
| :--- | :---: | :---: | :---: |
| **Model F1-Score (Holdout Split)** | $\ge 90.0\%$ | **95.03%** (LSTM), **94.99%** (GRU) | ✅ Exceeded |
| **Model ROC-AUC** | $\ge 0.950$ | **0.9774** (GRU), **0.9750** (LR) | ✅ Exceeded |
| **DOM Analysis Turnaround** | $< 5.0\text{ s}$ | $1.2\text{ s} - 2.8\text{ s}$ | ✅ Met |
| **Unit Test Coverage** | $100\%$ critical paths | $5/5$ test suites passing | ✅ Met |
| **Web Build Size** | $< 500\text{ KB}$ gzip | $93.9\text{ KB}$ JS, $2.5\text{ KB}$ CSS | ✅ Met |

---

## 8. Release Roadmap

- **Milestone 1 (Foundations):** Raw corpus preparation, text normalization, initial TF-IDF baselines. *(Completed)*
- **Milestone 2 (Deep Learning & SHAP):** LSTM/GRU architectures, SHAP token attribution integration. *(Completed)*
- **Milestone 3 (MLOps Refactoring):** Modular component decoupling, automated pipeline orchestration, master notebook. *(Completed)*
- **Milestone 4 (Product Polish):** Sentinel Amber UI, custom vector favicons, Chrome extension Manifest V3. *(Completed)*
- **Milestone 5 (Future Vision):** Multi-lingual tokenization, transformer fine-tuning (DistilRoBERTa), user feedback loop.
