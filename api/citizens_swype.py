######################################## IMPORTS AND INIT

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

######################################## GLOBAL VARIABLES

# Citizens Bank authentication parameters
LOGIN_URL = "https://www.accessmycardonline.com/"
MINIMUM_REWARDS_BALANCE = 25.0

# Chrome webdriver
OPTIONS = webdriver.ChromeOptions()
# OPTIONS.add_argument('log-level=3')
CHROME_SERVICE = Service(ChromeDriverManager().install())
CHROME = webdriver.Chrome(service=Service(executable_path='./chromedriver'), options=OPTIONS)
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
  CHROME.find_element("id", "username").send_keys(username)
  CHROME.find_element("id", "password").send_keys(password)
  CHROME.find_element("id", "loginButton").click()
  # Delay to allow for rendering
  time.sleep(3.0)
  # Check for failure
  if (len(CHROME.find_elements("xpath", "//div[@class='alert alert-danger']")) != 0):
      raise Exception("Login failed.")
    
# Citizens Bank check rewards balance
def get_rewards_balance(username, password):
  # Login to bank
  auth(username, password)
  # Retrieve rewards balance information
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
  CHROME.find_elements("xpath", "//div[@role='button']")[3].click()
  time.sleep(3.0)
  CHROME.find_elements("partial link text", "Redeem Now")[1].click()
  time.sleep(3.0)
  # TODO: IMPLEMENT AFTER $25.00 BALANCE