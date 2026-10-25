import pytest
import pandas as pd
import numpy as np
from src.components.data_validation import DataValidation
from src.components.feature_engineering import LinguisticFeatureExtractor

def test_data_validation_valid():
    validator = DataValidation()
    df = pd.DataFrame({
        "page_id": [1, 2],
        "text": ["Hurry only 2 left in stock!", "Welcome to our store"],
        "label": [1, 0],
        "Pattern Category": ["Scarcity", "Not Dark Pattern"]
    })
    report = validator.validate_dataframe(df, "TestSample")
    assert report["status"] is True
    assert len(report["errors"]) == 0

def test_data_validation_missing_col():
    validator = DataValidation()
    df = pd.DataFrame({
        "text": ["Sample text only"]
    })
    report = validator.validate_dataframe(df, "InvalidSample")
    assert report["status"] is False
    assert any("label" in err for err in report["errors"])

def test_data_validation_invalid_label():
    validator = DataValidation()
    df = pd.DataFrame({
        "text": ["Sample text"],
        "label": [99]
    })
    report = validator.validate_dataframe(df, "InvalidLabelSample")
    assert report["status"] is False
    assert any("invalid label" in err.lower() for err in report["errors"])

def test_data_validation_conflicting_labels():
    validator = DataValidation()
    df = pd.DataFrame({
        "text": ["Exclusive deal ends soon", "Exclusive deal ends soon"],
        "label": [1, 0]
    })
    report = validator.validate_dataframe(df, "ConflictingSample")
    assert report["status"] is False
    assert report["conflicting_labels"] == 1
    assert any("conflicting labels" in err.lower() for err in report["errors"])

def test_linguistic_feature_extractor():
    extractor = LinguisticFeatureExtractor()
    texts = [
        "Hurry! ONLY 2 items remaining in stock at $19.99! Claim now!",
        "Contact customer service for more information."
    ]
    features = extractor.transform(texts)
    assert isinstance(features, np.ndarray)
    assert features.shape == (2, 15)
    
    # Feature 0: char_count
    assert features[0, 0] > 0
    # Feature 8: has_number (1st text has 2 and 19.99, 2nd has none)
    assert features[0, 8] == 1.0
    assert features[1, 8] == 0.0
    # Feature 9: has_currency ($ in 1st text)
    assert features[0, 9] == 1.0
    assert features[1, 9] == 0.0
    # Feature 14: total_cues
    assert features[0, 14] > 0.0
    assert len(extractor.get_feature_names_out()) == 15
