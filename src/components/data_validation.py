import pandas as pd
from src.utils.logger import get_logger
from src.utils.config_loader import load_schema

logger = get_logger(__name__)

class DataValidation:
    """Component to validate dataset schema, missing values, and integrity."""
    
    def __init__(self, schema: dict = None):
        self.schema = schema or load_schema()
        self.required_columns = [
            col for col, meta in self.schema["columns"].items() if meta.get("required", False)
        ]
        self.allowed_labels = self.schema["columns"]["label"].get("allowed_values", [0, 1])

    def validate_dataframe(self, df: pd.DataFrame, dataset_name: str = "Dataset") -> dict:
        """Validates dataframe columns, data types, and value constraints."""
        logger.info(f"=== [STAGE 2: DATA VALIDATION] Validating {dataset_name} ===")
        
        errors = []
        validation_status = True
        
        # 1. Check required columns
        for col in self.required_columns:
            if col not in df.columns:
                errors.append(f"Missing required column: '{col}'")
                validation_status = False
                
        if not validation_status:
            logger.error(f"Validation failed for {dataset_name}: {errors}")
            return {"status": False, "errors": errors}

        # 2. Check null values in required columns
        null_counts = df[self.required_columns].isnull().sum().to_dict()
        for col, null_c in null_counts.items():
            if null_c > 0:
                errors.append(f"Column '{col}' has {null_c} null values.")
                validation_status = False
                
        # 3. Check label values
        invalid_labels = df[~df["label"].isin(self.allowed_labels)]
        if len(invalid_labels) > 0:
            errors.append(f"Found {len(invalid_labels)} rows with invalid label values not in {self.allowed_labels}")
            validation_status = False

        # 4. Check empty text strings
        empty_text_count = (df["text"].str.strip() == "").sum()
        if empty_text_count > 0:
            errors.append(f"Found {empty_text_count} rows with empty text.")
            validation_status = False

        class_distribution = df["label"].value_counts().to_dict()
        logger.info(f"{dataset_name} Schema Validation Status: {'PASSED' if validation_status else 'FAILED'}")
        logger.info(f"Class distribution: {class_distribution}")

        return {
            "status": validation_status,
            "total_rows": len(df),
            "columns": list(df.columns),
            "null_counts": null_counts,
            "class_distribution": class_distribution,
            "errors": errors
        }
