import numpy as np
from sklearn.pipeline import Pipeline

from preprocess.incident_types.incident_types_d import IncidentType
from models.model import Model, ArrayLike
from preprocess.report_data import ReportData
from preprocess.report_data_d import ColName

from training.description_classification.utils import load_svm, SVMPipeline


class SVMDescriptionClf(Model[SVMPipeline]):
    """Complement Naive Bayes model for description classification."""
    _model: Pipeline

    def __init__(self):
        self._model = load_svm()

    def predict(self, X: ArrayLike) -> np.ndarray:
        """Predict the primary incident type of the given descriptions.

        :param X: 1D array-like of descriptions to classify
        :return: 1D array of `IncidentType` predictions for the given descriptions.
        """
        predictions = self._model.predict(X)
        return np.array([IncidentType(prediction) for prediction in predictions])

    def partial_fit(self, X: ArrayLike, y: ArrayLike, classes: ArrayLike = None) -> object:
        pass


if __name__ == '__main__':
    clf = SVMDescriptionClf()
    df = ReportData().get_processed_data()
    print(clf.predict([df[ColName.DESC][0]]))
