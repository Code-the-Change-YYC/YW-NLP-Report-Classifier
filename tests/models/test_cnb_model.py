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


class TestCNBDescriptionClf(unittest.TestCase):

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
        # Create a copy of the model to use for testing
        test_model_path = 'cnb_desc_clf.test.pickle'
        with open(model_paths.cnb, 'rb') as prod_model, open(test_model_path, 'wb') as model:
            model.write(prod_model.read())

        try:
            clf = CNBDescriptionClf(model_path=test_model_path)
            previous_classes = list(clf._get_estimator().classes_)
            y = ['a wild incident type appears']
            clf.partial_fit(['a new incident occured'], y)
            
            clf = CNBDescriptionClf(model_path=test_model_path)
            new_classes = clf._get_estimator().classes_
            
            for cls in previous_classes:
                self.assertIn(cls, new_classes)
        finally:
            os.remove(test_model_path)

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
