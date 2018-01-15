from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from django.test import LiveServerTestCase    
from .Browser import Browser

class Base(LiveServerTestCase):
    def setUp(self):
        self.browser = Browser()
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        self.flag_close_browser = None
        self.browser.get(self.live_server_url)

    def tearDown(self):
        if self.flag_close_browser == 1:
            self.browser.quit()

    def login(self, user_name, password):
        self.find_element(By.NAME, 'user_name').send_keys(user_name)
        self.find_element(By.NAME, 'pwd').send_keys(password)
        self.find_element(By.TAG_NAME, 'button').submit()

    def find_element(self, find_type, element):
        obj = self.browser.find_element(find_type, element)
        if self.check_element_type(obj) and obj.is_displayed():
            obj.clear()
        return obj

    def find_elements(self, find_type, element):
        obj_list = self.browser.find_elements(find_type, element)
        for obj in obj_list:
            if self.check_element_type(obj) and obj.is_displayed():
                obj.clear()
        return obj_list
    
    def check_element_type(self,obj):
        element_type = obj.get_attribute("type")
        if element_type == "text":
            return 1
        elif element_type == "password":
            return 1
        elif element_type == "email":
            return 1
        else:
            return 0
