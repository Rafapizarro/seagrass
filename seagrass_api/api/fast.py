from datetime import datetime
from multiprocessing import set_start_method
import pandas as pd
from fastapi import APIRouter, FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()
# app = FastAPI()
# app.state.model = load_model()


# print("API predict step")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

@router.get("/predict")
def predict():
    """
    """
    return {'prediction': 'flower'}



@router.get("/")
def root():
    return {'greeting': 'Hello'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("taxifare.api.fast:app", host="0.0.0.0", port=8000, reload=True)
