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

    def train(self, X_train, y_train, X_val, y_val):
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
