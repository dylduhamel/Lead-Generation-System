import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utility.lead_database import Lead, Session
from Utility.lead_database_operations import json_to_database
from Utility.util import status_print
from Utility.twilio_api import send_email
from Scrapers.lee_county import LeeCountyScraper
from Scrapers.lee_county_code_enf import LeeCountyCodeEnf
from Scrapers.cinci_code_enf_API import CinciCodeEnfAPI
from Scrapers.cinci_code_enf import CinciCodeEnf
from Scrapers.orange_county_code_enf import OrangeCountyCodeEnf
from Scrapers.fort_myers_code_enf import FortMeyersEnf
from BatchData_services.skiptrace import skiptrace_leads
from BatchData_services.skiptrace import skiptrace_leads

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
    # for i in range(1,8):
    #     cinci_code_enf.start(i)

    # cinci_code_enf_API = CinciCodeEnfAPI()
    # for i in range(1,8):
    #     cinci_code_enf_API.start(i)

    # for i in range(1,8):
    #     lee_county_code_enf = LeeCountyCodeEnf()
    #     lee_county_code_enf.download_dataset(i)
    #     lee_county_code_enf.start()
    #     time.sleep(2)

    # orange_county_code_enf = OrangeCountyCodeEnf()
    # #orange_county_code_enf.download_dataset()
    # for i in range(0,8):
    #     orange_county_code_enf.start(i)

    
    #json_to_database()

    """
    Method call to BatchData API
    Completes the missing info for each lead in database
    """
    #skiptrace = skiptrace_leads()

    """
    Twilio API to send out SMS/Email messages 
    """
    #send_email()


    # End timing program execution
    end_time = time.time()
    execution_time = end_time - start_time
    status_print(f"Execution time of main function: {execution_time // 3600} hours {(execution_time % 3600) // 60} minutes {execution_time % 60} seconds")

