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
            # Create a base data object
            data_object = {
                "propertyAddress": {
                    "city": lead.property_city,
                    "street": lead.property_address,
                    "state": lead.property_state
                }
            }

            # Add zipcode if it's not None
            if lead.property_zipcode is not None:
                data_object["propertyAddress"]["zip"] = lead.property_zipcode

            # Append to the requests list
            data["requests"].append(data_object)

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

    # Query the database (WHERE WE EXTRACT JUST YESTERDAYS DATE
    # 
    # !!!!!!!!!!
    # )
    leads = session.query(Lead).all()

    # Make a single API call for all leads
    results = api_call(leads)

    # Export json to data.json
    with open('skip_trace.json', 'w') as file:
        json.dump(results, file)

    for lead, result in zip(leads, results):
        owner_first_name = result.get("name", {}).get("first")
        owner_last_name = result.get("name", {}).get("last")

        # Check if "phoneNumbers" key exists and its associated list is not empty
        phone_numbers = result.get("phoneNumbers", [])
        if phone_numbers:
            phone_number_1 = phone_numbers[0].get("number")
            phone_number_1_type = phone_numbers[0].get("type")

            if len(phone_numbers) > 1:
                phone_number_2 = phone_numbers[1].get("number")
                phone_number_2_type = phone_numbers[1].get("type")
        else:
            phone_number_1 = phone_number_1_type = phone_number_2 = phone_number_2_type = None

        email = result.get("emails", [{}])[0].get("email") if result.get("emails") else None

        # Update the fields in the database
        lead.owner_name = owner_first_name + ' ' + owner_last_name if owner_first_name and owner_last_name else lead.owner_name
        lead.phone_number_1 = phone_number_1 if phone_number_1 else lead.phone_number_1
        lead.phone_number_1_type = phone_number_1_type if phone_number_1_type else lead.phone_number_1_type
        lead.phone_number_2 = phone_number_2 if phone_number_2 else lead.phone_number_2
        lead.phone_number_2_type = phone_number_2_type if phone_number_2_type else lead.phone_number_2_type
        lead.email = email if email else lead.email

    # Commit the changes
    session.commit()
