from bs4 import BeautifulSoup
from urllib import request

html = "https://www.wine21.com/13_search/wine_list.html"
html = request.urlopen(html)
soup = BeautifulSoup(html,"html.parser")
a = soup.select('div.column_detail1 > div.cnt > div.tit > h4 > a ')
print(a)