import re
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.base import BaseEstimator, TransformerMixin
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Domain-specific lexicons compiled with word boundaries
URGENCY_REGEX = re.compile(
    r'\b(hurry|limited|expires|countdown|deal|fast|quick|ending|ends|last chance|now|clock|today only|flash sale)\b',
    re.IGNORECASE
)
SCARCITY_REGEX = re.compile(
    r'\b(only|left|stock|sold|remaining|demand|popular|few|almost gone|low stock|reserved)\b',
    re.IGNORECASE
)
SOCIAL_REGEX = re.compile(
    r'\b(bought|people|viewing|looking|others|trending|purchased|views|claimed|booked)\b',
    re.IGNORECASE
)
GUILT_REGEX = re.compile(
    r'\b(miss|hate|lose|regret|no thanks|skip|don\'t want|decline)\b',
    re.IGNORECASE
)

class LinguisticFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Scikit-learn compatible transformer extracting 15 domain-specific linguistic,
    syntactic, structural, and psychological dark pattern cue features.
    """
    
    FEATURE_NAMES = [
        "char_count",
        "word_count",
        "avg_word_length",
        "exclamation_count",
        "question_count",
        "uppercase_words",
        "uppercase_ratio",
        "digit_count",
        "has_number",
        "has_currency",
        "urgency_hits",
        "scarcity_hits",
        "social_hits",
        "guilt_hits",
        "total_cues"
    ]

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def _extract_single(self, text: str) -> list[float]:
        text_str = str(text) if text is not None else ""
        stripped = text_str.strip()
        words = stripped.split()
        
        char_count = float(len(stripped))
        word_count = float(len(words))
        avg_word_length = char_count / (word_count + 1e-5)
        
        exclamation_count = float(text_str.count("!"))
        question_count = float(text_str.count("?"))
        
        uppercase_words = float(sum(1 for w in words if w.isupper() and len(w) > 1))
        uppercase_ratio = uppercase_words / (word_count + 1e-5)
        
        digit_count = float(sum(c.isdigit() for c in text_str))
        has_number = 1.0 if digit_count > 0 else 0.0
        has_currency = 1.0 if bool(re.search(r'[$€£₹]', text_str)) else 0.0
        
        urgency_hits = float(len(URGENCY_REGEX.findall(text_str)))
        scarcity_hits = float(len(SCARCITY_REGEX.findall(text_str)))
        social_hits = float(len(SOCIAL_REGEX.findall(text_str)))
        guilt_hits = float(len(GUILT_REGEX.findall(text_str)))
        total_cues = urgency_hits + scarcity_hits + social_hits + guilt_hits
        
        return [
            char_count,
            word_count,
            avg_word_length,
            exclamation_count,
            question_count,
            uppercase_words,
            uppercase_ratio,
            digit_count,
            has_number,
            has_currency,
            urgency_hits,
            scarcity_hits,
            social_hits,
            guilt_hits,
            total_cues
        ]

    def transform(self, X) -> np.ndarray:
        if isinstance(X, pd.DataFrame):
            col = "text" if "text" in X.columns else X.columns[0]
            texts = X[col].tolist()
        elif isinstance(X, pd.Series):
            texts = X.tolist()
        else:
            texts = list(X)
            
        features = [self._extract_single(t) for t in texts]
        return np.array(features, dtype=np.float32)

    def get_feature_names_out(self, input_features=None) -> list[str]:
        return list(self.FEATURE_NAMES)

    def transform_to_df(self, X) -> pd.DataFrame:
        """Helper to return features directly as a labeled pandas DataFrame."""
        arr = self.transform(X)
        return pd.DataFrame(arr, columns=self.FEATURE_NAMES)


class DeepSequenceModel(nn.Module):
    """Deep sequence neural network architecture supporting LSTM and GRU."""
    
    def __init__(self, input_dim: int, hidden_dim: int = 64, model_type: str = "LSTM", dropout: float = 0.2):
        super(DeepSequenceModel, self).__init__()
        self.model_type = model_type.upper()
        self.hidden_dim = hidden_dim
        
        # Dense projection from TF-IDF vector space to hidden dimension
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        
        # Recurrent sequence layer
        if self.model_type == "LSTM":
            self.rnn = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)
        elif self.model_type == "GRU":
            self.rnn = nn.GRU(hidden_dim, hidden_dim, batch_first=True)
        else:
            raise ValueError(f"Unsupported model_type: {model_type}. Must be 'LSTM' or 'GRU'")
            
        # Classification head
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x is (batch_size, input_dim)
        h = torch.relu(self.fc1(x))
        h = self.dropout(h)
        # Add sequence dimension: (batch_size, 1, hidden_dim)
        h = h.unsqueeze(1)
        
        out, _ = self.rnn(h)
        out = out[:, -1, :] # Last recurrent state
        out = self.fc2(out)
        return self.sigmoid(out)


class TextSequenceDataset(Dataset):
    """PyTorch Dataset wrapper for vector representations and binary target labels."""
    
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

    def __len__(self) -> int:
        return len(self.X)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.X[idx], self.y[idx]


class FeatureEngineering:
    """Component to prepare feature representations and PyTorch DataLoaders."""
    
    def __init__(self):
        self.linguistic_extractor = LinguisticFeatureExtractor()

    @staticmethod
    def get_dataloaders(
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        batch_size: int = 32
    ) -> tuple[DataLoader, DataLoader]:
        """Creates training and validation PyTorch DataLoaders."""
        train_dataset = TextSequenceDataset(X_train, y_train)
        val_dataset = TextSequenceDataset(X_val, y_val)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        return train_loader, val_loader
