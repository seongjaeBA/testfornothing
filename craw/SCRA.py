'''
Created on 2018. 9. 27.

@author: kitcoop
'''

from urllib.request import urlopen, Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup

url = 'http://www.dogpre.com/shop/goods/goods_list.php?category=036004'
#querystring = {'address' : dong, 'key' : 'AIzaSyCovN925FdiVxp8_65-VPBN7S5tPSziAq0'}
#req= Request(url + urlencode(querystring), headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'})
req= Request(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'})

urldata = urlopen(req)
html = urldata.read()

soup = BeautifulSoup(html, 'html.parser')

print(soup) 