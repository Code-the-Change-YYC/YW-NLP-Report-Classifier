from fastapi import FastAPI, File, UploadFile

from models.cnb_model import CNBDescriptionClf
from server.schemas.predict import PredictIn, PredictOut
from server.schemas.submit import SubmitOut, SubmitIn
from server.risk_scores import risk_scores

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


@app.post("/api/submit/", response_model=SubmitOut)
async def submit_form(form: SubmitIn) -> SubmitOut:
    """Submit JSON form data from front end.

    Args:
        form (SubmitIn)

    Returns:
        SubmitOut: Request data alongside risk score.
    """

    print(form)

    # TODO: access values from `form` to sum up risk scores
    # -> form.form_fields.incident_type_primary to risk_scores.incident_type_to_risk
    program_risk = risk_scores.program_to_risk[form.form_fields.program]
    response_risk = risk_scores.response_to_risk[form.form_fields.immediate_response]
    incident_risk = risk_scores.response_to_risk[form.form_fields.incident_type_primary]

    risk_score = program_risk + response_risk + incident_risk


    return SubmitOut(form_fields=form.form_fields, risk_score=risk_score)