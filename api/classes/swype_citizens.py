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
            EC.presence_of_element_located((By.ID, "username")) #This is a dummy element
        )
        element.send_keys(self.username)
        Swype.CHROME.find_element("id", "password").send_keys(self.password)
        Swype.CHROME.find_element("id", "loginButton").click()
        # Delay to allow for rendering
        time.sleep(5.0)
        # Check for failure
        if (len(Swype.CHROME.find_elements("xpath", "//div[@class='alert alert-danger']")) != 0):
            raise Exception("Login failed.")
        
    def get_rewards_balance(self):
        # Login to bank
        self.auth()
        # Retrieve rewards balance information
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='card-currency']")) #This is a dummy element
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
            EC.presence_of_element_located((By.XPATH, "//div[@role='button']")) #This is a dummy element
        )
        Swype.CHROME.find_elements("xpath", "//div[@role='button']")[3].click()
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Redeem Now")) #This is a dummy element
        )
        Swype.CHROME.find_elements("partial link text", "Redeem Now")[1].click()
        # TODO: IMPLEMENT AFTER $25.00 BALANCE