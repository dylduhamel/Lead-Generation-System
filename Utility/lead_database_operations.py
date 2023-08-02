import os
import requests
import json
from sqlalchemy import update
from Utility.lead_database import Lead, Session

def add_lead_to_database(lead):
    session = Session()

    try:
        session.add(lead)
        session.commit()
    except Exception as e:
        print(f"Not able to add lead to database. An error has occoured: {e}")
        session.rollback()
    finally:
        session.close()

def json_to_database():
    # Create a session
    session = Session()

    # Query the database (WHERE WE EXTRACT JUST YESTERDAYS DATE
    # 
    # 
    # )
    leads = session.query(Lead).all()

    # Load the results from a json file instead of making an API call
    with open('data.json', 'r') as file:
        results = json.load(file)

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

        # Extract property information
        property_address = result.get("propertyAddress", {}).get("street", {})
        property_city = result.get("propertyAddress", {}).get("city", {})
        property_state = result.get("propertyAddress", {}).get("state", {})
        property_zipcode = result.get("propertyAddress", {}).get("zip", {})

        # Update the fields in the database
        lead.owner_name = owner_first_name + ' ' + owner_last_name if owner_first_name and owner_last_name else lead.owner_name
        lead.phone_number_1 = phone_number_1 if phone_number_1 else lead.phone_number_1
        lead.phone_number_1_type = phone_number_1_type if phone_number_1_type else lead.phone_number_1_type
        lead.phone_number_2 = phone_number_2 if phone_number_2 else lead.phone_number_2
        lead.phone_number_2_type = phone_number_2_type if phone_number_2_type else lead.phone_number_2_type
        lead.email = email if email else lead.email
        lead.property_address = property_address if property_address else lead.property_address
        lead.property_city = property_city if property_city else lead.property_city
        lead.property_state = property_state if property_state else lead.property_state
        lead.property_zipcode = property_zipcode if property_zipcode else lead.property_zipcode

    # Commit the changes
    session.commit()

