'''
Created on 2018. 9. 27.

@author: kitcoop
'''
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup

def scrapper(url) :
	req= Request(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'})
	urldata = urlopen(req)
	html = urldata.read()
	soup = BeautifulSoup(html, 'html.parser')
	print(soup)

scrapper('http://gall.dcinside.com/mgallery/board/view?id=mnet_k&no=2698119')
