import time
import inspect
import traceback
import logging
from datetime import date
from dateutil.relativedelta import relativedelta

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Utility.skiptrace import skiptrace_leads
from Utility import *
from Scrapers.Florida import *
from Scrapers.Ohio import *


logging.basicConfig(
    filename="processing.log", level=logging.ERROR, format="%(asctime)s - %(message)s"
)


def run_scraper(name, scraper_class, days=1, end_date=None):
    scraper = scraper_class()

    # Check if methods exist and then introspect for accepted parameters
    download_dataset_accepts_days = (
        "days" in inspect.signature(scraper.download_dataset).parameters
        if hasattr(scraper, "download_dataset")
        else False
    )
    download_dataset_accepts_end_date = (
        "end_date" in inspect.signature(scraper.download_dataset).parameters
        if hasattr(scraper, "download_dataset")
        else False
    )
    start_accepts_days = (
        "days" in inspect.signature(scraper.start).parameters
        if hasattr(scraper, "start")
        else False
    )
    start_accepts_end_date = (
        "end_date" in inspect.signature(scraper.start).parameters
        if hasattr(scraper, "start")
        else False
    )

    if hasattr(scraper, "download_dataset"):
        try:
            if download_dataset_accepts_days:
                scraper.download_dataset(days=days)
            elif download_dataset_accepts_end_date:
                scraper.download_dataset(end_date=end_date)
            else:
                scraper.download_dataset()
        except Exception as e:
            logging.error(f"Error in {name}: {str(e)}")

    if hasattr(scraper, "start"):
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

    run_scraper("CinciCodeEnf", CinciCodeEnf, days=1)
    run_scraper("CinciCodeEnfAPI", CinciCodeEnfAPI, days=1)

    future_date = date.today() + relativedelta(months=1)
    end_date = future_date.strftime("%m/%d/%Y")

    run_scraper("ClermontCountyForeclosure", ClermontCountyForeclosure, end_date=end_date)
    # More scraper calls foe each county...

    remove_duplicates()

    try:
        skiptrace_leads()
        json_to_database()
    except Exception as e:
        logging.error(f"Error during skiptrace or json processing: {str(e)}")

    try:
        email_csv()
    except Exception as e:
        logging.error(f"Error during email_csv: {str(e)}")

    end_time = time.time()
    execution_time = end_time - start_time
    status_print(
        f"Execution time of main function: {execution_time // 3600} hours {(execution_time % 3600) // 60} minutes {execution_time % 60} seconds"
    )