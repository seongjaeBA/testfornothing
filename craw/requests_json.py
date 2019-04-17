'''
Created on 2018. 9. 27.

@author: kitcoop
'''

import requests
from urllib.parse import urlparse

keyword = '강남역'
url = 'https://openapi.naver.com/v1/search/blog?query=' + keyword
result = requests.get(urlparse(url).geturl(),
					header = {'X-Naver-Clinet-Id': 'H1DC13DICQ8zIK84XwWn',
						'X-Naver-Clinet-Secret': '8sUQqFukKQ'})
json_obj = result.json()

for item in json_obj['items']:
	title = item['title'].replace('<b>','').replace('</b>','')
	link = item['link']
	bloggername = item['bloggername']
	print(title + '@' + link + '@' + bloggername)
	