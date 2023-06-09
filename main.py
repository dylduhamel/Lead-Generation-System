from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import pytz

def curr_date():
    current_date = datetime.datetime.now(pytz.timezone('America/New_York'))
    formatted_date = current_date.strftime("%m/%d/%Y")
    return formatted_date

def past_month_date(months_back, current_date):
    date_obj = datetime.datetime.strptime(current_date, "%m/%d/%Y")
    past_date = date_obj - datetime.timedelta(days=months_back*30)
    formatted_date = past_date.strftime("%m/%d/%Y")
    return formatted_date

DRIVER_PATH = "./chromedriver"
DOCUMENT_SEARCH_KEYS = "LI,LP"
# Window of time to search for documents [Choose month, set to 3]
CURRENT_DATE = curr_date()
PAST_DATE = past_month_date(3, CURRENT_DATE)

# Driver initialization
driver = webdriver.Chrome()
driver.get("https://or.leeclerk.org/LandMarkWeb/home/index")

# Home page
# Access the document search page
driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]/div/div[2]/a/img").click()
driver.find_element(By.XPATH, "//*[@id=\"idAcceptYes\"]").click()

# Search page
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "documentType-Consideration")))
    # Choose the specific documents to search for [lien, lis pendens]
    document_type_box = driver.find_element(By.ID, "documentType-DocumentType").send_keys(DOCUMENT_SEARCH_KEYS)
except NoSuchElementException:
    print("Element not found")

# Change the search date range
curr_date_input = driver.find_element(By.ID, "endDate-DocumentType")
# Use JavaScript to set the value of the element
driver.execute_script("""
    arguments[0].value = arguments[1];
    arguments[0].dispatchEvent(new Event('change'));
    """, curr_date_input, CURRENT_DATE)

past_date_input = driver.find_element(By.ID, "beginDate-DocumentType")
# Use JavaScript to set the value of the element
driver.execute_script("""
    arguments[0].value = arguments[1];
    arguments[0].dispatchEvent(new Event('change'));
    """, past_date_input, PAST_DATE)

# Submit search
driver.find_element(By.XPATH, "//*[@id=\"submit-DocumentType\"]").click()


# Wait to see current page
try:
    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
finally:
    driver.quit()
