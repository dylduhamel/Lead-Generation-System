'''
Incomplete
'''

import os
import math
import logging
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
#from Utils.lead_database import Lead
#from Utils.lead_database_operations import add_lead_to_database
#from Utils.geo_location import get_zipcode

class FortMeyersEnf():
    def __init__(self):
        
        # Set up logging
        logging.basicConfig(filename='processing.log', level=logging.INFO)

        ## Load environment variables from .env file
        load_dotenv()

         # Calculate yesterday's date
        self.yesterday = (datetime.now() - timedelta(8)).strftime('%Y-%m-%dT00:00:00.000')
    
        #set file path *temp
        self.read_file = r'C:\Users\Jake\Documents\LISTS\test_code_enf_FM.csv' 

        # Calculate yesterday's date
        

        # List of keywords to search for
        self.keywords = ["nuisance accumulation", "junk", "trash", "lot mow", "plywood", "inoperable", 
                    "tents", "tires", "abandoned", "water", "boat", "grass", "debris", "trailer",
                    "vacant", "damaged roof", "damage", "parts", "trees", "utilities", "refridgerator", "graffiti"]

        # List of keywords to exclude
        self.exclusions = [ "gvwr", "commercial", "btr", "business"]


    def start(self):
        try:
            #load csv into a data frame 
            df = pd.read_csv(self.read_file)
        except Exception as e: 
            logging.error(f"Failed to load CSV file: {e}")
            exit()
        
        try:
            #select only the desired columns
            #this is set up for having the data set from the previous day 
            #if longer is desired want to add "Opened Date", "Closed Date" to determined if case is still open 
            df = df[[ "Address", "Description", "Status", "Type" ]]
        except KeyError:
            print(f"No new records on {self.yesterday} for Cinci code enforcments.\n")

        #df = df.to_dict("records")

        #Convert the Address and Description to lowercase for case-insensitive matching
        df["Address"] = df["Address"].str.lower()
        df["Description"] = df["Description"].str.lower()
        df["Status"] = df["Status"].str.lower()
        df["Type"] = df["Type"].str.lower()
 

        # Handle empty or missing values
        df = df.dropna(subset=['Address', 'Description'])

        selected_rows = pd.DataFrame(columns=df.columns)

            
        keywords_pattern = '|'.join(self.keywords)
        selected_rows = df[df['Description'].str.contains(keywords_pattern, case=False, na=False)]

        # Remove rows where an exclusion keyword is found
        exclusions_pattern = '|'.join(self.exclusions)
        selected_rows = selected_rows[~selected_rows['Description'].str.contains(exclusions_pattern, case=False, na=False)]
        
        selected_rows.to_json("data.json", orient="records")  
        

