import numpy as np

from seagrass_api.ml_logic.data import clean_data, get_data_with_cache, load_data_to_bq
from seagrass_api.ml_logic.registry import load_model, save_model
from seagrass_api.params import *

from pathlib import Path
import pandas as pd
from colorama import Fore, Style

def preprocess(
    # TODO : WHICH features we preprocess
    features: list=[]
) -> None:
    """
    Requests for all data needed
    """
    # TODO : TO CHANGE IF WE WANT ANOTHER TABLE
    table_name = "seagrass"

    # Selection of the BQ table
    bq_table = TABLE_NAMES[table_name]

    # Selection of the features
    # TODO : pass into query builders : https://dev.to/chanon-mike/using-python-and-orm-sqlalchemy-with-google-bigquery-4gga
    query = f"""
        SELECT *
        FROM `{GCP_PROJECT}`.{BQ_DATASET}.{bq_table}_{DATA_SIZE}
        WHERE condition
        ORDER BY pickup_datetime
    """

    # Retrieve data using `get_data_with_cache`
    # TODO : save data with specific features
    data_query_cache_path = Path(LOCAL_DATA_PATH).joinpath("raw", f"query_{features}_{DATA_SIZE}.csv")
    data_query = get_data_with_cache(
        query=query,
        gcp_project=GCP_PROJECT,
        cache_path=data_query_cache_path,
        data_has_header=True
    )

    # Process data
    # TODO : clean all data
    data_clean = clean_data(data_query)

    # TODO : ALL PREPROCESS STEPS
    # TODO : split ?
    # TODO : preprocess_features(X)
    data_processed = pd.DataFrame([])

    # TODO : load data preprocessed into BigQuery
    load_data_to_bq(
        data_processed,
        gcp_project=GCP_PROJECT,
        bq_dataset=BQ_DATASET,
        table=f'processed_{DATA_SIZE}',
        truncate=True
    )


def train(
        # TODO : WHICH features the user want
        features: list=[],
        split_ratio: float = 0.02, # 0.02 represents ~ 1 month of validation data on a 2009-2015 train set
        learning_rate=0.0005,
        batch_size = 256,
        patience = 2
    ) -> float:
    # TODO : TO CHANGE IF WE WANT ANOTHER TABLE
    table_name = "seagrass"

    # Selection of the BQ table
    bq_table = TABLE_NAMES[table_name]

    # Selection of the features
    # TODO : pass into query builders : https://dev.to/chanon-mike/using-python-and-orm-sqlalchemy-with-google-bigquery-4gga
    query = f"""
        SELECT *
        FROM `{GCP_PROJECT}`.{BQ_DATASET}.{bq_table}_{DATA_SIZE}
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
        features: list=[],
        stage: str = "Production"
    ) -> float:
    """
    Evaluate the performance of the latest production model on processed data
    Return METRICS
    """
    print(Fore.MAGENTA + "\n⭐️ Use case: evaluate" + Style.RESET_ALL)

    # TODO : check if we can loed models
    model = load_model(stage=stage)
    assert model is not None

    # TODO : handle the features
    # Query your BigQuery processed table and get data_processed using `get_data_with_cache`
    query = f"""
        SELECT * EXCEPT(_0)
        FROM `{GCP_PROJECT}`.{BQ_DATASET}.processed_{DATA_SIZE}
        WHERE {features}'
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
    preprocess()
    train()
    evaluate()
    pred()
