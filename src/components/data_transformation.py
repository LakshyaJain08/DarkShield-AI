import re
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from src.utils.logger import get_logger
from src.utils.config_loader import load_config, get_project_root
from src.utils.common import save_object

logger = get_logger(__name__)

def clean_text(text: str) -> str:
    """Cleans and standardizes raw text input."""
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Replace URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # Remove HTML tags if any
    text = re.sub(r"<.*?>", " ", text)
    # Remove excessive punctuation repetitions but keep word characters
    text = re.sub(r"[^\w\s\$\%\!\?]", " ", text)
    # Collapse multiple whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

class DataTransformation:
    """Component to clean text, fit vectorizer on train split, and transform train/test data."""
    
    def __init__(self, config: dict = None):
        self.config = config or load_config()
        self.root = get_project_root()
        self.transform_cfg = self.config["data_transformation"]
        
        self.max_features = self.transform_cfg.get("max_features", 1000)
        self.ngram_range = tuple(self.transform_cfg.get("ngram_range", [1, 2]))
        self.sublinear_tf = self.transform_cfg.get("sublinear_tf", True)
        self.stop_words = self.transform_cfg.get("stop_words", "english")
        self.preprocessor_path = self.root / self.transform_cfg["preprocessor_path"]
        
        self.vectorizer = None

    def initiate_data_transformation(
        self, train_df: pd.DataFrame, test_df: pd.DataFrame
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, TfidfVectorizer]:
        """Cleans text, fits TfidfVectorizer ONLY on train_df, transforms test_df, and saves vectorizer."""
        logger.info("=== [STAGE 3: DATA TRANSFORMATION] Starting Text Transformation ===")
        
        # 1. Clean train and test text
        logger.info("Normalizing and cleaning text features...")
        train_clean = train_df["text"].apply(clean_text)
        test_clean = test_df["text"].apply(clean_text)
        
        y_train = train_df["label"].values.astype(int)
        y_test = test_df["label"].values.astype(int)
        
        # 2. Strict ML Best Practice: Fit vectorizer strictly on training split
        logger.info(f"Fitting TfidfVectorizer on training set (max_features={self.max_features}, ngrams={self.ngram_range})...")
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            ngram_range=self.ngram_range,
            sublinear_tf=self.sublinear_tf,
            stop_words=self.stop_words
        )
        
        X_train = self.vectorizer.fit_transform(train_clean).toarray()
        logger.info(f"Fitted vectorizer with {len(self.vectorizer.get_feature_names_out())} vocabulary terms.")
        
        # 3. Transform test split
        X_test = self.vectorizer.transform(test_clean).toarray()
        logger.info(f"Transformed train shape: {X_train.shape}, test shape: {X_test.shape}")
        
        # 4. Save preprocessor artifact
        save_object(self.preprocessor_path, self.vectorizer)
        logger.info(f"Saved fitted vectorizer artifact to: {self.preprocessor_path}")
        logger.info("=== [STAGE 3: DATA TRANSFORMATION] Completed Successfully ===")
        
        return X_train, X_test, y_train, y_test, self.vectorizer
