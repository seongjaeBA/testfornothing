'''
Created on 2022. 05. 13.

@author: ysj

'''
import os
from time import sleep
from turtle import window_width
# import secrets
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

#https://pypi.org/project/webdriver-manager/
# from webdriver_manager.firefox import GeckoDriverManager
"""
Test Case Item
"""
TC_USER_ID = ['seong1898@gmail.com', 'dsab', 'dasdfn@donexist.com', 'seong1898@gmail.com', 'seong1898@gmail.com']
TC_PW = ['{비번}', 'aas', '{비번}', 'aas', '1234567']
TC_URL = ['한글-wrong-case1','test-wrong-case2-','-test-wrong-case3','@test-wrong-case4','test99999999912', 'how-to-make-clear-case']
TC_EMAIL = ['seong1898@gmail.com', '{확인_가능한_테스트_메일}', 'dasdfn@donexist.com', 'asdfw']
TC_KEYS = [Keys.ENTER,Keys.SPACE, Keys.SPACE, Keys.SPACE]
AUTH_PASSWORD = '{비번}'


class Swit_Qa_Test:
    def __init__(self):
        """
        headless browser init
        could use chrome|firefox
        
        wait use like sleep
        """
        sleep_time = 2
        driver_window_width = 480
        driver_window_height = 320
        
        # chrome driver path setting
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        driver_path = f'./{chrome_ver}/chromedriver.exe'

        if os.path.exists(driver_path):
            print(f"chrom driver is insatlled: {driver_path}")
        else:
            print(f"install the chrome driver(ver: {chrome_ver})")
            chromedriver_autoinstaller.install(True)

        # Driver init
        self.driver = webdriver.Chrome(executable_path = driver_path)
        #firefox setting
        # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        #time delay setting
        self.wait = WebDriverWait(self.driver, sleep_time)

        # set window size
        # driver.set_window_size(driver_window_width, driver_window_height)

        # maximize window
        self.driver.maximize_window()

        # 드라이버 유지 시간(초)
        # driver.implicitly_wait(60)
        
    def login(self, url = 'https://swit.io/', membership = "free-standard"):
        """
        사이트 로그인
        브라우저 사이즈에 따른 UI 변경 적용
        Test Case(TC) item 에따른 pass fail test
        
        Args:
            url (str, optional): _description_. Defaults to 'https://swit.io/'.
            membership (str, optional): _description_. Defaults to "free-standard".
        """
        #driver.get('크롤링 대상 사이트')
        self.driver.get(url)
        
        # get initial window size
        if self.driver.get_window_size()['width'] >= 1020:
            self.driver.find_element_by_link_text("로그인").click()
        else:
            # side_menu_btn= driver.find_element_by_class_name('menu-open-btn').send_keys(Keys.ENTER)
            self.driver.find_element_by_class_name('menu-open-btn').click()

            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "로그인")))
            self.driver.find_element_by_link_text("로그인").click()

        self.driver.find_element_by_class_name(membership).click()
        
        
        # 리스트가 아닌 빠른 내용으로 처리
        # swit_id = self.driver.find_element_by_id('id')
        # swit_id.clear()
        # swit_id.send_keys(TC_USER_ID[0])
        # swit_pw = self.driver.find_element_by_id('password')
        # swit_pw.clear()
        # swit_pw.send_keys(TC_PW[0])
        # self.driver.find_element_by_css_selector("button[type='submit']").click()        
        
        i = len(TC_USER_ID) - 1
        
        while i > -1:
            '''
            
            예외 처리 더 필요!!!!!!!
            
            '''
            print(TC_USER_ID[i], TC_PW[i])
            swit_id = self.driver.find_element_by_id('id')
            swit_id.clear()
            swit_id.send_keys(TC_USER_ID[i])
            swit_pw = self.driver.find_element_by_id('password')
            swit_pw.clear()
            swit_pw.send_keys(TC_PW[i])
            # sleep(1)            
            try:
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
                # print("Btn Clickable")
                self.driver.find_element_by_css_selector("button[type='submit']").click()
                if self.driver.current_url == 'https://app.swit.io/swit-home':
                    print("Btn Clickable")
                    break
                else:
                    print('wrong information') 
            except WebDriverException:
                print("Element is not clickable")
            i += -1

    def build_ws(self):
        """
        워크스페이스(WS) 생성
        워크스페이스 팀 동료 초대
        외부 서비스 연동은 제외
        
        예외 케이스 리포팅 및 log 기록 코드 필요
        """
        #ws init
        sleep(10)
        # self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="workspace-add-card"]')))         
        add_card = self.driver.find_element(By.CSS_SELECTOR, 'a[class="workspace-add-card"]')
        add_card.click()        
        swit_ws_name = self.driver.find_element_by_id('workspaceName')
        swit_ws_name.clear()
        swit_ws_name.send_keys('test')
        swit_ws_url = self.driver.find_element_by_id('workspaceUrl')
        for i in TC_URL:
            swit_ws_url.clear()
            swit_ws_url.send_keys(i)
            try:
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
                print("Btn Clickable")
                self.driver.find_element_by_css_selector("button[type='submit']").click()
            except WebDriverException:
                print("Element is not clickable")
            
        sleep(5)
        team_invite_mail = self.driver.find_element_by_id('[object Object]')
        for i in range(len(TC_KEYS)):
            team_invite_mail.send_keys(TC_EMAIL[i])
            team_invite_mail.send_keys(TC_KEYS[i])
            sleep(3)
        self.driver.find_element_by_css_selector("button[type='button']").click()
        sleep(3)
        modal_btn_gr = self.driver.find_element_by_css_selector("div[class='modal-button-group']")
        modal_btn_gr.find_element_by_tag_name("button").click()
        # sleep(2)
        # self.driver.find_element_by_css_selector("input[type='checkbox']").click()
        # self.driver.find_element_by_xpath('//*[@id="globalLayoutScroll"]/div[3]/swit-workspace-build-page/div/swit-workspace-invitation-page/swit-workspace-invitation-form/div[2]/div/div/ul/li/ul/li[1]/swit-input-text/span/input').get_attribute('value')
        self.driver.find_element_by_css_selector("a[class ='link-skip']").click()
        # self.driver.find_element_by_css_selector("button[class ='link-skip']").click()
        sleep(10)
                
    def del_ws(self):
        """
        ws 삭제
        예외처리 확인 필요
        """
        self.driver.find_element_by_css_selector("span[class ='selected-title selected-title--limit']").click()
        sleep(1)
        self.driver.find_element_by_css_selector("a[class ='primary-link']").click()
        sleep(2)
        self.driver.find_element_by_link_text("워크스페이스 삭제").click()
        sleep(1)
        self.driver.find_element_by_css_selector("button[class ='button button--simple']").click()
        password_input = self.driver.find_element_by_id('password')
        password_input.send_keys(AUTH_PASSWORD)
        self.driver.find_element_by_id('checkTest').click()
        sleep(1)
        self.driver.find_element_by_css_selector("button[type ='submit']").click()
                
    def logout(self):
        """
        swit home에서 logout case
        예외 처리 및 다른 루트 로그아웃도 필요
        """
        sleep(5)
        self.driver.find_element_by_css_selector("a[class ='member-info__link']").click()
        sleep(2)
        self.driver.find_element_by_css_selector("a[class ='sign-out-link']").click()
        
        
        pass  
    
test = Swit_Qa_Test()
test.login()
test.build_ws()
test.del_ws()
test.logout()
# while(True):
#     pass

    
