import os
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


class CinciCodeEnf():
    def __init__(self):
        ## Initialization
        self.url = "https://cagismaps.hamilton-co.org/PropertyActivity/propertyMaintenance"
        self.document_search = webdriver.Chrome()
        self.document_search.get(self.url)

    def download_dataset(self):

        # Dataset options page
        self.document_search.find_element(By.XPATH,"/html/body/div[8]/nav/div/div[3]/div/ul[1]/li/div[3]/i").click()
