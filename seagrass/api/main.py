from datetime import datetime
from multiprocessing import set_start_method
import pandas as pd
import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
# http://localhost:8000/predict?latitudes=40,41&longitudes=-1,0
def get_seagrass_prediction(latitudes: float, longitudes: float):
    # load the model from the state
    xgb_model = app.state.model

    # create random placeholder values
    res = {
        "lat": latitudes,
        "lon": longitudes,
        "po4": 0.024890,
        "no3": 0.100141,
        "si": 4.213321,
        "nh4": 0.037484,
        "bottom_temp": 12.952122,
        "chlorophyll": -0.453486,
        "avg_temp": 19.954823,
        "salinity": 37.309742,
        "depth": -0.422800,
    }

    # create df from random placeholder values
    df = pd.DataFrame([res])

    # predict probabilities with loaded model
    probs = xgb_model.predict_proba(df)
    probs = [float(p) for p in probs[0]]
    # return probabilities
    # latitudes = latitudes.split(",")
    # longitudes = longitudes.split(",")

    # Test return from API
    return {"pred": probs}
