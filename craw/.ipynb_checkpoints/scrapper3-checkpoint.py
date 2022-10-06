from selenium import webdriver
from selenium.webdriver.common.keys import Keys

keyword = input('키워드 입력: ')

path = '/Python/chromedriver'
driver = webdriver.Chrome(executable_path=r'C:/Python/chromedriver/chromedriver')
# 드라이버 유지 시간(초)
driver.implicitly_wait(60)

#driver.get('크롤링 대상 사이트')
driver.get('http://www.dogpre.com/')
#elem = driver.find_element_by_분류("키워드 입력 장소")
#elem = driver.find_element(분휴, "키워드 입력 장소")
elem = driver.find_element('name', "search_word")
#elem.send_keys(keyword를 보내겠다)
elem.send_keys(keyword)
#elem.send_keys(Keys.RETURN) 키 값을 보내는 명령어
elem.send_keys(Keys.RETURN)
#elem.submit() 이걸로도 가능

