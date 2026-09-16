import os
import shutil
from pathlib import Path
from src.utils.logger import get_logger
from src.utils.config_loader import load_config, get_project_root
from src.utils.common import ensure_dir

logger = get_logger(__name__)

class ModelPusher:
    """Component to push the best validated model artifacts directly to production backend for website inference."""
    
    def __init__(self, config: dict = None):
        self.config = config or load_config()
        self.root = get_project_root()
        self.pusher_cfg = self.config["model_pusher"]
        
        self.models_dir = self.root / self.pusher_cfg.get("models_dir", "models")
        self.production_dir = self.root / self.pusher_cfg.get("production_dir", "backend/models")
        
        self.artifacts = [
            "logistic_regression.pkl",
            "svm.pkl",
            "lstm.pth",
            "gru.pth",
            "vectorizer.pkl"
        ]

    def push_models_to_production(self) -> dict:
        """Copies all model and preprocessor artifacts into backend/models/ for live web app inference."""
        logger.info(f"=== [STAGE 6: MODEL PUSHER] Pushing Best Models to Production ===")
        ensure_dir(self.production_dir)
        
        pushed_files = []
        errors = []
        
        for artifact in self.artifacts:
            src_file = self.models_dir / artifact
            dest_file = self.production_dir / artifact
            
            if not src_file.exists():
                err_msg = f"Artifact missing in source models directory: {src_file}"
                logger.error(err_msg)
                errors.append(err_msg)
                continue
                
            shutil.copyfile(src_file, dest_file)
            size_kb = dest_file.stat().st_size / 1024
            logger.info(f"Successfully deployed: {artifact} ({size_kb:.2f} KB) -> {dest_file}")
            pushed_files.append(artifact)
            
        success = len(errors) == 0 and len(pushed_files) == len(self.artifacts)
        logger.info(f"Model Pusher Status: {'DEPLOYED SUCCESSFULLY' if success else 'PARTIAL DEPLOYMENT'}")
        logger.info("=== [STAGE 6: MODEL PUSHER] Completed Successfully ===")
        
        return {
            "status": success,
            "pushed_artifacts": pushed_files,
            "destination": str(self.production_dir),
            "errors": errors
        }
