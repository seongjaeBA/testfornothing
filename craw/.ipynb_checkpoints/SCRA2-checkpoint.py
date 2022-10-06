'''
Created on 2018. 9. 27.

@author: kitcoop
'''

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

with urllib.request.urlopen('http://www.dogpre.com/shop/goods/goods_list.php?category=036004') as request:
	html = request.read()
	soup = BeautifulSoup(html, 'html.parser')
	
	print(soup)