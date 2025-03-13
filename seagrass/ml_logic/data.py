from pathlib import Path
import pandas as pd
from colorama import Fore, Style
from google.cloud import bigquery

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # TODO : CLEAN DATA STEP
    print("✅ data cleaned")

    return df


def get_data_with_cache(
        gcp_project:str,
        query:str,
        cache_path:Path,
        data_has_header=True
    ) -> pd.DataFrame:
    """
    Retrieve `query` data from BigQuery, or from `cache_path` if the file exists
    Store at `cache_path` if retrieved from BigQuery for future use
    """
    # # TODO : change the code if we want this locally / BigQuery
    # if cache_path.is_file():
    #     print(Fore.BLUE + "\nLoad data from local CSV..." + Style.RESET_ALL)
    #     df = pd.read_csv(cache_path, header='infer' if data_has_header else None)
    # else:

    print(Fore.BLUE + "\nLoad data from BigQuery server..." + Style.RESET_ALL)
    # TODO : load from BigQuery
    client = bigquery.Client(project=gcp_project)
    query_job = client.query(query)
    result = query_job.result()
    df = result.to_dataframe()

    # # Store as CSV if the BQ query returned at least one valid line
    # if df.shape[0] > 1:
    #     df.to_csv(cache_path, header=data_has_header, index=False)

    print(f"✅ Data loaded, with shape {df.shape}")

    return df


def load_data_to_bq(
        data: pd.DataFrame,
        gcp_project:str,
        bq_dataset:str,
        table: str,
        truncate: bool
    ) -> None:
    """
    - Save the DataFrame to BigQuery
    - Empty the table beforehand if `truncate` is True, append otherwise
    """

    assert isinstance(data, pd.DataFrame)
    # Load data onto full_table_name
    # TODO : change table if needed
    full_table_name = f"{gcp_project}.{bq_dataset}.{table}"

    print(Fore.BLUE + f"\nSave data to BigQuery @ {full_table_name}...:" + Style.RESET_ALL)

    # TODO : change according to columns we want
    data.columns = [f"_{column}" if not str(column)[0].isalpha() and not str(column)[0] == "_" else str(column) for column in data.columns]

    client = bigquery.Client()

    # Define write mode and schema
    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    print(f"\n{'Write' if truncate else 'Append'} {full_table_name} ({data.shape[0]} rows)")

    # Load data
    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  # wait for the job to complete

    print(f"✅ Data saved to bigquery, with shape {data.shape}")
