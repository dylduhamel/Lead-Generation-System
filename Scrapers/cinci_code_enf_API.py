'''
Incomplete
'''

import os
import math
import pandas as pd
from sodapy import Socrata
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Utils.lead_database import Lead
from Utils.lead_database_operations import add_lead_to_database
from Utils.geo_location import get_zipcode

class CinciCodeEnfAPI():
    def __init__(self):
        ## Load environment variables from .env file
        load_dotenv()

        # App token for authenticated requests
        MyAppToken = os.getenv("CINCI_API_TOKEN")

        # Create a client instance
        self.client = Socrata("data.cincinnati-oh.gov",
                        MyAppToken,
                        username=os.getenv("CINCI_API_USERNAME"),
                        password=os.getenv("CINCI_API_PASSWORD"))

        # Calculate yesterday's date
        # CHANGE DELTA BACK TO 1
        self.yesterday = (datetime.now() - timedelta(8)).strftime('%Y-%m-%dT00:00:00.000')

    def start(self):
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

        # Convert the DataFrame to JSON and save to a file
        df.to_json('data.json', orient='records')

        # Convert the DataFrame to a list of dictionaries (for each row)
        records = df.to_dict('records')

        # Print the records
        for record in records:
            # Create new lead
            lead = Lead()

            # API call to obtain zipcode from coords
            zipcode = get_zipcode(record["latitude"], record["longitude"])
            
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
                
            # Check if full_address is nan
            if isinstance(record["full_address"], float) and math.isnan(record["full_address"]):
                lead.property_address = None
            else:
                lead.property_address = record["full_address"]
            
            if isinstance(zipcode, float) and math.isnan(zipcode):
                lead.property_zipcode = None
            else:
                lead.property_zipcode = zipcode
                
            lead.property_city = "Cincinnati"
            lead.property_state = "OH"

            # add lead to database
            print(lead, '\n')
            #add_lead_to_database(lead)


