import requests
import urllib.parse

keyword = '디퓨저'
encText = urllib.parse.quote('에어컨')
url = 'https://openapi.naver.com/v1/search/blog?query=' + encText