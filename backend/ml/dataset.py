import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

def load_data(filepath='backend/data/dataset.tsv'):
    df = pd.read_csv(filepath, sep='\t')
    df = df.dropna(subset=['text', 'label'])
    # Optional: basic cleaning
    df['text'] = df['text'].str.lower()
    return df

def get_tfidf_features(df, max_features=1000):
    vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english')
    X = vectorizer.fit_transform(df['text']).toarray()
    y = df['label'].values
    return X, y, vectorizer

# For PyTorch LSTM/GRU
class TextDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]
