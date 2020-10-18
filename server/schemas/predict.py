from pydantic import BaseModel, Field
from typing import List, Tuple, Optional


class PredictIn(BaseModel):
    text: str
    num_predictions: Optional[int] = Field(
        None,
        title="Number of predictions",
        description="The number of classes to request predictions for, default/0 will return all classes.",
    )


class PredictOut(BaseModel):
    input_text: str
    predictions: List[Tuple[str, float]]
