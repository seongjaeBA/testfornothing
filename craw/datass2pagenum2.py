import requests
from bs4 import BeautifulSoup

maximum = 0
page = 2

#강아지 대통령
response = requests.get('http://www.dogpre.com/shop/goods/goods_list.php?category=036&search_word=%BB%E7%B7%E1&parent_sno=&scroll=0&cateType=&v_category=&category=036')
source = response.text
soup = BeautifulSoup(source, 'html.parser')
paging = soup.find('div', {'class' : 'pagination'})
print(paging)

while 1:
	page_list = paging.findAll('a', {'href' : '?category=036&search_word=%BB%E7%B7%E1&parent_sno&scroll=0&cateType&v_category&page=' + str(page)})
	if not page_list:
		maximum = page - 1
		break
	page = page + 1
print("총 " + str(maximum) + " 개의 페이지가 확인 됬습니다.")
