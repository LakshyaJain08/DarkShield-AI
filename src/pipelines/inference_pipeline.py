import os
import torch
import numpy as np
from pathlib import Path
from src.utils.logger import get_logger
from src.utils.config_loader import get_project_root, load_config
from src.utils.common import load_object, load_torch_model
from src.components.feature_engineering import DeepSequenceModel
from src.components.data_transformation import clean_text

logger = get_logger(__name__)

class InferencePipeline:
    """Production inference pipeline loading trained models and performing predictions."""
    
    def __init__(self, models_dir: str = None):
        self.root = get_project_root()
        if models_dir:
            self.models_dir = Path(models_dir)
        else:
            # Prefer backend/models if exists, else models/
            prod_dir = self.root / "backend" / "models"
            if prod_dir.exists() and (prod_dir / "vectorizer.pkl").exists():
                self.models_dir = prod_dir
            else:
                self.models_dir = self.root / "models"
                
        self._load_artifacts()

    def _load_artifacts(self):
        """Loads vectorizer and model weights into memory."""
        logger.info(f"Loading inference artifacts from: {self.models_dir}")
        self.vectorizer = load_object(self.models_dir / "vectorizer.pkl")
        self.input_dim = len(self.vectorizer.get_feature_names_out())
        
        # Classical Models
        self.lr_model = load_object(self.models_dir / "logistic_regression.pkl")
        self.svm_model = load_object(self.models_dir / "svm.pkl")
        
        # Deep Learning Models (Dynamically load hidden dimension from checkpoints)
        lstm_weights = torch.load(self.models_dir / "lstm.pth", map_location=torch.device("cpu"))
        lstm_hdim = lstm_weights["fc1.weight"].shape[0]
        self.lstm_model = DeepSequenceModel(self.input_dim, hidden_dim=lstm_hdim, model_type="LSTM")
        self.lstm_model.load_state_dict(lstm_weights)
        self.lstm_model.eval()
        
        gru_weights = torch.load(self.models_dir / "gru.pth", map_location=torch.device("cpu"))
        gru_hdim = gru_weights["fc1.weight"].shape[0]
        self.gru_model = DeepSequenceModel(self.input_dim, hidden_dim=gru_hdim, model_type="GRU")
        self.gru_model.load_state_dict(gru_weights)
        self.gru_model.eval()
        logger.info(f"All model artifacts loaded successfully (LSTM hdim={lstm_hdim}, GRU hdim={gru_hdim}).")

    def predict(self, text: str, model_name: str = "logistic_regression") -> dict:
        """Runs inference for a given text snippet with selected model."""
        cleaned = clean_text(text)
        X = self.vectorizer.transform([cleaned]).toarray()
        
        if model_name == "logistic_regression":
            probs = self.lr_model.predict_proba(X)[0]
            confidence = float(probs[1])
            is_dark = bool(self.lr_model.predict(X)[0])
        elif model_name == "svm":
            probs = self.svm_model.predict_proba(X)[0]
            confidence = float(probs[1])
            is_dark = bool(self.svm_model.predict(X)[0])
        elif model_name == "lstm":
            with torch.no_grad():
                out = self.lstm_model(torch.tensor(X, dtype=torch.float32)).item()
            confidence = float(out)
            is_dark = confidence >= 0.5
        elif model_name == "gru":
            with torch.no_grad():
                out = self.gru_model(torch.tensor(X, dtype=torch.float32)).item()
            confidence = float(out)
            is_dark = confidence >= 0.5
        else:
            raise ValueError(f"Unknown model name: {model_name}")

        return {
            "text": text,
            "cleaned_text": cleaned,
            "model": model_name,
            "is_dark_pattern": is_dark,
            "confidence": confidence
        }
