import os
import glob
import joblib
import hdbscan
import numpy as np
import xgboost as xgb
from pathlib import Path
from sklearn.metrics import f1_score, classification_report
from seagrass.params import LOCAL_REGISTRY_PATH
# import optuna


class XGBTrainer:
    def __init__(self, params=None):
        if params is None:
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
        else:
            self.model = xgb.XGBClassifier(**params)

        self.trained = False
        self.model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", "xgb.ubj")

    def fit_model(self, X_train, y_train, X_val, y_val):
        self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=False,
            eval_metric="mlogloss",
            early_stopping_rounds=self.model.early_stopping_rounds,
        )
        self.trained = True
        return self.model

    def train_eval(self, X_train, y_train, X_val, y_val, X_test, y_test):
        print("Training model...\n")

        self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=0,
        )

        self.trained = True
        # print("Training complete.\n")

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
        #

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

    """FROM HERE STARTS THE OPTUNA PART"""

    def xgb_get_params(trial):
        params = {
            "objective": "multi:softmax",
            # "booster": "dart",  # trial.suggest_categorical("booster", ["gbtree", "dart"]),
            "n_jobs": -1,
            "verbosity": 0,
            "learning_rate": trial.suggest_float("learning_rate", 0.001, 0.7),
            "max_depth": trial.suggest_int("max_depth", 3, 20, step=1),
            # "max_leaves": trial.suggest_int("max_leaves", 10, 100, step=1),
            "n_estimators": trial.suggest_int("n_estimators", 200, 2000, step=10),
            # "num_parallel_tree": trial.suggest_int("n_estimators", 1, 10, step=1),
            # "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 100.0, log=True),
            # "reg_lambda": trial.suggest_float("reg_lambda", 0.0, 10.0, step=0.1),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0, step=0.1),
            # "max_delta_step": trial.suggest_int("max_delta_step", 1, 10, step=1),
            # "min_child_weight": trial.suggest_int("min_child_weight", 1, 10, step=1),
            "colsample_bytree": trial.suggest_float(
                "colsample_bytree", 0.1, 1.0, log=True
            ),
            # "colsample_bylevel": trial.suggest_float(
            #     "colsample_bylevel ", 0.1, 1.0, log=True
            # ),
            # "colsample_bynode": trial.suggest_float("colsample_bynode", 0.1, 1.0, log=True),
            # "rate_drop":   trial.suggest_float("rate_drop", 1e-8, 1.0, log=True),
            # "skip_drop":   trial.suggest_float("skip_drop", 1e-8, 1.0, log=True),
            # "scale_pos_weight": trial.suggest_float(
            #     "scale_pos_weight", 1.0, 10.0, step=0.1
            # ),
            "min_child_weight": trial.suggest_int(
                "min_child_weight", 1, 10, step=1
            ),  # Regularization
            "reg_alpha": trial.suggest_float(
                "reg_alpha", 1e-8, 10.0, log=True
            ),  # L1 regularization
            "reg_lambda": trial.suggest_float(
                "reg_lambda", 0.0, 10.0, step=0.1
            ),  # L2 regularization
            "eval_metric": "mlogloss",
            "random_state": 42,
        }
        return params

    # def create_objective(X_train, y_train, X_val, y_val) -> int | str:
    #     def objective(trial):
    #         params = xgb_get_params(trial)
    #         model = XGBTrainer(params=params)
    #         f1 = model.train_eval(X_train, y_train, X_val, y_val, X_test, y_test)
    #         # model = xgb.XGBClassifier(**params)
    #         # model.fit(X_train, y_train, X_val, y_val)
    #         # return model.score(X_val, y_val)

    #         return f1

    #     return objective

    # '''THIS PART IS TO BE EXECUTED IN THE NOTEBOOK'''

    # objective = create_objective(X_train, y_train, X_val, y_val)
    # sampler = optuna.samplers.TPESampler(seed=42)
    # study = optuna.create_study(
    #         #storage="/data",
    #         direction="maximize",
    #         sampler=sampler,
    #         study_name="optuna_seagrass",
    #         load_if_exists=True,
    #     )
    # study.optimize(objective, n_trials=1000)


if __name__ == "__main__":
    model = XGBTrainer().load()
    model.load()
