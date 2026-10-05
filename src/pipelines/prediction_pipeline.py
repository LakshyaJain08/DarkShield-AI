import re
import numpy as np
import torch
import shap
from src.utils.logger import get_logger
from src.components.data_transformation import clean_text
from .inference_pipeline import InferencePipeline

logger = get_logger(__name__)

STRONG_DARK_PATTERNS = [
    (r"\b(?:hurry|act now|limited time|deal of the day|lightning deal|expires in|ends in)\b", "Urgency / Deal Pressure"),
    (r"\bonly\s+\d+\s+left\b|\b\d+\s+left in stock\b|\blast chance\b|\blow stock\b", "Artificial Scarcity"),
    (r"\bno thanks[,\s]+i (?:don't|hate|prefer|like)\b|\bno,\s*i want to pay\b", "Confirmshaming"),
    (r"\bsubscribe\s*&\s*save\b|\bauto-deliver\b|\bcontinuous subscription\b", "Subscription Trap / Forced Continuity"),
    (r"\border within\b.*\bto get it\b|\bclaimed\s*\d+%\b", "Countdown / Claimed Pressure"),
    (r"\b\d+\s+people (?:are viewing|bought|have this in their cart)\b", "Artificial Social Proof"),
    (r"\bm\.?r\.?p\.?:?\s*(?:₹|\$|rs\.?)\s*\d+.*save\s+\d+%", "Reference Price Anchoring")
]

class PredictionPipeline:
    """Production prediction pipeline that delivers calibrated predictions paired with SHAP explainability."""
    
    def __init__(self, models_dir: str = None, vectorizer = None):
        self.inference = InferencePipeline(models_dir)
        if vectorizer is not None:
            self.vectorizer = vectorizer
            self.inference.vectorizer = vectorizer
        else:
            self.vectorizer = self.inference.vectorizer
            
        self.feature_names = self.vectorizer.get_feature_names_out()

    def predict_with_explanation(self, text: str, model_name: str = "logistic_regression", elements: list = None) -> dict:
        """Computes prediction and SHAP token attributions using element-level granular scanning when available."""
        # If discrete candidate UI snippets are provided, run calibrated element-level detection
        if elements and len(elements) > 0:
            cleaned_snippets = [clean_text(s) for s in elements]
            X_snips = self.vectorizer.transform(cleaned_snippets).toarray()
            
            if model_name == "logistic_regression":
                probs = self.inference.lr_model.predict_proba(X_snips)[:, 1]
            elif model_name == "svm":
                probs = self.inference.svm_model.predict_proba(X_snips)[:, 1]
            elif model_name == "lstm":
                with torch.no_grad():
                    out = self.inference.lstm_model(torch.tensor(X_snips, dtype=torch.float32)).numpy()
                probs = np.array(out).flatten()
            elif model_name == "gru":
                with torch.no_grad():
                    out = self.inference.gru_model(torch.tensor(X_snips, dtype=torch.float32)).numpy()
                probs = np.array(out).flatten()
            else:
                probs = np.zeros(len(elements))
                
            flagged = []
            for idx, p in enumerate(probs):
                snippet_text = elements[idx]
                matched_category = None
                for pattern, cat in STRONG_DARK_PATTERNS:
                    if re.search(pattern, snippet_text, re.IGNORECASE):
                        matched_category = cat
                        break
                        
                # High-precision verification rule:
                # Element must have model confidence >= 75% AND match an established deceptive taxonomy pattern
                if p >= 0.75 and matched_category:
                    flagged.append({
                        "text": snippet_text,
                        "confidence": float(p),
                        "category": matched_category
                    })
                    
            flagged.sort(key=lambda x: x["confidence"], reverse=True)
            is_dark = len(flagged) > 0
            
            if is_dark:
                confidence = float(np.mean([el["confidence"] for el in flagged[:5]]))
                focus_text = flagged[0]["text"]
            else:
                confidence = float(min(probs)) if len(probs) > 0 else 0.005
                focus_text = text[:300]
                
            # Compute SHAP explanation on the focal text snippet
            explanation = self._explain_snippet(focus_text, model_name) if is_dark else []
            
            return {
                "text": text,
                "cleaned_text": clean_text(text),
                "model": model_name,
                "is_dark_pattern": is_dark,
                "confidence": confidence,
                "flagged_elements": flagged,
                "explanation": explanation
            }
            
        # Single snippet fallback
        base_result = self.inference.predict(text, model_name)
        base_result["flagged_elements"] = []
        base_result["explanation"] = self._explain_snippet(base_result["cleaned_text"], model_name)
        return base_result

    def _explain_snippet(self, text: str, model_name: str) -> list:
        cleaned = clean_text(text)
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
            
        return explanation

