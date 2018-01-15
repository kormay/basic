from selenium import webdriver

class Browser():
    browser = None
    def __new__(cls):
        if Browser.browser == None:
            Browser.browser = webdriver.Firefox()
        return Browser.browser