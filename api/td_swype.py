######################################## IMPORTS AND INIT

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
load_dotenv()

######################################## GLOBAL VARIABLES

# TD USA Credit Card authentication parameters
LOGIN_URL = "https://onlinebanking.tdbank.com/#/authentication/login"
USER_LOGIN = os.getenv("TD_USER_ID")        # Insert TD username
USER_PASSWORD = os.getenv("TD_PASSWORD")  # Insert password
MINIMUM_REWARDS_BALANCE = 25.0

# Chrome webdriver
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('log-level=3')
CHROME = webdriver.Chrome(service=Service(executable_path=r'/usr/local/bin/chromedriver'), options=OPTIONS)
# Bypass bot detection
CHROME.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

######################################## FUNCTIONS

# Bank authentication
def auth():
    # Navigate to login page
    CHROME.get(LOGIN_URL)
    # Delay to allow for rendering
    time.sleep(3.0)
    # Input credentials and login
    CHROME.find_element("id", "psudoUsername").send_keys(USER_LOGIN)
    CHROME.find_element("id", "password").send_keys(USER_PASSWORD)
    CHROME.find_element("xpath", "//button[@type='submit']").click()
    # Delay to allow for rendering
    time.sleep(10.0)
    # Check for security code retrieval
    if(len(CHROME.find_elements("xpath", "//h1[@aria-label='Security Code Verification']")) != 0):
        # Text message for security code
        CHROME.find_element("xpath", "//button[@aria-label='Text me']").click()
        # Ask user for security code
        sec_code = input("Enter security code: ")
        # Send security code
        CHROME.find_element("xpath", "//input[@aria-label='Enter security code']").send_keys(sec_code)
        CHROME.find_element("xpath", "//button[@aria-label='Submit']").click()
    # Check for failure
    if (len(CHROME.find_elements("xpath", "//div[@class='ngp-infobar ngp-infobar-error']")) != 0):
        raise Exception("Login failed.")
    
# Check rewards balance
def get_rewards_balance():
    # Login to bank
    auth()
    # Retrieve rewards balance information
    CHROME.find_element("xpath", "//span[@aria-label='TD Cash']").click()
    time.sleep(3.0)
    CHROME.find_element("xpath", "//a[@aria-label='Redeem rewards.']").click()
    time.sleep(10.0)
    window_after = CHROME.window_handles[1]
    CHROME.switch_to.window(window_after)
    rewards_balance_str = CHROME.find_element("id", "exposed-rewards-convertedValue").text
    rewards_balance_float = float(rewards_balance_str)
    return rewards_balance_float
    

# Redeem rewards
def redeem_rewards():
    # Check sufficient rewards balance
    rewards_balance = get_rewards_balance()
    if (rewards_balance < MINIMUM_REWARDS_BALANCE):
      raise Exception("Rewards balance insufficient.")
    # Commence redemption process
    CHROME.find_element("partial link text", "Redeem Again").click()
    time.sleep(3.0)
    CHROME.find_element("xpath", "//img[@alt='Jump to Statement Credit']").click()
    time.sleep(3.0)
    # TODO: IMPLEMENT AFTER $25.00 BALANCE

######################################## MAIN

if __name__ == "__main__":
    redeem_rewards()

    # Print exit message and quit
    print("PROCESS COMPLETE.")
    CHROME.close()
    quit()