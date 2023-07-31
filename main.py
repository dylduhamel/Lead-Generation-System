from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utility.lead_database import Lead, Session
from Scrapers.lee_county import LeeCountyScraper
from Scrapers.lee_county_code_enf import LeeCountyCodeEnf
from Scrapers.cinci_code_enf_API import CinciCodeEnfAPI
from Scrapers.cinci_code_enf import CinciCodeEnf
from Scrapers.orange_county_code_enf import OrangeCountyCodeEnf
from Scrapers.fort_myers_code_enf import FortMeyersEnf
from BatchData_services.skiptrace import skiptrace_leads
from BatchData_services.skiptrace import skiptrace_leads

## Main
if __name__ == "__main__":
    """
    All daily calls to "lead generating scripts"
    Each script will add all available lead info to database
    """
    #cinci_code_enf = CinciCodeEnf()
    #cinci_code_enf.download_dataset()
    # for i in range(1,20):
    #     cinci_code_enf.start(i)

    #cinci_code_enf_API = CinciCodeEnfAPI()
    # Iterate up to last 20 days
    # for i in range(1,20):
    #     cinci_code_enf_API.start(i)

    # lee_county_code_enf = LeeCountyCodeEnf()
    # for i in range(1,2):
    #     lee_county_code_enf.download_dataset(i)
    #     lee_county_code_enf.start()

    orange_county_code_enf = OrangeCountyCodeEnf()
    #orange_county_code_enf.download_dataset()
    for i in range(0,5):
        orange_county_code_enf.start(i)

    #fort_myers_code_enf = FortMeyersEnf()

    """
    Method call to BatchData API
    Completes the missing info for each lead in database
    """
    #skiptrace = skiptrace_leads()

    """
    Twilio API to send out SMS/Email messages 
    """