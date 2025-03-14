import os
import glob
import joblib
import hdbscan
import numpy as np
import xgboost as xgb
from pathlib import Path
from sklearn.metrics import f1_score, classification_report
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

    def train_test(self, X_train, y_train, X_val, y_val, X_test, y_test):
        print("\nTraining model...\n")

        self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=False,
        )

        self.trained = True
        print("Training complete.\n")

        y_pred = self.model.predict(X_test)

        f1 = f1_score(y_test, y_pred, average="macro")
        print(f"\nMacro F1 score: {f1:.6f}\n")

        return f1

    def save(self, f1: float):
        """Save the trained model with an F1-score-based filename"""
        if not self.trained:
            raise ValueError("\n❌ Error: Model must be trained before saving.\n")

        model_dir = os.path.join(LOCAL_REGISTRY_PATH, "models")
        os.makedirs(model_dir, exist_ok=True)  # Ensure directory exists

        # Save model with F1 score in filename
        model_path = os.path.join(model_dir, f"{float(f1):.3f}_xgb.ubj")
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


class Clusterer:
    def __init__(self):
        self.model = None
        self.cluster_amount = None
        self.trained = False
        self.saved = False

    def fit_predict(self, data):
        self.model = hdbscan.HDBSCAN(
            min_cluster_size=10,
            min_samples=3,
            metric="euclidean",
            cluster_selection_method="eom",
        )
        data = data[["lat", "lon"]]
        data = np.radians(data)

        cluster_labels = self.model.fit_predict(data)
        self.trained = True

        cluster_amount = len(np.unique(cluster_labels))
        self.cluster_amount = cluster_amount

        return cluster_labels, cluster_amount

    def save(self, filename=None):
        if not self.trained:
            raise ValueError("\n❌ Error: Model must be trained before saving.\n")

        model_dir = os.path.join(LOCAL_REGISTRY_PATH, "models")
        os.makedirs(model_dir, exist_ok=True)
        #

        if filename is None:
            filename = os.path.join(
                model_dir, f"hdbscan_{self.cluster_amount}_clusters.pkl"
            )

        joblib.dump(self.model, filename)
        self.saved = True

        print(f"✅ Model saved as {filename}")

    def load(self, path=None):
        model_dir = os.path.join(LOCAL_REGISTRY_PATH, "models")

        # If no path is provided, find the latest saved model
        if path is None:
            model_files = glob.glob(os.path.join(model_dir, "hdbscan_*.pkl"))
            if not model_files:
                raise ValueError("\n❌ Error: No saved models found.\n")
            path = max(model_files, key=os.path.getctime)  # Load most recent model

        if not os.path.isfile(path):
            raise ValueError(f"\n❌ Error: Model file {path} does not exist.\n")

        self.model = joblib.load(path)
        self.trained = True
        self.saved = True
        print(f"✅ Model loaded from {path}")

        return self.model


if __name__ == "__main__":
    model = XGBTrainer().load()
    model.load()
