from server import credentials
from server.credentials import credentials
from typing import List, Optional, Sequence, cast

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import log_loss

from training.description_classification import model_paths
from models.model import Model, ArrayLike
from preprocess.report_data import ReportData
from preprocess.report_data_d import ColName
from training.description_classification.utils import load_cnb, CNBPipeline, save_cnb, spacy_tokenizer

PROD = 'production'
DEV = 'development'

IS_DEV = credentials.PYTHON_ENV == DEV


class CNBDescriptionClf(Model[CNBPipeline]):
    """Complement Naive Bayes model for description classification."""

    _model: CNBPipeline
    _model_path: str

    def __init__(self, model_path: str = None):
        """
        Params:
            model_path: A specific model to load. This parameter is mostly for
            testing, leave as `None` for a model to be chosen automatically.
        """
        if model_path is not None:
            self._model_path = model_path
            self._model = load_cnb(self._model_path, copy_from_prod=False)
        else:
            self._model_path = model_paths.cnb_dev if IS_DEV else model_paths.cnb
            self._model = load_cnb(self._model_path, copy_from_prod=True)

    def predict(self, X: ArrayLike) -> np.ndarray:
        """Predict the primary incident type of the given descriptions.

        :param X: 1D array-like of descriptions to classify
        :return: 1D array of `IncidentType` predictions for the given descriptions.
        """
        predictions = self._model.predict(X)
        return np.array([prediction for prediction in predictions])

    def partial_fit(self, X: ArrayLike, y: List[str]):
        """Update the model and save the updates.

        Params:
            X: Input descriptions.
            y: Incident types to use as labels for each description.
        """
        label_classes = self._get_classes(list(y))
        # If a previously trained label was found
        if label_classes is not None:
            est = self._get_estimator()
            word_vec: TfidfVectorizer = self._model.steps[0][1]
            vectors = word_vec.transform(X)
            est.partial_fit(vectors, label_classes)
            save_cnb(self._model, self._model_path)

        return self

    def predict_multiple(self,
                         X: ArrayLike,
                         num_predictions: int = None) -> np.ndarray:
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
        second. The confidence values are represented as strings.
        """
        num_classes = len(self._model.classes_)
        if not num_predictions or num_predictions > num_classes:
            num_predictions = num_classes

        return self._predictions_with_proba(self._model.predict_proba(X),
                                            num_predictions)

    def create_model(self,
                     descriptions: Sequence[str],
                     incident_types: Sequence[str],
                     all_incident_types: Sequence[str] = None) -> CNBPipeline:
        """Creates a CNB description classifier pipeline and trains it with the
        given data.

        Params:
            descriptions: Descriptions to train on. Must not contains missing values.

            incident_types: The incident types corresponding to the descriptions. Must not contains missing values.

            all_incident_types: All possible incident types which the model
            might receive. If this is not given, the unique values from
            `incident_types` will be used instead. This parameter should be used
            to ensure the model does not fail on incident types which are not in
            `incident_types`, but may appear later during partial fitting.
        """
        word_vec = TfidfVectorizer(
            tokenizer=spacy_tokenizer,
            token_pattern=r"\b\w+\b",
            ngram_range=(1, 2),
            min_df=2,
        )
        model = ComplementNB(alpha=1.2)
        cnb = make_pipeline(word_vec, model)
        if all_incident_types is not None:
            vectors = word_vec.fit_transform(descriptions)
            model.partial_fit(vectors,
                              incident_types,
                              classes=all_incident_types)
        else:
            cnb.fit(descriptions, incident_types)

        return cast(CNBPipeline, cnb)

    def retrain_model(self,
                      descriptions: Sequence[str],
                      incident_types: Sequence[str],
                      all_incident_types: Sequence[str] = None):
        """Retrain current model with new data, save old model. 

        Args:
            descriptions (Sequence[str]): Descriptions to train on. 
            incident_types (Sequence[str]): The incident types for descriptions. 
            all_incident_types: See `create_model`.
        """
        save_cnb(self._model, model_path=model_paths.backup)
        self._model = self.create_model(descriptions,
                                        incident_types,
                                        all_incident_types=all_incident_types)
        save_cnb(self._model, model_path=self._model_path)
        print('Model successfully retrained.')

    def _predictions_with_proba(self, proba: ArrayLike,
                                num_predictions: int) -> np.ndarray:
        """Utility for joining probabilities with their incident type
        predictions and ordering them.

        :param proba: Probabilities, for example as returned by `predict_proba`.
        :param num_predictions: The number of predictions to give for each
        sample.
        :return: `(proba_0, num_predictions, 2)` array `Y` of prediction sets
        for each row of probabilities, where each row of `Y` is a list of
        predictions ordered by confidence, and each prediction is an 2 length
        array with the `IncidentType` prediction as the first element and the
        confidence as the second. The confidence values are represented as strings.
        """
        top_indices: np.ndarray = proba.argsort()[:,
                                                  -1:-(num_predictions + 1):-1]
        top_proba: np.ndarray = np.take_along_axis(proba, top_indices, axis=1)
        predictions: np.ndarray = self._model.classes_[top_indices]
        incident_types = np.array([p for p in predictions.flat
                                   ]).reshape(predictions.shape)
        return np.dstack((incident_types, top_proba))

    def _get_classes(self, labels: List[str]) -> Optional[List[str]]:
        """Returns the classes each label in `labels` was determined to
        most likely correspond to based on similarity, or `None` if a likely
        class was not found for any of the labels.
        """
        est = self._get_estimator()
        label_classes = []
        all_classes = list(est.classes_)
        for label in labels:
            transformed_label = label.lower()
            i = 0
            class_index = None
            while class_index is None and i < len(all_classes):
                if transformed_label == all_classes[i].lower():
                    class_index = i
                i += 1

            if class_index is None:
                return None
            else:
                label_class = all_classes[class_index]

            label_classes.append(label_class)

        return label_classes

    def _get_estimator(self) -> ComplementNB:
        return self._model.steps[-1][1]


if __name__ == "__main__":

    clf = CNBDescriptionClf()
    df = ReportData().get_processed_data()
    X = df[ColName.DESC][:5]
    y = df[ColName.INC_T1][:5]

    clf.partial_fit(X, y)

    print(clf.predict(X))

    multi_predict = clf.predict_multiple(X, 5)
    for i, prediction_set in enumerate(multi_predict):
        print("For description")
        print(X[i])
        for prediction_with_proba in prediction_set:
            print("We predict", prediction_with_proba[0], " with ",
                  prediction_with_proba[1], " confidence")
