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
 
 
 '''
 # chrome driver path setting
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver.exe'

if os.path.exists(driver_path):
    print(f"chrom driver is insatlled: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver})")
    chromedriver_autoinstaller.install(True)

#browser setting
# options = Options()

#지정한 user-agent로 설정합니다.
# user_agent = "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
# options.add_argument('user-agent=' + user_agent)
#headless모드 브라우저가 뜨지 않고 실행됩니다.
# options.add_argument('headless') 
#실행되는 브라우저 크기를 지정.
# options.add_argument('--window-size= x, y')
#브라우저 최대화. 
# options.add_argument('--start-maximized') 
#브라우저 풀스크린 모드.
# options.add_argument('--start-fullscreen') 
#브라우저 이미지 로딩 x.
# options.add_argument('--blink-settings=imagesEnabled=false')
#브라우저 음소거. 
# options.add_argument('--mute-audio')
#시크릿 모드 브라우저. 
# options.add_argument('incognito') 

# Driver init
driver = webdriver.Chrome(executable_path = driver_path)

# set window size
# driver.set_window_size(480, 320)

# maximize window
# driver.maximize_window()
 '''