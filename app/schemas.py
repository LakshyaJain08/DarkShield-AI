from pydantic import BaseModel, Field
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Text content or DOM extract to analyze")
    model: str = Field("logistic_regression", description="Model architecture: logistic_regression, svm, lstm, gru")

class TokenContribution(BaseModel):
    word: str
    contribution: float

class PredictionResponse(BaseModel):
    text: str
    model: str
    is_dark_pattern: bool
    confidence: float
    explanation: List[TokenContribution] = []

class URLAnalyzeRequest(BaseModel):
    url: str
    model: str = "logistic_regression"
