import requests
from bs4 import BeautifulSoup
import pandas as pd
from utility.visited_calendar_leads import save_global_list_hamilton, hamilton_county_visited_leads
from utility.lead_database import Lead, Session
from utility.util import curr_date, status_print

class HamiltonCountyForeclosure():
    def __init__(self):
        # Initialize

        # Hamilton site
        self.url = "https://www.hcso.org/community-services/search-property-sales/property-sales/"

        # Create a list to store our table rows
        self.data = []

        # This is used for status tracking
        self.scraper_name = "hamilton_county_foreclosure.py"
        self.county_website = "Hamilton County Sheriff Foreclosure"
        
        # Create a new database Session
        self.session = Session()

        # Make a GET request to the website
        self.response = requests.get(self.url)

        # Parse the HTML content
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

        status_print(f"Initialized variables -- {self.scraper_name}")

    def start(self):
        # Find the table on the webpage
        table = self.soup.find('table')

        status_print(f"Beginning scraping -- {self.scraper_name}")

        # Iterate over the table rows
        for row in table.find_all('tr'):
            # Create a list to store the data for each row
            row_data = []
            # Find all 'td' tags (table data) in the row
            td_tags = row.find_all('td')
            # If the length of td_tags is not 0
            if len(td_tags) > 0:
                # Iterate over the 'td' tags
                for tag in td_tags:
                    # Append the text of each tag to our row_data list
                    row_data.append(tag.text.strip())
                # Append the row_data to our data list
                self.data.append(row_data)

        # Create the dataframe
        df = pd.DataFrame(self.data, columns=["Case Number", "Plaintiff Name", "Defendant Name", "Address", "Attorney Name", "Attorney Phone", "Min Bid", "Appraisal", "Area", "Withdrawn", "Sale Date"])

        # Iterate over the DataFrame and print each row's values
        for index, row in df.iterrows():
            if row["Address"] not in hamilton_county_visited_leads:
                # Create new lead
                lead = Lead()

                # Date added to DB
                time_stamp = curr_date()
                lead.date_added = time_stamp

                defendant_name = row["Defendant Name"]
                last_name, first_name = defendant_name.split(', ')
                lead.first_name_owner = first_name
                lead.last_name_owner = last_name

                # Document type
                lead.document_type = "Foreclosure"

                # Address
                lead.property_address = row["Address"]

                # City and State
                lead.property_city = "Cincinnati"
                lead.property_state = "Ohio"

                # Website tracking
                lead.county_website = self.county_website

                # print(lead)
                # print("\n")

                # Add lead to db
                self.session.add(lead)

                # Add to visited list
                hamilton_county_visited_leads.append(row["Address"])
                save_global_list_hamilton()
        
        # Add new session to DB
        self.session.commit()
        # Relinquish resources
        self.session.close()
        
        status_print(f"DB committed -- {self.scraper_name}")