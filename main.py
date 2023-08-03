import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utility.lead_database import Lead, Session
from Utility.lead_database_operations import json_to_database, remove_duplicates
from Utility.util import status_print
from Utility.twilio_api import send_email
from Utility.visited_calendar_leads import lee_county_visited_leads, clermont_county_visited_leads
from Scrapers.lee_county import LeeCountyScraper
from Scrapers.lee_county_code_enf import LeeCountyCodeEnf
from Scrapers.cinci_code_enf_API import CinciCodeEnfAPI
from Scrapers.cinci_code_enf import CinciCodeEnf
from Scrapers.orange_county_code_enf import OrangeCountyCodeEnf
from Scrapers.fort_myers_code_enf import FortMeyersEnf
from Scrapers.clermont_county_foreclosure import ClermontForeclosure
from Scrapers.lee_county_foreclosure import LeeCountyForeclosure
from BatchData_services.skiptrace import skiptrace_leads
from BatchData_services.skiptrace import skiptrace_leads
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse

# Entry point
if __name__ == "__main__":
    # Begin timing program execution
    start_time = time.time()

    """
    All daily calls to "lead generating scripts"
    Each script will add all available lead info to database
    """

    # cinci_code_enf = CinciCodeEnf()
    # cinci_code_enf.download_dataset()
    # cinci_code_enf.start(1)

    # cinci_code_enf_API = CinciCodeEnfAPI()
    # cinci_code_enf_API.start(1)

    # lee_county_code_enf = LeeCountyCodeEnf()
    # lee_county_code_enf.download_dataset(1)
    # lee_county_code_enf.start()

    # orange_county_code_enf = OrangeCountyCodeEnf()
    # orange_county_code_enf.download_dataset()
    # orange_county_code_enf.start(1)

    # # Get today's date and add one day to get tomorrow's date
    # start_date = datetime.datetime.now() + datetime.timedelta(days=1)
    # end_date = parse('09/01/2023')
    # # Generate a list of all dates from start_date to end_date
    # dates = list(rrule(DAILY, dtstart=start_date, until=end_date))

    # # Iterate over the dates
    # for date in dates:
    #     clermont_county_forclosure = ClermontForeclosure(date.strftime("%m/%d/%Y"))
    #     clermont_county_forclosure.start()

    # # End date
    # end_date = parse('09/15/2023')
    # # Generate a list of all dates from start_date to end_date
    # dates = list(rrule(DAILY, dtstart=start_date, until=end_date))

    # # Iterate over the dates
    # for date in dates:
    #     lee_county_forclosure = LeeCountyForeclosure(date.strftime("%m/%d/%Y"))
    #     lee_county_forclosure.start()

    '''
    Remove any duplicate address from today
    CHECK WHAT DUPES WE HAVE FROM ORANGE BEFORE
    '''
    #remove_duplicates()

    """
    Method call to BatchData API
    Completes the missing info for each lead in database and exports to JSON

    Read from JSON and append to database
    """
    #skiptrace = skiptrace_leads()
    
    #json_to_database()

    """
    Twilio API to send out SMS/Email messages 
    """
    #send_email()


    # End timing program execution
    end_time = time.time()
    execution_time = end_time - start_time
    status_print(f"Execution time of main function: {execution_time // 3600} hours {(execution_time % 3600) // 60} minutes {execution_time % 60} seconds")

