import os
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from .dataset import load_data, get_tfidf_features
import torch
import torch.nn as nn
import torch.optim as optim

class DeepSequenceModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, model_type='LSTM'):
        super(DeepSequenceModel, self).__init__()
        self.model_type = model_type
        # Using a simple dense layer to map TF-IDF to hidden dim as a simplified "sequence" step for this prototype
        # In a full DL pipeline, we'd use word embeddings and sequence padding.
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        if model_type == 'LSTM':
            self.rnn = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)
        elif model_type == 'GRU':
            self.rnn = nn.GRU(hidden_dim, hidden_dim, batch_first=True)
            
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x is (batch, input_dim) TF-IDF vector
        x = torch.relu(self.fc1(x))
        # Add sequence dimension for RNN (batch, 1, hidden_dim)
        x = x.unsqueeze(1)
        
        if self.model_type in ['LSTM', 'GRU']:
            out, _ = self.rnn(x)
            out = out[:, -1, :] # Take last hidden state
        else:
            out = x.squeeze(1)
            
        out = self.fc2(out)
        return self.sigmoid(out)

def train_baselines(X_train, y_train, models_dir):
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(X_train, y_train)
    with open(os.path.join(models_dir, 'logistic_regression.pkl'), 'wb') as f:
        pickle.dump(lr_model, f)
        
    print("Training SVM...")
    svm_model = SVC(kernel='linear', probability=True)
    svm_model.fit(X_train, y_train)
    with open(os.path.join(models_dir, 'svm.pkl'), 'wb') as f:
        pickle.dump(svm_model, f)

def train_dl_model(X_train, y_train, model_type, models_dir, epochs=10):
    print(f"Training {model_type}...")
    model = DeepSequenceModel(input_dim=X_train.shape[1], hidden_dim=64, model_type=model_type)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    X_t = torch.tensor(X_train, dtype=torch.float32)
    y_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_t)
        loss = criterion(outputs, y_t)
        loss.backward()
        optimizer.step()
        
    torch.save(model.state_dict(), os.path.join(models_dir, f'{model_type.lower()}.pth'))

if __name__ == "__main__":
    os.makedirs('backend/models', exist_ok=True)
    print("Loading data...")
    df = load_data('backend/data/dataset.tsv')
    X, y, vectorizer = get_tfidf_features(df)
    
    with open('backend/models/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    train_baselines(X_train, y_train, 'backend/models')
    train_dl_model(X_train, y_train, 'LSTM', 'backend/models', epochs=20)
    train_dl_model(X_train, y_train, 'GRU', 'backend/models', epochs=20)
    print("Training complete.")
