import pytest
from src.pipelines.prediction_pipeline import PredictionPipeline

def test_prediction_pipeline():
    pipeline = PredictionPipeline()
    
    # 1. Dark pattern sample
    dark_sample = "FLASH SALE! Limited time only. Hurry, only 1 left in stock!"
    res_dark = pipeline.predict_with_explanation(dark_sample, model_name="logistic_regression")
    assert res_dark["is_dark_pattern"] is True
    assert res_dark["confidence"] > 0.5
    assert len(res_dark["explanation"]) > 0

    # 2. Benign sample
    benign_sample = "Standard cotton t-shirt with crew neck and short sleeves."
    res_benign = pipeline.predict_with_explanation(benign_sample, model_name="logistic_regression")
    assert res_benign["is_dark_pattern"] is False
    assert res_benign["confidence"] < 0.5

def test_all_models_inference():
    pipeline = PredictionPipeline()
    sample = "Sale ends in 5 minutes! 400 people are viewing this."
    
    for model_name in ["logistic_regression", "svm", "lstm", "gru"]:
        res = pipeline.predict_with_explanation(sample, model_name=model_name)
        assert "confidence" in res
        assert 0.0 <= res["confidence"] <= 1.0
        assert isinstance(res["is_dark_pattern"], bool)
