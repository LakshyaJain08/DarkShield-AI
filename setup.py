from setuptools import setup, find_packages

setup(
    name="darkshield-ml",
    version="2.0.0",
    author="DarkShield AI Team",
    description="End-to-End MLOps Pipeline for E-Commerce Dark Pattern Detection",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "torch",
        "shap",
        "pyyaml",
        "matplotlib",
        "seaborn",
        "fastapi",
        "uvicorn"
    ],
    python_requires=">=3.9",
)
