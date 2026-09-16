import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Ensure root is on path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.pipelines.prediction_pipeline import PredictionPipeline
from app.schemas import AnalyzeRequest, PredictionResponse

app = FastAPI(title="DarkShield AI - Model Serving API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = PredictionPipeline()

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "DarkShield AI Serving API", "version": "2.0.0"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: AnalyzeRequest):
    try:
        result = pipeline.predict_with_explanation(request.text, model_name=request.model)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8001, reload=True)
