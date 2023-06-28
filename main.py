from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import OwnerLead, Session
from owner_info import Owner
from Scrapers.lee_county import LeeCountyScraper
import datetime
import pytz

## Functions
def curr_date():
    current_date = datetime.datetime.now(pytz.timezone('America/New_York'))
    formatted_date = current_date.strftime("%m/%d/%Y")
    return formatted_date

def past_month_date(months_back, current_date):
    date_obj = datetime.datetime.strptime(current_date, "%m/%d/%Y")
    past_date = date_obj - datetime.timedelta(days=months_back*30)
    formatted_date = past_date.strftime("%m/%d/%Y")
    return formatted_date


# Wait to see current page
# try:
#     element = WebDriverWait(document_search, 100).until(
#         EC.presence_of_element_located((By.ID, "myDynamicElement"))
#     )
# finally:
#     document_search.quit()


if __name__ == "__main__":
    # Here we would call each scraper. This would execute once a day. Compute the time it takes to execute as well as output general infomation to stdout
    lee_county = LeeCountyScraper("https://or.leeclerk.org/LandMarkWeb/home/index", curr_date(), past_month_date(3, curr_date()))
    #lee_county.scrape()
    # Database testing
    #lee_county.add_to_database()
