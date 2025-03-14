FROM python:3.10.6

COPY requirements_prod.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY seagrass /seagrass
# COPY tests /tests

CMD uvicorn seagrass.api.main:app --host 0.0.0.0 --port $PORT
