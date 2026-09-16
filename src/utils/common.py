import os
import pickle
import json
import torch
from pathlib import Path
from typing import Any
from .logger import get_logger

logger = get_logger(__name__)

def ensure_dir(path: str | Path) -> None:
    """Ensures that a directory exists, creating parents if necessary."""
    os.makedirs(path, exist_ok=True)

def save_object(file_path: str | Path, obj: Any) -> None:
    """Saves a python object using pickle."""
    try:
        ensure_dir(os.path.dirname(file_path))
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)
        logger.info(f"Saved object successfully at: {file_path}")
    except Exception as e:
        logger.error(f"Error saving object at {file_path}: {e}")
        raise e

def load_object(file_path: str | Path) -> Any:
    """Loads a python object using pickle."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as f:
            obj = pickle.load(f)
        return obj
    except Exception as e:
        logger.error(f"Error loading object from {file_path}: {e}")
        raise e

def save_json(file_path: str | Path, data: dict) -> None:
    """Saves a dictionary as formatted JSON."""
    try:
        ensure_dir(os.path.dirname(file_path))
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved JSON data at: {file_path}")
    except Exception as e:
        logger.error(f"Error saving JSON at {file_path}: {e}")
        raise e

def load_json(file_path: str | Path) -> dict:
    """Loads JSON data from file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {e}")
        raise e

def save_torch_model(file_path: str | Path, model: torch.nn.Module) -> None:
    """Saves PyTorch state dict."""
    try:
        ensure_dir(os.path.dirname(file_path))
        torch.save(model.state_dict(), file_path)
        logger.info(f"Saved PyTorch model weights at: {file_path}")
    except Exception as e:
        logger.error(f"Error saving PyTorch model at {file_path}: {e}")
        raise e

def load_torch_model(file_path: str | Path, model: torch.nn.Module, device: str = "cpu") -> torch.nn.Module:
    """Loads weights into a PyTorch model."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Model file not found: {file_path}")
        state_dict = torch.load(file_path, map_location=torch.device(device))
        model.load_state_dict(state_dict)
        model.eval()
        return model
    except Exception as e:
        logger.error(f"Error loading PyTorch model from {file_path}: {e}")
        raise e
