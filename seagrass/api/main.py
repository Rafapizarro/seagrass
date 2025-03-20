from datetime import datetime
from multiprocessing import set_start_method
import pandas as pd
import uvicorn
import os
import numpy as np
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import supabase

from seagrass.params import *

from seagrass.api.connexion import DBConnexion
from seagrass.ml_logic.model import XGBTrainer

app = FastAPI()
app.state.model = XGBTrainer().load()
# save the model into the state

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allpipows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def get_pred_point(data):
    if "model" not in app.state:
        raise HTTPException(status_code=404, detail="Error during loading")

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
        "depth": data["depth"],
    }

    # create df from values
    df = pd.DataFrame([res], columns=res.keys())

    # predict probabilities with loaded model
    probs = xgb_model.predict_proba(df)
    probs = {
        "coordinates": [res["lat"], res["lon"]],
        "targets": [float(p) for p in probs[0]],
        "features": {
            # "po4": res["po4"],
            # "no3": res["no3"],
            # "si": res["si"],
            # "nh4": res["nh4"],
            # "bottom_temp": res["bottom_temp"],
            "chlorophyll": chlorophyll if chlorophyll else None,
            # "avg_temp": res["avg_temp"],
            "salinity": res["salinity"],
            "depth": res["depth"],
        },
    }
    # return probabilities

    return probs


@app.get("/point")
# http://localhost:8000/predict?latitude=32.9999&longitudes=13.9999
def get_point_prediction(latitude: float, longitude: float):
    db_client = DBConnexion().get_connexion()

    result = (
        db_client.table("seagrass_features")
        .select("*")
        .eq("latitude", latitude)
        .eq("longitude", longitude)
        .execute()
    )

    if "data" in result:
        points_probs = [get_pred_point(p) for idx, p in enumerate(result.data)]

        # # Test return from API
        return {"preds": points_probs}
    else:
        return {"preds": []}


@app.get("/predict")
# http://localhost:8000/predict?latitudes=32.8125+32.9999&longitudes=13.8333+13.9999
def get_seagrass_prediction(latitudes: str, longitudes: str):
    if "model" not in app.state:
        raise HTTPException(status_code=404, detail="Error during loading")

    # load the model from the state
    xgb_model = app.state.model

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

    if "data" in result:
        points_probs = get_pred_point(result.data)

        # # Test return from API
        return {"preds": points_probs}
    else:
        return {"preds": []}
