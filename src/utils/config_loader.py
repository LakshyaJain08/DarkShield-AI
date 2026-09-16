import os
import yaml
from pathlib import Path

def get_project_root() -> Path:
    """Returns root directory of the ML project."""
    return Path(__file__).resolve().parent.parent.parent

def load_config(config_path: str = "src/config/config.yaml") -> dict:
    """Loads configuration yaml file."""
    root = get_project_root()
    full_path = root / config_path
    if not full_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {full_path}")
    with open(full_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

def load_schema(schema_path: str = "src/config/schema.yaml") -> dict:
    """Loads schema definition yaml file."""
    root = get_project_root()
    full_path = root / schema_path
    if not full_path.exists():
        raise FileNotFoundError(f"Schema file not found at: {full_path}")
    with open(full_path, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    return schema
