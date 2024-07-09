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
from utils import *

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

if __name__ == "__main__":
    start_time = time.time()

    future_date = date.today() + relativedelta(months=1)
    end_date = future_date.strftime("%m/%d/%Y")

    # Create a lock for managing database access
    lock = threading.Lock()

    # Create threads for each scraper
    threads = [
        threading.Thread(target=run_scraper, args=("ClermontCountyForeclosure", ClermontCountyForeclosure, lock, 1, end_date)),
        threading.Thread(target=run_scraper, args=("LeeCountyForeclosure", LeeCountyForeclosure, lock, 1, end_date)),
        threading.Thread(target=run_scraper, args=("FranklinCountyForeclosure", FranklinCountyForeclosure, lock, 1, end_date)),
        threading.Thread(target=run_scraper, args=("PinellasCountyForeclosure", PinellasCountyForeclosure, lock, 1, end_date))
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All scrapers have finished execution.")


    # run_scraper("DuvalCountyForeclosure", DuvalCountyForeclosure, end_date=end_date)
    # run_scraper("ButlerCountyForeclosure", ButlerCountyForeclosure, end_date=end_date)
    # run_scraper("HamiltonCountyForeclosure", HamiltonCountyForeclosure)
    # run_scraper("FairfieldCountyForeclosure", FairfieldCountyForeclosure, end_date=end_date)
    # run_scraper("CharlotteCountyForeclosure", CharlotteCountyForeclosure, end_date=end_date)
    # run_scraper("MarionCountyForeclosure", MarionCountyForeclosure, end_date=end_date)
    # run_scraper("MarionCountyTaxdeed", MarionCountyTaxdeed, end_date=end_date)
    # run_scraper("AlachuaCountyForeclosure", AlachuaCountyForeclosure, end_date=end_date)
    # run_scraper("StLucieCountyForeclosure", StLucieCountyForeclosure, end_date=end_date)
    # run_scraper("SarasotaCountyTaxdeed", SarasotaCountyTaxdeed, end_date=end_date)
    # run_scraper("NassauCountyForeclosure", NassauCountyForeclosure, end_date=end_date)
    # run_scraper("NassauCountyTaxdeed", NassauCountyTaxdeed, end_date=end_date)
    # run_scraper("BrowardCountyForeclosure", BrowardCountyForeclosure, end_date=end_date)
    # run_scraper("OrangeCountyFoeclosure", OrangeCountyForeclosure, end_date=end_date)
    # run_scraper("MiamiDadeForeclosure", MiamiDadeForeclosure, end_date=end_date)
    # run_scraper("PolkCountyTaxdeed", PolkCountyTaxdeed, end_date=end_date)
    # run_scraper("LeeCountyTaxdeed", LeeCountyTaxdeed, end_date=end_date)
    # run_scraper("DuvalCountyTaxdeed", DuvalCountyTaxdeed, end_date=end_date)
    # run_scraper("CuyahogaCountyForeclosure", CuyahogaCountyForeclosure, end_date=end_date)
    # run_scraper("VolusiaCountyTaxdeed", VolusiaCountyTaxdeed, end_date=end_date)
    # run_scraper("PalmBeachForeclosure", PalmBeachForeclosure, end_date=end_date)
    # run_scraper("HillsboroughCountyForeclosure", HillsboroughCountyForeclosure, end_date=end_date)
    # run_scraper("PolkCountyForeclosure", PolkCountyForeclosure, end_date=end_date)
    # run_scraper("PalmBeachTaxdeed", PalmBeachTaxdeed, end_date=end_date)
    # run_scraper("SummitCountyForeclosure", SummitCountyForeclosure, end_date=end_date)
    # run_scraper("MontgomeryCountyForeclosure", MontgomeryCountyForeclosure, end_date=end_date)
    # run_scraper("MahoningCountyForeclosure", MahoningCountyForeclosure, end_date=end_date)
    # run_scraper("LucasCountyForeclosure", LucasCountyForeclosure, end_date=end_date)
    # run_scraper("LorainCountyForeclosure", LorainCountyForeclosure, end_date=end_date)
    # run_scraper("LakeCountyForeclosure", LakeCountyForeclosure, end_date=end_date)
    # run_scraper("HuronCountyForeclosure", HuronCountyForeclosure, end_date=end_date)
    # run_scraper("SeminoleCountyForeclosure", SeminoleCountyForeclosure, end_date=end_date)
    # run_scraper("VolusiaCountyForeclosure", VolusiaCountyForeclosure, end_date=end_date)
    # run_scraper("PascoCountyForeclosure", PascoCountyForeclosure, end_date=end_date)
    # run_scraper("EscambiaCountyForeclosure", EscambiaCountyForeclosure, end_date=end_date)
    # run_scraper("BayCountyTaxdeed", BayCountyTaxdeed, end_date=end_date)
    # run_scraper("BrevardCountyTaxdeed", BrevardCountyTaxdeed, end_date=end_date)
    # run_scraper("HillsboroughCountyTaxdeed", HillsboroughCountyTaxdeed, end_date=end_date)
    # run_scraper("PascoCountyTaxdeed", PascoCountyTaxdeed, end_date=end_date)
    # run_scraper("ManateeCountyForeclosure", ManateeCountyForeclosure, end_date=end_date)
    # run_scraper("PuntamCountyTaxdeed", PuntamCountyTaxdeed, end_date=end_date)
    # run_scraper("ClermontCountyForeclosure", ClermontCountyForeclosure, end_date=end_date)
    # run_scraper("LeeCountyForeclosure", LeeCountyForeclosure, end_date=end_date)
    # run_scraper("FranklinCountyForeclosure", FranklinCountyForeclosure, end_date=end_date)
    # run_scraper("PinellasCountyForeclosure", PinellasCountyForeclosure, end_date=end_date)
    # run_scraper("DuvalCountyForeclosure", DuvalCountyForeclosure, end_date=end_date)
    # run_scraper("ButlerCountyForeclosure", ButlerCountyForeclosure, end_date=end_date)
    # run_scraper("HamiltonCountyForeclosure", HamiltonCountyForeclosure)
    # run_scraper("FairfieldCountyForeclosure", FairfieldCountyForeclosure, end_date=end_date)
    # run_scraper("CharlotteCountyForeclosure", CharlotteCountyForeclosure, end_date=end_date)
    # run_scraper("MarionCountyForeclosure", MarionCountyForeclosure, end_date=end_date)
    # run_scraper("MarionCountyTaxdeed", MarionCountyTaxdeed, end_date=end_date)
    # run_scraper("AlachuaCountyForeclosure", AlachuaCountyForeclosure, end_date=end_date)
    # run_scraper("StLucieCountyForeclosure", StLucieCountyForeclosure, end_date=end_date)
    # run_scraper("SarasotaCountyTaxdeed", SarasotaCountyTaxdeed, end_date=end_date)
    # run_scraper("NassauCountyForeclosure", NassauCountyForeclosure, end_date=end_date)
    # run_scraper("NassauCountyTaxdeed", NassauCountyTaxdeed, end_date=end_date)
    # run_scraper("BrowardCountyForeclosure", BrowardCountyForeclosure, end_date=end_date)
    # run_scraper("OrangeCountyFoeclosure", OrangeCountyForeclosure, end_date=end_date)
    # run_scraper("MiamiDadeForeclosure", MiamiDadeForeclosure, end_date=end_date)
    # run_scraper("PolkCountyTaxdeed", PolkCountyTaxdeed, end_date=end_date)
    # run_scraper("LeeCountyTaxdeed", LeeCountyTaxdeed, end_date=end_date)
    # run_scraper("DuvalCountyTaxdeed", DuvalCountyTaxdeed, end_date=end_date)
    # run_scraper("CuyahogaCountyForeclosure", CuyahogaCountyForeclosure, end_date=end_date)
    # run_scraper("VolusiaCountyTaxdeed", VolusiaCountyTaxdeed, end_date=end_date)
    # run_scraper("PalmBeachForeclosure", PalmBeachForeclosure, end_date=end_date)
    # run_scraper("HillsboroughCountyForeclosure", HillsboroughCountyForeclosure, end_date=end_date)
    # run_scraper("PolkCountyForeclosure", PolkCountyForeclosure, end_date=end_date)
    # run_scraper("PalmBeachTaxdeed", PalmBeachTaxdeed, end_date=end_date)
    # run_scraper("SummitCountyForeclosure", SummitCountyForeclosure, end_date=end_date)
    # run_scraper("MontgomeryCountyForeclosure", MontgomeryCountyForeclosure, end_date=end_date)
    # run_scraper("MahoningCountyForeclosure", MahoningCountyForeclosure, end_date=end_date)
    # run_scraper("LucasCountyForeclosure", LucasCountyForeclosure, end_date=end_date)
    # run_scraper("LorainCountyForeclosure", LorainCountyForeclosure, end_date=end_date)
    # run_scraper("LakeCountyForeclosure", LakeCountyForeclosure, end_date=end_date)
    # run_scraper("HuronCountyForeclosure", HuronCountyForeclosure, end_date=end_date)
    # run_scraper("SeminoleCountyForeclosure", SeminoleCountyForeclosure, end_date=end_date)
    # run_scraper("VolusiaCountyForeclosure", VolusiaCountyForeclosure, end_date=end_date)
    # run_scraper("PascoCountyForeclosure", PascoCountyForeclosure, end_date=end_date)
    # run_scraper("EscambiaCountyForeclosure", EscambiaCountyForeclosure, end_date=end_date)
    # run_scraper("BayCountyTaxdeed", BayCountyTaxdeed, end_date=end_date)
    # run_scraper("BrevardCountyTaxdeed", BrevardCountyTaxdeed, end_date=end_date)
    # run_scraper("HillsboroughCountyTaxdeed", HillsboroughCountyTaxdeed, end_date=end_date)
    # run_scraper("PascoCountyTaxdeed", PascoCountyTaxdeed, end_date=end_date)
    # run_scraper("ManateeCountyForeclosure", ManateeCountyForeclosure, end_date=end_date)
    # run_scraper("PuntamCountyTaxdeed", PuntamCountyTaxdeed, end_date=end_date)

    end_time = time.time()
    execution_time = end_time - start_time
    status_print(
        f"Execution time of main function: {execution_time // 3600} hours {(execution_time % 3600) // 60} minutes {execution_time % 60} seconds"
    )
