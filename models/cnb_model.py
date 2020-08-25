import numpy as np
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
        pass


if __name__ == '__main__':
    clf = CNBDescriptionClf()
    df = ReportData().get_processed_data()
    print(clf.predict([df[ColName.DESC][0]]))
