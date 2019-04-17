from urllib.request import urlopen, Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup as BS

URL = 'http://www.11st.co.kr/category/DisplayCategory.tmall?'
query = {'method' : 'getDisplayCategory2Depth', 'dispCtgrNo' : 1003115}
req = Request(URL + urlencode(query), headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'})
urldata=urlopen(req)
html = urldata.read()
soup=BS(html, 'html.parser')

for index in range(1, 41):
	productURL = soup.find('a',{'data-log-index':index}).get('href')
	preq = Request(productURL, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'})
	purldata=urlopen(preq)
	phtml = purldata.read()
	psoup=BS(phtml, 'html.parser')
	print(psoup.text)
	
	#productPrdInfo


#prd_inf=product.find('a').get('body')