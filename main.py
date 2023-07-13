from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import Lead, Session
from owner_info import Owner
from Scrapers.lee_county import LeeCountyScraper
from Scrapers.lee_county_Enf import LeeCountyEnf
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

## Main
if __name__ == "__main__":
    #lee_county_enf = LeeCountyEnf()
    #lee_county_enf.start()
    pass