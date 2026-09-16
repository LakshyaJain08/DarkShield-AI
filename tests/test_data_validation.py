import pytest
import pandas as pd
from src.components.data_validation import DataValidation

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
