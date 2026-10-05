from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.scraper import scrape_page
from services.ocr import extract_text_from_image
from ml.inference import predict_and_explain
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="DarkShield AI Backend")

# Allow CORS for the frontend and extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str
    model: str = "logistic_regression"

@app.post("/analyze/url")
def analyze_url(request: URLRequest):
    try:
        # 1. Scrape text and candidate UI snippets directly from web page via Playwright DOM extraction
        text, snippets, screenshot_bytes = scrape_page(request.url)
        if not text or not text.strip():
            return {"status": "error", "message": "No text found on the page."}
        
        # 2. Predict and Explain with calibrated element-level detection
        result = predict_and_explain(text, request.model, elements=snippets)
        return {"status": "success", "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/all")
def analyze_all(request: URLRequest):
    try:
        # Scrape text and candidate UI snippets once
        text, snippets, screenshot_bytes = scrape_page(request.url)
        if not text or not text.strip():
            return {"status": "error", "message": "No text found on the page."}
        
        models = ['logistic_regression', 'svm', 'lstm', 'gru']
        results = {}
        for m in models:
            results[m] = predict_and_explain(text, m, elements=snippets)
            
        return {"status": "success", "text": text, "models": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...), model: str = Form("logistic_regression")):
    try:
        image_bytes = await file.read()
        
        # 1. Extract Text
        text = extract_text_from_image(image_bytes)
        if not text.strip():
            return {"status": "error", "message": "No text found in the image."}
        
        # 2. Predict and Explain
        result = predict_and_explain(text, model)
        return {"status": "success", "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
