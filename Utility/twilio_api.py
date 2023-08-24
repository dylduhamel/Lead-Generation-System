import os
import base64
from dotenv import load_dotenv
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType
from Utility.lead_database import Session, Lead
from Utility.util import curr_date
from sqlalchemy import or_

def email_csv():
    # Load .env file
    load_dotenv()

    # Initialize the session
    session = Session()

    # Query for values added today
    today = curr_date() 

    # Query database using session.query
    code_enforcement_leads = session.query(Lead).filter(Lead.date_added == today, 
                                             Lead.first_name_owner != None, 
                                             Lead.first_name_owner != '', 
                                             Lead.phone_number_1 != None, 
                                             Lead.phone_number_1 != '', 
                                             Lead.document_type == "Code Enforcement").all()

    tax_and_foreclosure_leads = session.query(Lead).filter(Lead.date_added == today, 
                                             Lead.first_name_owner != None, 
                                             Lead.first_name_owner != '', 
                                             Lead.phone_number_1 != None, 
                                             Lead.phone_number_1 != '', 
                                             or_(Lead.document_type == "Foreclosure", Lead.document_type == "Taxdeed")).all()

    # Convert query results to dataframes
    df1 = pd.DataFrame([{column: getattr(lead, column) for column in Lead.__table__.columns.keys()} for lead in code_enforcement_leads])
    df2 = pd.DataFrame([{column: getattr(lead, column) for column in Lead.__table__.columns.keys()} for lead in tax_and_foreclosure_leads])

    if not df1.empty:
        # Get the list of current column names
        cols = list(df1.columns)

        # Remove 'first_name_owner' and 'last_name_owner' from their current positions in the list
        cols.remove('first_name_owner')
        cols.remove('last_name_owner')

        # Add 'first_name_owner' and 'last_name_owner' at the desired positions
        cols.insert(2, 'first_name_owner')  # at index 2 
        cols.insert(3, 'last_name_owner')   # at index 3

        # Reorder the dataframe according to the modified list of column names
        df1 = df1[cols]

    if not df2.empty:
        # Get the list of current column names
        cols = list(df2.columns)

        # Remove 'first_name_owner' and 'last_name_owner' from their current positions in the list
        cols.remove('first_name_owner')
        cols.remove('last_name_owner')

        # Add 'first_name_owner' and 'last_name_owner' at the desired positions
        cols.insert(2, 'first_name_owner')  # at index 2 
        cols.insert(3, 'last_name_owner')   # at index 3

        # Reorder the dataframe according to the modified list of column names
        df2 = df2[cols]

    # Convert DataFrames to CSV and save
    csv_filepath1 = "./Data/csv_exports/code_enforcement.csv"
    csv_filepath2 = "./Data/csv_exports/foreclosure_taxdeed.csv"
    csv_filename1 = "code_enforcement.csv"
    csv_filename2 = "foreclosure_taxdeed.csv"
    df1.to_csv(csv_filepath1, index=False)
    df2.to_csv(csv_filepath2, index=False)

    # Load SendGrid API key and email addresses
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL") 
    TO_EMAIL = os.getenv("TO_EMAIL")  
    TO_EMAIL_SELF = os.getenv("TO_EMAIL_SELF")

    # Read CSV data and convert to Base64
    with open(csv_filepath1, "rb") as f:
        data1 = base64.b64encode(f.read()).decode()
    with open(csv_filepath2, "rb") as f:
        data2 = base64.b64encode(f.read()).decode()

    # Create attachments
    attachment1 = Attachment(
        FileContent(data1),
        FileName(csv_filename1),
        FileType('text/csv')
    )
    attachment2 = Attachment(
        FileContent(data2),
        FileName(csv_filename2),
        FileType('text/csv')
    )

    # Create message
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=[TO_EMAIL, TO_EMAIL_SELF],
        subject='Sending CSV Data',
        plain_text_content='Hey Gents,\n\n\tHere is all of the data pulled in the last 24 hours.'
    )

    message.attachment = [attachment1, attachment2]

    # Create SendGrid client
    sg = SendGridAPIClient(SENDGRID_API_KEY)

    # Send email
    response = sg.send(message)

    print(response.status_code)