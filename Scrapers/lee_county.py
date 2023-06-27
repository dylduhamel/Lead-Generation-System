from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import OwnerLead, Session

class LeeCountyScraper():
     def __init__(self, url, curr_date, past_date):
          ## Variables
          self.document_search_PATH = "./chromedocument_search"
          self.DOCUMENT_SEARCH_KEYS = "LI,LP"
          # Window of time to search for documents [Choose month, set to 3]
          self.CURRENT_DATE = curr_date
          self.PAST_DATE = past_date
          selfowner_list = []

          ## Initialization
          #self.document_search = webdriver.Chrome()
          #self.document_search.get(url)
          # document_information = webdriver.Chrome()
          # document_information.get("https://www.leepa.org/")

          ## Database
          self.session = Session()

     def scrape(self):
          ## Home Page
          # Access the document search page
          self.document_search.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]/div/div[2]/a/img").click()
          self.document_search.find_element(By.XPATH, "//*[@id=\"idAcceptYes\"]").click()


          ## Search Page
          try:
               WebDriverWait(self.document_search, 10).until(EC.presence_of_element_located((By.ID, "documentType-Consideration")))
               # Choose the specific documents to search for [lien, lis pendens]
               document_type_box = self.document_search.find_element(By.ID, "documentType-DocumentType").send_keys(self.DOCUMENT_SEARCH_KEYS)
          except NoSuchElementException:
               print("Element not found")

          # Change the search date range
          curr_date_input = self.document_search.find_element(By.ID, "endDate-DocumentType")
          # Use JavaScript to set the value of the element
          self.document_search.execute_script("""
          arguments[0].value = arguments[1];
          arguments[0].dispatchEvent(new Event('change'));
          """, curr_date_input, self.CURRENT_DATE)

          past_date_input = self.document_search.find_element(By.ID, "beginDate-DocumentType")
          # Use JavaScript to set the value of the element
          self.document_search.execute_script("""
          arguments[0].value = arguments[1];
          arguments[0].dispatchEvent(new Event('change'));
          """, past_date_input, self.PAST_DATE)

          # Submit search
          self.document_search.find_element(By.XPATH, "//*[@id=\"submit-DocumentType\"]").click()

          ## Extracting table data
          try:
               WebDriverWait(self.document_search, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/div[2]/div/div[3]/div[1]/div/div[3]/table/tbody/tr/td/div/div[8]/table/tbody")))
               # Choose the specific documents to search for [lien, lis pendens]
               # Locate the table body
               tbody = self.document_search.find_element(By.XPATH, "/html/body/div[5]/div/div/div/div[2]/div/div[3]/div[1]/div/div[3]/table/tbody/tr/td/div/div[8]/table/tbody")
          except NoSuchElementException:
               print("Element not found")

          # Find all table rows within the table body
          rows = tbody.find_elements(By.TAG_NAME, 'tr')

          # Initialize an empty list to hold the data
          data = []

          # Iterate over each row
          for row in rows:
               cells = row.find_elements(By.TAG_NAME, 'td')
          
          # Ensure the row has at least 7 cells
          if len(cells) >= 8:
               # Extract the text from the 7th cell and append it to the data list
               cells[7].click()

          # Extract data from other website with folio ID 

          # Return back to table view
          try:
               WebDriverWait(self.document_search, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div/div/div[2]/div[1]/div[1]/a[1]")))
               # Choose the specific documents to search for [lien, lis pendens]
               self.document_search.find_element(By.XPATH, "/html/body/div[6]/div/div/div[2]/div[1]/div[1]/a[1]").click()
          except NoSuchElementException:
               print("Element not found")

          ### THEN CALL THE GET_DOCUMENT_INFO

     def get_document_info(self, driver, owner_list):
          owner_name = ""
          owner_address = ""

          name_box = driver.find_element(By.XPATH, "/html/body/form/div[5]/div/div/div[1]/div/div/div/div[1]/div[1]/table/tbody/tr/td[2]")
          name_list = name_box.find_elements(By.CLASS_NAME, 'bold')

          for name in name_list:
               owner_name += name.text()

          address_box = driver.find_element(By.XPATH, "/html/body/form/div[5]/div/div/div[1]/div/div/div/div[1]/div[1]/table/tbody/tr/td[3]/div/div[1]")
          address_list = address_box.find_elements(By.STYLE_NAME, "margin-left: 2px;")

          for address in address_list:
               owner_address += address.text()

          owner = Owner(name=owner_name, address=owner_address)
          owner_list.append(owner)
          print(owner_name)
          print(owner_address)

     def add_to_database(self):
          try:
               new_home = OwnerLead(owner_name="mike", home_style="awesome", address="4518")
               self.session.add(new_home)
               self.session.commit()
          except Exception as e:
               print(f"Insert failed due to: {e}")
               self.session.rollback()