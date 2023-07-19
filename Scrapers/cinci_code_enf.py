import os
import time
import math
import pandas as pd
import logging
from sodapy import Socrata
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Utils.lead_database import Lead
from Utils.lead_database_operations import add_lead_to_database
from Utils.geo_location import get_zipcode
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CinciCodeEnf():
    def __init__(self):
        # Initialization
        self.url = "https://cagismaps.hamilton-co.org/PropertyActivity/propertyMaintenance"
        self.driver = webdriver.Chrome()
        self.file_name = "PropertyActivity.csv"
        self.file_path = "/home/dylan/Downloads"
        self.read_file = ""

    def download_dataset(self):
        # Start driver
        self.driver.get(self.url)

        try:
            # Wait for a specific element to be present
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

        except TimeoutException:
            print("Timeout, element not found")

        # Dataset options page
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,"recordDetailsButton")))
            self.driver.find_element(By.ID,"recordDetailsButton").click()
        except NoSuchElementException:
            print("Can not find record details button.")

        # Download page
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exportButton")))
            self.driver.find_element(By.ID, "exportButton").click()
        except NoSuchElementException:
            print("Can not find download button.")

        # Date dropdown selection
        try:
            # Wait for the dropdown button to be clickable and click it
            dropdown_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'exportDateRangeDropdown'))
            )
            dropdown_button.click()

            # Wait for the options to be visible and click the desired option
            dropdown_option = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[7]/div/div/div[2]/div[2]/div/div/div[2]/ul/li[8]/a'))  # Replace 'Option Text' with your option
            )
            dropdown_option.click()
        except NoSuchElementException:
            print("Can not find dropdown.")

        # Limit records checkbox
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div/div[2]/div[2]/div/div/div[4]/ul/li/div/label")))
            self.driver.find_element(By.XPATH, "/html/body/div[7]/div/div/div[2]/div[2]/div/div/div[4]/ul/li/div/label").click()
        except NoSuchElementException:
            print("Can not find checkbox.")

        # Download csv
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exportDataSubmitBtn")))
            self.driver.find_element(By.ID, "exportDataSubmitBtn").click()
        except NoSuchElementException:
            print("Can not find download button.")

        # Wait for the file to be downloaded
        while not os.path.exists(os.path.join(self.file_path, self.file_name)): 
            time.sleep(1)

        # Relinquish resources
        self.driver.quit()

        # DELETE FILE FOR NEXT TIME

    def start(self):
        #format for local data set 
        self.read_file = self.file_path + "/" + self.file_name

        # List of keywords to search for
        self.keywords = ["code enforcement - buildings with residences", "trash/litter/tall grass complaint", "zoning code enforcement - residential uses", "abandoned vehicle code enforcement", "health environmental code enforcement"]

        try:
            df = pd.read_csv(self.read_file)
        except Exception as e:
            logging.error(f"Failed to load CSV file: {e}")
            exit()
        
        try:
            df= df[["COMP_TYPE_DESC", "X_COORD", "Y_COORD", "YN_ACTIVITY_REPORT", "STREET_NO", "STREET_DIRECTION", "STREET_NAME", "COMP_TYPE_DESC", "WORK_TYPE"]] 
        except KeyError:
            print(f"No new records for Cinci code enforcments.\n")

        # Drop rows with empty values
        df = df.dropna(subset=[ "X_COORD", "Y_COORD", "STREET_NAME"])

        # Drop the second occurrence of the "COMP_TYPE_DESC" column
        df = df.loc[:, ~df.columns.duplicated()]

        # Convert the keywords list into a regex pattern
        keywords_pattern = '|'.join(self.keywords)

        # Check the "COMP_TYPE_DESC" column for the keywords
        mask_keywords = df['COMP_TYPE_DESC'].astype(str).str.contains(keywords_pattern, case=False, na=False)

        # Check the "YN_ACTIVITY_REPORT" column for the value "Y"
        mask_activity = df['YN_ACTIVITY_REPORT'] == 'Y'

        # Combine the two masks using the & operator to ensure both conditions are met
        combined_mask = mask_keywords & mask_activity

        # Filter the DataFrame based on the combined mask
        selected_rows = df[combined_mask]
        
        records = selected_rows.to_dict("records")

        for record in records:
            # Create new lead
            lead = Lead()

            

