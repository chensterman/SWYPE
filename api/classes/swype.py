######################################## IMPORTS AND INIT

from abc import ABC, abstractmethod
from selenium import webdriver

######################################## GLOBAL VARIABLES
 
class Swype(ABC):

    # Chrome webdriver
    OPTIONS = webdriver.ChromeOptions()
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
 
    @abstractmethod
    def auth(self):
        pass

    @abstractmethod
    def get_rewards_balance(self):
        pass

    @abstractmethod
    def redeem_rewards(self):
        pass

    def close_browser(self):
        Swype.CHROME.close()