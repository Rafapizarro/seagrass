from datetime import datetime
from multiprocessing import set_start_method
import pandas as pd
import uvicorn
import os
import numpy as np
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import supabase

from seagrass.params import *

from seagrass.api.connexion import DBConnexion
from seagrass.ml_logic.model import XGBTrainer

app = FastAPI()
<<<<<<< HEAD
<<<<<<< HEAD
app.state.model = XGBTrainer().load()
# save the model into the state
=======
# load the model into the state
>>>>>>> 18dbd0ae0e921d8370ea73d4380007ece1d3e54b
=======
# load the model into the state
>>>>>>> 18dbd0ae0e921d8370ea73d4380007ece1d3e54b

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allpipows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/predict")
<<<<<<< HEAD
<<<<<<< HEAD
# http://localhost:8000/predict?latitudes=32.8125+32.9999&longitudes=13.8333+13.9999
def get_seagrass_prediction(latitudes: str, longitudes: str):
    # load the model from the state
    xgb_model = app.state.model

    lats = latitudes.split(" ")
    longs = longitudes.split(" ")

    db_client = DBConnexion().get_connexion()

    # result = (
    #     db_client.table("seagrass_features")
    #     .select("*")
    #     .eq("latitude", latitudes)
    #     .eq("longitude", longitudes)
    #     .execute()
    # )
    result = (
        db_client.table("seagrass_features")
        .select("*")
        .gt("latitude", float(lats[0]))
        .lt("latitude", float(lats[1]))
        .gt("longitude", float(longs[0]))
        .lt("longitude", float(longs[1]))
        .execute()
    )
    # return result.data

    def get_all_pred_points(data):
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
        }
        # return probabilities

        return probs

    points_probs = [get_all_pred_points(p) for idx, p in enumerate(result.data)]

    # # Test return from API
    return {"preds": points_probs}
=======
# http://localhost:8000/predict?latitudes=40,41&longitudes=-1,0
def get_seagrass_prediction(latitudes: str, longitudes: str):
    # load the model from the state

    #create random placeholder values

    # create df from random placeholder values

    # predict probabilities with loaded model

    #return probabilities
    latitudes = latitudes.split(",")
    longitudes = longitudes.split(",")

    # Test return from API
    return {"latitudes": latitudes, "longitudes": longitudes}
>>>>>>> 18dbd0ae0e921d8370ea73d4380007ece1d3e54b
=======
# http://localhost:8000/predict?latitudes=40,41&longitudes=-1,0
def get_seagrass_prediction(latitudes: str, longitudes: str):
    # load the model from the state

    #create random placeholder values

    # create df from random placeholder values

    # predict probabilities with loaded model

    #return probabilities
    latitudes = latitudes.split(",")
    longitudes = longitudes.split(",")

    # Test return from API
    return {"latitudes": latitudes, "longitudes": longitudes}
>>>>>>> 18dbd0ae0e921d8370ea73d4380007ece1d3e54b
