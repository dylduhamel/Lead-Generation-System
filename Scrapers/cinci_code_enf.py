import os
import time
import math
import pandas as pd
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
        self.filename = "PropertyActivity.csv"
        self.file_path = "/home/dylan/Downloads"

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
        while not os.path.exists(os.path.join(self.file_path, self.filename)): 
            time.sleep(1)

        # Relinquish resources
        self.driver.quit()

        # DELETE FILE FOR NEXT TIME
