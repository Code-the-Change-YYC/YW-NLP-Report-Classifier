import numpy as np

from models.model import Model, ArrayLike

from os import path

dir_path = path.dirname(path.realpath(__file__))


class CNBModel(Model):
    """Complement Naive Bayes model for classification."""
    weights_file = path.join(dir_path, '..', 'model_output', 'cnb.pkl')

    def __init__(self, weights_file: str = weights_file):
        super().__init__(weights_file)

    def predict(self, X: ArrayLike) -> np.ndarray:
        pass

    def partial_fit(self, X: ArrayLike, y: ArrayLike, classes: ArrayLike = None) -> object:
        pass
