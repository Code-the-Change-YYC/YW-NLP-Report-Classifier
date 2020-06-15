import pandas as pd
from vectorizer import Vectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


class SklearnVectorizer(Vectorizer):
    def __init__(self):
        self.vectorizer = CountVectorizer(stop_words="english", strip_accents="unicode")

    def vectorize(self, strings: np.ndarray) -> np.ndarray:
        corpus = strings.tolist()
        X = self.vectorizer.fit_transform(corpus)

        return X.toarray()
