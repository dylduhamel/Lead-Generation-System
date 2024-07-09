# @author Dylan Duhamel {duhadm19@alumni.wfu.edu}
# @date Feb. 10, 2024

import sys

sys.path.append("..")

import inspect
import time
import threading
from datetime import date
from dateutil.relativedelta import relativedelta

from scrapers.Florida import *
from scrapers.Ohio import *
from utils.util import status_print


def run_scraper(name, scraper_class, lock, days=1, end_date=None):
    scraper = scraper_class(lock)

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

    if hasattr(scraper, "start"):
        try:
            if start_accepts_days:
                scraper.start(days=days)
            elif start_accepts_end_date:
                scraper.start(end_date=end_date)
            else:
                scraper.start()
        except Exception as e:
            print(f"Error in {name}: {str(e)}")


def run_scraper_batch(scraper_batch, lock, end_date):
    for name, scraper_class in scraper_batch:
        run_scraper(name, scraper_class, lock, 1, end_date)


def partition_scrapers(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last) : int(last + avg)])
        last += avg

    return out


scrapers = [
    ("ClermontCountyForeclosure", ClermontCountyForeclosure),
    ("LeeCountyForeclosure", LeeCountyForeclosure),
    ("FranklinCountyForeclosure", FranklinCountyForeclosure),
    ("PinellasCountyForeclosure", PinellasCountyForeclosure),
    # ("DuvalCountyForeclosure", DuvalCountyForeclosure),
    # ("ButlerCountyForeclosure", ButlerCountyForeclosure),
    # ("HamiltonCountyForeclosure", HamiltonCountyForeclosure),
    # ("FairfieldCountyForeclosure", FairfieldCountyForeclosure),
    # ("CharlotteCountyForeclosure", CharlotteCountyForeclosure),
    # ("MarionCountyForeclosure", MarionCountyForeclosure),
    # ("MarionCountyTaxdeed", MarionCountyTaxdeed),
    # ("AlachuaCountyForeclosure", AlachuaCountyForeclosure),
    # ("StLucieCountyForeclosure", StLucieCountyForeclosure),
    # ("SarasotaCountyTaxdeed", SarasotaCountyTaxdeed),
    # ("NassauCountyForeclosure", NassauCountyForeclosure),
    # ("NassauCountyTaxdeed", NassauCountyTaxdeed),
    # ("BrowardCountyForeclosure", BrowardCountyForeclosure),
    # ("OrangeCountyForeclosure", OrangeCountyForeclosure),
    # ("MiamiDadeForeclosure", MiamiDadeForeclosure),
    # ("PolkCountyTaxdeed", PolkCountyTaxdeed),
    # ("LeeCountyTaxdeed", LeeCountyTaxdeed),
    # ("DuvalCountyTaxdeed", DuvalCountyTaxdeed),
    # ("CuyahogaCountyForeclosure", CuyahogaCountyForeclosure),
    # ("VolusiaCountyTaxdeed", VolusiaCountyTaxdeed),
    # ("PalmBeachForeclosure", PalmBeachForeclosure),
    # ("HillsboroughCountyForeclosure", HillsboroughCountyForeclosure),
    # ("PolkCountyForeclosure", PolkCountyForeclosure),
    # ("PalmBeachTaxdeed", PalmBeachTaxdeed),
    # ("SummitCountyForeclosure", SummitCountyForeclosure),
    # ("MontgomeryCountyForeclosure", MontgomeryCountyForeclosure),
    # ("MahoningCountyForeclosure", MahoningCountyForeclosure),
    # ("LucasCountyForeclosure", LucasCountyForeclosure),
    # ("LorainCountyForeclosure", LorainCountyForeclosure),
    # ("LakeCountyForeclosure", LakeCountyForeclosure),
    # ("HuronCountyForeclosure", HuronCountyForeclosure),
    # ("SeminoleCountyForeclosure", SeminoleCountyForeclosure),
    # ("VolusiaCountyForeclosure", VolusiaCountyForeclosure),
    # ("PascoCountyForeclosure", PascoCountyForeclosure),
    # ("EscambiaCountyForeclosure", EscambiaCountyForeclosure),
    # ("BayCountyTaxdeed", BayCountyTaxdeed),
    # ("BrevardCountyTaxdeed", BrevardCountyTaxdeed),
    # ("HillsboroughCountyTaxdeed", HillsboroughCountyTaxdeed),
    # ("PascoCountyTaxdeed", PascoCountyTaxdeed),
    # ("ManateeCountyForeclosure", ManateeCountyForeclosure),
    # ("PutnamCountyTaxdeed", PuntamCountyTaxdeed),
]

if __name__ == "__main__":
    start_time = time.time()

    future_date = date.today() + relativedelta(months=1)
    end_date = future_date.strftime("%m/%d/%Y")

    # Create a lock for managing database access
    lock = threading.Lock()

    # Partition scrapers for number of threads
    scraper_batches = partition_scrapers(scrapers, 4)

    threads = []
    for batch in scraper_batches:
        thread = threading.Thread(
            target=run_scraper_batch, args=(batch, lock, end_date)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All scrapers have finished execution.")

    end_time = time.time()
    execution_time = end_time - start_time
    status_print(
        f"Execution time of main function: {execution_time // 3600} hours {(execution_time % 3600) // 60} minutes {execution_time % 60} seconds"
    )
