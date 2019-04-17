'''
Created on 2018. 9. 27.

@author: kitcoop
'''
import requests
from bs4 import BeautifulSoup

def scrapper(url) :
	result = requests.get(url)
	soup = BeautifulSoup(result.content, 'html.parser')
	
	print(result.content)
	
scrapper('http://www.dogpre.com/shop/goods/goods_list.php?category=036004')