import unittest

import numpy as np

from incident_types.incident_types_d import IncidentType
from models.cnb_model import CNBDescriptionClf


class TestCNBDescriptionClf(unittest.TestCase):
    def test_predictions_with_proba(self):
        clf = CNBDescriptionClf()
        classes = clf._model.classes_
        num_classes = len(classes)
        single_proba = list(range(num_classes, 0, -1))
        proba = np.array([single_proba for _ in range(3)])
        result = clf._predictions_with_proba(proba, 3)
        for prediction_set in result:
            for i, prediction_with_proba in enumerate(prediction_set):
                self.assertEqual(prediction_with_proba[0], IncidentType(classes[i]))
                self.assertEqual(prediction_with_proba[1], single_proba[i])


if __name__ == '__main__':
    unittest.main()
