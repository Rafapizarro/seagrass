FROM python:3.10.6

COPY requirements_prod.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY seagrass /seagrass
COPY 0.825_xgb.ubj /root/.seagrass/mlops/training_outputs/models/0.825_xgb.ubj
# COPY tests /tests

CMD uvicorn seagrass.api.main:app --host 0.0.0.0 --port $PORT
