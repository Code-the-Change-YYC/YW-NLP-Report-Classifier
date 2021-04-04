import contextlib
import os
from training.description_classification.utils import save_cnb
import unittest
from tempfile import NamedTemporaryFile

import numpy as np

from preprocess.incident_types.incident_types_d import IncidentType
from models.cnb_model import CNBDescriptionClf
from training.description_classification import model_paths

test_descriptions = [
    'a description', 'another description', 'and another description'
]
test_inc_types = [
    IncidentType.CLIENT_P.value, IncidentType.CHI_ABD.value,
    IncidentType.ABU_CLI.value
]

@contextlib.contextmanager
def test_model_context():
    # Create a copy of the model to use for testing
    test_model_path = 'cnb_desc_clf.test.pickle'
    with open(model_paths.cnb, 'rb') as prod_model, open(test_model_path, 'wb') as model:
        model.write(prod_model.read())

    try:
        clf = CNBDescriptionClf(model_path=test_model_path)
        yield clf, test_model_path
    finally:
        os.remove(test_model_path)

class TestCNBDescriptionClf(unittest.TestCase):

    def test_retrain_model_fewer_incident_types(self):
        """Asserts that retraining the model with a list of all incident types
        that does not include some incident types in the training examples does
        not break things. For example, if an incident type is removed in Sanity,
        but we still have descriptions with those as incident types in the
        dataset, the model should handle that."""
        with test_model_context() as (clf, test_model_path):
            test_inc_types_fewer = test_inc_types[1:]
            clf.retrain_model(test_descriptions, test_inc_types, all_incident_types=test_inc_types_fewer)
            self.assertSetEqual(set(test_inc_types_fewer), set(clf._model.classes_))
            clf.predict(['a description'])
            test_descriptions_fewer = test_descriptions[1:]
            clf.partial_fit(test_descriptions_fewer, test_inc_types_fewer)
            clf.predict(['a description'])

    def test_retrain_model_extra_incident_types(self):
        """Asserts that retraining the model with a list of all incident types
        that includes some incident types that are not in the training examples does
        not break things. For example, if an incident type is added in Sanity,
        but we don't have any training examples for that type, the model should
        handle that."""
        with test_model_context() as (clf, test_model_path):
            new_inc_type = "a new incident type"
            test_inc_types_extra = test_inc_types + [new_inc_type]
            clf.retrain_model(test_descriptions, test_inc_types, all_incident_types=test_inc_types_extra)
            self.assertSetEqual(set(test_inc_types_extra), set(clf._model.classes_))
            clf.predict(['a description'])
            test_descriptions_extra = test_descriptions + ['a new description']
            clf.partial_fit(test_descriptions_extra, test_inc_types_extra)
            clf.predict(['a description'])

    def test_create_model_integration(self):
        """Asserts that the created model doesn't break when used in the rest of
        the methods."""
        with NamedTemporaryFile() as f:
            clf = CNBDescriptionClf()
            model = clf.create_model(test_descriptions, test_inc_types)
            save_cnb(model, f.name)

            clf = CNBDescriptionClf(model_path=f.name)
            clf.predict(test_descriptions)
            clf.partial_fit(test_descriptions, test_inc_types)
            clf.predict_multiple(test_descriptions)

    def test_create_model(self):
        clf = CNBDescriptionClf()
        model = clf.create_model(test_descriptions, test_inc_types)
        model.predict(['a description'])

    def test_predictions_with_proba(self):
        clf = CNBDescriptionClf()
        classes = clf._model.classes_
        num_classes = len(classes)
        single_proba = list(range(num_classes, 0, -1))
        proba = np.array([single_proba for _ in range(3)])
        result = clf._predictions_with_proba(proba, 3)
        for prediction_set in result:
            for i, prediction_with_proba in enumerate(prediction_set):
                self.assertEqual(prediction_with_proba[0], classes[i])
                self.assertEqual(float(prediction_with_proba[1]), single_proba[i])

    def test_partial_fit_handles_new_classes(self):
        with test_model_context() as (clf, test_model_path):
            previous_classes = list(clf._get_estimator().classes_)
            y = ['a wild incident type appears']
            clf.partial_fit(['a new incident occured'], y)
            
            clf = CNBDescriptionClf(model_path=test_model_path)
            new_classes = clf._get_estimator().classes_
            
            for cls in previous_classes:
                self.assertIn(cls, new_classes)

    def test_get_classes_handles_unknown(self):
        clf = CNBDescriptionClf()
        new_labels = ['Some new label', 'Another new label']
        result = clf._get_classes(new_labels)
        self.assertIs(result, None)

    def test_get_classes_handles_known(self):
        clf = CNBDescriptionClf()
        original_classes = list(clf._get_estimator().classes_)
        labels = original_classes[:4]
        classes = clf._get_classes(labels)
        self.assertEqual(labels, classes)

    def test_get_classes_handles_similar(self):
        clf = CNBDescriptionClf()
        original_classes = list(clf._get_estimator().classes_)
        labels = original_classes[:4]
        similar_labels = [cls.upper() for cls in labels]
        classes = clf._get_classes(similar_labels)
        self.assertEqual(labels, classes)

if __name__ == '__main__':
    unittest.main()
