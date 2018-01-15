from selenium.webdriver.common.by import By

from functional_tests.base import Base
import time

NEW_USER_PK = None

class User_Management(Base):
    def test_order1_add(self):
        self.browser.get(self.live_server_url+"/attendence/employee/manage")
        time.sleep(1)

        old_pks = []
        new_pks = []
        for tr in Base.find_elements(self, By.TAG_NAME, 'tr'):
            if tr.is_displayed():
                pk_value = tr.get_attribute("pk")
                if pk_value != None:
                    old_pks.append(pk_value)

        Base.find_element(self, By.ID, 'employee_add').click()
        Base.find_element(self, By.NAME,'user_name').send_keys('auto_test')
        Base.find_element(self, By.NAME, 'first_name').send_keys('auto_test')
        Base.find_element(self, By.NAME, 'last_name').send_keys('auto_test')
        Base.find_element(self, By.NAME, 'email').send_keys('add_email@auto_test.com')
        Base.find_element(self, By.ID, 'employee_save').click()
        time.sleep(1)

        for tr in Base.find_elements(self, By.TAG_NAME, 'tr'):
            if tr.is_displayed():
                pk_value = tr.get_attribute("pk")
                if pk_value != None:
                    new_pks.append(pk_value)

        old_count=len(old_pks)
        new_count=len(new_pks)
        self.assertEqual(old_count, new_count-1)

        same_pk_no = []
        for i in range(0, new_count):
            for j in range(0, old_count):
                if new_pks[i] == old_pks[j]:
                    same_pk_no.append(i)
                    break

        self.assertEqual(old_count, len(same_pk_no))

        global NEW_USER_PK
        for i in range(0, new_count):
            if i not in same_pk_no:
                NEW_USER_PK = new_pks[i]
                break

    def test_order2_edit(self):
        self.browser.get(self.live_server_url+"/attendence/employee/manage")
        time.sleep(1)

        old_email = 'add_email@auto_test.com'
        new_email = 'edit_email@auto_test.com'

        old_flag = 0
        new_flag = 0
        tr_list = Base.find_elements(self, By.TAG_NAME, 'tr')
        for i in range(1, len(tr_list)):
            email_td = Base.find_element(self, By.XPATH, '//*[@id="employee_list_table"]/tbody/tr[' + str(i) + ']/td[4]')
            if email_td.text == old_email:
                old_flag = 1
            elif email_td.text == new_email:
                new_flag = 1

        self.assertEqual(1, old_flag)
        self.assertEqual(0, new_flag)  

        #找到之前添加的信息进行修改
        for edit_btn in Base.find_elements(self, By.NAME, 'employee_edit'):
            if edit_btn.is_displayed():
                pk_value = edit_btn.get_attribute("data-pk")
                if pk_value == NEW_USER_PK:
                    edit_btn.click()
                    time.sleep(1)
                    # Base.find_element(self, By.NAME, 'user_name').send_keys('auto_test')
                    # Base.find_element(self, By.NAME, 'first_name').send_keys('auto_test')
                    # Base.find_element(self, By.NAME, 'last_name').send_keys('auto_test')
                    Base.find_element(self, By.NAME, 'email').send_keys(new_email)
                    Base.find_element(self, By.ID, 'employee_save').click()
                    break
        time.sleep(1)

        old_flag = 0
        new_flag = 0
        tr_list = Base.find_elements(self, By.TAG_NAME, 'tr')
        for i in range(1, len(tr_list)):
            email_td = Base.find_element(self, By.XPATH, '//*[@id="employee_list_table"]/tbody/tr[' + str(i) + ']/td[4]')
            if email_td.text == old_email:
                old_flag = 1
            elif email_td.text == new_email:
                new_flag = 1

        self.assertEqual(0, old_flag)
        self.assertEqual(1, new_flag)

    def test_order3_cancel(self):
        self.browser.get(self.live_server_url+"/attendence/employee/manage")
        time.sleep(1)

        old_pks = []
        new_pks = []
        for tr in Base.find_elements(self, By.TAG_NAME, 'tr'):
            if tr.is_displayed():
                pk_value = tr.get_attribute("pk")
                if pk_value != None:
                    old_pks.append(pk_value)

        # 找到之前添加的信息进行删除
        for del_btn in Base.find_elements(self, By.NAME, 'employee_delete'):
            if del_btn.is_displayed():
                pk_value = del_btn.get_attribute("data-pk")
                if pk_value == NEW_USER_PK:
                    del_btn.click()
                    Base.find_element(self, By.ID, 'confirm_yes').click()
                    break
        time.sleep(1)

        global NEW_USER_PK
        NEW_USER_PK = None

        for tr in Base.find_elements(self, By.TAG_NAME, 'tr'):
            if tr.is_displayed():
                pk_value = tr.get_attribute("pk")
                if pk_value != None:
                    new_pks.append(pk_value)

        old_count=len(old_pks)
        new_count=len(new_pks)
        self.assertEqual(old_count, new_count+1)

        same_pk_no = []
        for i in range(0, new_count):
            for j in range(0, old_count):
                if new_pks[i] == old_pks[j]:
                    same_pk_no.append(i)
                    break

        self.assertEqual(new_count, len(same_pk_no))
        self.flag_close_browser = 1
