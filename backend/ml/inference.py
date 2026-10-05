import os
import sys
from pathlib import Path

# Add project root to sys.path to ensure src is importable
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from src.pipelines.prediction_pipeline import PredictionPipeline
    pipeline = PredictionPipeline()
    
    def predict_and_explain(text, model_name='logistic_regression', elements=None):
        return pipeline.predict_with_explanation(text, model_name, elements=elements)
except Exception as e:
    # Graceful fallback to standalone logic if src is unavailable
    import pickle
    import torch
    import shap
    import numpy as np
    from .train import DeepSequenceModel

    MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))

    with open(os.path.join(MODELS_DIR, 'vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle.load(f)

    with open(os.path.join(MODELS_DIR, 'logistic_regression.pkl'), 'rb') as f:
        lr_model = pickle.load(f)

    with open(os.path.join(MODELS_DIR, 'svm.pkl'), 'rb') as f:
        svm_model = pickle.load(f)

    input_dim = len(vectorizer.get_feature_names_out())
    lstm_weights = torch.load(os.path.join(MODELS_DIR, 'lstm.pth'), map_location='cpu')
    lstm_hdim = lstm_weights['fc1.weight'].shape[0]
    lstm_model = DeepSequenceModel(input_dim, lstm_hdim, 'LSTM')
    lstm_model.load_state_dict(lstm_weights)
    lstm_model.eval()

    gru_weights = torch.load(os.path.join(MODELS_DIR, 'gru.pth'), map_location='cpu')
    gru_hdim = gru_weights['fc1.weight'].shape[0]
    gru_model = DeepSequenceModel(input_dim, gru_hdim, 'GRU')
    gru_model.load_state_dict(gru_weights)
    gru_model.eval()

    def predict_and_explain(text, model_name='logistic_regression'):
        X = vectorizer.transform([text]).toarray()
        confidence = 0.0
        is_dark_pattern = False

        if model_name == 'logistic_regression':
            probs = lr_model.predict_proba(X)[0]
            confidence = float(probs[1])
            is_dark_pattern = bool(lr_model.predict(X)[0])
            explainer = shap.LinearExplainer(lr_model, X, feature_perturbation="interventional")
            shap_values = explainer.shap_values(X)
        elif model_name == 'svm':
            probs = svm_model.predict_proba(X)[0]
            confidence = float(probs[1])
            is_dark_pattern = bool(svm_model.predict(X)[0])
            coef = svm_model.coef_[0]
            shap_values = coef * X[0]
        elif model_name in ['lstm', 'gru']:
            model = lstm_model if model_name == 'lstm' else gru_model
            X_t = torch.tensor(X, dtype=torch.float32)
            with torch.no_grad():
                output = model(X_t).item()
            confidence = float(output)
            is_dark_pattern = confidence > 0.5
            explainer = shap.DeepExplainer(model, torch.zeros((1, X.shape[1]), dtype=torch.float32))
            shap_values = explainer.shap_values(X_t)
        
        feature_names = vectorizer.get_feature_names_out()
        sv = np.array(shap_values).flatten()
        present_indices = np.where(X[0] > 0)[0]

        if len(present_indices) > 0:
            present_scores = sv[present_indices]
            top_present = present_indices[np.argsort(present_scores)[-5:]][::-1]
            explanation = [
                {"word": str(feature_names[i]).strip("[]'\""), "contribution": float(sv[i])}
                for i in top_present if sv[i] > 0
            ]
        else:
            top_indices = np.argsort(sv)[-5:][::-1]
            explanation = [
                {"word": str(feature_names[i]).strip("[]'\""), "contribution": float(sv[i])}
                for i in top_indices if sv[i] > 0
            ]
        
        return {
            "text": text,
            "is_dark_pattern": is_dark_pattern,
            "confidence": confidence,
            "explanation": explanation
        }

