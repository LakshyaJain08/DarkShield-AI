import os
import nbformat as nbf
from pathlib import Path

def create_01_eda_notebook():
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell("""# 📊 01: Exploratory Data Analysis (EDA)
### DarkShield AI - Deep Analysis of Dark Pattern Corpus

This notebook provides an in-depth visual and statistical exploration of deceptive patterns in e-commerce interfaces.
"""),
        nbf.v4.new_code_cell("""import sys, os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(os.getcwd()).parent if Path(os.getcwd()).name == "notebooks" else Path(os.getcwd())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.components.data_ingestion import DataIngestion

sns.set_theme(style="darkgrid")
plt.rcParams['figure.facecolor'] = '#121214'
plt.rcParams['axes.facecolor'] = '#18181b'
plt.rcParams['text.color'] = '#f4f4f5'
plt.rcParams['axes.labelcolor'] = '#a1a1aa'
plt.rcParams['xtick.color'] = '#a1a1aa'
plt.rcParams['ytick.color'] = '#a1a1aa'

ingestion = DataIngestion()
train_df, test_df = ingestion.initiate_data_ingestion()
print(f"Loaded {len(train_df)} training samples and {len(test_df)} test samples.")
display(train_df.head())
"""),
        nbf.v4.new_markdown_cell("### Target Class Distribution"),
        nbf.v4.new_code_cell("""plt.figure(figsize=(7, 4))
sns.countplot(data=train_df, x='label', palette=['#3b82f6', '#ef4444'])
plt.title("Class Balance (0: Benign, 1: Dark Pattern)", color='#f4f4f5', pad=10)
plt.show()
"""),
        nbf.v4.new_markdown_cell("### Subcategory Frequency"),
        nbf.v4.new_code_cell("""dark_df = train_df[train_df['label'] == 1]
plt.figure(figsize=(9, 4))
sns.countplot(data=dark_df, y='Pattern Category', order=dark_df['Pattern Category'].value_counts().index, palette='mako')
plt.title("Dark Pattern Categories", color='#f4f4f5', pad=10)
plt.show()
""")
    ]
    nb.cells = cells
    with open("notebooks/01_eda.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print("Created notebooks/01_eda.ipynb")

def create_02_data_preparation_notebook():
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell("""# 🧹 02: Data Preparation & Transformation
### DarkShield AI - Cleaning, Normalization & Vectorizer Fitting

This notebook validates data schema and demonstrates the strict ML best practice of fitting text vectorizers solely on the training split.
"""),
        nbf.v4.new_code_cell("""import sys, os
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(os.getcwd()).parent if Path(os.getcwd()).name == "notebooks" else Path(os.getcwd())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation

ingestion = DataIngestion()
train_df, test_df = ingestion.initiate_data_ingestion()

validator = DataValidation()
val_res = validator.validate_dataframe(train_df, "Train Set")
print("Validation Status:", val_res["status"])

transformer = DataTransformation()
X_train, X_test, y_train, y_test, vec = transformer.initiate_data_transformation(train_df, test_df)
print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")
print(f"Top terms: {list(vec.get_feature_names_out()[:10])}")
""")
    ]
    nb.cells = cells
    with open("notebooks/02_data_preparation.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print("Created notebooks/02_data_preparation.ipynb")

def create_03_model_experimentation_notebook():
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell("""# 🧪 03: Model Experimentation & Hyperparameter Tuning
### DarkShield AI - Systematic Tuning Across 4 Architectures

This notebook demonstrates hyperparameter tuning across Logistic Regression, SVM, LSTM, and GRU, followed by comparative evaluation and model pusher synchronization.
"""),
        nbf.v4.new_code_cell("""import sys, os
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(os.getcwd()).parent if Path(os.getcwd()).name == "notebooks" else Path(os.getcwd())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher

ingestion = DataIngestion()
train_df, test_df = ingestion.initiate_data_ingestion()

transformer = DataTransformation()
X_train, X_test, y_train, y_test, vec = transformer.initiate_data_transformation(train_df, test_df)

trainer = ModelTrainer()
models_dict = trainer.initiate_model_training(X_train, y_train, X_test, y_test)

evaluator = ModelEvaluation()
summary, metrics = evaluator.evaluate_all(models_dict, X_test, y_test)
display(summary)

pusher = ModelPusher()
pusher.push_models_to_production()
""")
    ]
    nb.cells = cells
    with open("notebooks/03_model_experimentation.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print("Created notebooks/03_model_experimentation.ipynb")

if __name__ == "__main__":
    create_01_eda_notebook()
    create_02_data_preparation_notebook()
    create_03_model_experimentation_notebook()
