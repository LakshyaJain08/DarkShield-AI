import os
import shutil
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.utils.logger import get_logger
from src.utils.config_loader import load_config, get_project_root
from src.utils.common import ensure_dir

logger = get_logger(__name__)

class DataIngestion:
    """Component to handle data ingestion, raw storage, and train-test splitting."""
    
    def __init__(self, config: dict = None):
        self.config = config or load_config()
        self.root = get_project_root()
        self.ingestion_cfg = self.config["data_ingestion"]
        
        self.raw_data_path = self.root / self.ingestion_cfg["raw_data_path"]
        self.train_data_path = self.root / self.ingestion_cfg["train_data_path"]
        self.test_data_path = self.root / self.ingestion_cfg["test_data_path"]
        self.test_size = self.ingestion_cfg.get("test_size", 0.2)
        self.random_state = self.ingestion_cfg.get("random_state", 42)

    def initiate_data_ingestion(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Loads raw data, saves to data/raw, splits into train/test, and persists to data/processed."""
        logger.info("=== [STAGE 1: DATA INGESTION] Starting Data Ingestion ===")
        
        ensure_dir(self.raw_data_path.parent)
        ensure_dir(self.train_data_path.parent)
        
        # If raw dataset is not in data/raw yet, copy from backend/data/dataset.tsv or ec-darkpattern/dataset/dataset.tsv
        if not self.raw_data_path.exists():
            backup_source_1 = self.root / "backend" / "data" / "dataset.tsv"
            backup_source_2 = self.root / "ec-darkpattern" / "dataset" / "dataset.tsv"
            
            if backup_source_1.exists():
                shutil.copyfile(backup_source_1, self.raw_data_path)
                logger.info(f"Copied raw dataset from {backup_source_1} to {self.raw_data_path}")
            elif backup_source_2.exists():
                shutil.copyfile(backup_source_2, self.raw_data_path)
                logger.info(f"Copied raw dataset from {backup_source_2} to {self.raw_data_path}")
            else:
                raise FileNotFoundError(f"Source raw dataset not found in backend or ec-darkpattern directories.")
        
        logger.info(f"Reading dataset from: {self.raw_data_path}")
        df = pd.read_csv(self.raw_data_path, sep="\t")
        logger.info(f"Loaded raw dataset with shape: {df.shape}")
        
        # Clean nulls in required columns
        initial_len = len(df)
        df = df.dropna(subset=["text", "label"])
        logger.info(f"Dropped {initial_len - len(df)} rows with missing text or label. Retained {len(df)} rows.")
        
        # Stratified train/test split to maintain class ratio
        train_df, test_df = train_test_split(
            df,
            test_size=self.test_size,
            stratify=df["label"],
            random_state=self.random_state
        )
        
        # Save to processed directory
        train_df.to_csv(self.train_data_path, index=False)
        test_df.to_csv(self.test_data_path, index=False)
        logger.info(f"Saved train data ({len(train_df)} rows) to: {self.train_data_path}")
        logger.info(f"Saved test data ({len(test_df)} rows) to: {self.test_data_path}")
        logger.info("=== [STAGE 1: DATA INGESTION] Completed Successfully ===")
        
        return train_df, test_df
