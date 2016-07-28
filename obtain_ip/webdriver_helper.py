import sys
import time
import traceback
from selenium import webdriver
# from applitools.eyes import Eyes
from selenium.common.exceptions import NoSuchElementException as nsee
from selenium.common.exceptions import StaleElementReferenceException
#from Tools.helpers.web.search_dojo_grid import SearchDojoGrid

class Webdriver_Helper:
    def __init__(self):
        pass

    # Debugging function used to help
    # in negative testing
    def print_traceback(self):
        traceback.print_exc(file=sys.stdout)

    #Check dropdown history xpaths and element ids. 
    #This speeds up selenium web tests
    def add_history(self, compare, path):
        print("Writing history")
        history_file = 'history_dropdowns.txt'
        _file = open(history_file, 'r')
        found = False
        try:
            for line in _file:
                _compare = line.split(':')[0]
                _path    = line.split(':')[1].split('\n')[0]
                if compare == _compare and path == _path:
                    found = True
            _file.close()
            if not found:
                print("Writing history 2")
                _file2 = open(history_file, 'a')
                _file2.write(compare+":"+path+"\n")
                _file2.close()
        except(Exception):
            self.print_traceback()

    #Check dropdown history xpaths and element ids. 
    #This speeds up selenium web tests
    def check_history(self, compare):
        history_file = 'history_dropdowns.txt'
        _file = open(history_file, 'r')
        history = list()
        for line in _file:
            try:
                if line.split(':')[0] == compare:
                    history.append(line.split(':')[1].split('\n')[0])
            except(Exception):
                pass
        return history

    # Select from dropdown using xpath. Iterate through 'menu_items'
    def select_item_from_dropdown_by_id(self, driver, pre, post, compare):
        no_error = True
        found_item = False
        i = -5
        history = self.check_history(compare)
        history_done = False
        history_index = 0
        while no_error and not found_item:
            try:
                xpath = None
                if not history_done and len(history) > 0:
                    xpath = history[history_index]
                    print("HISTORY: "+xpath)
                    history_index = history_index + 1
                    if history_index >= len(history):
                        history_done = True
                else:
                    pre = '//td[@id=\'dijit_MenuItem_'
                    post = '_text\']'
                    xpath = pre + str(i) + post
                    i = i + 1

                item = driver.find_element_by_xpath(xpath)
                print(xpath+" : "+item.text)
                if (len(item.text) > 0):
                    print(item.text + " : " + compare)
                if (item.text == compare):
                    time.sleep(1)
                    driver.execute_script('window.scrollTo('+str(item.location['x'])+', ' + str(item.location['y'])+ ');')
                    time.sleep(1)
                    item.click()
                    self.add_history(compare, xpath)
                    found_item = True

            except(nsee):
                if i > 500:
                    print("No more items...")
                    no_error = False

    # Select from dropdown using xpath. Split xpath in 2
    def select_item_from_dropdown(self, driver, pre, post, compare):
        no_error = True
        found_item = False
        i = 1
        history = self.check_history(compare)
        history_done = False
        history_index = 0
        while no_error and not found_item:
            try:
                item_path = None
                if not history_done and len(history) > 0:
                    item_path = history[history_index]
                    print("HISTORY: "+item_path)
                    history_index = history_index + 1
                    if history_index >= len(history):
                        history_done = True
                else:
                    item_path = pre + str(i) + post
                    i = i + 1
                item = driver.find_element_by_xpath(item_path)
                print(item.text + " : " + compare)
                if (item.text == compare):
                    item.click()
                    found_item = True
                    self.add_history(compare, item_path)
                
            except(nsee):
                print("No more items...")
                no_error = False

    # Select from dropdown using xpath. Split xpath in 2
    def return_all_items_from_dropdown_by_id(self, driver, pre, post):
        no_error = True
        i = 1
        items = {}
        while no_error:
            try:
                item_path = pre + str(i) + post
                i = i + 1
                item = driver.find_element_by_id(item_path)
                if (item.text != ""):
                    #print(item.text)
                    items[item.text] = item.text
            except(nsee):
                print("No more items...")
                no_error = False
        return items

    # With element refresh(for stale exception)
    def wait_for_clickable_stale(self, driver, element_path, css_xpath, error_msg=None,
                                 limit=False, limit_count=500, raise_exception=False):
        _raise_exception = False
        try:
            if (css_xpath == "xpath"):
                element = driver.find_element_by_xpath(element_path)
            else:
                element = driver.find_element_by_css_selector(element_path)
            not_clickable = True
            itr = 0
            while not_clickable:
                itr = itr + 1
                try:
                    element.click()
                    print("Clicked ["+element_path+"]")
                    not_clickable = False
                except Exception:
                    if error_msg != None:
                        print(error_msg)
                        time.sleep(1)
                    if limit and itr > limit_count:
                        not_clickable = False
                        if raise_exception ==True:
                            _raise_exception = True
                    # refresh
                    if (css_xpath == "xpath"):
                        element = driver.find_element_by_xpath(element_path)
                    else:
                        element = driver.find_element_by_css_selector(element_path)
            return element
        except(StaleElementReferenceException, nsee):
            if _raise_exception == True:
                raise Exception
            return None

    def wait_for_clickable(self, element, error_msg=None, limit=False):
        time.sleep(1)
        not_clickable = True
        itr = -1
        try_again = True
        while not_clickable:
            itr = itr + 1
            try:
                element.click()
                not_clickable = False
            except Exception:
                if error_msg != None:
                    print(error_msg)
                if limit and itr > 250:
                    if not try_again:
                        not_clickable = False
                    try_again = False
                    itr = -1

    def select_options(self, element, items, optionsCannotBeZero=False):
        options = element.find_elements_by_tag_name('option')
        print(len(options))
        if (optionsCannotBeZero and len(options) < 1):
            while len(options) < 1:
                options = element.find_elements_by_tag_name('option')
        for option in options:
            for item in items:
                if option.text == item:
                    print(option.text)
                    option.click()

    def return_all_element_options(self, element):
        options = element.find_elements_by_tag_name('option')
        options_dict = {}
        print(len(options))
        for option in options:
            options_dict[option.text] = option.text
        return options_dict


    def form_http_url(self, user, password, server, port, path, debug=False):
        url = "http://" + user + ":" + password + "@" + server + ':' + port + path
        if debug:
            print(url)
        return url

    def find_click_ok_instance(self, driver, pre='#dijit_form_Button_', post='_label',
                               css=None, xpath=None, limit=True, raise_exception=False):
        found_ok = False
        index = -5
        limit_count = 100
        has_reset = False
        while not found_ok:
            try:
                if xpath == None:
                    css = pre + str(index) + post
                    ok = driver.find_element_by_css_selector(css)
                else:
                    ok = driver.find_element_by_xpath(xpath)
                if ok.text == "OK":
                    found_ok = True
                    ok.click()
            except nsee:
                if xpath == None:
                    print("Failed on: " + css)
                else:
                    print("Failed on: " + xpath)
                if ((not has_reset) and index >= limit_count):
                    index = -5
                    has_reset = True
                else:
                    index = index + 1
                if index > limit_count and limit == True:
                    found_ok = True
                    print("[ERROR] - Limit reached, no OK form button found.")
                    if raise_exception == True:
                        raise Exception


    def wait_for_clickable_by_id(self, driver, element_id, limit=None, err_msg=None):
        not_clicked = True
        counter = 0
        while not_clicked:
            try:
                driver.find_element_by_id(element_id).click()
                not_clicked = False
                print("Element found and clicked by ID ["+str(element_id)+"]")
            except(Exception):
                counter = counter + 1
                if counter & counter >= limit:
                    not_clicked = False
                    if err_msg:
                        print(err_msg)
                    else:
                        print("Element could NOT be found and clicked by ID ["+str(element_id)+"]")

    def wait_for_element_stale(self, driver, element_path, css_xpath, error_msg=None, limit=False, limit_count=500):
        try:
            if (css_xpath == "xpath"):
                element = driver.find_element_by_xpath(element_path)
            else:
                element = driver.find_element_by_css_selector(element_path)
            not_clickable = True
            itr = 0
            while not_clickable:
                itr = itr + 1
                try:
                    if not element.is_displayed():
                        raise Exception
                    else:
                        print("Can see ["+element_path+"]")
                        not_clickable = False
                except Exception:
                    if error_msg != None:
                        print(error_msg)
                        time.sleep(2)
                    if limit and itr > limit_count:
                        not_clickable = False
                    # refresh
                    if (css_xpath == "xpath"):
                        element = driver.find_element_by_xpath(element_path)
                    else:
                        element = driver.find_element_by_css_selector(element_path)
            return element
        except(StaleElementReferenceException, nsee):
            return None

    def wait_for_element_with_text(self, driver,
                                   element_path,
                                   css_xpath,
                                   text ,
                                   error_msg=None,
                                   limit=False,
                                   limit_count=500):
        try:
            if (css_xpath == "xpath"):
                element = driver.find_element_by_xpath(element_path)
            else:
                element = driver.find_element_by_css_selector(element_path)
            not_clickable = True
            itr = -5
            while not_clickable:
                itr = itr + 1
                try:
                    if not element.is_displayed() and str(element.text) == text:
                        raise Exception
                    else:
                        print("Can see ["+element_path+"] with text: " + str(element.text))
                        not_clickable = False
                except Exception:
                    if error_msg != None:
                        print(error_msg)
                        time.sleep(2)
                    if limit and itr > limit_count:
                        not_clickable = False
                    # refresh
                    if (css_xpath == "xpath"):
                        element = driver.find_element_by_xpath(element_path)
                    else:
                        element = driver.find_element_by_css_selector(element_path)
            return element
        except(StaleElementReferenceException, nsee):
            return None

    #returns the number in the grid so above method 
    #can click down to that task.
    def find_grid_element_by_worker(self, driver, worker):
        grid_index = None
        for i in range(1, 150):
            try:
                self.click_grid_row_employee_tab(driver, i, cycle=False)
                          #//*[@id="aworkersNode-row-2"]/table/tr/td[1]
                          #//*[@id="aworkersNode-row-2"]
                xpath = "//div[@id='aworkersNode-row-"+str(i)+"']/table/tr/td[1]"
                #xpath = "//td[@class='dgrid-cell dgrid-column-comments field-comments' @role='gridcell'"
                element = driver.find_element_by_xpath(xpath)
                #print(element.text + " : " + str(i))
                #print("'"+worker+"'=='"+element.text+"'?")
                if worker == element.text:
                    print(element.text + " : " + str(i))
                    grid_index = i
                    break
            except(Exception):
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)
                print('skip worker name: '+str(i))
        if grid_index == None:
            print("Worker Element was not found for: " + str(worker))
        return grid_index

    def click_grid_row_employee_tab(self, driver, index, cycle=True):
        #if task_number > 24:
            #cycle all tasks
        if cycle == True:
            for i in range(1, index):
                row_xpath ="//div[@id='aworkersNode-row-"+str(i)+"']"
                row_id="aworkersNode-row-"+str(i)
                self.wait_for_clickable_by_id(driver, row_id, limit=500)
        #obtain rows
        row_xpath ="//div[@id='aworkersNode-row-"+str(index)+"']"
        row_id="aworkersNode-row-"+str(index)
        self.wait_for_clickable_by_id(driver, row_id, limit=500)

    '''def find_grid_element_by_fields(self, driver,tab=None, search_criteria=None ):
        sdg = SearchDojoGrid()
        data = sdg.get_rows(driver,tab, search_criteria=search_criteria)
        print(data)
        #sdg.cycle_rows_to_element(data[0])
        return data'''

    #Must have grid visible obviously.
    def select_row_of_grid(self, driver, element):
        sdg = SearchDojoGrid()
        sdg.cycle_rows_to_element(element, driver=driver)