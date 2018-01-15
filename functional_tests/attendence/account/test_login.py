from selenium.webdriver.common.by import By
from functional_tests.base import Base

class Login(Base):
    def test_order1_login_with_incorrect_info(self): 
        Base.login(self, 'admin', 'incorrect')
        self.assertIn('Username or password is incorrect', self.find_element(By.TAG_NAME, 'body').text)
        
    def test_order2_login_with_correct_info(self):
        Base.login(self, 'root', 'max123')
        self.assertIn(self.live_server_url+"/attendence/index", self.browser.current_url)