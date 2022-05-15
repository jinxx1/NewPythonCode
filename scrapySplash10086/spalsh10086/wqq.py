import requests
import json
import re
from lxml import etree
from lxml import html

import time
from concurrent.futures import ThreadPoolExecutor
from urllib import parse# mark1

import faker
faker = faker.Faker()# mark2
session = requests.Session()
headers = {
'User-Agent':faker.user_agent(),# use to mark2 #构造请求头池
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}
def get_result(p):
    url = f'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=100&page={p}'

    response = session.get(url=url,headers=headers)
    html = etree.HTML(response.text)
    result = html.xpath("//table[@id='node_list']//a/@href")# mark3

    result_list = []
    for i in result:# use to mark3
        ddict = {}
        ddict['artcle_url'] = parse.urljoin(url, i)# mark4 相对地址形成一个绝对地址
        title = html.xpath("//*[@href ='{}']/@title".format(i))# mark5
        ddict['title'] = ''.join(title)# mark6
        time = html.xpath("//*[@href ='{}']/../../td[4]/text()".format(i))# mark7
        timeRex = re.findall("\d{4}-\d{2}-\d{2}",''.join(time))# mark8

        from dateutil.parser import parse as par# mark9  从字符串中解析出时间对象
        ddict['time'] = str(par(''.join(timeRex)))# use to mark9
        result_list.append(ddict)
    return result_list

    # 我写的存入本地json，跟你写的存入看看有什么区别
    # with open("山西政府采购.json","w",encoding='utf-8') as f:
    #     f.write(json.dumps(result_list,ensure_ascii=False))

    # 你写的存入本地json
    # with open("山西政府采购.json","a",encoding='utf-8') as f :
    #     f.write(json.dumps(result_list))
def getArticeinfo(artice):
    for i in artice:
        url = i['artcle_url']
        response = session.get(url=url,headers=headers)
        xml = etree.HTML(response.text)
        result = xml.xpath('//*[@id="t"]/table')
        results = html.tostring(result[0])
        print(results)
        print(i)
        print('---------------')

def main(maxPage):

# requests方式，建议同一个网站不要开多线程。会让对方网站受不了的。封IP导致程序无法进行。
#     pool = ThreadPoolExecutor(max_workers=30)
#     pool.map(get_result,[p for p in range(1,100)])
    for n in range(1,maxPage+1):
        artice = get_result(n)
        getArticeinfo(artice)
        if n >2:
            break
if __name__ == '__main__':
    main(1)
