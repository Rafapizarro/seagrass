import os
import glob
import joblib
import hdbscan
import numpy as np
import xgboost as xgb
from pathlib import Path
from sklearn.metrics import f1_score, classification_report
from seagrass.params import LOCAL_REGISTRY_PATH


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

    def fit_model(self, X_train, y_train, X_val, y_val):
        self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=False,
        )
        self.trained = True
        return self.model

    def train_eval(self, X_train, y_train, X_val, y_val, X_test, y_test):
        print("Training model...\n")

        self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=False,
        )

        self.trained = True
        print("Training complete.\n")

        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)
        y_pred = y_pred_proba.argmax(axis=1)

        f1 = f1_score(y_test, y_pred, average="macro")
        print(f"\nMacro F1 score: {f1:.6f}\n")
        class_report = classification_report(y_test, y_pred)
        print(class_report)

        return f1

    def save(self, f1: float):
        """Save the trained model with an F1-score-based filename"""
        if not self.trained:
            raise ValueError("\nError: Model must be trained before saving.\n")

        model_dir = os.path.join(LOCAL_REGISTRY_PATH, "models")
        os.makedirs(model_dir, exist_ok=True)

        model_path = os.path.join(model_dir, f"{float(f1):.3f}_xgb.ubj")
        self.model.save_model(model_path)
        print(f"\nModel saved as {model_path}\n")

    def load(self):
        """Load the most recent saved model automatically"""
        model_dir = os.path.join(LOCAL_REGISTRY_PATH, "models")

        model_files = list(Path(model_dir).glob("*.ubj"))

        if not model_files:
            raise FileNotFoundError(
                "\nNo saved models found. Train and save the model first.\n"
            )

        latest_model = max(model_files, key=os.path.getctime)

        self.model.load_model(str(latest_model))
        print(f"\nLoaded model: {latest_model}\n")

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
            raise ValueError("\nError: Model must be trained before saving.\n")

        model_dir = os.path.join(LOCAL_REGISTRY_PATH, "models")
        os.makedirs(model_dir, exist_ok=True)

        if filename is None:
            filename = os.path.join(
                model_dir, f"hdbscan_{self.cluster_amount}_clusters.pkl"
            )

        joblib.dump(self.model, filename)
        self.saved = True

        print(f"Model saved as {filename}")

    def load(self, path=None):
        model_dir = os.path.join(LOCAL_REGISTRY_PATH, "models")
        os.makedirs(model_dir, exist_ok=True)

        if path is None:
            model_files = glob.glob(os.path.join(model_dir, "hdbscan_*.pkl"))
            if not model_files:
                raise ValueError("\nError: No saved models found.\n")
            path = max(model_files, key=os.path.getctime)

        if not os.path.isfile(path):
            raise ValueError(f"\nError: Model file {path} does not exist.\n")

        self.model = joblib.load(path)
        self.trained = True
        self.saved = True
        print(f"Model loaded from {path}")

        return self.model


if __name__ == "__main__":
    model = XGBTrainer().load()
    model.load()
