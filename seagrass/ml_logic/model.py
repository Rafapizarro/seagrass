from typing import Tuple
from keras import Model
import numpy as np


def initialize_model(input_shape: tuple) -> Model:
    # TODO : Initialize the IDEAL model (fine-tuned, good scores, etc)
    return

# TODO : If we have a NN
def compile_model(model: Model, learning_rate=0.0005) -> Model:
    return


def train_model(
    # TODO : manage the paramters for the .fit step
        model: Model,
        X: np.ndarray,
        y: np.ndarray,
        batch_size=256,
        patience=2,
        validation_data=None, # overrides validation_split
        validation_split=0.3
    ) -> Tuple[Model, dict]:
    return

# TODO : evaluate and get metrics
def evaluate_model(
        model: Model,
        X: np.ndarray,
        y: np.ndarray,
        batch_size=64
    ) -> Tuple[Model, dict]:
    """
    Evaluate trained model performance on the dataset
    """
    return
