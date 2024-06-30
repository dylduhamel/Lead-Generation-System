import csv
import json
import logging

from sqlalchemy import or_, text, update

from utils.lead_database import Lead, Session
from utils.util import curr_date, status_print

logging.basicConfig(filename="processing.log", level=logging.ERROR, format='%(asctime)s - %(message)s')


def add_lead_to_database(lead):
    session = Session()

    try:
        session.add(lead)
        session.commit()
    except Exception as e:
        logging.error(
            f"Not able to add lead to database. An error has occoured: {e}")
        session.rollback()
    finally:
        session.close()


def json_to_database():
    # Create a session
    session = Session()

    # Query for values added today
    today = curr_date()
    # today = "09/27/2023" # If you want to skiptrace date other than today

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
            result.get("emails", [{}])[0].get(
                "email") if result.get("emails") else None
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
    DELETE t1 FROM LEAD_DB_STANDARD.LEAD t1
    INNER JOIN LEAD_DB_STANDARD.LEAD t2 
    WHERE t1.LEAD_ID > t2.LEAD_ID AND t1.PROPERTY_ADDRESS = t2.PROPERTY_ADDRESS
    """

    # Execute the DELETE query
    session.execute(text(query))

    # Commit the changes
    session.commit()

    status_print("Duplicates removed successfully.")


def export_to_csv():
    session = Session()

    today = curr_date()
    # Uncomment below if you want to set a specific date
    # today = "09/27/2023"

    filename = f"email-marketing-{today.replace('/', '-')}.csv"

    # Query database using session.query
    leads = session.query(Lead).filter(Lead.date_added == today,
                                       Lead.first_name_owner != None,
                                       Lead.email != None).all()

    # leads = session.query(Lead).filter(or_(Lead.date_added == today, Lead.date_added == "10/18/2023")).all()

    # Open a CSV file and write the queried data
    with open(filename, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Writing the header
        writer.writerow(["date_added", "property_address",
                        "first_name_owner", "last_name_owner", "email"])

        # Writing the data rows
        for lead in leads:
            writer.writerow([lead.date_added, lead.property_address, lead.first_name_owner.capitalize(
            ), lead.last_name_owner.capitalize(), lead.email])

    session.close()
