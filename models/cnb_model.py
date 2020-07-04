import numpy as np

from models.model import Model, ArrayLike


class CNBModel(Model):
    """Complement Naive Bayes model for classification."""
    def train(self, X: ArrayLike, y: ArrayLike) -> object:
        pass

    def predict(self, X: ArrayLike) -> np.ndarray:
        pass

    def partial_fit(self, X: ArrayLike, y: ArrayLike, classes: ArrayLike = None) -> object:
        pass
