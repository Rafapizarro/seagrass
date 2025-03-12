import pandas as pd
import geopandas as gpd
from shapely import wkt
from google.cloud import bigquery


def load_features(limit=None) -> gpd.GeoDataFrame:
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
    df = df.to_crs("EPSG:32633")
    return df

def load_targets(limit=None) -> gpd.GeoDataFrame:
    client = bigquery.Client()
    query = f"""
    SELECT *
    FROM `seagrass-lewagon.seagrass.seagrass_global_target`
    """

    if limit:
        query += f" LIMIT {limit}"
        print(query)

    data = client.query(query).to_dataframe()
    data["coordinates"] = data["coordinates"].apply(wkt.loads)
    df = gpd.GeoDataFrame(data, geometry="coordinates")
    df.crs = "EPSG:32633"
    df = df.to_crs("EPSG:32633")
    return df

def merge_data(features: gpd.GeoDataFrame, targets: gpd.GeoDataFrame,max_distance:int) -> gpd.GeoDataFrame:
    df = gpd.sjoin_nearest(features, targets, how="left",max_distance=max_distance)
    return df

if __name__ == "__main__":
    features = load_features()
    targets = load_targets()
    df = merge_data(features, targets, max_distance=1000)
    print(df.head())
