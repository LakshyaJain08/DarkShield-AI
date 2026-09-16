import os
import torch
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    classification_report
)

from src.utils.logger import get_logger
from src.utils.config_loader import load_config, get_project_root
from src.utils.common import save_json, ensure_dir

logger = get_logger(__name__)

class ModelEvaluation:
    """Component to rigorously evaluate models, calculate metrics, and generate comparative plots."""
    
    def __init__(self, config: dict = None):
        self.config = config or load_config()
        self.root = get_project_root()
        self.eval_cfg = self.config["model_evaluation"]
        
        self.metrics_output_path = self.root / self.eval_cfg.get("metrics_output_path", "outputs/metrics.json")
        self.cm_path = self.root / self.eval_cfg.get("confusion_matrix_path", "outputs/confusion_matrices.png")
        self.roc_path = self.root / self.eval_cfg.get("roc_curve_path", "outputs/roc_curves.png")
        
        ensure_dir(self.metrics_output_path.parent)

    def _get_predictions_and_probs(self, model, X: np.ndarray, model_name: str) -> tuple[np.ndarray, np.ndarray]:
        """Extracts class predictions and positive class probabilities across model paradigms."""
        if model_name in ["logistic_regression", "svm"]:
            preds = model.predict(X)
            probs = model.predict_proba(X)[:, 1]
        elif model_name in ["lstm", "gru"]:
            model.eval()
            with torch.no_grad():
                X_t = torch.tensor(X, dtype=torch.float32)
                raw_out = model(X_t).squeeze(1).cpu().numpy()
                probs = raw_out
                preds = (raw_out >= 0.5).astype(int)
        else:
            raise ValueError(f"Unknown model name: {model_name}")
            
        return preds, probs

    def evaluate_all(self, trained_models: dict, X_test: np.ndarray, y_test: np.ndarray) -> tuple[pd.DataFrame, dict]:
        """Evaluates all trained models, computes comparative metrics, and saves visual plots."""
        logger.info("=== [STAGE 5: MODEL EVALUATION] Starting Comprehensive Model Evaluation ===")
        
        results = {}
        table_rows = []
        predictions_dict = {}
        probs_dict = {}
        
        for name, data in trained_models.items():
            model = data["model"]
            preds, probs = self._get_predictions_and_probs(model, X_test, name)
            
            predictions_dict[name] = preds
            probs_dict[name] = probs
            
            acc = float(accuracy_score(y_test, preds))
            prec = float(precision_score(y_test, preds, zero_division=0))
            rec = float(recall_score(y_test, preds, zero_division=0))
            f1 = float(f1_score(y_test, preds, zero_division=0))
            auc = float(roc_auc_score(y_test, probs))
            
            results[name] = {
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1_score": f1,
                "roc_auc": auc,
                "tuning_meta": data.get("meta", {})
            }
            
            table_rows.append({
                "Model": name.upper(),
                "Accuracy": f"{acc:.4f}",
                "Precision": f"{prec:.4f}",
                "Recall": f"{rec:.4f}",
                "F1-Score": f"{f1:.4f}",
                "ROC-AUC": f"{auc:.4f}"
            })
            
            logger.info(f"Model {name.upper()}: Acc={acc:.4f} | Prec={prec:.4f} | Rec={rec:.4f} | F1={f1:.4f} | AUC={auc:.4f}")

        # Save metrics json
        save_json(self.metrics_output_path, results)
        summary_df = pd.DataFrame(table_rows)

        # 1. Plot Confusion Matrices
        self._plot_confusion_matrices(predictions_dict, y_test)

        # 2. Plot ROC Curves
        self._plot_roc_curves(probs_dict, y_test)
        
        logger.info("=== [STAGE 5: MODEL EVALUATION] Completed Successfully ===")
        return summary_df, results

    def _plot_confusion_matrices(self, predictions_dict: dict, y_test: np.ndarray) -> None:
        """Generates and saves 2x2 grid of confusion matrices."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.patch.set_facecolor("#121214")
        axes = axes.flatten()
        
        labels = ["Benign (0)", "Dark Pattern (1)"]
        colors = ["#3b82f6", "#10b981", "#f59e0b", "#ec4899"]
        
        for idx, (model_name, preds) in enumerate(predictions_dict.items()):
            ax = axes[idx]
            cm = confusion_matrix(y_test, preds)
            
            # Dark theme styling
            ax.set_facecolor("#18181b")
            sns.heatmap(
                cm,
                annot=True,
                fmt="d",
                cmap="Blues" if idx % 2 == 0 else "YlOrBr",
                cbar=False,
                xticklabels=labels,
                yticklabels=labels,
                ax=ax,
                annot_kws={"size": 14, "weight": "bold"}
            )
            ax.set_title(f"{model_name.upper()} Confusion Matrix", color="#f4f4f5", fontsize=14, pad=12)
            ax.set_xlabel("Predicted Label", color="#a1a1aa", fontsize=11)
            ax.set_ylabel("True Label", color="#a1a1aa", fontsize=11)
            ax.tick_params(colors="#a1a1aa")
            
        plt.tight_layout()
        plt.savefig(self.cm_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
        plt.close()
        logger.info(f"Saved Confusion Matrices plot to: {self.cm_path}")

    def _plot_roc_curves(self, probs_dict: dict, y_test: np.ndarray) -> None:
        """Generates and saves comparative ROC curve plot."""
        plt.figure(figsize=(9, 7))
        plt.gcf().patch.set_facecolor("#121214")
        ax = plt.gca()
        ax.set_facecolor("#18181b")
        
        colors = {
            "logistic_regression": "#3b82f6",
            "svm": "#10b981",
            "lstm": "#f59e0b",
            "gru": "#ec4899"
        }
        
        for name, probs in probs_dict.items():
            fpr, tpr, _ = roc_curve(y_test, probs)
            auc_val = roc_auc_score(y_test, probs)
            plt.plot(fpr, tpr, label=f"{name.upper()} (AUC = {auc_val:.4f})", color=colors.get(name, "#ffffff"), lw=2.2)
            
        plt.plot([0, 1], [0, 1], "k--", color="#71717a", lw=1.5, label="Random Guess (AUC = 0.50)")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate (1 - Specificity)", color="#a1a1aa", fontsize=12)
        plt.ylabel("True Positive Rate (Sensitivity)", color="#a1a1aa", fontsize=12)
        plt.title("Comparative ROC Curves (All Models)", color="#f4f4f5", fontsize=15, pad=14)
        plt.legend(loc="lower right", facecolor="#27272a", edgecolor="#3f3f46", labelcolor="#f4f4f5")
        plt.grid(True, linestyle="--", alpha=0.25, color="#52525b")
        ax.tick_params(colors="#a1a1aa")
        
        plt.tight_layout()
        plt.savefig(self.roc_path, dpi=300, facecolor=plt.gcf().get_facecolor(), bbox_inches="tight")
        plt.close()
        logger.info(f"Saved ROC curves plot to: {self.roc_path}")
