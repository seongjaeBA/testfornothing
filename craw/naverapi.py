'''
Created on 2018. 9. 27.

@author: kitcoop
'''
import os
import sys
import urllib.request

client_id = 'JyP8ZGwBvgwzajxGWs7m'
client_secret = 'WC3_t8TCMu'
encText = urllib.parse.quote('에어컨')
url = 'https://openapi.naver.com/v1/search/blog?query=' + encText
request = urllib.request.Request(url)
request.add.header('X-Naver-Client-Id', client_id)
request.add.header('X-Naver-Client-Secret', client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
	response_body = response.read()
	print(response_body.decode('utf-8'))
else:
	print('error')