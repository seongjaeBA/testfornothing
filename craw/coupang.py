from urllib.request import urlopen, Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup as BS

URL = 'https://www.coupang.com/np/search?component=&q=%EB%AF%B8%EB%B0%B1%ED%99%94%EC%9E%A5%ED%92%88&channel=user'
query = {'method' : 'getDisplayCategory2Depth', 'dispCtgrNo' : 1003115}
req = Request(URL + urlencode(query), headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'})
urldata=urlopen(req)
html = urldata.read()

soup=BS(html, 'html.parser')
print(soup)