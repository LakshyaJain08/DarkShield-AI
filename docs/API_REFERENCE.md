# 📡 DarkShield AI — REST API Reference Specification

**Base URL:** `http://127.0.0.1:8000` (FastAPI Server)  
**API Version:** 2.0.0  
**Format:** JSON  
**Authentication:** Open (Local / Internal Prototype)  

---

## 1. Endpoints Overview

| Method | Endpoint | Description | Typical Latency |
| :---: | :--- | :--- | :---: |
| `GET` | `/` | Health check & service readiness | $< 5\text{ ms}$ |
| `POST` | `/analyze/url` | Scrapes target URL via Playwright DOM extraction and runs specified model | $1.2\text{ s} - 2.8\text{ s}$ |
| `POST` | `/analyze/all` | Scrapes URL once and evaluates all 4 models in parallel | $1.5\text{ s} - 3.2\text{ s}$ |
| `POST` | `/analyze/image` | Accepts image upload, performs OCR, and classifies extracted text | $2.0\text{ s} - 4.5\text{ s}$ |
| `POST` | `/predict` | Direct raw text classification with SHAP token attribution | $< 50\text{ ms}$ |

---

## 2. Endpoint Specifications

### 2.1 Health Check
- **URL:** `GET /`
- **Response:**
  ```json
  {
    "status": "healthy",
    "service": "DarkShield AI Backend",
    "version": "2.0.0"
  }
  ```

---

### 2.2 Live URL Analysis (Single Model)
Scrapes visible DOM text from the target web page using headless Playwright Chromium and classifies it using the requested machine learning model.

- **URL:** `POST /analyze/url`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "url": "https://www.amazon.in/dp/B01MZ9GNNN",
    "model": "logistic_regression"
  }
  ```
  *Parameters:*
  - `url` *(string, required)*: Fully qualified HTTP/HTTPS web page URL.
  - `model` *(string, optional, default: `"logistic_regression"`)*: One of `logistic_regression`, `svm`, `lstm`, `gru`.

- **Success Response (HTTP 200):**
  ```json
  {
    "status": "success",
    "data": {
      "text": "FLASH SALE | LIMITED TIME ONLY! Hurry, only 2 left in stock!",
      "cleaned_text": "flash sale limited time only! hurry only 2 left in stock!",
      "model": "logistic_regression",
      "is_dark_pattern": true,
      "confidence": 0.9954,
      "explanation": [
        { "word": "left", "contribution": 1.9729 },
        { "word": "stock", "contribution": 1.0907 },
        { "word": "items", "contribution": 1.0634 },
        { "word": "order", "contribution": 0.8739 },
        { "word": "sale", "contribution": 0.7795 }
      ]
    }
  }
  ```

---

### 2.3 Multi-Model URL Benchmark
Scrapes the target page once and runs all four model architectures in parallel, allowing instant side-by-side agreement analysis.

- **URL:** `POST /analyze/all`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "url": "https://www.booking.com/hotel/us/times-square.html",
    "model": "all"
  }
  ```

- **Success Response (HTTP 200):**
  ```json
  {
    "status": "success",
    "text": "In high demand! 1,200 people booked this room in the last 24 hours.",
    "models": {
      "logistic_regression": {
        "is_dark_pattern": true,
        "confidence": 0.9821,
        "explanation": [
          { "word": "demand", "contribution": 1.452 },
          { "word": "booked", "contribution": 0.891 }
        ]
      },
      "svm": {
        "is_dark_pattern": true,
        "confidence": 0.9785,
        "explanation": [
          { "word": "demand", "contribution": 1.341 }
        ]
      },
      "lstm": {
        "is_dark_pattern": true,
        "confidence": 0.9912,
        "explanation": [
          { "word": "demand", "contribution": 0.124 }
        ]
      },
      "gru": {
        "is_dark_pattern": true,
        "confidence": 0.9934,
        "explanation": [
          { "word": "demand", "contribution": 0.131 }
        ]
      }
    }
  }
  ```

---

### 2.4 Raw Text Prediction (Direct API)
- **URL:** `POST /predict`
- **Request Body:**
  ```json
  {
    "text": "Flash sale ends in 5 minutes! Only 1 seat remaining.",
    "model": "svm"
  }
  ```
- **Success Response (HTTP 200):**
  ```json
  {
    "text": "Flash sale ends in 5 minutes! Only 1 seat remaining.",
    "model": "svm",
    "is_dark_pattern": true,
    "confidence": 0.989,
    "explanation": [
      { "word": "flash", "contribution": 1.251 },
      { "word": "sale", "contribution": 0.982 },
      { "word": "remaining", "contribution": 0.871 }
    ]
  }
  ```

---

## 3. Error Handling & HTTP Status Codes

| HTTP Code | Reason | Example Response Body |
| :---: | :--- | :--- |
| `400 Bad Request` | Malformed parameters or empty text | `{"status": "error", "message": "No text found on the page."}` |
| `422 Unprocessable` | Pydantic schema validation failure | `{"detail": [{"loc": ["body", "url"], "msg": "field required", "type": "value_error.missing"}]}` |
| `500 Server Error` | Scraper network timeout or inference error | `{"detail": "Navigation timeout of 30000ms exceeded"}` |

---

## 4. Code Invocation Examples

### Python (`requests`)
```python
import requests

payload = {
    "url": "https://www.amazon.in/dp/B01MZ9GNNN",
    "model": "logistic_regression"
}

response = requests.post("http://127.0.0.1:8000/analyze/url", json=payload)
data = response.json()
print("Dark Pattern Detected:", data["data"]["is_dark_pattern"])
print("Confidence:", data["data"]["confidence"])
```

### cURL
```bash
curl -X POST "http://127.0.0.1:8000/analyze/url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com", "model": "logistic_regression"}'
```
