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
from Utility.visited_calendar_leads import save_global_list_lee, lee_county_visited_leads
from Utility.lead_database import Lead, Session
from Utility.lead_database_operations import add_lead_to_database
from Utility.util import curr_date, status_print

logging.basicConfig(filename="processing.log", level=logging.ERROR, format='%(asctime)s - %(message)s')

class LeeCountyForeclosure:
    def __init__(self):
        # Initialization

        # Webdriver
        self.driver = webdriver.Chrome()

        # This is used for status tracking
        self.scraper_name = "lee_county_foreclosure.py"
        self.county_website = "Lee County Foreclosure"

        status_print(f"Initialized variables -- {self.scraper_name}")

    def start(self, end_date):
        # Get today's date and add one day to get tomorrow's date
        start_date = datetime.datetime.now() + datetime.timedelta(days=1)
        end_date = parse(end_date)
        # Generate a list of all dates from start_date to end_date
        dates = list(rrule(DAILY, dtstart=start_date, until=end_date))

        # Create new database session
        session = Session()

        # Iterate over the dates CLERMONT
        for date in dates:
            # Get URL with current date
            self.url = f'https://www.lee.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=PREVIEW&AUCTIONDATE={date}'
             # Initialize driver
            self.driver.get(self.url)

            try:
                # Wait until an auction item is present in the webpage
                WebDriverWait(self.driver, 1.0).until(EC.presence_of_element_located((By.CLASS_NAME, "AUCTION_ITEM")))

                # Wait if the element is loading the waiting records
                WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'Loading')))

                html_doc = self.driver.page_source
                soup = BeautifulSoup(html_doc, 'html.parser')

                # Check number of pages
                max_pages_elem = soup.find(id='maxWA')
                if max_pages_elem:
                    try:
                        max_pages = int(max_pages_elem.get_text(strip=True))
                    except ValueError:
                        max_pages = 1
                else:
                    max_pages = 1

                all_items = []

                for current_page in range(1, max_pages + 1):
                    if current_page > 1:
                        # If it's not the first page, click the next page button
                        WebDriverWait(self.driver, 1.0).until(EC.presence_of_element_located((By.CLASS_NAME, "PageRight")))
                        next_page_btn = self.driver.find_element(By.CLASS_NAME, "PageRight")
                        next_page_btn.click()

                        # Wait until an auction item is present in the webpage
                        time.sleep(2)

                        # Wait for the page to load
                        WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'Loading')))

                        # Parse the new page source
                        html_doc = self.driver.page_source
                        soup = BeautifulSoup(html_doc, 'html.parser')

                    # Extract items
                    head_w_div = soup.find(class_='Head_W')
                    items = head_w_div.find_all(class_='AUCTION_ITEM')
                    all_items.extend(items)

                for item in all_items:
                    details_table = item.find(class_='AUCTION_DETAILS')
                    rows = details_table.find_all('tr')
                    data = {row.th.get_text(strip=True): row.td.get_text(strip=True) for row in rows}
                    
                    case_status = data.get('Case Status:', None)
                    property_address = data.get('Property Address:', None)
                    appraised_value = data.get('Appraised Value:', None)
                    
                    # Find city and zip code
                    for i, row in enumerate(rows):
                        if row.th.get_text(strip=True) == 'Property Address:':
                            city_zip_data = rows[i+1].td.get_text(strip=True)
                            break
                    else:
                        city_zip_data = None

                    # Getting city and zip data extracted
                    try:
                        if city_zip_data is not None:
                            city, zip_code = map(str.strip, city_zip_data.split(','))
                            zip_code = zip_code.split('- ')[1]
                        else:
                            raise ValueError("City zip data is None")
                    except ValueError as e:
                        print(f"Error splitting city and zip data: '{e}'")
                        city, zip_code = None, None
                    
                    # Check if it has been seen before
                    if property_address is not None and property_address not in lee_county_visited_leads:
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
                        lee_county_visited_leads.append(property_address)
                        save_global_list_lee()

            except Exception as e:
                print(f"AUCTION_ITEM element not found. Moving on. {str(e)}")

        # Add new session to DB
        session.commit()
        # Relinquish resources
        session.close()

        # Relinquish resources
        self.driver.quit()
        
        status_print(f"DB committed -- {self.scraper_name}")


