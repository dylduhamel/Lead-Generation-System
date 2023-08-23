'''
Complete

Note: This does not return the zipcode. Only the street, city, state
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
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

logging.basicConfig(filename="processing.log", level=logging.ERROR, format='%(asctime)s - %(message)s')

class CinciCodeEnf():
    def __init__(self):
        # Initialization

        # This is used for status tracking
        self.scraper_name = "cinci_code_enf.py"
        self.county_website = "Cincinnati Code Enforcement"
        self.url = "https://cagismaps.hamilton-co.org/PropertyActivity/propertyMaintenance"

        # Set options for headless mode
        # options = Options()
        # options.add_argument('--headless')

        # Initialize the browser (assumes Chrome here)
        self.driver = webdriver.Chrome()

        self.file_name = "PropertyActivity.csv"
        self.file_path = "/home/dylan/Downloads"
        #self.file_path = "/Users/dylanduhamel/Downloads"
        self.read_file = ""

        status_print(f"Initialized variables -- {self.scraper_name}")

    def download_dataset(self):
        # Start driver
        self.driver.get(self.url)

        status_print(f"Chrome driver created. Beginning scraping -- {self.scraper_name}")

        try:
            # Wait for a specific element to be present
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

        except Exception as e:
            logging.error("Timeout, element not found")

        # Dataset options page
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,"recordDetailsButton")))
            self.driver.find_element(By.ID,"recordDetailsButton").click()
        except Exception as e:
            logging.error("Can not find record details button.")


        # Wait for page to load completely
        time.sleep(10)
        
        # Download page
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exportButton")))
            self.driver.find_element(By.ID, "exportButton").click()
        except Exception as e:
            logging.error("Can not find download button.")

        # Date dropdown selection
        try:
            # Wait for the dropdown button to be clickable and click it
            dropdown_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'exportDateRangeDropdown'))
            )
            dropdown_button.click()

            # Wait for the options to be visible and click the desired option
            dropdown_option = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[7]/div/div/div[2]/div[2]/div/div/div[2]/ul/li[8]/a')) 
            )
            dropdown_option.click()
        except Exception as e:
            logging.error("Can not find dropdown.")

        time.sleep(3)

        # Limit records checkbox
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "limitedToView")))
            self.driver.find_element(By.ID, "limitedToView").click()
        except Exception as e:
            logging.error("Can not find checkbox.")

        time.sleep(3)

        # Download csv
        try:
            WebDriverWait(self.driver, 25).until(EC.presence_of_element_located((By.ID, "exportDataSubmitBtn")))
            self.driver.find_element(By.ID, "exportDataSubmitBtn").click()
        except Exception as e:
            logging.error("Can not find download button.")

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
        self.yesterday = today - timedelta(days=days)

        # Format the date in the desired format (month/day/year) with no leading zero
        self.formatted_date = self.yesterday.strftime("%-m/%-d/%Y")

        # Create a new database Session
        session = Session()

        # Path to downloaded CSV
        # Format for local data set 
        self.read_file = self.file_path + "/" + self.file_name

        # List of keywords to search for
        #self.keywords = ["code enforcement - buildings with residences", "trash/litter/tall grass complaint", "zoning code enforcement - residential uses", "abandoned vehicle code enforcement", "health environmental code enforcement"]
        self.keywords = [""]

        try:
            df = pd.read_csv(self.read_file)
        except Exception as e:
            logging.error(f"Failed to load CSV file: {e}")
            exit()
        
        try:
            df= df[["COMP_TYPE_DESC", "X_COORD", "Y_COORD", "YN_ACTIVITY_REPORT", "STREET_NO", "STREET_DIRECTION", "STREET_NAME", "COMP_TYPE_DESC", "WORK_TYPE", "ENTERED_DATE"]] 
        except KeyError:
            logging.error(f"No new records for Cinci code enforcments.\n")

        # Drop rows with empty values
        df = df.dropna(subset=[ "X_COORD", "Y_COORD", "STREET_NAME"])

        # Drop the second occurrence of the "COMP_TYPE_DESC" column
        df = df.loc[:, ~df.columns.duplicated()]

        # Convert the keywords list into a regex pattern
        #keywords_pattern = '|'.join(self.keywords)

        # Check the "COMP_TYPE_DESC" column for the keywords
        #mask_keywords = df['COMP_TYPE_DESC'].astype(str).str.contains(keywords_pattern, case=False, na=False)

        # Check the "YN_ACTIVITY_REPORT" column for the value "Y"
        mask_activity = df['YN_ACTIVITY_REPORT'] == 'Y'

        # Combine the two masks using the & operator to ensure both conditions are met
        #combined_mask = mask_keywords & mask_activity

        # Filter the DataFrame based on the combined mask
        selected_rows = df[mask_activity]
        
        records = selected_rows.to_dict("records")

        status_print(f"Adding records to database -- {self.scraper_name}")

        # Iterate through records
        for record in records:
            if record["ENTERED_DATE"] == self.formatted_date:
                # Create new lead
                lead = Lead()

                # Date added to DB
                time_stamp = curr_date()
                lead.date_added = time_stamp

                # Document type
                lead.document_type = "Code Enforcement"

                # Document subtype & description
                lead.document_subtype = record["COMP_TYPE_DESC"]

                # Append street_no to street_name
                street_num = str(int(record["STREET_NO"]))
                address = street_num + " " + record["STREET_NAME"]
                lead.property_address = clean_string(address)

                # City and State
                lead.property_city = "Cincinnati"
                lead.property_state = "Ohio"

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
