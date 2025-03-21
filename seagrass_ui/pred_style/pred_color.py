import numpy as np
import os

colors = {
    0: "black",  # No seagrass
    1: "orange",  # Not reported
    2: "blue",
    3: "green",
    4: "purple",
}


def get_pred_color(pred: list, seagrass_presence: float):
    class_pred = pred[1:]
    max_pred = class_pred.index(max(class_pred))
    return colors[max_pred + 1]


def get_pred_opacity(pred: list, seagrass_presence: float):
    if seagrass_presence > 10:
        if seagrass_presence > 50:
            return 1
        return 0.6
    opacity = 1 - (pred[0] / sum(pred))
    return opacity if opacity > 0.1 else 0.025
