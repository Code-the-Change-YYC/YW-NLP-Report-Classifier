from abc import ABC, abstractmethod

import pandas as pd


class Vectorizer(ABC):
    @abstractmethod
    def vectorize(self, strings: pd.Series) -> pd.Series:
        """Transforms strings into their vectorized representation suitable for
        use as a feature vector.

        :param strings: Series of strings to be vectorized.
        :return: Vectorized representation of strings.
        """
        ...
