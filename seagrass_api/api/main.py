from datetime import datetime
from multiprocessing import set_start_method
import pandas as pd
import uvicorn
from fastapi import APIRouter, FastAPI
from seagrass_api.ml_logic.registry import load_model
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# app.state.model = load_model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allpipows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/predict")
def predict():
    """
    """
    return {'prediction': 'flower'}



@app.get("/")
def root():
    return {'greeting': 'Hello'}


if __name__ == "__main__":
    uvicorn.run("seagrass_api.api.main:app", host="0.0.0.0", port=8000, reload=True)
