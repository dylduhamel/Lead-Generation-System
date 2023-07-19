import os
import math
import pandas as pd
import logging
#from sodapy import Socrata
#from datetime import datetime, timedelta
#from dotenv import load_dotenv
#from Utils.lead_database import Lead
#from Utils.lead_database_operations import add_lead_to_database
#from Utils.geo_location import get_zipcode
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class CinciCodeEnf():
    # def __init__(self):
    #     ## Initialization
    #     self.url = "https://cagismaps.hamilton-co.org/PropertyActivity/propertyMaintenance"
    #     self.document_search = webdriver.Chrome()
    #     self.document_search.get(self.url)

    # def download_dataset(self):

    #     # Dataset options page
    #     self.document_search.find_element(By.XPATH,"/html/body/div[8]/nav/div/div[3]/div/ul[1]/li/div[3]/i").click()

    def start(self):
        #format for local data set 
        
        self.read_file = r'C:\Users\Jake\Documents\LISTS\PropertyActivity (7).csv' 

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
            print(f"No new records on  for Cinci code enforcments.\n")

        

        # Handle empty or missing values
        df = df.dropna(subset=[ "X_COORD", "Y_COORD", "STREET_NAME"])

        # Convert the keywords list into a regex pattern
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

        # Output the filtered DataFrame as a JSON file
        selected_rows.to_json("data.json", orient="records")





        
        