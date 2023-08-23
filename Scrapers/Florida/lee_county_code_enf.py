'''
Complete
'''

import os
import time
import math
import datetime
import pytz
import pandas as pd
import logging
from sodapy import Socrata
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Utility.lead_database import Lead, Session
from Utility.lead_database_operations import add_lead_to_database
from Utility.util import get_zipcode, curr_date, status_print, clean_string
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

logging.basicConfig(filename="processing.log", level=logging.ERROR, format='%(asctime)s - %(message)s')

class LeeCountyCodeEnf():
    def __init__(self):
        # Initialization
    
        self.scraper_name = "lee_county_code_enf.py"
        self.county_website = "Lee County Code Enforcement"
        self.url = "https://accelaaca.leegov.com/aca/Cap/CapHome.aspx?module=CodeEnforcement&TabName=CodeEnforcement"
        
        # Set options for headless mode
        #options = Options()
        #options.add_argument('--headless')

        self.driver = webdriver.Chrome()

        # Format date for file name
        current_date = datetime.now(pytz.timezone('America/New_York'))
        formatted_date = current_date.strftime("%Y%m%d")
        

        self.file_name = "RecordList" + formatted_date + ".csv"
        self.file_path = "/home/dylan/Downloads"
        # Path to downloaded CSV
        self.read_file = self.file_path + "/" + self.file_name

        # List of keywords to search for
        self.keywords = ["Nuisance Accumulation", "junk", "trash", "lot mow", "plywood", "Inoperable", 
                    "tents", "tires", "Abandoned", "boat", "Overgrown grass", "debris", 
                    "vacant", "damaged roof", "damage", "parts"]

        # List of keywords to exclude
        self.exclusions = ["Permit", "construction", "GVWR", "Builder", "vacant"]

        status_print(f"Initialized variables -- {self.scraper_name}")
    
    def download_dataset(self, days):
        status_print(f"Chrome driver created. Beginning scraping -- {self.scraper_name}")

        # Compute yesterdays date for getting recent entries
        today = datetime.now()

        # Calculate yesterday's date
        yesterday = today - timedelta(days=days)

        # Format the date in the desired format (month/day/year) with no leading zero
        formatted_date = yesterday.strftime("%m/%d/%Y")

        # Start driver
        self.driver.get(self.url)

        try:
            # Wait for a specific element to be present
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except Exception as e:
            logging.error("Timeout, element not found")

        # Record dropdown selection
        try:
            select = Select(self.driver.find_element(By.ID, "ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType"))

            # Select the option by its value
            select.select_by_value("CodeEnforcement/Complaint/NA/NA")
        except Exception as e:
            logging.error("Can not find dropdown.")

        time.sleep(1)

        # Time input start
        try:
            # Change the search date range
            curr_date_input = self.driver.find_element(By.ID, "ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate")
            # Use JavaScript to set the value of the element
            self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
            """, curr_date_input, formatted_date)
        except Exception as e:
            logging.error("Can not input box.")

        # Time input end
        try:
            # Change the search date range
            curr_date_input = self.driver.find_element(By.ID, "ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate")
            # Use JavaScript to set the value of the element
            self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
            """, curr_date_input, formatted_date)
        except Exception as e:
            logging.error("Can not input box.")

        time.sleep(1)

        # Search 
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_PlaceHolderMain_btnNewSearch")))
            self.driver.find_element(By.ID, "ctl00_PlaceHolderMain_btnNewSearch").click()
        except Exception as e:
            logging.error("Can not find search button")

        # Download csv
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList_gdvPermitListtop4btnExport")))
            self.driver.find_element(By.ID, "ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList_gdvPermitListtop4btnExport").click()
        except Exception as e:
            logging.error("Can not find download button.")    

        # Wait for the file to be downloaded 
        while not os.path.exists(os.path.join(self.file_path, self.file_name)): 
            time.sleep(1)

        # Relinquish resources
        self.driver.quit()

        status_print(f"Scraping complete. Driver relinquished -- {self.scraper_name}")
        
    def start(self):
        status_print(f"Beginning data format and transfer to DB -- {self.scraper_name}")

        # Create a new database Session
        session = Session()

        try:
            # Load the csv file into a DataFrame
            df = pd.read_csv(self.read_file)
        except Exception as e:
            logging.error(f"Failed to load CSV file: {e}")
            exit()
        
        # Convert the Description to lowercase for case-insensitive matching 
        df['Description'] = df['Description'].str.lower()

        # Handle empty or missing values
        df = df.dropna(subset=['Address', 'Description'])

        # Create a new DataFrame to hold rows where a keyword is found
        selected_rows = pd.DataFrame(columns=df.columns)

        for keyword in self.keywords:
            keyword_rows = df[df['Description'].str.contains(keyword.lower())]
            selected_rows = pd.concat([selected_rows, keyword_rows])
            
        # Remove rows where an exclusion keyword is found
        for exclusion in self.exclusions:
            selected_rows = selected_rows[~selected_rows['Description'].str.contains(exclusion.lower())]

        # Remove rows where status is closed
        selected_rows = selected_rows[~selected_rows['Status'].str.contains("Closed-Non Enforcement")]

        # Split the 'Address' field into separate 'Address', 'City_State_Zip' fields
        selected_rows[['Address', 'City_State_Zip']] = selected_rows['Address'].str.split(',', n=1, expand=True)

        # Split the 'City_State_Zip' field into separate 'City', 'State_Zip' fields
        selected_rows[['City', 'State_Zip']] = selected_rows['City_State_Zip'].str.split('FL', n=1, expand=True)

        # Split the 'State_Zip' field into separate 'State', 'Zip' fields
        selected_rows[['State', 'Zip']] = selected_rows['State_Zip'].str.split(' ', n=1, expand=True)

        # Remove unnecessary columns
        selected_rows = selected_rows.drop(columns=['Record Number', 'Status', 'Related Records', 'City_State_Zip', 'State_Zip'])

        # Populate 'State' column with 'FL'
        selected_rows['State'] = 'FL'

        # Reorder the columns
        selected_rows = selected_rows[['Address', 'City', 'State', 'Zip', 'Description']]

        # Remove duplicates based on 'Address'
        selected_rows = selected_rows.drop_duplicates(subset='Address')

        records = selected_rows.to_dict("records")

        status_print(f"Adding records to database -- {self.scraper_name}")

        # Iterate through records
        for record in records:
            # Create new lead
            lead = Lead()

            # Date added to DB
            time_stamp = curr_date()
            lead.date_added = time_stamp

            # Document type
            lead.document_type = "Code Enforcement"

            # Document subtype & description
            lead.document_subtype = record["Description"]

            # Document address 
            lead.property_address = clean_string(record["Address"])

            # Document Zip
            lead.property_zipcode = clean_string(record["Zip"])

            # City and State
            lead.property_city = clean_string(record["City"])
            lead.property_state = clean_string(record["State"])

            # Website tracking
            lead.county_website = self.county_website

            # print(lead)
            # print("\n")

            session.add(lead)

        # Add new session to DB
        session.commit()
        # Relinquish resources
        session.close()

        # Delete the file so it can be run again
        os.remove(os.path.join(self.file_path, self.file_name))

        status_print(f"DB committed and {self.file_name} removed -- {self.scraper_name}")
