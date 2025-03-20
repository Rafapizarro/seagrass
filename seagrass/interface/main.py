import os
import numpy as np
import os

from sklearn.model_selection import train_test_split

from seagrass.ml_logic.preprocessor import train_test_val_split

import geopandas as gpd
from pathlib import Path
from seagrass.ml_logic.model import XGBTrainer, Clusterer

from seagrass.ml_logic.load_data import load_features, load_targets, merge_data
from seagrass.params import (
    BQ_DATASET,
    FEATURE_LABELS,
    GCP_PROJECT,
    LOCAL_DATA_PATH,
    TARGET_LABEL,
)
from seagrass.utils import stringify_crs_distance, get_data_size


def preprocess(max_distance=0.01, limit=None) -> None:
    """
    Requests and preprocess the data needed.

    Parameters
    ----------
    max_distance : float
        Maximum distance (in CRS units) allowed between polygons and points for joining.
        For EEPSG:3035, distance is measured in meters (e.g., 1000 = 1 km).
    limit : int or None
        Size of the data requested.
        If None, fetch all.

    Returns
    -------
    gpd.GeoDataFrame
        Merged GeoDataFrame resulting from a left spatial join.
    """
    # Save data with :
    #   - size of data
    #   - CRS distance

    # Set limit of the data to train
    size_data = get_data_size(limit)

    # Set CRS distance for the points embedded in the target polygons
    str_crs_distance = stringify_crs_distance(max_distance)

    print(f"Merge data with {size_data} data size, CRS : {str_crs_distance} km")

    features_cache_path = os.path.join(
        f"{LOCAL_DATA_PATH}", f"{BQ_DATASET}_features_{size_data}.parquet"
    )
    targets_cache_path = os.path.join(
        f"{LOCAL_DATA_PATH}", f"{BQ_DATASET}_targets_{size_data}.parquet"
    )

    main_data_cache_path = os.path.join(
        f"{LOCAL_DATA_PATH}",
        f"{BQ_DATASET}_data_{size_data}_{str_crs_distance}_km.parquet",
    )

    features = load_features(features_cache_path, limit)
    targets = load_targets(targets_cache_path, limit)

    data_query = merge_data(
        cache_path=main_data_cache_path,
        features=features,
        targets=targets,
        max_distance=max_distance,
        size_data=size_data,
    )

    # Process data
    # # TODO : clean all data
    # data_clean = clean_data(data_query)


def train(
    # TODO : WHICH features the user want
    max_distance=0.01,
    limit=None,
    split_ratio: float = 0.02,  # 0.02 represents ~ 1 month of validation data on a 2009-2015 train set
    learning_rate=0.0005,
    batch_size=256,
    patience=2,
) -> float:
    # train data with :
    #   - size of data
    #   - CRS distance

    # Set limit of the data to train
    size_data = get_data_size(limit)

    # Set CRS distance for the points embedded in the target polygons
    str_crs_distance = stringify_crs_distance(max_distance)

    # Selection of the BQ table
    bq_table = f"data_{size_data}_{str_crs_distance}_km"

    # Selection of the features
    # TODO : pass into query builders : https://dev.to/chanon-mike/using-python-and-orm-sqlalchemy-with-google-bigquery-4gga
    # query = f"""
    #     SELECT *
    #     FROM `{GCP_PROJECT}`.{BQ_DATASET}.{bq_table}
    #     WHERE condition
    #     ORDER BY pickup_datetime
    # """
    print(f"{BQ_DATASET}_{bq_table}.parquet")
    main_data_cache_path = os.path.join(
        f"{LOCAL_DATA_PATH}", f"{BQ_DATASET}_{bq_table}.parquet"
    )
    df = gpd.read_parquet(main_data_cache_path)

    # TODO : Fetch preprocess data
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

    X_train, X_val, X_test, y_train, y_val, y_test = train_test_val_split(df)

    model = XGBTrainer()

    f1 = model.train_eval(X_train, y_train, X_val, y_val, X_test, y_test)

    model.save(f1)

    return X_test, y_test


def evaluate(
    max_distance=0.01,
    limit=None,
):
    model = XGBTrainer()
    model.load()


if __name__ == "__main__":
    # TODO : MAKE THE PIPELINE
    preprocess(max_distance=0.01)
    train(max_distance=0.01)
    # evaluate(max_distance=0.01)
    # pred()
