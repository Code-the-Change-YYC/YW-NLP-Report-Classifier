from pydantic import BaseModel


class PredictIn(BaseModel):
    text: str


class PredictOut(BaseModel):
    input_text: str
    prediction: float
    sentiment: str
