import pandas as pd
from src.utils.logger import get_logger
from src.utils.config_loader import load_schema

logger = get_logger(__name__)

class DataValidation:
    """Component to validate dataset schema, missing values, duplicates, and data integrity."""
    
    def __init__(self, schema: dict = None):
        self.schema = schema or load_schema()
        self.required_columns = [
            col for col, meta in self.schema["columns"].items() if meta.get("required", False)
        ]
        self.allowed_labels = self.schema["columns"]["label"].get("allowed_values", [0, 1])
        self.allowed_categories = self.schema.get("categories", [])

    def validate_dataframe(self, df: pd.DataFrame, dataset_name: str = "Dataset") -> dict:
        """Validates dataframe columns, null values, duplicates, label constraints, and text integrity."""
        logger.info(f"=== [STAGE 2: DATA VALIDATION] Validating {dataset_name} ===")
        
        errors = []
        warnings = []
        validation_status = True
        
        # 1. Check required columns
        for col in self.required_columns:
            if col not in df.columns:
                errors.append(f"Missing required column: '{col}'")
                validation_status = False
                
        if not validation_status:
            logger.error(f"Validation failed for {dataset_name}: {errors}")
            return {"status": False, "errors": errors, "warnings": warnings}

        # 2. Check null values across all present columns
        null_counts = df.isnull().sum().to_dict()
        for col in self.required_columns:
            null_c = null_counts.get(col, 0)
            if null_c > 0:
                errors.append(f"Required column '{col}' has {null_c} null values.")
                validation_status = False
                
        # 3. Check label values constraints
        invalid_labels = df[~df["label"].isin(self.allowed_labels)]
        if len(invalid_labels) > 0:
            errors.append(f"Found {len(invalid_labels)} rows with invalid label values not in {self.allowed_labels}")
            validation_status = False

        # 4. Check empty / whitespace-only text strings
        empty_text_mask = df["text"].fillna("").astype(str).str.strip() == ""
        empty_text_count = int(empty_text_mask.sum())
        if empty_text_count > 0:
            errors.append(f"Found {empty_text_count} rows with empty or whitespace-only text.")
            validation_status = False

        # 5. Check exact and text-level duplicates
        exact_dups_count = int(df.duplicated().sum())
        if exact_dups_count > 0:
            warnings.append(f"Found {exact_dups_count} exact duplicate rows.")

        text_stripped = df["text"].fillna("").astype(str).str.strip().str.lower()
        text_dups_count = int(text_stripped.duplicated().sum())
        if text_dups_count > 0:
            warnings.append(f"Found {text_dups_count} case-insensitive duplicate text occurrences.")

        # 6. Check for conflicting labels on identical text
        dup_texts = df[text_stripped.duplicated(keep=False)]
        conflicting_texts_count = 0
        if len(dup_texts) > 0:
            grouped = dup_texts.groupby(text_stripped)["label"].nunique()
            conflicting_texts_count = int((grouped > 1).sum())
            if conflicting_texts_count > 0:
                errors.append(f"Critical Inconsistency: Found {conflicting_texts_count} unique texts with conflicting labels (both 0 and 1)!")
                validation_status = False

        # 7. Check category-label consistency if Pattern Category column is present
        category_inconsistencies = 0
        if "Pattern Category" in df.columns:
            mismatched_neg = (df["label"] == 0) & (df["Pattern Category"].astype(str).str.lower() != "not dark pattern")
            mismatched_pos = (df["label"] == 1) & (df["Pattern Category"].astype(str).str.lower() == "not dark pattern")
            category_inconsistencies = int((mismatched_neg | mismatched_pos).sum())
            if category_inconsistencies > 0:
                errors.append(f"Found {category_inconsistencies} rows where 'label' conflicts with 'Pattern Category'.")
                validation_status = False

        # 8. Check text length anomalies (outliers)
        char_lengths = df["text"].fillna("").astype(str).str.len()
        extreme_short_count = int((char_lengths <= 3).sum())
        extreme_long_count = int((char_lengths > 500).sum())
        if extreme_short_count > 0:
            warnings.append(f"Found {extreme_short_count} extremely short text samples (<= 3 characters).")
        if extreme_long_count > 0:
            warnings.append(f"Found {extreme_long_count} extremely long text samples (> 500 characters).")

        class_distribution = df["label"].value_counts().to_dict()
        logger.info(f"{dataset_name} Validation Status: {'PASSED' if validation_status else 'FAILED'}")
        logger.info(f"Class distribution: {class_distribution} | Exact Dups: {exact_dups_count} | Nulls: {null_counts}")

        return {
            "status": validation_status,
            "total_rows": len(df),
            "columns": list(df.columns),
            "null_counts": null_counts,
            "exact_duplicates": exact_dups_count,
            "text_duplicates": text_dups_count,
            "conflicting_labels": conflicting_texts_count,
            "empty_text_count": empty_text_count,
            "extreme_short_count": extreme_short_count,
            "extreme_long_count": extreme_long_count,
            "category_inconsistencies": category_inconsistencies,
            "class_distribution": class_distribution,
            "errors": errors,
            "warnings": warnings
        }
