import requests

from server.credentials import Credentials
from server.interceptum_adapter import InterceptumAdapter
from server.risk_scores.risk_assessment import get_risk_assessment
from fastapi import FastAPI, HTTPException

from models.cnb_model import CNBDescriptionClf
from server.schemas.predict import PredictIn, PredictOut
from server.schemas.submit import Form, SubmitOut, SubmitIn

app = FastAPI()
clf = CNBDescriptionClf()
credentials = Credentials()
interceptum = InterceptumAdapter(credentials)

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
    'Authorization': f'Bearer {credentials.sanity_read_token}',
}


def run_query(uri, query, headers):
    request = requests.post(uri, json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(
            f"Unexpected status code returned: {request.status_code}")


def update_model(form_fields: Form):
    "Update the classifier from the form submission"
    clf.partial_fit([form_fields.description], [form_fields.incident_type_primary])


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.post("/api/predict/", response_model=PredictOut)
async def predict(predict_in: PredictIn) -> PredictOut:
    """Predict most probable incident types from input string.

    Args:
        predict_in (PredictIn): Input text and number of predictions to return.

    Returns:
        PredictOut: JSON containing input text and predictions with their
        probabilities.
    """
    inc_types = run_query(credentials.sanity_gql_endpoint, formQuery, headers)['data']['CirForm']['primaryIncTypes']
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
    send_email: bool = credentials.PYTHON_ENV == "production"
    try:
        risk_assessment = get_risk_assessment(form.form_fields, email_for_high_risk=do_email)
        # NOTE: `email_for_high_risk` disabled for rn to avoid spam
    except KeyError as ke:
        raise HTTPException(
            422, detail={"error": f"Incorrect request parameter/key: {ke}"})

    update_model(form.form_fields)

    redirect_url = interceptum.call_api(form.form_fields.dict())
    return SubmitOut(form_fields=form.form_fields,
                     risk_assessment=risk_assessment.value,
                     redirect_url=redirect_url)
