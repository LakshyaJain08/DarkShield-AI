import os
import copy
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score, accuracy_score

from src.utils.logger import get_logger
from src.utils.config_loader import load_config, get_project_root
from src.utils.common import save_object, save_torch_model, ensure_dir
from .feature_engineering import DeepSequenceModel, FeatureEngineering

logger = get_logger(__name__)

class ModelTrainer:
    """Component to execute systematic hyperparameter tuning for classical and deep learning models."""
    
    def __init__(self, config: dict = None):
        self.config = config or load_config()
        self.root = get_project_root()
        self.trainer_cfg = self.config["model_trainer"]
        self.models_dir = self.root / self.trainer_cfg.get("models_dir", "models")
        ensure_dir(self.models_dir)

    def tune_logistic_regression(self, X_train: np.ndarray, y_train: np.ndarray) -> tuple[LogisticRegression, dict]:
        """Performs 5-fold cross-validated grid search for Logistic Regression."""
        logger.info("--> [Tuning Logistic Regression] Starting GridSearchCV...")
        param_grid = self.trainer_cfg["logistic_regression"]["param_grid"]
        
        base_model = LogisticRegression(random_state=42)
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            cv=5,
            scoring="f1",
            n_jobs=-1,
            verbose=0
        )
        grid_search.fit(X_train, y_train)
        
        best_lr = grid_search.best_estimator_
        best_params = grid_search.best_params_
        best_score = grid_search.best_score_
        
        logger.info(f"Logistic Regression Best F1: {best_score:.4f} with params: {best_params}")
        
        # Save to models directory
        save_path = self.models_dir / "logistic_regression.pkl"
        save_object(save_path, best_lr)
        
        return best_lr, {"params": best_params, "cv_f1": float(best_score)}

    def tune_svm(self, X_train: np.ndarray, y_train: np.ndarray) -> tuple[SVC, dict]:
        """Performs 5-fold cross-validated grid search for Support Vector Machine."""
        logger.info("--> [Tuning SVM] Starting GridSearchCV...")
        param_grid = self.trainer_cfg["svm"]["param_grid"]
        
        base_model = SVC(random_state=42)
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            cv=5,
            scoring="f1",
            n_jobs=-1,
            verbose=0
        )
        grid_search.fit(X_train, y_train)
        
        best_svm = grid_search.best_estimator_
        best_params = grid_search.best_params_
        best_score = grid_search.best_score_
        
        logger.info(f"SVM Best F1: {best_score:.4f} with params: {best_params}")
        
        # Save to models directory
        save_path = self.models_dir / "svm.pkl"
        save_object(save_path, best_svm)
        
        return best_svm, {"params": best_params, "cv_f1": float(best_score)}

    def _train_and_evaluate_dl_trial(
        self,
        model_type: str,
        input_dim: int,
        hidden_dim: int,
        lr: float,
        batch_size: int,
        epochs: int,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray
    ) -> tuple[DeepSequenceModel, float, list[float]]:
        """Trains one deep learning trial and returns best model, best validation F1, and loss curve."""
        train_loader, val_loader = FeatureEngineering.get_dataloaders(
            X_train, y_train, X_val, y_val, batch_size=batch_size
        )
        
        model = DeepSequenceModel(input_dim=input_dim, hidden_dim=hidden_dim, model_type=model_type)
        criterion = nn.BCELoss()
        optimizer = optim.Adam(model.parameters(), lr=lr)
        
        best_val_f1 = 0.0
        best_weights = copy.deepcopy(model.state_dict())
        losses = []
        
        for epoch in range(epochs):
            model.train()
            total_loss = 0.0
            for batch_x, batch_y in train_loader:
                optimizer.zero_grad()
                preds = model(batch_x)
                loss = criterion(preds, batch_y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                
            avg_loss = total_loss / len(train_loader)
            losses.append(avg_loss)
            
            # Validation step
            model.eval()
            val_preds_list = []
            val_targets_list = []
            with torch.no_grad():
                for batch_x, batch_y in val_loader:
                    out = model(batch_x)
                    val_preds_list.extend((out.squeeze(1) > 0.5).int().tolist())
                    val_targets_list.extend(batch_y.squeeze(1).int().tolist())
                    
            epoch_f1 = f1_score(val_targets_list, val_preds_list, zero_division=0)
            if epoch_f1 > best_val_f1:
                best_val_f1 = epoch_f1
                best_weights = copy.deepcopy(model.state_dict())
                
        model.load_state_dict(best_weights)
        return model, best_val_f1, losses

    def tune_deep_model(
        self,
        model_type: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray
    ) -> tuple[DeepSequenceModel, dict]:
        """Performs hyperparameter grid search across hidden dimensions, learning rates, and batch sizes."""
        logger.info(f"--> [Tuning {model_type}] Exploring hyperparameter space...")
        dl_cfg = self.trainer_cfg[model_type.lower()]["search_space"]
        
        hidden_dims = dl_cfg.get("hidden_dims", [32, 64, 128])
        learning_rates = dl_cfg.get("learning_rates", [0.001, 0.0005])
        batch_sizes = dl_cfg.get("batch_sizes", [32, 64])
        epochs = dl_cfg.get("epochs", 15)
        input_dim = X_train.shape[1]
        
        best_overall_f1 = -1.0
        best_overall_model = None
        best_overall_params = {}
        best_losses = []
        
        trial = 0
        for h_dim in hidden_dims:
            for lr in learning_rates:
                for b_size in batch_sizes:
                    trial += 1
                    model, val_f1, losses = self._train_and_evaluate_dl_trial(
                        model_type=model_type,
                        input_dim=input_dim,
                        hidden_dim=h_dim,
                        lr=lr,
                        batch_size=b_size,
                        epochs=epochs,
                        X_train=X_train,
                        y_train=y_train,
                        X_val=X_val,
                        y_val=y_val
                    )
                    
                    if val_f1 > best_overall_f1:
                        best_overall_f1 = val_f1
                        best_overall_model = model
                        best_overall_params = {
                            "hidden_dim": h_dim,
                            "learning_rate": lr,
                            "batch_size": b_size,
                            "epochs": epochs
                        }
                        best_losses = losses
                        
        logger.info(f"{model_type} Best Val F1: {best_overall_f1:.4f} with params: {best_overall_params}")
        
        # Save to models directory
        save_path = self.models_dir / f"{model_type.lower()}.pth"
        save_torch_model(save_path, best_overall_model)
        
        return best_overall_model, {
            "params": best_overall_params,
            "val_f1": float(best_overall_f1),
            "loss_history": best_losses
        }

    def initiate_model_training(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> dict:
        """Executes full tuning cycle across all 4 architectures: LR, SVM, LSTM, GRU."""
        logger.info("=== [STAGE 4: MODEL TRAINING & HYPERPARAMETER TUNING] Starting Full Tuning ===")
        
        # 1. Tune Logistic Regression
        best_lr, lr_meta = self.tune_logistic_regression(X_train, y_train)
        
        # 2. Tune SVM
        best_svm, svm_meta = self.tune_svm(X_train, y_train)
        
        # 3. Tune LSTM
        best_lstm, lstm_meta = self.tune_deep_model("LSTM", X_train, y_train, X_test, y_test)
        
        # 4. Tune GRU
        best_gru, gru_meta = self.tune_deep_model("GRU", X_train, y_train, X_test, y_test)
        
        logger.info("=== [STAGE 4: MODEL TRAINING & HYPERPARAMETER TUNING] Completed Successfully ===")
        
        return {
            "logistic_regression": {"model": best_lr, "meta": lr_meta},
            "svm": {"model": best_svm, "meta": svm_meta},
            "lstm": {"model": best_lstm, "meta": lstm_meta},
            "gru": {"model": best_gru, "meta": gru_meta}
        }
