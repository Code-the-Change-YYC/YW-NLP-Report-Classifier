from pathlib import Path

from tensorflow.keras.models import load_model
from tensorflow.python.keras.engine.functional import Functional

from .custom_objects.custom_objects import TextVectorization, custom_standardization


class MLModel:
    weights_path = Path("server/ml/weights/")
    _model: Functional = None

    def __init__(self, weights_path: str = None):
        """Model class for ML-model related methods and attributes.

        Args:
            weights_path (str, optional): For testing different models. 
            Defaults to None.

        Raises:
            ValueError: If the model path does not exist.
        """
        if weights_path:
            self.weights_path = weights_path
        if not self.weights_path.exists():
            raise ValueError("Model path does not exist.")
        if not self._model:
            self.load()

    def train(self):
        pass

    def load(self):
        """Load TF model with custom objects.
        """
        self._model = load_model(
            self.weights_path,
            custom_objects={
                "TextVectorization": TextVectorization,
                "custom_standardization": custom_standardization,
            },
        )

    def predict(self, input_string: str, as_array: bool = False):
        """Generate prediction from ML model.

        Args:
            input_string (str)

        Returns:
            float: Predicted sentiment of text.
        """
        prediction_array = self._model.predict([input_string])
        prediction = prediction_array.item()
        return prediction
