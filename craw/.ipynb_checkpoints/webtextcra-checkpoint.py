from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json

#강아지 대통령
temp_list = []
temp_dict = {}


for page_number in range(1, 2):
	URL = 'http://www.dogpre.com/shop/goods/goods_list.php?category=036&search_word&page=' + str(page_number)
	response = Request(URL, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)', 'accept-language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'})
	urldata = urlopen(response)
	html = urldata.read()
	soup = BeautifulSoup(html, 'html.parser')
	
	find_product = soup.select("div.srch-prdc-list.row.del-tag.cate_list.listStyleOther > div.item-goods")

	for product in find_product :
		link = product.find('a').get('href')
		img = product.find('a').find('img').get('src')
		ur = product.find('div',{'class':'star'}).find('em',{'class':'review-prdc'}).text
		price = product.find('span',{'class':'listItemTitle'}).find('span').text
		evalue = product.find('div',{'class':'star'}).find('span',{'class':'ic-star'}).find('em').text
		name= product.find('span',{'class' : 'tit-prdc'}).text
		print(name)
		'''
		temp_list.append([name, img, price, evalue, ur, link])
		temp_dict[str(name)] = {'img':img, 'name':name, 'price':price, 'evaluation':evalue, 'user_report': ur, 'link': link}
		'''
		temp_list.append([img, price, evalue, ur, link])
		temp_dict[str(link)] = {'img':img, 'price':price, 'evaluation':evalue, 'user_report': ur, 'link': link}
		
with open('mnet_chart.json', 'w', encoding='utf-8') as file :
	json.dump(temp_dict, file, ensure_ascii=False, indent='\t')





