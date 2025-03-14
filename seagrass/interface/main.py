import os
import numpy as np
import geopandas as gpd
from pathlib import Path
from seagrass.ml_logic.model import XGBTrainer
from sklearn.model_selection import train_test_split
from seagrass.ml_logic.load_data import load_features, load_targets, merge_data
from seagrass.params import LOCAL_DATA_PATH, BQ_DATASET, FEATURE_LABELS, TARGET_LABEL


def get_data(merged_data_path) -> gpd.GeoDataFrame:
    """
    Requests for all data needed
    """
    if Path(merged_data_path).is_file():
        print("\nLoad merged data from local Parquet file...\n")
        data = gpd.read_parquet(merged_data_path)
    else:
        features = load_features(
            cache_path=os.path.join(
                f"{LOCAL_DATA_PATH}", f"{BQ_DATASET}_features.parquet"
            )
        )
        target = load_targets(
            cache_path=os.path.join(
                f"{LOCAL_DATA_PATH}", f"{BQ_DATASET}_target.parquet"
            )
        )
        data = merge_data(
            cache_path=merged_data_path,
            features=features,
            targets=target,
            max_distance=0.01,
        )

    return data


def train():
    merge_data_path = os.path.join(f"{LOCAL_DATA_PATH}", f"{BQ_DATASET}_merged.parquet")
    df = get_data(merged_data_path=merge_data_path)
    target_map = {
        None: 0,
        "Not reported": 1,
        "Posidoniaceae": 2,
        "Cymodoceaceae": 3,
        "Hydrocharitaceae": 4,
    }
    X = df[FEATURE_LABELS]
    y = df[TARGET_LABEL].map(target_map)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.25, stratify=y_train, random_state=42
    )

    model = XGBTrainer()

    f1 = model.train(X_train, y_train, X_val, y_val)

    model.save(f1)

    return X_test, y_test


def load_model():
    model = XGBTrainer()
    model.load()


if __name__ == "__main__":
    load_model()
