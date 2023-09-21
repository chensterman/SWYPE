######################################## IMPORTS AND INIT

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

######################################## GLOBAL VARIABLES

# Citizens Bank authentication parameters
LOGIN_URL = "https://www.accessmycardonline.com/"
MINIMUM_REWARDS_BALANCE = 25.0

# Chrome webdriver
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('--no-sandbox')
OPTIONS.add_argument('--headless')
OPTIONS.add_argument('--ignore-certificate-errors')
OPTIONS.add_argument('--disable-dev-shm-usage')
OPTIONS.add_argument('--disable-extensions')
OPTIONS.add_argument('--disable-gpu')
# OPTIONS.add_argument('log-level=3')
CHROME = webdriver.Chrome(options=OPTIONS)
# Bypass bot detection
CHROME.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

######################################## FUNCTIONS

# Citizens Bank authentication
def auth(username, password):
  # Navigate to login page
  CHROME.get(LOGIN_URL)
  # Delay to allow for rendering
  time.sleep(3.0)
  # Input credentials and login
  element = WebDriverWait(CHROME, 15).until(
    EC.presence_of_element_located((By.ID, "username")) #This is a dummy element
  )
  element.send_keys(username)
  CHROME.find_element("id", "password").send_keys(password)
  CHROME.find_element("id", "loginButton").click()
  # Delay to allow for rendering
  time.sleep(5.0)
  # Check for failure
  if (len(CHROME.find_elements("xpath", "//div[@class='alert alert-danger']")) != 0):
      raise Exception("Login failed.")
    
# Citizens Bank check rewards balance
def get_rewards_balance(username, password):
  # Login to bank
  auth(username, password)
  # Retrieve rewards balance information
  WebDriverWait(CHROME, 15).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='card-currency']")) #This is a dummy element
  )
  rewards_balance_str = CHROME.find_elements("xpath", "//div[@class='card-currency']")[1].text.strip()
  rewards_balance_float = float(rewards_balance_str[1:])
  return rewards_balance_float
    
# Citizens Bank redeem rewards
def redeem_rewards(username, password):
  # Check sufficient rewards balance
  rewards_balance = get_rewards_balance(username, password)
  if (rewards_balance < MINIMUM_REWARDS_BALANCE):
     raise Exception("Rewards balance insufficient.")
  # Commence redemption process
  WebDriverWait(CHROME, 15).until(
    EC.presence_of_element_located((By.XPATH, "//div[@role='button']")) #This is a dummy element
  )
  CHROME.find_elements("xpath", "//div[@role='button']")[3].click()
  WebDriverWait(CHROME, 15).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Redeem Now")) #This is a dummy element
  )
  CHROME.find_elements("partial link text", "Redeem Now")[1].click()
  # TODO: IMPLEMENT AFTER $25.00 BALANCE