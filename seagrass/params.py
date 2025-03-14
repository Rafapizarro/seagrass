import os

##################  ENV VARIABLES  #####################
DATA_SIZE = os.environ.get("DATA_SIZE")
MODEL_TARGET = os.environ.get("MODEL_TARGET")
GCP_PROJECT = os.environ.get("GCP_PROJECT")
BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_REGION = os.environ.get("BQ_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

COPERNICUSMARINE_SERVICE_USERNAME = os.environ.get("COPERNICUSMARINE_SERVICE_USERNAME")
COPERNICUSMARINE_SERVICE_PASSWORD = os.environ.get("COPERNICUSMARINE_SERVICE_PASSWORD")

##################  CONSTANTS  #####################
LOCAL_DATA_PATH = os.path.join(os.path.expanduser("~"), ".seagrass", "mlops", "data")
LOCAL_REGISTRY_PATH = os.path.join(
    os.path.expanduser("~"), ".seagrass", "mlops", "training_outputs"
)

##################  DATABASE  #####################

FEATURE_LABELS = [
    "avg_temp",
    "bottom_temp",
    "cholorophyll",
    "depth",
    "no3",
    "si",
    "po4",
    "nh4",
    "salinity",
]
TARGET_LABEL = ["family"]

################## VALIDATIONS #################

env_valid_options = dict(
    DATA_SIZE=["1k", "200k", "all"],
    MODEL_TARGET=["local", "gcs", "mlflow"],
)


def validate_env_value(env, valid_options):
    env_value = os.environ[env]
    if env_value not in valid_options:
        raise NameError(
            f"Invalid value for {env} in `.env` file: {env_value} must be in {valid_options}"
        )
