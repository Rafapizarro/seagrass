import os
import xgboost as xgb
from pathlib import Path
from sklearn.metrics import f1_score, classification_report
from seagrass.params import LOCAL_REGISTRY_PATH
from sklearn.utils.class_weight import compute_sample_weight


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


    def fit_model(self, X_train, y_train, X_val, y_val):
        sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)
        self.model.fit(
            X_train,
            y_train,
            sample_weight=sample_weight,
            eval_set=[(X_val, y_val)],
            verbose=False,
            eval_metric="mlogloss",
            early_stopping_rounds=self.model.early_stopping_rounds,
        )
        self.trained = True
        return self


    def train_eval(self, X_train, y_train, X_val, y_val, X_test, y_test):
        print("Training model...")

        sample_weight = compute_sample_weight(class_weight="balanced", y=y_train)

        self.model.fit(
            X_train,
            y_train,
            sample_weight=sample_weight,
            eval_set=[(X_val, y_val)],
            verbose=0,
        )
        self.trained = True
        print("Training complete.\n")

        y_pred_proba = self.model.predict_proba(X_test)
        y_pred = y_pred_proba.argmax(axis=1)

        f1 = f1_score(y_test, y_pred, average="macro")
        # class_report = classification_report(y_test, y_pred)
        # print(class_report)

        print(f"Macro F1 score: {f1:.6f}\n")

        return f1


    def save(self, f1: float):
        self.f1 = f1

        if not self.trained:
            raise ValueError("\nError: Model must be trained before saving.\n")

        self.model_path = os.path.join(
            LOCAL_REGISTRY_PATH, "models", f"{f1:.3f}xgb.ubj"
        )

        os.makedirs(os.path.join(LOCAL_REGISTRY_PATH, "models"), exist_ok=True)
        self.model.save_model(self.model_path)
        print("\nModel saved.\n")

    def load(self):
        if not Path(self.model_path).is_file():
            raise ValueError("\nError: Model must be saved before loading.\n")

        model = self.model.load_model(self.model_path)

        return model
