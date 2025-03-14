import os
import pandas as pd
import geopandas as gpd
from shapely import wkt
from pathlib import Path
from seagrass.ml_logic.data import load_data_to_bq
from seagrass.params import *
from google.cloud import bigquery

from seagrass.utils import stringify_crs_distance


def load_features(cache_path: Path, limit=None) -> gpd.GeoDataFrame:
    """
    Load features data from local cache or BigQuery.

    Parameters
    ----------
    cache_path : Path
        Local path to your features parquet file.
    limit : int, optional
        Limit the number of rows fetched from BigQuery.

    Returns
    -------
    GeoDataFrame
        Features data with CRS set to EPSG:4326.
    """

    if Path(cache_path).is_file():
        print("\nLoad data from local Parquet file...")
        data = pd.read_parquet(cache_path)

    else:
        print("\nLoad data from BigQuery server...")
        client = bigquery.Client()
        query = f"""
        SELECT *
        FROM `{GCP_PROJECT}.{BQ_DATASET}.merged_features`
        """
        if limit:
            query += f" LIMIT {limit}"
        data = client.query(query).to_dataframe()
        data.to_parquet(cache_path)

    gdf = gpd.GeoDataFrame(
        data, geometry=gpd.points_from_xy(data.lon, data.lat), crs="EPSG:32633"
    )

    return gdf


def load_targets(cache_path: Path, limit=None) -> gpd.GeoDataFrame:
    """
    Load target data from local cache or BigQuery.

    Parameters
    ----------
    cache_path : Path
        Local path to your features target file.
    limit : int, optional
        Limit the number of rows fetched from BigQuery.

    Returns
    -------
    GeoDataFrame
        Target data with CRS set to EPSG:32633.
    """

    if Path(cache_path).is_file():
        print("\nLoad data from local Parquet file...")
        data = pd.read_parquet(cache_path)

    else:
        print("\nLoad data from BigQuery server...")
        client = bigquery.Client()
        query = f"""
        SELECT *
        FROM `{GCP_PROJECT}.{BQ_DATASET}.seagrass_global_target`
        """
        if limit:
            query += f" LIMIT {limit}"
        data = client.query(query).to_dataframe()
        data.to_parquet(cache_path)

    data["coordinates"] = data["coordinates"].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(data, geometry="coordinates", crs="EPSG:32633")

    return gdf


def merge_data(
    features: gpd.GeoDataFrame,
    targets: gpd.GeoDataFrame,
    cache_path: Path,
    size_data="all",
    max_distance=0.01,
) -> gpd.GeoDataFrame:
    """
    Merge feature and target GeoDataFrames using a spatial nearest join.

    Parameters
    ----------
    features : gpd.GeoDataFrame
        Feature data with CRS set to EPSG:32633.
    targets : gpd.GeoDataFrame
        Target data with CRS set to EPSG:32633.
    max_distance : float
        Maximum distance (in CRS units) allowed between polygons and points for joining.
        For EEPSG:3035, distance is measured in meters (e.g., 0.01 degrees = ~1 km).

    Returns
    -------
    gpd.GeoDataFrame
        Merged GeoDataFrame resulting from a left spatial join.
    """
    if Path(cache_path).is_file():
        print("\nLoad data from local Parquet file...")
        df = pd.read_parquet(cache_path)

    else:
        print("\nMerging files...")
        df = gpd.sjoin_nearest(features, targets, how="left", max_distance=max_distance)
        df["geometry"] = df["geometry"].apply(wkt.dumps)

        # Save all main data to local files
        df.to_parquet(cache_path)

        # Set CRS distance for the points embedded in the target polygons
        crs_distance = stringify_crs_distance(max_distance)

        # TODO : load data preprocessed into BigQuery
        load_data_to_bq(
            df,
            gcp_project=GCP_PROJECT,
            bq_dataset=BQ_DATASET,
            table=f"data_{size_data}_{crs_distance}_km",
            truncate=True,
        )
        print("\nFiles merged!")

    return df


# if __name__ == "__main__":
# features = load_features(cache_path=os.path.join(f"{LOCAL_DATA_PATH}",f"{BQ_DATASET}_features.parquet"))
# targets = load_targets(cache_path=os.path.join(f"{LOCAL_DATA_PATH}",f"{BQ_DATASET}_targets.parquet"))
# df = merge_data(cache_path=os.path.join(f"{LOCAL_DATA_PATH}",f"{BQ_DATASET}_features.parquet"), features,targets)
