from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('https://mogi.vn/mua-nha?cp=3')
bs = BeautifulSoup(html.read(), 'html.parser')

links = []
titles = []
for points in bs.find_all('a', class_='link-overlay'):
    titles.append(points.text) 
    links.append(points.get('href'))
print(titles, len(titles))
print(links, len(links))

next_page = bs.find('a', title="Trang kế")

print(next_page.get('href'))
