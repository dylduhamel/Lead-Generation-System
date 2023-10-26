import csv
import json
import logging
import pandas as pd
from sqlalchemy import update, text, or_
from Utility.lead_database import Lead, Session
from Utility.util import curr_date, status_print

logging.basicConfig(filename="processing.log", level=logging.ERROR, format='%(asctime)s - %(message)s')

def add_lead_to_database(lead):
    session = Session()

    try:
        session.add(lead)
        session.commit()
    except Exception as e:
        logging.error(f"Not able to add lead to database. An error has occoured: {e}")
        session.rollback()
    finally:
        session.close()


"""
Function to add all skiptraced data to DB
Only adds data to the leads who have date_added == curr_date()
"""


def json_to_database():
    # Create a session
    session = Session()

    # Query for values added today
    today = curr_date()
    #today = "09/27/2023" # If you want to skiptrace date other than today 

    leads = session.query(Lead).filter(Lead.date_added == today).all()
    # leads = session.query(Lead).filter(or_(Lead.date_added == today, Lead.date_added == "10/25/2023")).all()

    # UNIX filename issues
    today = today.replace("/", "-")

    # Load the results from a json file instead of making an API call
    with open(f"./Data/Skiptrace/skiptrace_{today}.json", "r") as file:
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
            phone_number_1 = (
                phone_number_1_type
            ) = phone_number_2 = phone_number_2_type = None

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


def remove_duplicates():
    # Initialize the session
    session = Session()

    # Query to find duplicate rows
    query = f"""
    DELETE t1 FROM leads t1
    INNER JOIN leads t2 
    WHERE t1.id > t2.id AND t1.property_address = t2.property_address
    """

    # Execute the DELETE query
    session.execute(text(query))

    # Commit the changes
    session.commit()

    status_print("Duplicates removed successfully.")


def export_to_csv(filename="output.csv"):
    session = Session()

    today = curr_date()
    # Uncomment below if you want to set a specific date
    # today = "09/27/2023"

    # Query database using session.query
    #code_enforcement_leads = session.query(Lead).filter(Lead.date_added == today).all()
    code_enforcement_leads = session.query(Lead).filter(or_(Lead.date_added == today, Lead.date_added == "10/18/2023")).all()

    # Open a CSV file and write the queried data
    with open(filename, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Writing the header
        writer.writerow(["property_address", "property_city", "property_state", "property_zipcode"])

        # Writing the data rows
        for lead in code_enforcement_leads:
            writer.writerow([lead.property_address, lead.property_city, lead.property_state, lead.property_zipcode])

    session.close()