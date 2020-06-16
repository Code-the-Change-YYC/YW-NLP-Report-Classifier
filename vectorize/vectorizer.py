from abc import ABC, abstractmethod

import numpy as np


class Vectorizer(ABC):
    @abstractmethod
    def vectorize(self, strings: np.ndarray) -> np.ndarray:
        """Transforms strings into their vectorized representation suitable for
        use as a feature vector.

        :param strings: Strings to be vectorized.
        :return: Array of vectorized representations of strings.
        """
        ...
