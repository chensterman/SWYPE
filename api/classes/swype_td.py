import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .swype import Swype

class SwypeTD(Swype):

    def __init__(self, login_url, minimum_rewards_balance, username, password):
        self.login_url = login_url
        self.minimum_rewards_balance = minimum_rewards_balance
        self.username = username
        self.password = password

    def auth(self):
        # Navigate to login page
        Swype.CHROME.get(self.login_url)
        # Delay to allow for rendering
        element = WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.ID, "psudoUsername"))
        )
        # Input credentials and login
        element.send_keys(self.username)
        Swype.CHROME.find_element("id", "password").send_keys(self.password)
        Swype.CHROME.find_element("xpath", "//button[@type='submit']").click()
        # Delay to allow for rendering
        time.sleep(5.0)
        # Check for security code retrieval
        if(len(Swype.CHROME.find_elements("xpath", "//h1[@aria-label='Security Code Verification']")) != 0):
            # Text message for security code
            Swype.CHROME.find_element("xpath", "//button[@aria-label='Text me']").click()
            # Ask user for security code
            sec_code = input("Enter security code: ")
            # Send security code
            Swype.CHROME.find_element("xpath", "//input[@aria-label='Enter security code']").send_keys(sec_code)
            Swype.CHROME.find_element("xpath", "//button[@aria-label='Submit']").click()
        # Check for failure
        if (len(Swype.CHROME.find_elements("xpath", "//div[@class='ngp-infobar ngp-infobar-error']")) != 0):
            raise Exception("Login failed.")
        
    def get_rewards_balance(self):
        # Login to bank
        self.auth()
        # Retrieve rewards balance information
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.XPATH, "//span[@aria-label='TD Cash']"))
        )
        Swype.CHROME.find_element("xpath", "//span[@aria-label='TD Cash']").click()
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Redeem rewards.']"))
        )
        Swype.CHROME.find_element("xpath", "//a[@aria-label='Redeem rewards.']").click()
        time.sleep(10.0)
        window_after = Swype.CHROME.window_handles[1]
        Swype.CHROME.switch_to.window(window_after)
        rewards_balance_str = Swype.CHROME.find_element("id", "exposed-rewards-convertedValue").text
        rewards_balance_float = float(rewards_balance_str)
        return rewards_balance_float
        
    def redeem_rewards(self):
        # Check sufficient rewards balance
        rewards_balance = self.get_rewards_balance()
        if (rewards_balance <self.minimum_rewards_balance):
            raise Exception("Rewards balance insufficient.")
        # Commence redemption process
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Redeem Again")) #This is a dummy element
        )
        Swype.CHROME.find_element("partial link text", "Redeem Again").click()
        WebDriverWait(Swype.CHROME, 15).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='Jump to Statement Credit']")) #This is a dummy element
        )
        Swype.CHROME.find_element("xpath", "//img[@alt='Jump to Statement Credit']").click()
        time.sleep(3.0)
        # TODO: IMPLEMENT AFTER $25.00 BALANCE