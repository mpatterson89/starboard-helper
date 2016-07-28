
from .webdriver_init import WebdriverInit
from .webdriver_helper import Webdriver_Helper

class ObtainIP:

    def __init__(self):
        self.web_init = WebdriverInit()
        self.wdh = Webdriver_Helper()


    def obtain_ip(self):
        #url = 'http://www.whatsmyip.org'
        url = 'http://www.whatismyip.org'
        #url = 'http://www.google.com'
        driver = self.web_init.setup_driver('Chrome')
        driver.get(url)
        print('opening...')
        element = driver.find_element_by_xpath('/html/body/div[2]/span').text
        #element = driver.find_element_by_xpath('//span[@id=\'ip\']')
        print(element)
        try:
            driver.close()
        except Exception:
            pass
        return element