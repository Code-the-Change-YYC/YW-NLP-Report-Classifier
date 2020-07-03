from abc import ABC, abstractmethod
from typing import NewType, Union, Iterable

import numpy as np

"""Numpy array_like type"""
ArrayLike = NewType('ArrayLike', Union[np.ndarray, Iterable, int, float])


class Model(ABC):
    @abstractmethod
    def train(self, X: ArrayLike, y: ArrayLike) -> object:
        """Train the model according to `X`, `y`.

        :param X: array_like training vectors of shape (n_samples, n_features)
        :param y: array_like target values of shape (n_samples,)
        :return: self
        """
        ...

    @abstractmethod
    def predict(self, X: ArrayLike) -> np.ndarray:
        """Predict target values based an array of test vectors X.

        :param X: array_like test vectors of shape (n_samples, n_features)
        :return: `ndarray` of predicted target values for `X` of shape (n_samples,)
        """
        ...

    @abstractmethod
    def partial_fit(self, X: ArrayLike, y: ArrayLike, classes: ArrayLike = None) -> object:
        """Perform incremental fitting on a batch of samples given by `X`, `y`.

        :param X: array_like training vectors of shape (n_samples, n_features)
        :param y: array_like target values of shape (n_samples,)
        :param classes: List of all classes that can appear in `y`.
        """
        ...
