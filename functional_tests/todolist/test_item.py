from selenium import webdriver
from django.test import LiveServerTestCase
from functional_tests.Browser import Browser
import time

class ItemTest(LiveServerTestCase):
    def setUp(self):
        self.browser = Browser()
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        
    def tearDown(self):
        self.browser.quit()

    def test_can_add_an_item(self):
        browser = self.browser
        browser.get(self.live_server_url + '/todolist/item/add')
        self.assertEqual(browser.title, 'add item')