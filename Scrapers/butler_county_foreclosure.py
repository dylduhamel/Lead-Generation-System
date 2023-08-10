import time
import datetime
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from Utility.visited_calendar_leads import save_global_list_clermont, clermont_county_visited_leads
from Utility.lead_database import Lead, Session
from Utility.lead_database_operations import add_lead_to_database
from Utility.util import curr_date, status_print


class ButlerCountyForeclosure:
    def __init__(self):
        # Initialization

        # Chrome driver
        self.driver = webdriver.Chrome()

        # This is used for status tracking
        self.scraper_name = "butler_county_foreclosure.py"
        self.county_website = "Clermont County Sheriff Foreclosure"

        status_print(f"Initialized variables -- {self.scraper_name}")

    def start(self, end_date):
        # Get today's date and add one day to get tomorrow's date
        start_date = datetime.datetime.now() + datetime.timedelta(days=1)
        end_date = parse(end_date)
        # Generate a list of all dates from start_date to end_date
        dates = list(rrule(DAILY, dtstart=start_date, until=end_date))

        # Iterate over the dates CLERMONT
        for curr_date in dates:
            self.url = f'https://butler.sheriffsaleauction.ohio.gov/index.cfm?zaction=AUCTION&Zmethod=PREVIEW&AUCTIONDATE={curr_date}'
             # Initialize driver
            self.driver.get(self.url)