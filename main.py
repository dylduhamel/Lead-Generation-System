from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.lead_database import Lead, Session
from Scrapers.lee_county import LeeCountyScraper
from Scrapers.lee_county_code_enf import LeeCountyCodeEnf
from Scrapers.cinci_code_enf import CinciCodeEnf

## Main
if __name__ == "__main__":
    """
    All daily calls to "lead generating scripts"
    Each script will add all available lead info to database
    """
    cinci_code_enf = CinciCodeEnf()
    cinci_code_enf.download_dataset()


    """
    Method call to BatchData API
    Completes the missing info for each lead in database
    """
    