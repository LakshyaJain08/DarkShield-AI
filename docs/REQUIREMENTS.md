# 📋 DarkShield AI — Software & System Requirements

**Document Version:** 2.0.0  
**Target Environments:** Local Development Workstation, Production Linux Server, Docker Container  

---

## 1. Hardware Specifications

| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Processor (CPU)** | Dual-core x86_64 or Apple Silicon (2.0 GHz) | Quad-core or higher (Intel Core i5/i7, AMD Ryzen 5+, Apple M-series) |
| **Memory (RAM)** | 8 GB RAM | 16 GB RAM or higher |
| **Disk Storage** | 4 GB free disk space (models, datasets, Playwright Chromium binaries) | 10 GB SSD storage |
| **Graphics (GPU)** | Not required (CPU inference supported) | Optional: NVIDIA GPU with CUDA 11.8+ for accelerated neural training |

---

## 2. Operating System & Runtime Prerequisites

- **Supported Operating Systems:**
  - Microsoft Windows 10 / 11 (64-bit)
  - Linux (Ubuntu 20.04+, Debian 11+, RHEL 8+)
  - macOS (Monterey 12.0+ or newer)
- **Runtimes:**
  - **Python:** Version `3.10.x` or `3.11.x` (Recommended: Python 3.10.0+)
  - **Node.js:** Version `18.x` or `20.x` LTS
  - **Package Managers:** `pip >= 21.0`, `npm >= 9.0`

---

## 3. Python Package Dependency Matrix

| Package Name | Minimum Version | Purpose in DarkShield AI |
| :--- | :---: | :--- |
| `torch` | `>= 2.0.0` | Deep sequence neural models (LSTM, GRU), autograd, tensor ops |
| `scikit-learn` | `>= 1.3.0` | Classical classifiers (LogisticRegression, SVC), TF-IDF, GridSearchCV |
| `numpy` | `>= 1.24.0` | Array manipulation, vector math, SHAP attribution flattening |
| `pandas` | `>= 2.0.0` | Tabular data ingestion, schema manipulation, metric summaries |
| `shap` | `>= 0.45.0` | Model-agnostic feature attributions and token-level saliency |
| `fastapi` | `>= 0.100.0` | Asynchronous REST API framework for serving model predictions |
| `uvicorn` | `>= 0.23.0` | ASGI web server for FastAPI execution |
| `pydantic` | `>= 2.0.0` | Schema validation for HTTP request/response payloads |
| `playwright` | `>= 1.40.0` | Headless Chromium browser automation for dynamic DOM extraction |
| `pyyaml` | `>= 6.0` | Declarative pipeline configuration and schema parsing |
| `matplotlib` | `>= 3.7.0` | Visual plotting for ROC curves, confusion matrices, and loss curves |
| `seaborn` | `>= 0.12.0` | Statistical data visualization and dark-themed confusion matrix grids |
| `ipykernel` | `>= 6.20.0` | Jupyter interactive execution engine for master notebooks |
| `nbformat` | `>= 5.9.0` | Programmatic notebook creation and manipulation |
| `pytest` | `>= 7.4.0` | Automated testing framework for schema and inference validation |

---

## 4. Frontend & Browser Extension Dependencies

| Package / Technology | Version | Purpose |
| :--- | :---: | :--- |
| `react` | `^19.0.0` | Component-based UI library for web intelligence dashboard |
| `react-dom` | `^19.0.0` | Virtual DOM rendering for React |
| `vite` | `^8.3.0` | Next-generation frontend build tool and local dev server |
| `lucide-react` | `^1.16.0` | SVG iconography (Shield, Zap, Layers, Cpu, etc.) |
| `axios` | `^1.7.0` | Promise-based HTTP client for FastAPI backend communication |
| `Chrome Extensions API` | `Manifest V3` | Browser extension permissions (`activeTab`, `scripting`) |

---

## 5. Network & Port Allocations

| Port | Service / Component | Protocol | Description |
| :---: | :--- | :---: | :--- |
| `8000` | FastAPI Backend Server | HTTP / TCP | Live API server handling `/analyze/url`, `/analyze/all` |
| `5173` | React Frontend Dashboard | HTTP / TCP | Vite development server for web UI |
| `8001` | Standalone App Model API | HTTP / TCP | Optional isolated model serving container |

---

## 6. Installation & Verification Guide

### Step 1: Clone and Create Virtual Environment
```bash
# Clone the repository
git clone <repository-url>
cd "Black Pattern Detection"

# Create Python virtual environment
python -m venv backend/venv

# Activate virtual environment (Windows PowerShell)
.\backend\venv\Scripts\Activate.ps1

# Activate virtual environment (Linux/macOS)
source backend/venv/bin/activate
```

### Step 2: Install Python Dependencies & Playwright Browsers
```bash
pip install -r requirements.txt
playwright install chromium
```

### Step 3: Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### Step 4: Run Automated Verification Suite
```bash
python -m pytest tests/
```
All unit tests should report `PASSED`.
