from server.interceptum_adapter import InterceptumAdapter
from server.risk_scores.risk_assessment import get_risk_assessment
from fastapi import FastAPI, HTTPException

from models.cnb_model import CNBDescriptionClf
from server.schemas.predict import PredictIn, PredictOut
from server.schemas.submit import SubmitOut, SubmitIn

app = FastAPI()
clf = CNBDescriptionClf()
interceptum = InterceptumAdapter(account_name='', username='', password='')


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


@app.post("/api/submit/", response_model=SubmitOut)
async def submit_form(form: SubmitIn) -> SubmitOut:
    """Submit JSON form data from front end.

    Args:
        form (SubmitIn)

    Returns:
        SubmitOut: Request data alongside risk score.
    """
    try:
        risk_assessment = get_risk_assessment(form.form_fields)
    except KeyError as ke:
        raise HTTPException(
            422, detail={"error": f"Incorrect request parameter/key: {ke}"})

    redirect_url = interceptum.call_api(form.form_fields.dict())
    return SubmitOut(form_fields=form.form_fields,
                     risk_assessment=risk_assessment.value,
                     redirect_url=redirect_url)
