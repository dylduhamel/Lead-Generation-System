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


class FortMeyersEnf():
    def __init__(self):
        # Initialization

        # This is used for status tracking
        self.scraper_name = "fort_myers_code_enf.py"
        self.county_website = "Fort Myers Code Enforcement"
        self.url = "https://cdservices.cityftmyers.com/EnerGovProd/SelfService#/search"

        # Set options for headless mode
        # options = Options()
        # options.add_argument('--headless')

        # Initialize the browser (assumes Chrome here)
        self.driver = webdriver.Chrome()

        # File name is entered upon download
        self.download_name = "fort_myers_code_enf"
        self.file_name = self.download_name + ".csv"
        self.file_path = "/home/dylan/Downloads"
        self.read_file = ""
        
        # List of keywords to exclude
        # This exclusion is added because BTR means Business Tax Receipt
        self.exclusions = ["btr", "airbnb", "commercial"]

        status_print(f"Initialized variables -- {self.scraper_name}")
    def download_dataset(self,days):
        
        # Calculate dates needed for download entry 
        today = datetime.now()
        self.today = today.strftime("%m/%d/%Y")

        yesterday = today - timedelta(days=days)
        self.yesterday = yesterday.strftime("%m/%d/%Y")

        # Start driver
        self.driver.get(self.url)

        status_print(f"Chrome driver created. Beginning scraping -- {self.scraper_name}")

        try:
            # Wait for a specific element to be present
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

        except TimeoutException:
            print("Timeout, element not found")

        # Dataset options page
        try: 
            self.dropdown_button = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID,"SearchModule")))
            self.select_dropdown = Select(self.dropdown_button)
            self.select_dropdown.select_by_visible_text("Code Case")
        except NoSuchElementException:
            print("Can not find Code Case.")

        time.sleep(3)

        # Set dates for search
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "button-Advanced")))
            self.driver.find_element(By.ID, "button-Advanced").click()
        except NoSuchElementException:
            print("Can not find Advanced button.")

        # Enter in dates for search 
        try:
            self.driver.execute_script("document.getElementById('OpenedDateFrom').value= arguments[0];", self.yesterday)
        except NoSuchElementException:
            print("Could not find and enter yesterdays date")

        try:
            self.driver.execute_script("document.getElementById('OpenedDateTo').value= arguments[0];", self.today)
        except NoSuchElementException:
            print("Could not find and enter yesterdays date")
        
        # Run query 
        try: 
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID, "button-Search")))
            self.driver.find_element(By.ID, "button-Search").click()
        except NoSuchElementException:
            print("Can not find search button")
        
        # Wait for search to run
        time.sleep(5)

        # Download file 
        try:
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "button-Export")))
            self.driver.find_element(By.ID, "button-Export")
        except NoSuchElementException:
            print("Can not find export button")

        # Name File 
        try:
            self.driver.execute_script("document.getElementById('filename').value= arguments[0];", self.download_name )
        except NoSuchElementException:
            print ("Could not enter file name")

        # Download file 
        try: 
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "Okclick")))
            self.driver.find_element(By.ID, "Okclick")
        except NoSuchElementException:
            print ("Can not find ok button")

        time.sleep(10)

        self.driver.quit()

        status_print(f"Scraping complete. Driver relinquished -- {self.scraper_name}")

    def start(self,days):
        status_print(f"Beginning data format and transfer to DB -- {self.scraper_name}")

        # Create a new database Session
        session = Session()

        # Compute yesterdays date for getting recent entries
        today = datetime.now()

        # Calculate yesterday's date
        self.yesterday = today - timedelta(days=days)
        
        self.read_file = self.file_name + self.file_path

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

        #Convert the Address and Description to lowercase for case-insensitive matching
        df["Address"] = df["Address"].str.lower()
        df["Description"] = df["Description"].str.lower()
        df["Status"] = df["Status"].str.lower()
        df["Type"] = df["Type"].str.lower()
 

        # Handle empty or missing values
        df = df.dropna(subset=['Address', 'Description'])

        selected_rows = pd.DataFrame(columns=df.columns)
        
        # Check if the code inforcement is against a business 
        for exclusion in self.exclusions:
             selected_rows = selected_rows[~selected_rows['Description'].str.contains(exclusion.lower(), case =False, na = False)]
        
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

        print(len(records))

        # Iterate through records
        for record in records:
            # Create new lead
            lead = Lead()

            # Date added to DB
            time_stamp = curr_date()
            lead.date_added = time_stamp

            # Document type
            lead.document_type = record["Type"]

            # Document subtype & description
            lead.document_subtype = record["Description"]

            # Document address 
            lead.property_address = clean_string(record["Address"])

            # Document Zip
            lead.property_zipcode = clean_string(record["Zip"])

            # City and State
            lead.property_city = clean_string(record["City"])
            lead.property_state = clean_string(record["State"])

            print(lead)
            print("\n")

            #session.add(lead)

        # Add new session to DB
        #session.commit()
        # Relinquish resources
        #session.close()

        # Delete the file so it can be run again
        #os.remove(os.path.join(self.file_path, self.file_name))

        status_print(f"DB committed and {self.file_name} removed -- {self.scraper_name}")
