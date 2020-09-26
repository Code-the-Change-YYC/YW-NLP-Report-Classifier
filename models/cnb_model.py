import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline

from incident_types.incident_types_d import IncidentType
from models.model import Model, ArrayLike
from report_data import ReportData
from report_data_d import ColName
from training.description_classification.utils import load_cnb, CNBPipeline


class CNBDescriptionClf(Model[CNBPipeline]):
    """Complement Naive Bayes model for description classification."""
    _model: Pipeline

    def __init__(self):
        self._model = load_cnb()

    def predict(self, X: ArrayLike) -> np.ndarray:
        """Predict the primary incident type of the given descriptions.

        :param X: 1D array-like of descriptions to classify
        :return: 1D array of `IncidentType` predictions for the given descriptions.
        """
        predictions = self._model.predict(X)
        return np.array([IncidentType(prediction) for prediction in predictions])

    def partial_fit(self, X: ArrayLike, y: ArrayLike, classes: ArrayLike = None) -> object:
        est: ComplementNB = self._model.steps[-1][1]
        word_vec: TfidfVectorizer = self._model.steps[0][1]
        vectors = word_vec.transform(X)
        est.partial_fit(vectors, y)
        return self

    def predict_multiple(self, X: ArrayLike, num_predictions: int) -> np.ndarray:
        """Give the top `num_predictions` predictions for each sample with their
        confidences, ordered by confidence.

        :param X: Input descriptions to predict on.
        :param num_predictions: The number of predictions to give for each
        sample. If this is greater than the number of possible predictions, all
        predictions will be given.
        :return: `(X_0, num_predictions, 2)` array `Y` of prediction sets for
        each description, where each row of `Y` is a list of predictions ordered
        by confidence, and each prediction is an 2 length array with the
        `IncidentType` prediction as the first element and the confidence as the
        second.
        """
        classes = self._model.classes_
        num_classes = len(classes)
        if num_predictions > num_classes:
            num_predictions = num_classes

        return self._predictions_with_proba(self._model.predict_proba(X), num_predictions)

    def _predictions_with_proba(self, proba: ArrayLike, num_predictions: int) -> np.ndarray:
        """Utility for joining probabilities with their incident type
        predictions and ordering them.

        :param proba: Probabilities, for example as returned by `predict_proba`.
        :param num_predictions: The number of predictions to give for each
        sample.
        :return: `(proba_0, num_predictions, 2)` array `Y` of prediction sets
        for each row of probabilities, where each row of `Y` is a list of
        predictions ordered by confidence, and each prediction is an 2 length
        array with the `IncidentType` prediction as the first element and the
        confidence as the second.
        """
        top_indices: np.ndarray = proba.argsort()[:, -1:-(num_predictions + 1):-1]
        top_proba: np.ndarray = np.take_along_axis(proba, top_indices, axis=1)
        predictions: np.ndarray = self._model.classes_[top_indices]
        incident_types = np.array([IncidentType(p) for p in predictions.flat]).reshape(predictions.shape)
        return np.dstack((incident_types, top_proba))


if __name__ == '__main__':
    clf = CNBDescriptionClf()
    df = ReportData().get_processed_data()
    X = df[ColName.DESC][:5]
    y = df[ColName.INC_T1][:5]
    clf.partial_fit(X, y, list(set(y)))
    print(clf.predict(X))
    multi_predict = clf.predict_multiple(X, 5)
    for i, prediction_set in enumerate(multi_predict):
        print('For description')
        print(X[i])
        for prediction_with_proba in prediction_set:
            print(f'We predict {prediction_with_proba[0].value} with {prediction_with_proba[1]:.2f}% confidence')
