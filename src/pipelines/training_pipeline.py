import time
from src.utils.logger import get_logger
from src.utils.config_loader import load_config
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher

logger = get_logger(__name__)

class TrainingPipeline:
    """Master orchestration pipeline executing end-to-end MLOps workflow."""
    
    def __init__(self, config: dict = None):
        self.config = config or load_config()
        self.ingestion = DataIngestion(self.config)
        self.validation = DataValidation()
        self.transformation = DataTransformation(self.config)
        self.trainer = ModelTrainer(self.config)
        self.evaluation = ModelEvaluation(self.config)
        self.pusher = ModelPusher(self.config)

    def run_pipeline(self) -> dict:
        """Executes full pipeline and returns metrics, tuning details, and pusher status."""
        start_time = time.time()
        logger.info("===================================================================")
        logger.info("🚀 STARTING FULL END-TO-END DARK PATTERN TRAINING PIPELINE")
        logger.info("===================================================================")

        # 1. Ingestion
        train_df, test_df = self.ingestion.initiate_data_ingestion()

        # 2. Validation
        val_train = self.validation.validate_dataframe(train_df, "Train Set")
        val_test = self.validation.validate_dataframe(test_df, "Test Set")
        if not val_train["status"] or not val_test["status"]:
            raise ValueError(f"Data Validation Failed! Check logs for schema discrepancies.")

        # 3. Transformation & Feature Engineering
        X_train, X_test, y_train, y_test, vectorizer = self.transformation.initiate_data_transformation(
            train_df, test_df
        )

        # 4. Model Training & Hyperparameter Tuning
        trained_models = self.trainer.initiate_model_training(X_train, y_train, X_test, y_test)

        # 5. Model Evaluation
        summary_table, metrics_dict = self.evaluation.evaluate_all(trained_models, X_test, y_test)
        logger.info("\n" + summary_table.to_string(index=False))

        # 6. Model Pusher
        pusher_res = self.pusher.push_models_to_production()

        elapsed_sec = time.time() - start_time
        logger.info("===================================================================")
        logger.info(f"✅ PIPELINE FINISHED IN {elapsed_sec:.2f} SECONDS")
        logger.info("===================================================================")

        return {
            "elapsed_seconds": elapsed_sec,
            "summary_table": summary_table,
            "metrics": metrics_dict,
            "pusher": pusher_res
        }

if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()
