import time
import datetime
import logging
import inspect
from datetime import date
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utility.lead_database import Lead, Session
from Utility.lead_database_operations import json_to_database, remove_duplicates
from Utility.util import status_print
from Utility.twilio_api import email_csv
from Utility.visited_calendar_leads import (
    lee_county_visited_leads,
    clermont_county_visited_leads,
)
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
from Scrapers.Florida.charlotte_county_foreclosure import CharlotteCountyForeclosure
from Scrapers.Florida.marion_county_foreclosure import MarionCountyForeclosure
from Scrapers.Florida.fort_myers_code_enf import FortMeyersEnf
from Scrapers.Florida.alachua_county_foreclosure import AlachuaCountyForeclosure
from Scrapers.Florida.st_lucie_county_foreclosure import StLucieCountyForeclosure
from Scrapers.Florida.sarasota_county_taxdeed import SarasotaCountyTaxdeed
from Scrapers.Florida.marion_county_taxdeed import MarionCountyTaxdeed
from Scrapers.Florida.nassau_county_foreclosure import NassauCountyForeclosure
from Scrapers.Florida.nassau_county_taxdeed import NassauCountyTaxdeed
from BatchData_services.skiptrace import skiptrace_leads
from BatchData_services.skiptrace import skiptrace_leads
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse

logging.basicConfig(filename="processing.log", level=logging.ERROR, format='%(asctime)s - %(message)s')

def run_scraper(name, scraper_class, days=1, end_date=None):
    scraper = scraper_class()

    # Check if methods exist and then introspect for accepted parameters
    download_dataset_accepts_days = 'days' in inspect.signature(scraper.download_dataset).parameters if hasattr(scraper, 'download_dataset') else False
    download_dataset_accepts_end_date = 'end_date' in inspect.signature(scraper.download_dataset).parameters if hasattr(scraper, 'download_dataset') else False
    start_accepts_days = 'days' in inspect.signature(scraper.start).parameters if hasattr(scraper, 'start') else False
    start_accepts_end_date = 'end_date' in inspect.signature(scraper.start).parameters if hasattr(scraper, 'start') else False

    if hasattr(scraper, 'download_dataset'):
        try:
            if download_dataset_accepts_days:
                scraper.download_dataset(days=days)
            elif download_dataset_accepts_end_date:
                scraper.download_dataset(end_date=end_date)
            else:
                scraper.download_dataset()
        except Exception as e:
            logging.error(f"Error in {name}: {str(e)}")

    if hasattr(scraper, 'start'):
        try:
            if start_accepts_days:
                scraper.start(days=days)
            elif start_accepts_end_date:
                scraper.start(end_date=end_date)
            else:
                scraper.start()
        except Exception as e:
            logging.error(f"Error in {name}: {str(e)}")
            

if __name__ == "__main__":
    start_time = time.time()

    # Get the date two months from today
    future_date = date.today() + relativedelta(months=2)
    # Convert it to the "mm/dd/yyyy" format
    end_date = future_date.strftime('%m/%d/%Y')

    # Running each scraper
    # Code Enforcement 
    run_scraper("CinciCodeEnf", CinciCodeEnf, days=1)
    run_scraper("CinciCodeEnfAPI", CinciCodeEnfAPI, days=1)
    run_scraper("LeeCountyCodeEnf", LeeCountyCodeEnf, days=1)
    run_scraper("FortMeyersEnf", FortMeyersEnf, days=2)

    # Get the date two months from today
    future_date = date.today() + relativedelta(months=2)
    # Convert it to the "mm/dd/yyyy" format
    end_date = future_date.strftime('%m/%d/%Y')

    # Foreclosure and Taxdeed
    run_scraper("ClermontCountyForeclosure", ClermontCountyForeclosure, end_date=end_date)
    run_scraper("LeeCountyForeclosure", LeeCountyForeclosure, end_date=end_date)
    run_scraper("FranklinCountyForeclosure", FranklinCountyForeclosure, end_date=end_date)
    run_scraper("PinellasCountyForeclosure", PinellasCountyForeclosure, end_date=end_date)
    run_scraper("DuvalCountyForeclosure", DuvalCountyForeclosure, end_date=end_date)
    run_scraper("ButlerCountyForeclosure", ButlerCountyForeclosure, end_date=end_date)
    run_scraper("HamiltonCountyForeclosure", HamiltonCountyForeclosure)
    run_scraper("FairfieldCountyForeclosure", FairfieldCountyForeclosure, end_date=end_date)
    run_scraper("CharlotteCountyForeclosure", CharlotteCountyForeclosure, end_date=end_date)
    run_scraper("MarionCountyForeclosure", MarionCountyForeclosure, end_date=end_date)
    run_scraper("MarionCountyTaxdeed", MarionCountyTaxdeed, end_date=end_date)
    run_scraper("AlachuaCountyForeclosure", AlachuaCountyForeclosure, end_date=end_date)
    run_scraper("StLucieCountyForeclosure", StLucieCountyForeclosure, end_date=end_date)
    run_scraper("SarasotaCountyTaxdeed", SarasotaCountyTaxdeed, end_date=end_date)
    run_scraper("NassauCountyForeclosure", NassauCountyForeclosure, end_date=end_date)
    run_scraper("NassauCountyTaxdeed", NassauCountyTaxdeed, end_date=end_date)

    remove_duplicates()

    try:
        skiptrace_leads()
        json_to_database()
    except Exception as e:
        logging.error(f"Error during skiptrace or json processing: {str(e)}")

    # Change so that json returns a result so we dont email prematurely.


    # try:
    #     email_csv()
    # except Exception as e:
    #     logging.error(f"Error during email_csv: {str(e)}")

    end_time = time.time()
    execution_time = end_time - start_time
    status_print(
        f"Execution time of main function: {execution_time // 3600} hours {(execution_time % 3600) // 60} minutes {execution_time % 60} seconds"
    )
