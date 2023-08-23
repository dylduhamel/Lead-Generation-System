'''
Complete

Notes: Can also pull cinci building inspections 
'''

import os
import math
import pandas as pd
from sodapy import Socrata
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Utility.lead_database import Lead, Session
from Utility.lead_database_operations import add_lead_to_database
from Utility.util import status_print, curr_date, get_address_from_lat_lng

class CinciCodeEnfAPI():
    def __init__(self):
        # Initialization

        #  Load environment variables from .env file
        load_dotenv()

        self.scraper_name = "cinci_code_enf_API.py"
        self.county_website = "Cincinnati Code Enforcement API"

        # App token for authenticated requests
        MyAppToken = os.getenv("CINCI_API_TOKEN")

        # Create a client instance
        self.client = Socrata("data.cincinnati-oh.gov",
                        MyAppToken,
                        username=os.getenv("CINCI_API_USERNAME"),
                        password=os.getenv("CINCI_API_PASSWORD"))
        
        status_print(f"Initialized variables -- {self.scraper_name}")

    def start(self, days):
        status_print(f"Beginning data format and transfer to DB -- {self.scraper_name}")

        # Create a new database Session
        session = Session()

        # Calculate yesterday's date
        self.yesterday = (datetime.now() - timedelta(days)).strftime('%Y-%m-%dT00:00:00.000')

        # Make a request to the API and get the results
        # Filter results for records with an 'entered_date' from yesterday and limit to 2000 results
        results = self.client.get("cncm-znd6", entered_date=self.yesterday, limit=2000)

        # Convert results into a pandas DataFrame
        df = pd.DataFrame.from_records(results)

        try:
            # Select only the desired columns
            df = df[['work_type', 'work_subtype', 'city_id', 'latitude', 'longitude', 'full_address','status_class','data_status_display']]
        except KeyError:
            print(f"No new records on {self.yesterday} for Cinci code enforcments.\n")
            return

        # Filter out rows with 'Building Enforcement' in the 'work_subtype' column
        df = df[df['work_subtype'] != 'Building Enforcement']

        # Convert the DataFrame to JSON and save to a file
        df.to_json('data.json', orient='records')

        # Convert the DataFrame to a list of dictionaries (for each row)
        records = df.to_dict('records')

        status_print(f"Adding records to database -- {self.scraper_name}")

        # Print the records
        for record in records:
            # Create new lead
            lead = Lead()

            # Date added to DB
            time_stamp = curr_date()
            lead.date_added = time_stamp

            # Get property address from google api
            full_address = get_address_from_lat_lng(record["latitude"], record["longitude"])
            try:
                street_address = full_address.split(',')[0].strip()
                lead.property_address = street_address
            except:
                print("Was not able to add property address\n")
            
            # Check if document_type is nan
            if isinstance(record["work_type"], float) and math.isnan(record["work_type"]):
                lead.document_type = None
            else:
                lead.document_type = record["work_type"]
            
            # Check if document_subtype is nan
            if isinstance(record["work_subtype"], float) and math.isnan(record["work_subtype"]):
                lead.document_subtype = None
            else:
                lead.document_subtype = record["work_subtype"]
            
            # City and State 
            lead.property_city = "Cincinnati"
            lead.property_state = "Ohio"

            # Website tracking
            lead.county_website = self.county_website

            #print(lead, '\n')

            # Add lead to database
            session.add(lead)

        # Add new session to DB
        session.commit()
        # Relinquish resources
        session.close()

        status_print(f"DB committed -- {self.scraper_name}")

