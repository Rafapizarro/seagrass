import numpy as np
import os

from numerize import numerize

from seagrass.ml_logic.registry import load_model, save_model

from pathlib import Path
import pandas as pd
from colorama import Fore, Style

from seagrass.ml_logic.load_data import load_features, load_targets, merge_data
from seagrass.params import BQ_DATASET, GCP_PROJECT, LOCAL_DATA_PATH
from seagrass.utils import stringify_crs_distance, get_data_size

def preprocess(
    max_distance=0.01,
    limit=None
) -> None:
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
    # TODO : save data with :
    #   - size of data
    #   - CRS distance

    # Set limit of the data to train
    size_data = get_data_size(limit)

    # Set CRS distance for the points embedded in the target polygons
    str_crs_distance = stringify_crs_distance(max_distance)

    print(f"Merge data with {size_data} data size, CRS : {str_crs_distance} km")

    features_cache_path = os.path.join(f"{LOCAL_DATA_PATH}",f"{BQ_DATASET}_features_{size_data}.parquet")
    targets_cache_path = os.path.join(f"{LOCAL_DATA_PATH}",f"{BQ_DATASET}_targets_{size_data}.parquet")

    main_data_cache_path = os.path.join(f"{LOCAL_DATA_PATH}",f"{BQ_DATASET}_data_{size_data}_{str_crs_distance}_km.parquet")

    features = load_features(features_cache_path, limit)
    targets = load_targets(targets_cache_path, limit)

    data_query = merge_data(
        cache_path=main_data_cache_path,
        features=features,
        targets=targets,
        max_distance=max_distance,
        size_data=size_data
    )

    # Process data
    # # TODO : clean all data
    # data_clean = clean_data(data_query)


def train(
        # TODO : WHICH features the user want
        max_distance=0.01,
        limit=None,
        split_ratio: float = 0.02, # 0.02 represents ~ 1 month of validation data on a 2009-2015 train set
        learning_rate=0.0005,
        batch_size = 256,
        patience = 2
    ) -> float:
    # TODO : train data with :
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
    query = f"""
        SELECT *
        FROM `{GCP_PROJECT}`.{BQ_DATASET}.{bq_table}
        WHERE condition
        ORDER BY pickup_datetime
    """
    # TODO : Fetch preprocess data

    # TODO : Split the data (train, val ?, test ?)

    model = load_model()

    # TODO : Init model (+ compile if needed)

    # TODO : Train model

    # TODO : Save the results : locally / distant
    # save_results(params=params, metrics=dict(mae=val_mae))

    # Save model weight on the hard drive (and optionally on GCS too!)
    save_model(model=model)

    return

def evaluate(
        # TODO : WHICH features we evaluate
        max_distance=0.01,
        limit=None,
        stage: str = "Production"
    ) -> float:
    """
    Evaluate the performance of the latest production model on processed data
    Return METRICS
    """
    # TODO : evaluate data with :
    #   - size of data
    #   - CRS distance

    # Set limit of the data to train
    size_data = get_data_size(limit)

    # Set CRS distance for the points embedded in the target polygons
    crs_distance = stringify_crs_distance(max_distance)

    # Selection of the BQ table
    bq_table = f"data_{size_data}_{crs_distance}_km"

    print(Fore.MAGENTA + "\n⭐️ Use case: evaluate" + Style.RESET_ALL)

    # TODO : check if we can loed models
    model = load_model(stage=stage)
    assert model is not None

    # TODO : handle the features
    # Query your BigQuery processed table and get data_processed using `get_data_with_cache`
    query = f"""
        SELECT *
        FROM `{GCP_PROJECT}`.{BQ_DATASET}.{bq_table}
        WHERE condition
        ORDER BY pickup_datetime
    """

    return

def pred(X_pred: pd.DataFrame = None) -> np.ndarray:
    print("\n⭐️ Use case: predict")

    if X_pred is None:
        X_pred = pd.DataFrame(dict(
        # TODO : insert the fetures from users
    ))

    model = load_model()
    assert model is not None

    # TODO : preprocess and make predictions

    return

if __name__ == '__main__':
    # TODO : MAKE THE PIPELINE
    preprocess(max_distance=0.01, limit=10000)
    # train(max_distance=0.01, limit=10000)
    # evaluate(max_distance=0.01, limit=10000)
    # pred()
