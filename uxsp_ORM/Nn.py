import re

if __name__ == '__main__':
	with open('text.txt', 'r', encoding='utf-8') as ff:
		hhtml = ff.read()
	reg = re.findall("(<!--.*-->)", hhtml,re.M|re.S)
	for i in reg:
		hhtml = hhtml.replace(i,'')
	print(hhtml)