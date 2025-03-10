from datetime import datetime
from multiprocessing import set_start_method
import pandas as pd
from fastapi import APIRouter, FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
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
    import uvicorn
    uvicorn.run("seagrass_api.api.main:app", host="0.0.0.0", port=8000, reload=True)
