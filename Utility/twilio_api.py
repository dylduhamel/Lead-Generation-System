import os
import base64
from dotenv import load_dotenv
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType
from Utility.lead_database import Session
from Utility.util import curr_date

def send_email():
    # Load .env file
    load_dotenv()

    # Current date
    current_date = curr_date()

    # Initialize the session
    session = Session()

    # Write SQL queries
    query1 = "SELECT * FROM leads"  
    query2 = "SELECT * FROM leads WHERE document_type = 'Lien'" 

    # Use session to execute queries and get dataframes
    df1 = pd.read_sql_query(query1, session.bind)
    df2 = pd.read_sql_query(query2, session.bind)

    # Convert DataFrames to CSV and save
    # ADD DATE!!!!!
    csv_filename1 = "code_enforcement.csv"
    csv_filename2 = "lien_lis_penden.csv"
    df1.to_csv(csv_filename1, index=False)
    df2.to_csv(csv_filename2, index=False)

    # Load SendGrid API key and email addresses
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")  # The email to send from
    TO_EMAIL = os.getenv("TO_EMAIL")  # The email to send to

    # Read CSV data and convert to Base64
    with open(csv_filename1, "rb") as f:
        data1 = base64.b64encode(f.read()).decode()
    with open(csv_filename2, "rb") as f:
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
        to_emails=TO_EMAIL,
        subject='Sending CSV Data',
        plain_text_content='Your first complete Acuritas lead generating results are attached.'
    )

    message.attachment = [attachment1, attachment2]

    # Create SendGrid client
    sg = SendGridAPIClient(SENDGRID_API_KEY)

    # Send email
    response = sg.send(message)

    print(response.status_code)