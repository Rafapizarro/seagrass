import os
import pandas as pd
import geopandas as gpd
from seagrass.params import *
from pathlib import Path
from shapely import wkt
from google.cloud import bigquery


def load_features(
    cache_path:Path,
    limit=None) -> gpd.GeoDataFrame:
    """
    Positional Argument: complete local path to your features parquet file.
    Output: Features GeoDataFrame.
    """

    if Path(cache_path).is_file():
        print("\nLoad data from local Parquet...")
        data = pd.read_parquet(cache_path)
        df = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.lon, data.lat))
        df.crs = "EPSG:32633"
        df.to_crs("EPSG:32633")
    else:
        print("\nLoad data from BigQuery server...")
        client = bigquery.Client()
        query = """
        SELECT *
        FROM `seagrass-lewagon.seagrass.merged_features`
        """
        if limit:
            query += f" LIMIT {limit}"
        data = client.query(query).to_dataframe()
        df = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.lon, data.lat))
        df.crs = "EPSG:32633"
        df.to_crs("EPSG:32633")
        df.to_parquet(cache_path)

    return df


def load_targets(
    cache_path:Path,
    limit=None) -> gpd.GeoDataFrame:
    """
    cache_path: Complete local path to your target parquet file.
    Output: Target GeoDataFrame.
    """

    if Path(cache_path).is_file():
        print("\nLoad data from local Parquet...")
        data = pd.read_parquet(cache_path)
        data["coordinates"] = data["coordinates"].apply(wkt.loads)
        df = gpd.GeoDataFrame(data, geometry="coordinates")
        df.crs = "EPSG:32633"
        df.to_crs("EPSG:32633")

    else:
        print("\nLoad data from BigQuery...")
        client = bigquery.Client()
        query = f"""
        SELECT *
        FROM `seagrass-lewagon.seagrass.seagrass_global_target`
        """
        if limit:
            query += f" LIMIT {limit}"
        data = client.query(query).to_dataframe()
        data.to_parquet(cache_path)
        data["coordinates"] = data["coordinates"].apply(wkt.loads)
        df = gpd.GeoDataFrame(data, geometry="coordinates")
        df.crs = "EPSG:32633"
        df.to_crs("EPSG:32633")

    return df

def merge_data(
    features: gpd.GeoDataFrame,
    targets: gpd.GeoDataFrame,
    max_distance:int) -> gpd.GeoDataFrame:
    """
    features: Features GeoDataFrame. targets: Target GeoDataFrame,
    max_distance: Distance margin allowed between polygons and points for joining.
    Coordinate distance (e.g. 0.01 is ~1 km).
    Output: Merged geoDataFrame (left-join).
    """
    print("\nMerging files...")
    df = gpd.sjoin_nearest(features, targets, how="left",max_distance=max_distance)
    print("\nFiles merged!")

    return df

if __name__ == "__main__":
    features = load_features(cache_path=os.path.join(f"{LOCAL_DATA_PATH}",f"{BQ_DATASET}_features.parquet"))
    targets = load_targets(cache_path=os.path.join(f"{LOCAL_DATA_PATH}",f"{BQ_DATASET}_target.parquet"))
    df = merge_data(features, targets, max_distance=1000)
    print(df.head())
