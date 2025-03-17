import os

##################  ENV VARIABLES  #####################
GCP_PROJECT = os.environ.get("GCP_PROJECT")
BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_REGION = os.environ.get("BQ_REGION")

COPERNICUSMARINE_SERVICE_USERNAME = os.environ.get("COPERNICUSMARINE_SERVICE_USERNAME")
COPERNICUSMARINE_SERVICE_PASSWORD = os.environ.get("COPERNICUSMARINE_SERVICE_PASSWORD")

##################  CONSTANTS  #####################

LOCAL_DATA_PATH = os.path.join(os.path.expanduser("~"), "lewagon", "seagrass", "data")
LOCAL_REGISTRY_PATH = os.path.join(
    os.path.expanduser("~"), "lewagon", "seagrass", "training_outputs"
)

os.makedirs(LOCAL_DATA_PATH, exist_ok=True)
os.makedirs(LOCAL_REGISTRY_PATH, exist_ok=True)

##################  DATABASE  #####################
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

FEATURE_LABELS = [
    "lat",
    "lon",
    "po4",
    "no3",
    "si",
    "nh4",
    "bottom_temp",
    "chlorophyll",
    "avg_temp",
    "salinity",
    "depth",
]
TARGET_LABEL = "FAMILY"

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

CLASSES = ["No grass"]

################## VALIDATIONS #################


def validate_env_value(env, valid_options):
    env_value = os.environ[env]
    if env_value not in valid_options:
        raise NameError(
            f"Invalid value for {env} in `.env` file: {env_value} must be in {valid_options}"
        )
