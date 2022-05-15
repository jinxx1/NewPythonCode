# -*- coding: utf-8 -*-
import re

if __name__ == '__main__':
    import datetime,requests

    url = "http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/202112/t20211203_1514988.html"

    urlList = [{'catName': '河北省_省级_招标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/index_{}.html'},
               {'catName': '河北省_省级_中标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/zhbgg/index_{}.html'},
               {'catName': '河北省_省级_废标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/fbgg/index_{}.html'},
               {'catName': '河北省_省级_更正公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/gzgg/index_{}.html'},
               {'catName': '河北省_省级_单一来源', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/dyly/index_{}.html'},
               {'catName': '河北省_省级_合同公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/htgg/index_{}.html'},
               {'catName': '河北省_市县_招标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/index_746_{}.html'},
               {'catName': '河北省_市县_更正公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/gzgg/index_749_{}.html'},
               {'catName': '河北省_市县_中标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/zhbgg/index_746_{}.html'},
               {'catName': '河北省_市县_合同公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/htgg/index_750_{}.html'},
               {'catName': '河北省_市县_废标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/fbgg/index_746_{}.html'}]

    brow = requests.get(url)
    html= brow.text.encode(brow.encoding).decode('utf-8')

    regexhtml = re.findall("<!--主体 start-->(.*?)<!--主体 end-->",html,re.M|re.S)
    hhtml = ''.join(regexhtml).replace('\n','').replace(' ','')
    print(hhtml)
