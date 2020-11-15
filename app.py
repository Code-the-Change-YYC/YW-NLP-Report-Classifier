import requests

from server.risk_scores.risk_assessment import get_risk_assessment
from fastapi import FastAPI, HTTPException

from models.cnb_model import CNBDescriptionClf
from server.schemas.predict import PredictIn, PredictOut
from server.schemas.submit import SubmitOut, SubmitIn

app = FastAPI()
clf = CNBDescriptionClf()

SANITY_READ_TOKEN = 'sk3NUupsXKArTsNbHr8pLrHslLSghe7Vcsg8aRnQJnyzXwihYWkqTlh33Gp3EzYDEYBORzuQWa9IRI1Ah9ftAWFYvHkWDtt2WgMxcOqojINepTu4R8kzDss6cIoYTHXxHRaoitA5t1pxLwbPmF4N53cqfj3aJC55RgpokiJx3NFw7QBAClmw'
SANITY_GQL_ENDPOINT = 'https://33e21qir.api.sanity.io/v1/graphql/production/default'

formQuery = """
    {
        CirForm(id: "cirForm") {
            primaryIncTypes
        }
    }
"""

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {SANITY_READ_TOKEN}',
}


def run_query(uri, query, headers):
    request = requests.post(uri, json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(
            f"Unexpected status code returned: {request.status_code}")


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
    inc_types = run_query(SANITY_GQL_ENDPOINT, formQuery, headers)['data']['CirForm']['primaryIncTypes']
    input_string = predict_in.text
    num_predictions = predict_in.num_predictions
    [predictions] = clf.predict_multiple([input_string], num_predictions)
    predictions = [(pred[0].value, pred[1]) for pred in predictions]
    predictions = list(filter(lambda pred: pred[0] in inc_types, predictions))
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
            422, detail={"error": f"Incorrect request parameter/key: {ke}"}
        )
    return SubmitOut(form_fields=form.form_fields, risk_assessment=risk_assessment.value)
