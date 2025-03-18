import numpy as np
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer, LabelEncoder
from sklearn.model_selection import train_test_split
from colorama import Fore, Style


def preprocess_features(X: pd.DataFrame) -> np.ndarray:
    # TODO : ALL PREPROCESSING STEPS : feat. engineering, rescaler, encoder, etc
    encoder = LabelEncoder()

    # merge_df['FAMILY_lab_encoded'] = encoder.fit_transform(merge_df['FAMILY'])

    def create_sklearn_preprocessor() -> ColumnTransformer:
        return

    print(Fore.BLUE + "\nPreprocessing features..." + Style.RESET_ALL)

    preprocessor = create_sklearn_preprocessor()
    X_processed = preprocessor.fit_transform(X)

    print("✅ X_processed, with shape", X_processed.shape)

    return X_processed


def train_test_val_split(merge_df: pd.DataFrame):
    # Get the features and target from /data
    X = merge_df.drop(
        columns=[
            "index_right",
            "geometry",
            "int64_field_0",
            "datasetID",
            "BIO_CLASS",
            "fieldNotes",
            "habitat",
            "AREA_SQKM",
            "vernacular",
            "FAMILY",
            "GENUS",
            "scientific",
            "habitatID",
            "nameAccord",
            "eventDate",
            "verif",
            "Shape_Leng",
            "Shape_Area",
        ]
    )
    y = (
        merge_df["FAMILY"]
        .map(
            {
                None: 0,
                np.nan: 0,
                "Not reported": 1,
                "Posidoniaceae": 2,
                "Cymodoceaceae": 3,
                "Hydrocharitaceae": 1,
            }
        )
        .fillna(0)
    )

    # Split the data into training, validation, and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.25, random_state=42, stratify=y_train
    )

    print("X_train shape:", X_train.shape)
    print("X_val shape:", X_val.shape)
    print("y_train shape:", y_train.shape)
    print("y_val shape:", y_val.shape)
    print("X_test shape:", X_test.shape)
    print("y_test shape:", y_test.shape)

    return X_train, X_val, X_test, y_train, y_val, y_test
