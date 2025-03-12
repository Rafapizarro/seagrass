import numpy as np
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from colorama import Fore, Style

def preprocess_features(X: pd.DataFrame) -> np.ndarray:
    # TODO : ALL PREPROCESSING STEPS : feat. engineering, rescaler, encoder, etc
    def create_sklearn_preprocessor() -> ColumnTransformer:
        return

    print(Fore.BLUE + "\nPreprocessing features..." + Style.RESET_ALL)

    preprocessor = create_sklearn_preprocessor()
    X_processed = preprocessor.fit_transform(X)

    print("✅ X_processed, with shape", X_processed.shape)

    return X_processed
