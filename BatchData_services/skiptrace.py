'''
Important: Check for the values accessable. If It does not have the zipcode than do not add it. Or put in its empty value. You must check to see if it can compute the correct result with 
"propertyAddress": {
                    "city": lead.property_city,
                    "street": lead.property_address,
                    "state": lead.property_state,
                    "zip": NONE
                }
'''

import os
import requests
import json
from sqlalchemy import update
from Utility.lead_database import Lead, Session

def skiptrace_leads():
    # API call function
    def api_call(lead_list):
        api_token = os.getenv("BATCHDATA_SKIPTRACE_API_TOKEN")
        headers = {
            'Accept': 'application/json, application/xml',
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }

        data = {"requests": []}

        for lead in lead_list:
            data["requests"].append({
                "propertyAddress": {
                    "city": lead.property_city,
                    "street": lead.property_address,
                    "state": lead.property_state,
                    "zip": lead.property_zipcode
                }
            })

        try:
            response = requests.post('https://api.batchdata.com/api/v1/property/skip-trace', headers=headers, data=json.dumps(data))
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print ("Something went wrong", err)
        
        results = response.json()

        # Return results for all leads
        return results["results"]["persons"]

    # Create a session
    session = Session()

    # Query the database
    leads = session.query(Lead).all()

    # Make a single API call for all leads
    results = api_call(leads)

    for lead, result in zip(leads, results):
        try:
            owner_first_name = result["name"]["first"]
            owner_last_name = result["name"]["last"]
            phone_number_1 = result["phoneNumbers"][0]["number"]
            phone_number_1_type = result["phoneNumbers"][0]["type"]
            phone_number_2 = result["phoneNumbers"][1]["number"]
            phone_number_2_type = result["phoneNumbers"][1]["type"]
            email = result["emails"][0]["email"] if "emails" in result and result["emails"] else None
        except KeyError as err:
            print("KeyError: The key", err, "does not exist in the result")

        # Update the fields in the database
        lead.owner_name = owner_first_name + ' ' + owner_last_name if owner_first_name and owner_last_name else lead.owner_name
        lead.phone_number_1 = phone_number_1 if phone_number_1 else lead.phone_number_1
        lead.phone_number_1_type = phone_number_1_type if phone_number_1_type else lead.phone_number_1_type
        lead.phone_number_2 = phone_number_2 if phone_number_2 else lead.phone_number_2
        lead.phone_number_2_type = phone_number_2_type if phone_number_2_type else lead.phone_number_2_type
        lead.email = email if email else lead.email

    # Commit the changes
    session.commit()
