import sys
from . import webdriver_init as wdinit
from . import webdriver_helper as wdhelper
#from Helpers.Web.obtain_server_name import ObtainServerName
class WebTestInit():

    defaults = {
        'server':'http://www.whatsmyip.org',
        'browser':'Chrome',
        'port':'8085',
        'user':'trakdemo',
        'password':'trakdemo',
        'path':'/workassign/console.wa'
    }
    server = None
    browser=None
    port=None
    user=None
    password=None
    path=None
    wdh=None
    wdi=None
    url=None
    driver = None

    def __init__(self, **kwargs):

        if 'server' in kwargs.keys():
            self.server=kwargs['server']
        else:
            #obs = ObtainServerName()
            #self.defaults['server'] = obs.return_server_name()
            self.server = self.defaults['server']
        if 'browser' in kwargs.keys():
            self.browser=kwargs['browser']
        else:
            self.browser = self.defaults['browser']
        if 'port' in kwargs.keys():
            self.port = kwargs['port']
        else:
            self.port = self.defaults['port']
        if 'user' in kwargs.keys():
            self.user = kwargs['user']
        else:
            self.user = self.defaults['user']
        if 'password' in kwargs.keys():
            self.password = kwargs['password']
        else:
            self.password = self.defaults['password']
        if 'path' in kwargs.keys():
            self.path = kwargs['path']
        else:
            self.path = self.defaults['path']

        self.wdh = wdhelper.Webdriver_Helper()
        self.wdi = wdinit.WebdriverInit()
        self.url = self.wdh.form_http_url(self.user, self.password, self.server,
                                self.port, path=self.path)
        self.driver = self.wdi.setup_driver(self.browser)

########### EXAMPLE USAGE ############
'''
from Tools.helpers.mappings.web_transport_current_tasks_mappings import WebTransportCurrentTasksMappings as wtctm
from Tools.helpers.web.web_test_init import WebTestInit
import sys

init_options ={}
if len(sys.argv) >  1:
    init_options['server'] = sys.argv[1]

web_init = WebTestInit(**init_options)
#print(web_init.url)
driver = web_init.driver
driver.get(web_init.url)
driver.close()
'''
