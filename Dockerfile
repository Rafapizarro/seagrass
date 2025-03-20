FROM python:3.10.6

COPY requirements_prod.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY seagrass /seagrass
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
COPY 0.578xgb.ubj root/.seagrass/mlops/training_outputs/models/0.578xgb.ubj
=======
>>>>>>> 18dbd0ae0e921d8370ea73d4380007ece1d3e54b
=======
>>>>>>> 18dbd0ae0e921d8370ea73d4380007ece1d3e54b
=======
COPY 0.578xgb.ubj root/.seagrass/mlops/training_outputs/models/0.578xgb.ubj
>>>>>>> d04b5d7b2ebf61935a50d57d94b9dcacc17ac328
# COPY tests /tests

CMD uvicorn seagrass.api.main:app --host 0.0.0.0 --port $PORT
