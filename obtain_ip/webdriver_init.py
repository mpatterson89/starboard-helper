from selenium import webdriver
# from applitools.eyes import Eyes
from selenium.common.exceptions import NoSuchElementException
# from Tools.helpers.directory_helper import DirectoryHelper
import time
import sys
import traceback


# Example Use[####]:
# driver setup options:
#      chrome_driver_path, 'Chrome'
#      '', 'Firefox'
#      '', 'IE'
####  from Web import webdriver_init as wdi
####  wd = wdi.WebdriverInit()
####  driver = wd.setup_driver('Chrome')
# driver = setup_driver('', 'IE')
# driver = setup_driver('', 'Firefox')

class WebdriverInit:
    def __init__(self):
        # dir_h = DirectoryHelper()
        self.chrome_driver_path = '/Users/mpatterson/Dev/projects/starbound-helper/obtain_ip/chromedriver'  # dir_h.return_root(2)+'/Helpers/Web/chromedriver' #'C:\qa\Helpers\Web\chromedriver'

    # setup driver for specific browser
    def setup_driver(self, browser):

        try:
            # Start visual testing with browser viewport set to 1024x768.
            # Make sure to use the returned driver from this point on.
            if (browser == "Chrome"):
                return webdriver.Chrome(self.chrome_driver_path)
            if (browser == "Firefox"):
                return webdriver.Firefox()
            if (browser == "IE"):
                return webdriver.Ie()
        except Exception:
            print("Error: Cannot setup webdriver...")
            print(traceback.format_exc())

    # close driver
    def close_driver(self, driver):
        driver.quit()

    #	def createEyes():
    #	    eyes = Eyes()
    # This is your api key, make sure you use it in all your tests.

# eyes.api_key = 'E5Y8E5dwQOfm4kmC5fqLKHz9oDqss2pWLbh1020R1051063f0110'
#	    return eyes
