import json
from redis_dup import BloomFilter
bl = BloomFilter('uxue:url')

with open('pageALL,json','r') as ff:
	jsonT = json.load(ff)

for url in jsonT:
	if bl.exists(url):
		continue
	bl.insert(url)
