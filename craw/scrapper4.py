from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

keyword = input('�궎�썙�뱶 �엯�젰: ')

path = '/Python/chromedriver'
driver = webdriver.Chrome(executable_path=r'C:/Python/chromedriver/chromedriver')
# �뱶�씪�씠踰� �쑀吏� �떆媛�(珥�)
driver.implicitly_wait(60)

#driver.get('URL')
driver.get('http://www.dogpre.com/')
#elem = driver.find_element_by_attribute("속성")
#elem = driver.find_element(속성, "이름")
elem = driver.find_element('name', "search_word")
#elem.send_keys(keyword)
elem.send_keys(keyword)
#elem.send_keys(Keys.RETURN) 
elem.send_keys(Keys.RETURN)
#elem.submit() 

#copy xpath
a = driver.find_elements_by_xpath('//*[@id="wrap"]/main/div/div/div[2]/div[2]/div[1]/a[2]')
driver.get(a[0].get_attribute('href'))


req = driver.page_source
soup= BeautifulSoup(req, 'html.parser')
#copy selector
information_list= soup.select('#wrap > main > div.detail-cont > div.section.new-write > ul > li.comm')
for information in information_list:
	print(information.text) 