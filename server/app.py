from fastapi import FastAPI, File, UploadFile

from ml.ml_model import MLModel
from schemas.prediction import PredictIn, PredictOut
from validators import validate_input_string

app = FastAPI()
ml_model = MLModel()


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.post("/api/predict/", response_model=PredictOut)
async def predict(predict_in: PredictIn) -> PredictOut:
    """Predict sentiment from input string.

    Args:
        predict_in (PredictIn): String containing input text.

    Returns:
        PredictOut: JSON containing input text, prediction, and sentiment.
    """
    input_string = predict_in.text
    validate_input_string(input_string)
    prediction = ml_model.predict(input_string)
    sentiment = "good" if prediction >= 0.5 else "bad"
    return PredictOut(
        input_text=input_string, prediction=prediction, sentiment=sentiment
    )


@app.post("/api/submit/")
async def submit_form(xml_file: UploadFile = File(...)):
    return {"detail": "A"}
