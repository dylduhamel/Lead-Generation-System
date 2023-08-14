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
from Utility.twilio_api import email_csv
from Utility.visited_calendar_leads import lee_county_visited_leads, clermont_county_visited_leads
from Scrapers.Florida.lee_county import LeeCountyScraper
from Scrapers.Florida.lee_county_code_enf import LeeCountyCodeEnf
from Scrapers.Ohio.cinci_code_enf_API import CinciCodeEnfAPI
from Scrapers.Ohio.cinci_code_enf import CinciCodeEnf
from Scrapers.Florida.orange_county_code_enf import OrangeCountyCodeEnf
from Scrapers.Florida.fort_myers_code_enf import FortMeyersEnf
from Scrapers.Ohio.clermont_county_foreclosure import ClermontCountyForeclosure
from Scrapers.Florida.lee_county_foreclosure import LeeCountyForeclosure
from Scrapers.Ohio.franklin_county_foreclosure import FranklinCountyForeclosure
from Scrapers.Ohio.hamilton_county_foreclosure import HamiltonCountyForeclosure
from Scrapers.Florida.pinellas_county_foreclosure import PinellasCountyForeclosure
from Scrapers.Ohio.butler_county_foreclosure import ButlerCountyForeclosure
from Scrapers.Florida.duval_county_foreclosure import DuvalCountyForeclosure
from Scrapers.Ohio.fairfield_county_foreclosure import FairfieldCountyForeclosure
from Scrapers.Ohio.columbus_code_enf import ColumbusCodeEnf
from Scrapers.Florida.charlotte_county_foreclosure import CharlotteCountyForeclosure
from Scrapers.Florida.marion_county_foreclosure import MarionCountyForeclosure
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

    # # Cincinnati code enforcement
    # cinci_code_enf = CinciCodeEnf()
    # cinci_code_enf.download_dataset()
    # cinci_code_enf.start(1)

    # # Cincinnati code enforcement API
    # cinci_code_enf_API = CinciCodeEnfAPI()
    # cinci_code_enf_API.start(1)

    # Lee county code enforcement 
    lee_county_code_enf = LeeCountyCodeEnf()
    lee_county_code_enf.download_dataset(1)
    lee_county_code_enf.start()

    # # Orange county code enforcement [ Turned off for time being ]
    # # orange_county_code_enf = OrangeCountyCodeEnf()
    # # orange_county_code_enf.download_dataset()
    # # orange_county_code_enf.start(1)

    # # Columbus code enforcement
    # columbus_code_enf = ColumbusCodeEnf()   
    # columbus_code_enf.download_dataset(1)
    # columbus_code_enf.start()

    # # Claremont county foreclosure
    # clermont_county_forclosure = ClermontCountyForeclosure()
    # clermont_county_forclosure.start(end_date="09/01/2023")

    # # Lee county foreclosure
    # lee_county_forclosure = LeeCountyForeclosure()
    # lee_county_forclosure.start(end_date="09/15/2023")

    # # Franklin county foreclosure
    # franklin_county_forclosure = FranklinCountyForeclosure()
    # franklin_county_forclosure.start(end_date="09/10/2023")

    # # Pinellas county foreclosure
    # pinellas_county_forclosure = PinellasCountyForeclosure()
    # pinellas_county_forclosure.start(end_date="10/07/2023")

    # # Duval county foreclosure
    # duval_county_forclosure = DuvalCountyForeclosure()
    # duval_county_forclosure.start(end_date="09/01/2023")

    # # Butler county foreclosure
    # butler_county_foreclosure = ButlerCountyForeclosure()
    # butler_county_foreclosure.start(end_date="09/10/2023")

    # # Hamilton county foreclosure 
    # hamilton_county_foreclosure = HamiltonCountyForeclosure()
    # hamilton_county_foreclosure.start()

    # # Fairfield county foreclosure
    # fairfield_county_foreclosure = FairfieldCountyForeclosure()
    # fairfield_county_foreclosure.start("09/10/2023")

    # # Charlotte county foreclosure
    # charlotte_county_foreclosure = CharlotteCountyForeclosure()
    # charlotte_county_foreclosure.start(end_date="10/10/2023")

    # # Marion county foreclosure
    # marion_county_foreclosure = MarionCountyForeclosure()
    # marion_county_foreclosure.start(end_date="11/21/2023")

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
    #email_csv()


    # End timing program execution
    end_time = time.time()
    execution_time = end_time - start_time
    status_print(f"Execution time of main function: {execution_time // 3600} hours {(execution_time % 3600) // 60} minutes {execution_time % 60} seconds")

