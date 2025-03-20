import pandas as pd
from seagrass.ml_logic.load_data import load_bq_table
from seagrass.ml_logic.model import XGBTrainer
from sklearn.model_selection import train_test_split

def get_data_train():
    data = load_bq_table("seagrass","final_boss_coast")

    target_map = {
            None: 0,
            "Not reported": 1,
            "Posidoniaceae": 2,
            "Cymodoceaceae": 3,
            "Hydrocharitaceae": 4,
        }

    X = data[
        [
            "latitude_temp",
            "longitude_temp",
            "po4",
            "no3",
            "si",
            "nh4",
            "bottomT",
            "trend",
            "thetao",
            "so"        ]
    ]
    X.rename(columns={"latitude_temp":"lat",
                      "longitude_temp":"lon",
                      "bottomT":"bottom_temp",
                      "trend":"chlorophyll",
                      "thetao":"avg_temp",
                      "so":"salinity"},inplace=True)

    import ipdb;ipdb.set_trace()

    y = data["FAMILY"].map(target_map)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.25, stratify=y_train, random_state=42
    )

    model = XGBTrainer()
    f1 = model.train_eval(X_train, y_train, X_val, y_val, X_test, y_test)

    model.save(f1)

if __name__ == "__main__":
    get_data_train()
