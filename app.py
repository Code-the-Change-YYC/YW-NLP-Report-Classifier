from fastapi import FastAPI, File, UploadFile

from models.cnb_model import CNBDescriptionClf
from server.schemas.prediction import (
    PredictIn,
    PredictOut,
)

app = FastAPI()
clf = CNBDescriptionClf()


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.post("/api/predict/", response_model=PredictOut)
async def predict(predict_in: PredictIn) -> PredictOut:
    """Predict most probable incident types from input string.

    Args:
        predict_in (PredictIn): Input text and number of predictions to return.

    Returns:
        PredictMultiOut: JSON containing input text and predictions with their
        probabilities.
    """
    input_string = predict_in.text
    num_predictions = predict_in.num_predictions
    [predictions] = clf.predict_multiple([input_string], num_predictions)
    predictions = [(pred[0].value, pred[1]) for pred in predictions]
    return PredictOut(input_text=input_string, predictions=predictions)


@app.post("/api/submit/")
async def submit_form(xml_file: UploadFile = File(...)):
    return {"detail": "A"}
