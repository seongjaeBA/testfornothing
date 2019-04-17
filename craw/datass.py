from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

keyword = '사료'

path = '/Python/chromedriver'

#강아지 대통령
driver = webdriver.Chrome(executable_path=r'C:/Python/chromedriver/chromedriver')
driver.get('http://www.dogpre.com/')
elem = driver.find_element('name', "search_word")
elem.send_keys(keyword)
elem.send_keys(Keys.RETURN)
req = driver.page_source
soup= BeautifulSoup(req, 'html.parser')
information_list= soup.select('#wrap > main > div > div > div.srch-cont > div.srch-prdc-list.row.del-tag.cate_list.listStyleOther > div')
for information in information_list:
	print(information.text) 