from datetime import datetime
from multiprocessing import set_start_method
import pandas as pd
import uvicorn
from fastapi import APIRouter, FastAPI
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


@app.get("/predict")
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
        # create values
        res = {
            "lat": data["latitude"],
            "lon": data["longitude"],
            "po4": data["po4"],
            "no3": data["no3"],
            "si": data["si"],
            "nh4": data["nh4"],
            "bottom_temp": data["bottomT"],
            "chlorophyll": data["trend"],
            "avg_temp": data["thetao"],
            "salinity": data["so"],
            "depth": data["depth"],
        }

        # create df from values
        df = pd.DataFrame([res], columns=res.keys())

        # predict probabilities with loaded model
        probs = xgb_model.predict_proba(df)
        probs = {
            "coordinates": f"{data['latitude']}, {data['longitude']}",
            "targets": [float(p) for p in probs[0]],
        }
        # return probabilities

        return probs

    points_probs = [get_all_pred_points(p) for idx, p in enumerate(result.data)]

    # # Test return from API
    return {"preds": points_probs}
