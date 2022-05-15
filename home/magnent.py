import requests,re
from lxml import etree
from urllib import parse

baseUrl = "https://www.torrentkitty.net/search"
keyWord = 'WANZ-976'
url = parse.urljoin(baseUrl,keyWord)

brow = requests.get(url)
sel = etree.HTML(brow.text)

magLinks = sel.xpath('//a[@rel="magnet"]/@href')
print(magLinks)

# selector = etree.HTML()