import sys

sys.path.append("..")

import csv
import json
import logging
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import or_, text, update
from utils.lead_database import Lead, Session
from utils.util import status_print, call_api


def add_lead_to_database(full_addr, doc_type):
    parsed_addr = call_api("parse", method="post", data=full_addr)

    addr_object = {
        "property_number": parsed_addr["house_number"],
        "property_street": parsed_addr["road"],
        "property_city": parsed_addr["city"],
        "property_state": parsed_addr["state"],
        "property_zipcode": parsed_addr["postcode"],
    }

    res = call_api("check-duplicate", method="post", data=addr_object)
    if not res["is_duplicate"]:
        lead = Lead()
        lead.document_type = doc_type
        lead.property_number = parsed_addr["house_number"]
        lead.property_street = parsed_addr["road"]
        lead.property_city = parsed_addr["city"]
        lead.property_state = parsed_addr["state"]
        lead.property_zipcode = parsed_addr["postcode"]

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

    # Define todays date range
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    leads = (
        session.query(Lead)
        .filter(Lead.date_added >= today, Lead.date_added < tomorrow)
        .all()
    )

    # Load the results from a json file instead of making an API call
    with open(f"/tmp/skiptrace_{today}.json", "r") as file:
        results = json.load(file)

    for lead, result in zip(leads, results):
        owner_first_name = result.get("name", {}).get("first")
        owner_last_name = result.get("name", {}).get("last")

        # Check if "phoneNumbers" key exists and its associated list is not empty
        phone_numbers = result.get("phoneNumbers", [])
        if phone_numbers:
            phone_number_1 = phone_numbers[0].get("number")
            phone_number_1_type = phone_numbers[0].get("type")
            phone_number_2 = None
            phone_number_2_type = None
            if len(phone_numbers) > 1:
                phone_number_2 = phone_numbers[1].get("number")
                phone_number_2_type = phone_numbers[1].get("type")
        else:
            phone_number_1 = phone_number_1_type = phone_number_2 = (
                phone_number_2_type
            ) = None

        email = (
            result.get("emails", [{}])[0].get("email") if result.get("emails") else None
        )

        # Update the fields in the database
        lead.first_name_owner = (
            owner_first_name if owner_first_name else lead.first_name_owner
        )
        lead.last_name_owner = (
            owner_last_name if owner_last_name else lead.last_name_owner
        )
        lead.phone_number_1 = phone_number_1 if phone_number_1 else lead.phone_number_1
        lead.phone_number_1_type = (
            phone_number_1_type if phone_number_1_type else lead.phone_number_1_type
        )
        lead.phone_number_2 = phone_number_2 if phone_number_2 else lead.phone_number_2
        lead.phone_number_2_type = (
            phone_number_2_type if phone_number_2_type else lead.phone_number_2_type
        )
        lead.email = email if email else lead.email

    # Commit the changes
    session.commit()
    status_print("JSON-DB - Committed.")

def export_to_csv():
    session = Session()

    # Define todays date range
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    filename = f"email-marketing-{today.replace('/', '-')}.csv"

    # Query database using session.query
    leads = (
        session.query(Lead)
        .filter(
            Lead.date_added >= today,
            Lead.date_added < tomorrow,
            Lead.first_name_owner != None,
            Lead.email != None,
        )
        .all()
    )

    # Open a CSV file and write the queried data
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Writing the header
        writer.writerow(
            [
                "date_added",
                "property_number",
                "property_street",
                "property_city",
                "property_state",
                "property_zipcode",
                "first_name_owner",
                "last_name_owner",
                "email",
            ]
        )

        # Writing the data rows
        for lead in leads:
            writer.writerow(
                [
                    lead.date_added,
                    lead.property_number,
                    lead.property_street,
                    lead.property_state,
                    lead.property_zipcode,
                    lead.first_name_owner.capitalize(),
                    lead.last_name_owner.capitalize(),
                    lead.email,
                ]
            )

    session.close()
