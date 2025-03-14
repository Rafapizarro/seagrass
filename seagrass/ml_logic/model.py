import os
import xgboost as xgb
from pathlib import Path
from sklearn.metrics import f1_score
from seagrass.params import LOCAL_REGISTRY_PATH
from sklearn.utils.class_weight import compute_sample_weight


class XGBTrainer:
    def __init__(self):
        self.model = xgb.XGBClassifier(
            objective="multi:softmax",
            num_class=5,
            eval_metric="mlogloss",
            n_estimators=500,
            tree_method="hist",
            max_depth=5,
            min_child_weight=5,
            subsample=0.8,
            colsample_bytree=0.8,
            early_stopping_rounds=20,
            random_state=42,
        )
        self.trained = False
        self.model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", "xgb.ubj")

    def train_test(self, X_train, y_train, X_val, y_val):
        print("\nTraining model...\n")

        sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)

        self.model.fit(
            X_train,
            y_train,
            sample_weight=sample_weight,
            eval_set=[(X_val, y_val)],
            verbose=False,
        )
        self.trained = True
        print("\nTraining complete.\n")

        y_pred_proba = self.model.predict_proba(X_val)
        y_pred = y_pred_proba.argmax(axis=1)

        f1 = f1_score(y_val, y_pred, average="macro")
        print(f"\nMacro F1 score: {f1:.6f}\n")

        return f1

    def save(self, f1: float):
        """Save the trained model with an F1-score-based filename"""
        if not self.trained:
            raise ValueError("\n❌ Error: Model must be trained before saving.\n")

        model_dir = os.path.join(LOCAL_REGISTRY_PATH, "models")
        os.makedirs(model_dir, exist_ok=True)  # Ensure directory exists

        # Save model with F1 score in filename
        model_path = os.path.join(model_dir, f"{f1:.3f}_xgb.ubj")
        self.model.save_model(model_path)
        print(f"\n✅ Model saved at: {model_path}\n")

    def load(self):
        """Load the most recent saved model automatically"""
        model_dir = os.path.join(LOCAL_REGISTRY_PATH, "models")

        # Find all saved models
        model_files = list(Path(model_dir).glob("*.ubj"))

        if not model_files:
            raise FileNotFoundError(
                "\n❌ No saved models found! Train and save a model first.\n"
            )

        # Sort files by most recent (assuming names include scores like '0.853_xgb.ubj')
        latest_model = max(model_files, key=os.path.getctime)

        # Load the latest model
        self.model.load_model(str(latest_model))
        print(f"\n✅ Loaded model: {latest_model}\n")

        return self.model


if __name__ == "__main__":
    model = XGBTrainer().load()
    model.load()
