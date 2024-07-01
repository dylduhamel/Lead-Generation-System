import json
import os
from datetime import datetime, timedelta

import requests
from sqlalchemy import or_, update
from utils import *


def skiptrace_leads():
    # API call function
    def api_call(lead_list):
        api_token = os.getenv("BATCHDATA_SKIPTRACE_API_TOKEN")
        headers = {
            "Accept": "application/json, application/xml",
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

        data = {"requests": []}

        for lead in lead_list:
            # Create a base data object
            data_object = {
                "propertyAddress": {
                    "city": lead.property_city,
                    "street": lead.property_address,
                    "state": lead.property_state,
                }
            }

            # Add zipcode if it's not None
            if lead.property_zipcode is not None:
                data_object["propertyAddress"]["zip"] = lead.property_zipcode

            # Append to the requests list
            data["requests"].append(data_object)

        try:
            response = requests.post(
                "https://api.batchdata.com/api/v1/property/skip-trace",
                headers=headers,
                data=json.dumps(data),
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong", err)

        results = response.json()

        # Return results for all leads
        return results["results"]["persons"]

    # Create a session
    session = Session()

    # Define todays date range
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    leads = (
        session.query(Lead)
        .filter(Lead.date_added >= today, Lead.date_added < tomorrow)
        .all()
    )

    # Make a single API call for all leads
    # results = api_call(leads)
    results = leads
    print(results)

    # Export json to Skiptraced_data directory
    with open(f"/tmp/skiptrace_{today}.json", "w") as file:
        json.dump(results, file)

    status_print("Skiptrace - Written.")