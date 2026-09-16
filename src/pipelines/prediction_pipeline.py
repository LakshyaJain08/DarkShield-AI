import numpy as np
import torch
import shap
from src.utils.logger import get_logger
from .inference_pipeline import InferencePipeline

logger = get_logger(__name__)

class PredictionPipeline:
    """Production prediction pipeline that delivers predictions paired with SHAP explainability."""
    
    def __init__(self, models_dir: str = None, vectorizer = None):
        self.inference = InferencePipeline(models_dir)
        if vectorizer is not None:
            self.vectorizer = vectorizer
            self.inference.vectorizer = vectorizer
        else:
            self.vectorizer = self.inference.vectorizer
            
        self.feature_names = self.vectorizer.get_feature_names_out()

    def predict_with_explanation(self, text: str, model_name: str = "logistic_regression") -> dict:
        """Computes prediction and SHAP token attributions for interpretable detection."""
        base_result = self.inference.predict(text, model_name)
        cleaned = base_result["cleaned_text"]
        X = self.vectorizer.transform([cleaned]).toarray()
        
        explanation = []
        try:
            if model_name == "logistic_regression":
                coef = self.inference.lr_model.coef_[0]
                sv = (coef * X[0]).flatten()
                
            elif model_name == "svm":
                coef = self.inference.svm_model.coef_[0]
                sv = (coef * X[0]).flatten()
                
            elif model_name in ["lstm", "gru"]:
                model = self.inference.lstm_model if model_name == "lstm" else self.inference.gru_model
                explainer = shap.DeepExplainer(model, torch.zeros((1, X.shape[1]), dtype=torch.float32))
                X_t = torch.tensor(X, dtype=torch.float32)
                try:
                    shap_values = explainer.shap_values(X_t, check_additivity=False)
                except TypeError:
                    shap_values = explainer.shap_values(X_t)
                sv = np.array(shap_values).flatten()
            else:
                sv = np.zeros(X.shape[1])

            # Present words filter (words that appear in the document)
            present_indices = np.where(X[0] > 0)[0]
            if len(present_indices) > 0:
                present_scores = sv[present_indices]
                top_present = present_indices[np.argsort(present_scores)[-5:]][::-1]
                explanation = [
                    {"word": str(self.feature_names[i]).strip("[]'\""), "contribution": float(sv[i])}
                    for i in top_present if sv[i] > 0
                ]
            else:
                top_indices = np.argsort(sv)[-5:][::-1]
                explanation = [
                    {"word": str(self.feature_names[i]).strip("[]'\""), "contribution": float(sv[i])}
                    for i in top_indices if sv[i] > 0
                ]
        except Exception as e:
            logger.warning(f"Error extracting SHAP explanation: {e}")
            explanation = []

        base_result["explanation"] = explanation
        return base_result
