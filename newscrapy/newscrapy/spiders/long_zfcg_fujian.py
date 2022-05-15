# -*- coding: utf-8 -*-
import scrapy

from newscrapy.scrapyParse import *
from newscrapy.items import NewscrapyItem
from urllib import parse
import lxml.html
from newscrapy.api_png import *
import json, os


pathabs = os.path.abspath('.')
if 'spiders' in pathabs:
    pathabs = os.path.abspath('..')
pathabs = pathabs.replace('\\', '/')

jar_pool_file = pathabs + '/zfcg_fujian_jar.json'
pageNumFile = pathabs + '/zfcg_fujian_allpage.json'


def get_listulr():
    brow = requests.get('http://www.ccgp-fujian.gov.cn/index.html')
    resp = lxml.html.fromstring(brow.text.encode(brow.encoding))
    xpathget = resp.xpath("//div[@class='section section4']/div[@class='head']/a/@href")
    link = 'http://www.ccgp-fujian.gov.cn' + ''.join(xpathget)
    return link
def loadjar():
    try:
        jar = jsonload(jar_pool_file)
    except:
        return None, None

    listulr = get_listulr()
    return jar, listulr + "?page=1"

    # info = {
    #     'scrapy_jar':scrapy_jar,
    #     'csrfmiddlewaretoken':csrfmiddlewaretoken,
    #     'cover_pic_path':cover_pic_path,
    #     'savePath':savePath
    # }

def crash():
    listurl = get_listulr()
    info = get_cookies_by_headlessChrome_for_zfcgfujian(listurl,pathabs)
    result_lianzhong = img_main(file_name=info['cover_pic_path'], yzm_min='4', yzm_max='4', yzm_type='1105', tools_token='',
                                savePath=info['savePath'])
    code = json.loads(result_lianzhong)
    print('扫码平台返回的信息',code)
    orgurl = "{url}?csrfmiddlewaretoken={csrfmiddlewaretoken}&zone_code=&zone_name=&croporgan_name=&project_no=&fromtime=&endtime=&gpmethod=&agency_name=&title=&notice_type=&open_type=&verifycode={verifycode}"
    geturl = orgurl.format(url=listurl,
                           csrfmiddlewaretoken=info['csrfmiddlewaretoken'],
                           verifycode=code['data']['val'])
    with open(jar_pool_file, 'w', encoding='utf-8')as fi:
        json.dump(info['scrapy_jar'], fp=fi, ensure_ascii=False)
    return info['scrapy_jar'], geturl


# if __name__ == '__main__':
#     path1 = os.path.abspath('.')
#     print(path1)
#     if 'spider' in path1:
#         path1 = os.path.abspath('..')
#     print(path1)
#
#     exit()


