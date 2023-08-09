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


class ClermontCountyForeclosure:
    def __init__(self, date):
        # Initialization

        # Date for tracking
        self.page_date = date
        # Pass in the date
        self.url = f'https://clermont.sheriffsaleauction.ohio.gov/index.cfm?zaction=AUCTION&Zmethod=PREVIEW&AUCTIONDATE={date}'
        # Webdriver
        self.driver = webdriver.Chrome()

        # This is used for status tracking
        self.scraper_name = "clermont_county_foreclosure.py"
        self.county_website = "Clermont County Sheriff Foreclosure"

        status_print(f"Initialized variables -- {self.scraper_name}")

    def start(self):
        # Initialize driver
        self.driver.get(self.url)

        status_print(f"Chrome driver created. Beginning scraping on {self.page_date} -- {self.scraper_name}")

        # Create a new database Session
        session = Session()

        try:
            # Wait until an auction item is present in the webpage
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "AUCTION_ITEM")))

            html_doc = self.driver.page_source
            soup = BeautifulSoup(html_doc, 'html.parser')

            # Get the 'Head_W' div
            head_w_div = soup.find(class_='Head_W')

            # Get only auction items that are inside the 'Head_W' div
            items = head_w_div.find_all(class_='AUCTION_ITEM')

            for item in items:
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
                    else:
                        raise ValueError("City zip data is None")
                except ValueError as e:
                    print(f"Error splitting city and zip data: '{e}'")
                    city, zip_code = None, None
                
                # Check if it has been seen before
                if property_address is not None and property_address not in clermont_county_visited_leads:
                    # Create new lead
                    lead = Lead()

                    # Date added to DB
                    time_stamp = curr_date()
                    lead.date_added = time_stamp

                    # Document type
                    lead.document_type = "Foreclosure"

                    # Address
                    lead.property_address = property_address

                    # City and State
                    lead.property_city = city
                    lead.property_zipcode = zip_code
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

        except TimeoutException:
            print("AUCTION_ITEM element not found. Quitting the driver.")
            self.driver.quit()

        # Add new session to DB
        session.commit()
        # Relinquish resources
        session.close()

        # Relinquish resources
        self.driver.quit()
        
        status_print(f"DB committed -- {self.scraper_name}")


