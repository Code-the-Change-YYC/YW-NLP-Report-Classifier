from fastapi import FastAPI, File, UploadFile

from models.cnb_model import CNBDescriptionClf
from server.schemas.prediction import PredictIn, PredictOut
from server.validators import validate_input_string

app = FastAPI()
clf = CNBDescriptionClf()


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
    [prediction] = clf.predict([input_string])
    return PredictOut(
        input_text=input_string, prediction=prediction.value
    )


@app.post("/api/submit/")
async def submit_form(xml_file: UploadFile = File(...)):
    return {"detail": "A"}
