from datetime import datetime
from multiprocessing import set_start_method
import pandas as pd
import uvicorn
import os
import numpy as np
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import supabase
import json

from seagrass.params import *

from seagrass.api.connexion import DBConnexion
from seagrass.ml_logic.model import XGBTrainer

app = FastAPI()
app.state.model = XGBTrainer().load()
# if not app.state.model:
#     raise HTTPException(status_code=500, detail="ML model is not loaded.")

# save the model into the state
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allpipows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Get prediction for one specfic point
def get_pred_point(data):
    # load the model from the state
    xgb_model = app.state.model

    chlorophyll = data["trend"] if data["trend"] else np.nan

    # create values
    res = {
        "lat": data["latitude"],
        "lon": data["longitude"],
        "po4": data["po4"],
        "no3": data["no3"],
        "si": data["si"],
        "nh4": data["nh4"],
        "bottom_temp": data["bottomT"],
        "chlorophyll": chlorophyll,
        "avg_temp": data["thetao"],
        "salinity": data["so"],
        # "depth": data["depth"],
    }

    # create df from values
    df = pd.DataFrame([res], columns=res.keys())

    # predict probabilities with loaded model for 1 point
    probs = xgb_model.predict_proba(df)

    # return the prediction for 1 point
    probs = {
        "coordinates": [float(res["lat"]), float(res["lon"])],
        "targets": [float(p) for p in probs[0]],
        "features": {
            "po4": res["po4"],
            "no3": res["no3"],
            "si": res["si"],
            "nh4": res["nh4"],
            "bottom_temp": res["bottom_temp"],
            "chlorophyll": 0.0 if np.isnan(chlorophyll) else float(chlorophyll),
            "avg_temp": res["avg_temp"],
            "salinity": float(res["salinity"]),
            # "depth": float(res["depth"]),
        },
    }

    return probs


@app.get("/predict")
# http://localhost:8000/predict?latitudes=32.8125+32.9999&longitudes=13.8333+13.9999
def get_seagrass_prediction(latitudes: str, longitudes: str):
    # load the model from the state
    lats = latitudes.split(" ")
    longs = longitudes.split(" ")

    db_client = DBConnexion().get_connexion()

    result = (
        db_client.table("seagrass_features")
        .select("*")
        .gt("latitude", float(lats[0]))
        .lt("latitude", float(lats[1]))
        .gt("longitude", float(longs[0]))
        .lt("longitude", float(longs[1]))
        .execute()
    )

    if "data" in result.__dict__:
        if len(result.data) == 0:
            return {"preds": [{"error": "No data available for all of these points"}]}

        points_probs = [get_pred_point(p) for p in result.data]

        return {"preds": points_probs}

    else:
        return {"preds": [{"error": "No data available for all of these points"}]}


@app.get("/point")
# http://localhost:8000/point?latitude=-0.103683&longitude=39.458993
def get_point_prediction(latitude: float, longitude: float):
    db_client = DBConnexion().get_connexion()

    result = db_client.rpc(
        "get_closest_point", {"target_lon": longitude, "target_lat": latitude}
    ).execute()

    if "data" in result.__dict__:
        # check distance between the point and the closest point
        if float(result.data[0]["distance"]) > 0.1:
            return {"preds": [{"error": "No data available for this point"}]}

        point_prob = get_pred_point(result.data[0])

        # # Test return from API
        return {"preds": [point_prob]}
    else:
        return {"preds": [{"error": "No data available for this point"}]}
