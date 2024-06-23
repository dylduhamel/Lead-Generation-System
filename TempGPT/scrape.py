import time
import datetime
import logging
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from Utility.visited_calendar_leads import (
    save_global_list_clermont,
    clermont_county_visited_leads,
)
from Utility.lead_database import Lead, Session
from Utility.lead_database_operations import add_lead_to_database
from Utility.util import curr_date, status_print

logging.basicConfig(
    filename="processing.log", level=logging.ERROR, format="%(asctime)s - %(message)s"
)


class ClermontCountyForeclosure:
    def __init__(self):
        # Initialization

        # Chrome driver
        self.driver = webdriver.Chrome()

        # This is used for status tracking
        self.scraper_name = "clermont_county_foreclosure.py"
        self.county_website = "Clermont County Sheriff Foreclosure"

        status_print(f"Initialized variables -- {self.scraper_name}")

    def start(self, end_date):
        # Get today's date and add one day to get tomorrow's date
        start_date = datetime.datetime.now() + datetime.timedelta(days=1)
        end_date = parse(end_date)
        # Generate a list of all dates from start_date to end_date
        dates = list(rrule(DAILY, dtstart=start_date, until=end_date))

        # Create new database session
        session = Session()

        """
        SCRAPE HERE...
        """
                    # Check if it has been seen before
                    if (
                        property_address is not None
                        and property_address not in clermont_county_visited_leads
                    ):
                        # Create new lead
                        lead = Lead()

                        time_stamp = curr_date()
                        lead.date_added = time_stamp

                        # Document type
                        lead.document_type = "Foreclosure"

                        # Address
                        lead.property_address = property_address

                        # City and State
                        lead.property_city = city
                        lead.property_zipcode = zip_code[:5]
                        lead.property_state = "Ohio"

                        # Website tracking
                        lead.county_website = self.county_website

                        # print(lead)
                        # print("\n")

                        # Add lead to db
                        session.add(lead)

                        # Add to visited list
                        clermont_county_visited_leads.append(property_address)
                        save_global_list_clermont()

            except Exception as e:
                print(f"AUCTION_ITEM element not found. Moving on.")

        # Add new session to DB
        session.commit()
        # Relinquish resources
        session.close()

        # Relinquish resources
        self.driver.quit()

        status_print(f"DB committed -- {self.scraper_name}")
