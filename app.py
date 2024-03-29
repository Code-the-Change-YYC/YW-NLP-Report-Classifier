from typing import Dict
import requests
import json
import sys
import pandas as pd
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Request, Response, status
from traceback import format_exc

from preprocess.report_data_d import _ColName
from preprocess.report_data import ReportData
from server.credentials import credentials
from server.interceptum_adapter import InterceptumAdapter
from server.risk_scores.risk_assessment import RiskAssessment, get_risk_assessment

from models.cnb_model import CNBDescriptionClf
from server.schemas.predict import PredictIn, PredictOut
from server.schemas.submit import Form, SanityUpdate, SubmitOut, SubmitIn
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


def get_incident_types_from_sanity():
    inc_types_obj = run_query(credentials.sanity_gql_endpoint, form_query,
                              headers)['data']['CirForm']['primaryIncTypes']
    return list(map(lambda inc_type: inc_type['name'], inc_types_obj))


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
    inc_types = get_incident_types_from_sanity()
    input_string = predict_in.text
    num_predictions = predict_in.num_predictions
    [predictions] = clf.predict_multiple([input_string], num_predictions)
    predictions = [(pred[0], float(pred[1])) for pred in predictions]
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
        processed_form_data = report_data.process_form_submission(
            form.form_fields)
        collection.insert_one(processed_form_data.dict())
        background_tasks.add_task(background_processing, form.form_fields)
    else:
        print(
            'USE_WEBHOOK set to True: skipping MongoDB insert and model retrain.'
        )

    redirect_url = interceptum.call_api(form.form_fields.dict())
    return SubmitOut(form_fields=form.form_fields,
                     risk_assessment=risk_assessment.value,
                     redirect_url=redirect_url)


@app.post('/webhook/interceptum-post/')
async def interceptum_post_form(background_tasks: BackgroundTasks,
                                request: Request):
    xml = (await request.form()).get('VALUES_XML')
    form_dict = interceptum.xml_to_form_values(xml)
    if credentials.USE_WEBHOOK:
        background_tasks.add_task(background_processing, form_dict)
        processed_form_data = report_data.process_form_submission(form_dict)
        collection.insert_one(processed_form_data.dict())
    else:
        print('USE_WEBHOOK set to False: ignoring webhook response.')


@app.post("/webhook/sanity-update/")
async def sanity_update(sanity_update_in: SanityUpdate):
    """Endpoint for retraining the model when relevant changes to the form
    fields occur in Sanity.
    Assumes all data in the database has undergone preprocessing.
    """
    all_incidents_query = collection.find(
        projection=['description', 'incident_type_primary'])
    all_incidents = pd.DataFrame(list(all_incidents_query)).dropna()
    if 'cirForm' in sanity_update_in.ids.all:
        inc_types = get_incident_types_from_sanity()
        clf.retrain_model(all_incidents['description'],
                          all_incidents['incident_type_primary'],
                          all_incident_types=inc_types)


@app.post('/api/retrain')
async def retrain_model(response: Response, csv_file: UploadFile = File(...)):
    try:
        report_data = ReportData()
        dataframe = report_data.process_report_data(csv_file.file)
        descriptions = dataframe[_ColName.DESC].to_numpy()
        types = dataframe[_ColName.INC_T1].to_numpy()
        clf.retrain_model(descriptions, types)
        now = datetime.now()
        date_backup = "reports" + now.strftime("%m-%d-%Y")
        collection.aggregate([{"$out": date_backup}])
        collection.remove({})
        records = json.loads(dataframe.T.to_json()).values()
        collection.insert_many(records)
        return 'Successfully retrained model and updated database.'
    except:
        output_msg = 'An error occurred while trying to update the database and retrain the model. Please send the following error log to the Code the Change team at jofred.cayabyab1@ucalgary.ca, or to Randy Thornhill: '
        output_msg += format_exc()
        response.status_code = 500
        return output_msg
