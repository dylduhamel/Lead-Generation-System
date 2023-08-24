'''
Incomplete
'''

import os
import time
import math
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
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

logging.basicConfig(filename="processing.log", level=logging.ERROR, format='%(asctime)s - %(message)s')

class FortMeyersEnf():
    def __init__(self):
        # Initialization

        # This is used for status tracking
        self.scraper_name = "fort_myers_code_enf.py"
        self.county_website = "Fort Myers Code Enforcement"
        self.url = "https://cdservices.cityftmyers.com/EnerGovProd/SelfService#/search"

        # # Set options for headless mode
        # options = Options()
        # options.add_argument('--headless')

        # Initialize the browser (assumes Chrome here)
        self.driver = webdriver.Chrome()

        # File name is entered upon download
        self.download_name = "fort_myers_code_enf"
        self.file_name = self.download_name + ".csv"
        self.file_path = "/home/dylan/Downloads"
        self.read_file = self.file_path + "/" + self.file_name
        
        # List of keywords to exclude
        # This exclusion is added because BTR means Business Tax Receipt
        self.exclusions = ["btr", "airbnb", "commercial"]

        status_print(f"Initialized variables -- {self.scraper_name}")

    def download_dataset(self,days):
        # Calculate dates needed for download entry 
        today = datetime.now()
        start_date = today - timedelta(days=days)
        end_date = today - timedelta(days=1)
        self.start_date = start_date.strftime("%m/%d/%Y")
        self.end_date = end_date.strftime("%m/%d/%Y")

        # Start driver
        self.driver.get(self.url)

        status_print(f"Chrome driver created. Beginning scraping -- {self.scraper_name}")

        try:
            # Wait for a specific element to be present
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "SearchModule"))
            )
        except Exception as e:
            logging.error("Timeout, element not found")

        time.sleep(5)

        # Record dropdown selection
        try:
            # Locate the dropdown element
            dropdown_element = self.driver.find_element(By.ID, "SearchModule")

            # Create a Select object based on the dropdown element
            select = Select(dropdown_element)

            # Select the option by visible text
            select.select_by_visible_text("Code Case")
        except Exception as e:
            logging.error("Can not find dropdown.")

        time.sleep(3)

        # Advanced settings
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "button-Advanced")))
            self.driver.find_element(By.ID, "button-Advanced").click()
        except Exception as e:
            logging.error("Can not find Advanced button.")

        # Enter in dates for search 
        try:
            # Locate the data input start box
            date_start_element = self.driver.find_element(By.ID, "OpenedDateFrom")
            
            # Clear box if it has any input
            date_start_element.clear()

            # Input the value for yesterday
            date_start_element.send_keys(self.start_date)
        except Exception as e:
            logging.error("Could not find and enter yesterdays date")

        try:
            # Locate the data input end box
            date_end_element = self.driver.find_element(By.ID, "OpenedDateTo")
            
            # Clear box if it has any input
            date_end_element.clear()

            # Input the value for yesterday
            date_end_element.send_keys(self.end_date)
        except Exception as e:
            logging.error("Could not find and enter todays date")
        
        # Run query 
        try: 
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID, "button-Search")))
            self.driver.find_element(By.ID, "button-Search").click()
        except Exception as e:
            logging.error("Can not find search button")
        
        # Wait for search to run
        time.sleep(20)

        # Download file 
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "button-Export")))
            self.driver.find_element(By.ID, "button-Export").click()
        except Exception as e:
            logging.error("Can not find export button")

        time.sleep(5)
        
        # Name File 
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "filename")))
            # Locate the data input end box
            filename_element = self.driver.find_element(By.ID, "filename")
            
            # Clear box if it has any input
            filename_element.clear()

            # Input the value for yesterday
            filename_element.send_keys(self.download_name)
        except Exception as e:
            logging.error("Could not enter file name")

        time.sleep(1)

        # Download file 
        try: 
            WebDriverWait(self.driver, 25).until(EC.presence_of_element_located((By.ID, "Okclick")))
            self.driver.find_element(By.ID, "Okclick").click()
        except Exception as e:
            logging.error("Can not find ok button")

        # Timing of attmepted download
        start_time = time.time()
        elapsed_time = 0

        # Wait for the file to be downloaded or for 45 seconds to elapse
        while not os.path.exists(os.path.join(self.file_path, self.file_name)) and elapsed_time < 45:
            time.sleep(1)
            elapsed_time = time.time() - start_time

        # Check if the file hasn't been downloaded after 45 seconds
        if not os.path.exists(os.path.join(self.file_path, self.file_name)):
            logging.error(f"File was not downloaded after 45 seconds! : For scraper {self.scraper_name}")

        # Relinquish resources
        self.driver.quit()

        status_print(f"Scraping complete. Driver relinquished -- {self.scraper_name}")

    def start(self):
        status_print(f"Beginning data format and transfer to DB -- {self.scraper_name}")

        # Create a new database Session
        session = Session()

        try:
            #load csv into a data frame 
            df = pd.read_csv(self.read_file)
        except Exception as e: 
            logging.error(f"Failed to load CSV file: {e}")
            exit()

        #Convert the description to lowercase for case-insensitive matching
        df["Description"] = df["Description"].str.lower()
 
        # Handle empty or missing values
        df = df.dropna(subset=['Address', 'Description'])
    
        # Create a new DataFrame to hold rows where a keyword is found
        selected_rows = pd.DataFrame(columns=df.columns)
        
        # Copy all over from df
        selected_rows = df.copy()

        # Check if the code inforcement is against a business 
        for exclusion in self.exclusions:
             selected_rows = selected_rows[~selected_rows['Description'].str.contains(exclusion.lower(), case =False, na = False)]
        
        # Ensure the address is within FORT MYERS
        selected_rows = selected_rows[selected_rows['Address'].str.contains('FORT MYERS')]

        # Parse and format the address
        selected_rows[['Address', 'Rest']] = selected_rows['Address'].str.split('FORT MYERS', n=1, expand=True)

        # Split the 'Rest' field into separate 'State', 'Zip' fields
        selected_rows[['State', 'Zip']] = selected_rows['Rest'].str.split('FL', n=1, expand=True)

        # Populate 'State' column with 'FL'
        selected_rows['State'] = 'FL'

        # Populate 'City' column with 'FORT MYERS'
        selected_rows['City'] = 'FORT MYERS'

        # Remove unnecessary columns
        selected_rows = selected_rows.drop(columns=['Rest'])

        #strip leading and trailing whitespaces
        selected_rows['Address'] = selected_rows['Address'].str.strip()
        selected_rows['Zip'] = selected_rows['Zip'].str.strip()  
        
        records = selected_rows.to_dict("records")

        status_print(f"adding records to database -- {self.scraper_name}")

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
