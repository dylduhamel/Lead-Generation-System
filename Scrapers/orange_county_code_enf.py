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


class OrangeCountyCodeEnf():
    def __init__(self):
        # Initialization
    
        # Set up logging
        logging.basicConfig(filename='processing.log', level=logging.INFO)
        
        self.scraper_name = "orange_county_code_enf.py"
        self.county_website = "Orange County Code Enforcement"
        self.url = "https://netapps.ocfl.net/CETitleViolationSearch/"
        
        # Set options for headless mode
        #options = Options()
        #options.add_argument('--headless')

        # Scraper driver
        self.driver = webdriver.Chrome()

        # Format date for file name
        current_date = datetime.now(pytz.timezone('America/New_York'))
        formatted_date = current_date.strftime("%m%d%Y")

        self.file_name = "OpenActiveCodeEnforcementCases_" + formatted_date + ".xlsx"
        self.file_path = "/home/dylan/Downloads"
        self.read_file = ""

        # Keyword to be excluded 
        self.exclusions = ["on site sign"]

        status_print(f"Initialized variables -- {self.scraper_name}")
    
    def download_dataset(self):
        # Start driver
        self.driver.get(self.url)

        status_print(f"Chrome driver created. Beginning scraping -- {self.scraper_name}")

        try:
            #wait for a specific element to be present
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            print("Timeout, element not found")

        # Download csv
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "lnkSubmit")))
            self.driver.find_element(By.ID, "lnkSubmit").click()
        except NoSuchElementException:
            print("Can not find download button.")   

        # Wait for the file to be downloaded 
        while not os.path.exists(os.path.join(self.file_path, self.file_name)): 
            time.sleep(1)

        # Relinquish resources
        self.driver.quit()

        status_print(f"Scraping complete. Driver relinquished -- {self.scraper_name}")
    
    def start(self, days):
        status_print(f"Beginning data format and transfer to DB -- {self.scraper_name}")

        # Compute yesterdays date for getting recent entries
        today = datetime.now()

        # Calculate yesterday's date
        yesterday = today - timedelta(days=days)

        # Format the date in the desired format (month/day/year) with no leading zero
        formatted_date = yesterday.strftime("%m-%d-%Y")

        # Create a new database Session
        session = Session()
        
        # Path to downloaded xlsx
        # Format for local data set 
        self.read_file = self.file_path + "/" + self.file_name

        # Load the xlsx file into a DataFrame
        try:
            df = pd.read_excel(self.read_file, skiprows=4)
            df.columns = ["Incident ID", "Parcel ID", "Incident Address", "Incident Type", "Incident Status", "Violation Recorded Date"]
        except Exception as e:
            logging.error(f"Failed to load excel file: {e}")
            exit()

        # Convert the 'Violation Recorded Date' column to datetime format
        df['Violation Recorded Date'] = pd.to_datetime(df['Violation Recorded Date'])

        # Filter rows based on a specific date
        specific_date = pd.to_datetime(formatted_date) 
        df = df[df['Violation Recorded Date'] == specific_date]

        # Convert 'Violation Recorded Date' to string in YYYY-MM-DD format
        df['Violation Recorded Date'] = df['Violation Recorded Date'].dt.strftime('%m/%d/%Y')

        # Convert the Incident Type to lowercase for case-insensitive matching 
        df["Incident Type"] = df["Incident Type"].str.lower()

        # Handle empty or missing values 
        df = df.dropna(subset=['Incident Address'])

        # Handle NaN values in 'Incident Type' column
        df["Incident Type"] = df["Incident Type"].fillna("")

        # Filter rows based on exclusions and date
        for exclusion in self.exclusions:
            df = df[~df['Incident Type'].str.contains(exclusion.lower())]

        # Reorder the columns
        df = df[['Incident Address', 'Incident Type', 'Violation Recorded Date']]  # Include 'Violation Recorded Date'

        # Remove duplicates based on 'Address'
        df = df.drop_duplicates(subset='Incident Address')

        records = df.to_dict("records")

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
            lead.document_subtype = clean_string(record["Incident Type"])

            # Document address 
            lead.property_address = clean_string(record["Incident Address"])

            # City and State
            lead.property_city = "Orlando"
            lead.property_state = "Florida"

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
        #os.remove(os.path.join(self.file_path, self.file_name))

        status_print(f"DB committed and {self.file_name} removed -- {self.scraper_name}")


