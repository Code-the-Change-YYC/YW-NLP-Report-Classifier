from pydantic import BaseModel
from fastapi import Query
from typing import List, Tuple


class PredictIn(BaseModel):
    text: str = Query(..., min_length=3)


class PredictOut(BaseModel):
    input_text: str
    prediction: str


class PredictMultiIn(BaseModel):
    text: str = Query(..., min_length=3)
    num_predictions: int = Query(..., ge=2)


class PredictMultiOut(BaseModel):
    input_text: str
    predictions: List[Tuple[str, float]]
