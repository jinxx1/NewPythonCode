import os
import re

from crawltools import getBetweenDayList
from bs4 import BeautifulSoup


def filter_content(html):

    soup = BeautifulSoup(html, 'lxml')

    for i in soup.find_all(class_=re.compile("foot")):
        i.extract()
    for i in soup.find_all(id=re.compile("foot")):
        i.extract()
    for i in soup.find_all('script'):
        i.extract()
    for i in soup.find_all('div', attrs={'id': 'articleTool'}):
        i.extract()
    for i in soup.find_all('style'):
        i.extract()
    for i in soup.find_all('meta'):
        i.extract()




    return soup.prettify()
