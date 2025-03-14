from datetime import datetime
from multiprocessing import set_start_method
import pandas as pd
import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allpipows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/predict")
# http://localhost:8000/predict?latitudes=40,41&longitudes=-1,0
def get_seagrass_prediction(latitudes: str, longitudes: str):
    latitudes = latitudes.split(",")
    longitudes = longitudes.split(",")

    # Test return from API
    return {"latitudes": latitudes, "longitudes": longitudes}
