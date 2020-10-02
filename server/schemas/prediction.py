from pydantic import BaseModel
from typing import List, Tuple


class PredictIn(BaseModel):
    text: str


class PredictOut(BaseModel):
    input_text: str
    prediction: str


class PredictMultiIn(BaseModel):
    text: str
    num_predictions: int


class PredictMultiOut(BaseModel):
    input_text: str
    predictions: List[Tuple[str, float]]
