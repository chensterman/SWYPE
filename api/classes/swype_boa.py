import time
from .swype import Swype
from selenium.webdriver.support.ui import Select

class SwypeBOA(Swype):

    def __init__(self, login_url, minimum_rewards_balance, username, password):
        self.login_url = login_url
        self.minimum_rewards_balance = minimum_rewards_balance
        self.username = username
        self.password = password

    def auth(self):
        # Navigate to login page
        Swype.CHROME.get(self.login_url)
        # Delay to allow for rendering
        time.sleep(3.0)
        # Input credentials and login
        Swype.CHROME.find_element("id", "onlineId1").send_keys(self.username)
        Swype.CHROME.find_element("id", "passcode1").send_keys(self.password)
        Swype.CHROME.find_element("id", "signIn").click()
        # Delay to allow for rendering
        time.sleep(3.0)
        # Check for security code retrieval
        if(len(Swype.CHROME.find_elements("id", "RequestAuthCodeForm")) != 0):
            # Text message for security code
            Swype.CHROME.find_element("id", "btnARContinue").click()
            # Ask user for security code
            sec_code = input("Enter security code: ")
            # Send security code
            Swype.CHROME.find_element("id", "tlpvt-acw-authnum").send_keys(sec_code)
            Swype.CHROME.find_element("id", "yes-recognize").click()
            Swype.CHROME.find_element("id", "continue-auth-number").click()
        # Check for failure
        if (len(Swype.CHROME.find_elements("xpath", "//div[@class='error-skin']")) != 0):
            raise Exception("Login failed.")
        
    # Check rewards balance
    def get_rewards_balance(self):
        # Login to bank
        self.auth()
        # Retrieve rewards balance information
        Swype.CHROME.find_element("xpath", "//a[@name='onh_rewards_and_deals']").click()
        time.sleep(3.0)
        Swype.CHROME.find_element("id", "CREDIT_CARDS_TILE_tab").click()
        time.sleep(3.0)
        rewards_balance_str = Swype.CHROME.find_element("xpath", "//span[@class='NPI_L2 act-cash']").text[1:]
        rewards_balance_float = float(rewards_balance_str)
        print(rewards_balance_float)
        return rewards_balance_float
        

    # Redeem rewards balance
    def redeem_rewards(self):
        # Check sufficient rewards balance
        rewards_balance = self.get_rewards_balance()
        if (rewards_balance < self.minimum_rewards_balance):
            raise Exception("Rewards balance insufficient. ($25 minimum)")
        # Commence redemption process
        Swype.CHROME.find_element("partial link text", "View details/redeem").click()
        time.sleep(10.0)
        window_after = Swype.CHROME.window_handles[1]
        Swype.CHROME.switch_to.window(window_after)
        select = Select(Swype.CHROME.find_element("id", "redemption_option"))
        select_text = [value.text for value in select.options if "Statement Credit" in value.text][0]
        select.select_by_visible_text(select_text)
        # Input redemption amount
        redemption_amount = float(input("Enter amount you would like to redeem: "))
        if (redemption_amount > rewards_balance):
            raise Exception("Rewards balance insufficient.")
        Swype.CHROME.find_element("id", "redemption-amount-input").send_keys(redemption_amount)
        # Redeem amount
        Swype.CHROME.find_element("id", "redeem").click()
        time.sleep(3.0)
        Swype.CHROME.find_element("id", "complete-otr-confirm").click()
        time.sleep(3.0)
        if (len(Swype.CHROME.find_elements("id", "redeem-congrats")) == 0):
            raise Exception("Redemption failure.")
        time.sleep(3.0)

'''
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
'''