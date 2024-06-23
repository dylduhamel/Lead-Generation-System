from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Utility import *

session = Session()

lead = Lead()
lead.document_type = "Dylan!"


session.add(lead)

session.commit()
session.close()