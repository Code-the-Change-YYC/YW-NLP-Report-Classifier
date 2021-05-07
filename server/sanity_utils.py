import requests

from server.credentials import credentials

form_query = """
    {
        CirForm(id: "cirForm") {
            primaryIncTypes {
                name
            }
        }
    }
"""

timeframe_query = """
    {
        CirForm(id: "cirForm") {
            riskAssessmentTimeframe
        }
    }
"""

risk_scores_query = """
    {
        CirForm(id: "cirForm") {
            primaryIncTypes {
                name
                risk_weighting
            }
            programs {
                name
                risk_weighting
            }
            immediateResponses {
                name
                risk_weighting
            }
            servicesInvolved {
                name
                risk_weighting
            }
        }
    }
"""

minimum_email_score_query = """
    {
        CirForm(id: "cirForm") {
            minimumEmailRiskScore
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
