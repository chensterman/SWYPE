import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .swype import Swype

class SwypeCitizens(Swype):

    def __init__(self, login_url, minimum_rewards_balance, username, password):
        self.login_url = login_url
        self.minimum_rewards_balance = minimum_rewards_balance
        self.username = username
        self.password = password

    def auth(self):
        # Navigate to login page
        Swype.CHROME.get(self.login_url)
        # Input credentials and login
        element = WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        element.send_keys(self.username)
        Swype.CHROME.find_element("id", "password").send_keys(self.password)
        Swype.CHROME.find_element("id", "loginButton").click()
        # Delay to allow for rendering
        time.sleep(5.0)
        # Check for security code retrieval
        if(len(Swype.CHROME.find_elements("id", "sendActivationCode")) != 0):
            # Text message for security code
            Swype.CHROME.find_element("id", "sendActivationCode").click()
            # Ask user for security code
            sec_code = input("Enter security code: ")
            # Send security code
            Swype.CHROME.find_element("id", "oneTimePassCode").send_keys(sec_code)
            Swype.CHROME.find_element("xpath", "//button[@aria-label='Continue']").click()
        # Check for failure
        if (len(Swype.CHROME.find_elements("xpath", "//div[@class='alert alert-danger']")) != 0):
            raise Exception("Login failed.")
        
    def get_rewards_balance(self):
        # Login to bank
        self.auth()
        # Retrieve rewards balance information
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='card-currency']"))
        )
        rewards_balance_str = Swype.CHROME.find_elements("xpath", "//div[@class='card-currency']")[1].text.strip()
        rewards_balance_float = float(rewards_balance_str[1:])
        return rewards_balance_float
        
    def redeem_rewards(self):
        # Check sufficient rewards balance
        rewards_balance = self.get_rewards_balance()
        if (rewards_balance < self.minimum_rewards_balance):
            raise Exception("Rewards balance insufficient.")
        # Commence redemption process
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='button']"))
        )
        Swype.CHROME.find_elements("xpath", "//div[@role='button']")[3].click()
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Redeem Now"))
        )
        Swype.CHROME.find_elements("partial link text", "Redeem Now")[1].click()
        # Redemption pages - only increments of 25. Will go with default for now
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Continue']"))
        )
        Swype.CHROME.find_element("xpath", "//button[@aria-label='Continue']").click()
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Continue']"))
        )
        Swype.CHROME.find_element("xpath", "//button[@aria-label='Continue']").click()
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.ID, "termsAndConditionsId"))
        )
        Swype.CHROME.find_element("id", "termsAndConditionsId").click()
        Swype.CHROME.find_element("xpath", "//button[@aria-label='Redeem now']").click()