class LongZfcgFujianSpider(scrapy.Spider):
    name = 'long_zfcg_fujian'
    allowed_domains = ['ccgp-fujian.gov.cn']
    mysql_allurl = get_mysql_allurl(allowed_domains[0])

    def __init__(self):
        print('开始读取本地存储的jar文件')
        self.scrapy_jar, self.listurl = loadjar()
        if not self.scrapy_jar:
            print('jar文件打开错误，开启打码')
            self.scrapy_jar, self.listurl = crash()
        else:
            print('jar文件打开成功，开始爬取第一页')

    def start_requests(self):
        meta = {}
        meta['pageNum'] = 1

        yield scrapy.Request(url=self.listurl, callback=self.parse,
                             cookies=self.scrapy_jar, dont_filter=True, meta=meta)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//tr[@class='gradeX']/td/a/@href").extract()
        if len(link) == 0 and 'noticeverifycode/?' in response.text:
            print('发现验证码，在parse。开始执行打码活动')
            self.scrapy_jar, self.listurl = crash()
            yield scrapy.Request(url=self.listurl, callback=self.parse,
                                 cookies=self.scrapy_jar, dont_filter=True, meta=meta)

        else:
            print('在parse。抓到本页所有文章链接。')
            geturl = self.listurl.split('?')[0] + "?page={}"
            # for nn in range(1,20):
            #
            #     meta['pageNum'] = nn
            #     url = geturl.format(str(meta['pageNum']))
            #     print('抓取其他List页开始')
            #     yield scrapy.Request(url=url, callback=self.parseA,
            #                  cookies=self.scrapy_jar, meta=meta)

            list_100 = []
            for urlnum in range(2,34764):
                list_100.append(urlnum)
                if len(list_100) == 100:
                    print('抓取list第一页开始')
                    meta['pageNum'] = 1
                    url = geturl.format(str(meta['pageNum']))
                    yield scrapy.Request(url=url, callback=self.parseA,
                                     cookies=self.scrapy_jar, dont_filter=True, meta=meta)

                    for nn in list_100:
                        meta['pageNum'] = nn
                        url = geturl.format(str(meta['pageNum']))
                        print('抓取其他List页开始')
                        yield scrapy.Request(url=url, callback=self.parseA,
                                     cookies=self.scrapy_jar, meta=meta)
                    list_100 = []

    def parseA(self, response):
        meta = response.meta
        link = response.xpath("//tr[@class='gradeX']/td/a/@href").extract()
        if len(link) == 0 and 'noticeverifycode/?' in response.text:
            print('发现验证码，在parseA。停止本爬虫。所在页面：',meta['pageNum'])
            return None
        if not link:
            print('第{}页没有任何链接'.format(meta['pageNum']))
            return None

        notLink = []
        for uurl in link:
            weblink = parse.urljoin(response.url,uurl)
            if weblink in self.mysql_allurl:
                continue
            notLink.append(uurl)
        print('第{}页，去重后的链接个数为：{}'.format(meta['pageNum'],len(notLink)))
        if len(notLink) == 0:
            return None

        for num, webUrl in enumerate(notLink):
            title = ''.join(cleanList(response.xpath("//*[@href = '{}']/text()".format(webUrl)).extract()))
            if not title:
                continue
            area = ''.join(cleanList(response.xpath("//*[@href = '{}']/../../td[1]/text()".format(webUrl)).extract()))
            type = ''.join(cleanList(response.xpath("//*[@href = '{}']/../../td[2]/text()".format(webUrl)).extract()))
            TTILE = cleanList([area, type])
            meta['title'] = title
            meta['subclass'] = '_'.join(TTILE)

            ttime = ''.join(cleanList(response.xpath("//*[@href = '{}']/../../td[5]/text()".format(webUrl)).extract()))
            meta['issueTime'] = get_timestr(''.join(ttime))
            meta['contentNum'] = num
            meta['url'] = parse.urljoin(response.url, webUrl)
            yield scrapy.Request(url=meta['url'], callback=self.parse_content,
                                 cookies=self.scrapy_jar, meta=meta)

    def parse_content(self, response):
        meta = response.meta
        print('进入第{}页，第{}篇'.format(meta['pageNum'],meta['contentNum']))
        if 'noticeverifycode/?' in response.text:
            print('发现验证码，在content。停止本爬虫。所在页面：',meta['pageNum'],meta['contentNum'])
            return None
        item = NewscrapyItem()
        item['content'] = response.xpath("//div[@class = 'notice-con']").extract_first()
        if not item['content']:
            print('进入第{}页，文章{}篇没有查看到正文'.format(meta['pageNum'], meta['contentNum']))
            return None

        attch_link = cleanList(response.xpath("//div[@class='notice-foot']/a/@href").extract())
        if attch_link:
            attachmentListJson = []
            for atturl in attch_link:
                ddict = {}
                ddict['downloadUrl'] = parse.urljoin(response.url, atturl)
                try:
                    houzhui = ddict['downloadUrl'].split('.')[-1]
                except:
                    houzhui = 'nosuffix'.replace('uffix','')

                attName = response.xpath("//*[@href = '{}']/text()".format(atturl)).extract_first().strip()

                if not attName:
                    attName = 'noName'

                ddict['name'] = attName + "." + houzhui
                attachmentListJson.append(ddict)

            item['attachmentListJson'] = json.dumps(attachmentListJson, ensure_ascii=False)

        ttime = ''.join(cleanList(response.xpath("//div[@class='clearfix']/span/text()").extract()))
        getime = ttime.split('间：')[-1].split()
        item['issueTime'] = get_timestr(getime)
        if not item['issueTime']:
            item['issueTime'] = meta['issueTime']
        if not item['issueTime']:
            item['issueTime'] = '1999-01-01 00:00:00'

        item['pageNum'] = meta['pageNum']
        item['contentNum'] = meta['contentNum']
        item['site'] = self.allowed_domains[0]
        item['title'] = meta['title']
        item['subclass'] = meta['subclass']
        item['url'] = meta['url']


        yield item
