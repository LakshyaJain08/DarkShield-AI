import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
from src.utils.logger import get_logger

logger = get_logger(__name__)

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
        pass

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
