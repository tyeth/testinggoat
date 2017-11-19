#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import os
from unittest import skip
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timezone


MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):

    def setCurrentTest(self,x):
        self.CURRENT_TEST = f'{x}' + datetime.now(timezone.utc).strftime("%Y%m%d") + '.png'

    def setUp(self):
        self.CURRENT_TEST=''
        CHROME_PATH = '/c/Users/user/AppData/Local/Google/Chrome/Application/chrome.exe'
        CHROMEDRIVER_PATH = 'chromedriver.exe'
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        # chrome_options.binary_location = CHROME_PATH
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        #
        # driver = webdriver.Chrome(chrome_options=chrome_options
        #                           )
        #
        self.browser = webdriver.Chrome(
            #executable_path=CHROMEDRIVER_PATH,
            chrome_options=chrome_options)# driver
        #self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        # self.browser.quit()
        self.browser.get_screenshot_as_file(self.CURRENT_TEST)

        self.browser.close()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:

                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
