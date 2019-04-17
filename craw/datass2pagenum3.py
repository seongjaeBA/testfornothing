from bs4 import BeautifulSoup
import csv
import json
from urllib.request import urlopen, Request

def product_Crawling(soup):
	
	temp_list = []
	temp_dict = {}
	tr_list = soup.select('div.srch-prdc-list.row.del-tag.cate_list.listStyleOther > div.item-goods')
	
	for product in tr_list :
		link = product.find('a').get('href')
		img = product.find('a').find('img').get('src')
		ur = product.find('div',{'class':'star'}).find('em',{'class':'review-prdc'}).text
		price = product.find('span',{'class':'listItemTitle'}).find('span').text
		evalue = product.find('div',{'class':'star'}).find('span',{'class':'ic-star'}).find('em').text
		name= product.find('span',{'class' : 'tit-prdc'}).text


		temp_list.append([name, img, price, evalue, ur, link])
		temp_dict[str(name)] = {'name': name, 'img':img, 'price':price, 'evaluation':evalue, 'user_report': ur, 'link': link}
	
	return temp_list, temp_dict
#============================================================ End of product_Crawling() ============================================================#


def toCSV(product_list):
	with open('product_chart.csv', 'a', encoding='utf-8', newline='') as file :
		csvfile = csv.writer(file)
		for row in product_list:
			csvfile.writerow(row)
#============================================================ End of toCSV() ============================================================#


def toJson(product_dict):
	with open('product_chart.json', 'a', encoding='utf-8') as file :
		json.dump(product_dict, file, ensure_ascii=False, indent='\t')
#============================================================ End of toCSV() ============================================================#

product_list = []
product_dict = {}


for page in range(1, 27):
	URL = 'http://www.dogpre.com/shop/goods/goods_list.php?category=036&search_word&page=' + str(page)
	response = Request(URL, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)', 'accept-language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'})
	urldata = urlopen(response)
	html = urldata.read()
	soup = BeautifulSoup(html, 'html.parser')
	
	product_temp = product_Crawling(soup)
	product_list += product_temp[0]
	product_dict = dict(product_dict, **product_temp[1])

'''
# 리스트 출력

for item in product_list :
	print(item)

# 사전형 출력
for item in product_dict :
    print(item, product_dict[item]['img'], product_dict[item]['title'], product_dict[item]['artist'], product_dict[item]['album'])

# CSV파일 생성
toCSV(product_list)
''' 
	
# Json파일 생성
toJson(product_dict)


