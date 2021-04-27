from typing import Dict
from preprocess.report_data import ReportData

from server.credentials import credentials
from server.interceptum_adapter import InterceptumAdapter
from server.risk_scores.risk_assessment import get_risk_assessment
from fastapi import FastAPI, HTTPException, BackgroundTasks

from models.cnb_model import CNBDescriptionClf
from server.schemas.predict import PredictIn, PredictOut
from server.schemas.submit import Form, SubmitOut, SubmitIn
from server.connection import collection
from server.sanity_utils import form_query, timeframe_query, headers, run_query

app = FastAPI()
clf = CNBDescriptionClf()
interceptum = InterceptumAdapter(credentials)


def update_model(form_fields: Form):
    "Update the classifier from the form submission"
    clf.partial_fit([form_fields.description],
                    [form_fields.incident_type_primary])


report_data = ReportData()


def background_processing(form_fields: Form):
    update_model(form_fields)
    processed_form_data = report_data.process_form_submission(form_fields)
    collection.insert_one(processed_form_data.dict())


@app.get("/")
async def index():
    return {"Server status": "Healthy"}


@app.post("/api/predict/", response_model=PredictOut)
async def predict(predict_in: PredictIn) -> PredictOut:
    """Predict most probable incident types from input string.

    Params:
        predict_in (PredictIn): Input text and number of predictions to return.

    Returns:
        PredictOut: JSON containing input text and predictions with their
        probabilities.
    """
    inc_types_obj = run_query(credentials.sanity_gql_endpoint, form_query,
                              headers)['data']['CirForm']['primaryIncTypes']
    inc_types = list(map(lambda inc_type: inc_type['name'], inc_types_obj))
    input_string = predict_in.text
    num_predictions = predict_in.num_predictions
    [predictions] = clf.predict_multiple([input_string], num_predictions)
    predictions = [(pred[0].value, pred[1]) for pred in predictions]
    predictions = list(filter(lambda pred: pred[0] in inc_types, predictions))
    return PredictOut(input_text=input_string, predictions=predictions)


@app.post("/api/submit/", response_model=SubmitOut)
async def submit_form(form: SubmitIn,
                      background_tasks: BackgroundTasks) -> SubmitOut:
    """Submit JSON form data from front end.

    Params:
        form (SubmitIn)

    Returns:
        SubmitOut: Request data alongside risk score.
    """
    background_tasks.add_task(background_processing, form.form_fields)
    risk_assessment_timeframe = run_query(
        credentials.sanity_gql_endpoint, timeframe_query,
        headers)['data']['CirForm']['riskAssessmentTimeframe']
    try:
        risk_assessment = get_risk_assessment(
            form.form_fields, timeframe=risk_assessment_timeframe)
    except KeyError as ke:
        raise HTTPException(
            422, detail={"error": f"Incorrect request parameter/key: {ke}"})

    if not credentials.USE_WEBHOOK:
        background_tasks.add_task(background_processing, form)

    redirect_url = interceptum.call_api(form.form_fields.dict())
    return SubmitOut(form_fields=form.form_fields,
                     risk_assessment=risk_assessment.value,
                     redirect_url=redirect_url)


@app.post('/api/interceptum-post', response_model=SubmitOut)
async def interceptum_post_form(form_dict: Dict,
                                background_tasks: BackgroundTasks) -> SubmitOut:
    """Currently unusable."""
    # TODO: Map interceptum input to background task input
    if credentials.USE_WEBHOOK:
        background_tasks.add_task(background_processing, form_dict)
