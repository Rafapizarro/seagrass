import numpy as np

colors = {
    0: "red",  # Not reported
    1: "blue",
    2: "green",
    3: "yellow",
}


def get_pred_color(pred: list):
    class_pred = pred[1:]
    max_pred = class_pred.index(max(class_pred))
    return colors[max_pred]


def get_pred_opacity(pred: list):
    opacity = 1 - (pred[0] / sum(pred))
    return opacity if opacity > 0.1 else 0.1
