# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from scrapy.http.cookies import CookieJar
from NEW_GGZY.Pimg import fujianWord
cookie_jar = CookieJar()

HEA={
'Accept':'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Connection':'keep-alive',
'Host':'www.ccgp-fujian.gov.cn',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
     }

imgHEA = {

'Accept':'image/webp,*/*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Connection':'keep-alive',
'Host':'www.ccgp-fujian.gov.cn',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'


}

class CcgpFujianSpider(scrapy.Spider):
    name = 'ccgp_fujian'
    allowed_domains = ['www.ccgp-fujian.gov.cn']
    start_urls = ['http://www.ccgp-fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/?page={}']
    imgCodeUrl = 'http://www.ccgp-fujian.gov.cn/noticeverifycode/?1'

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for i in self.start_urls:
            meta['cishu'] = 1
            meta['url'] = i.format(str(meta['Num']))
            yield scrapy.Request(url=meta['url'],callback=self.parse, meta=meta,dont_filter=True,headers=HEA)
            yield scrapy.Request(url=self.imgCodeUrl,callback=self.parse, meta=meta,dont_filter=True,headers=imgHEA)

    def parse(self, response):
        meta = response.meta

        cookie_jar.extract_cookies(response, response.request)

        meta['cookiejar'] = cookie_jar

        csrf = response.xpath("//input[@name = 'csrfmiddlewaretoken']/@value").extract_first()

        for c in cookie_jar:
            cookies = re.findall("Cookie (.*?) for", str(c))
            cookies1 = (cookie.split('=', 1) for cookie in cookies)
            scrapy_cookies = dict(cookies1)
            break

        if '验证码' in response.text:
            print('验证码')
            while True:
                meta['cishu'] += 1
                yzma = fujianWord(Referer=response.url,cooikes=cookies[0],cishu=meta['cishu'])
                if not yzma:
                    meta['cishu'] += 1
                    continue
                else:
                    break

            notlist = re.findall("noticelist/(.*?)/\?page=",meta['url'])[0]
            tempUrl = 'http://www.ccgp-fujian.gov.cn/3500/noticelist/{notlist}/?csrfmiddlewaretoken={token}&zone_code=&zone_name=&croporgan_name=&project_no=&fromtime=&endtime=&gpmethod=&agency_name=&title=&notice_type=&open_type=&verifycode={yzma}'
            yzUrl = tempUrl.format(notlist=notlist,token=csrf,yzma=yzma)
            HEA['Referer'] = response.url
            HEA['Upgrade-Insecure-Requests'] = '1'

            yield scrapy.Request(url=yzUrl,callback=self.parse, meta=meta,dont_filter=True,headers=HEA,cookies=scrapy_cookies)


        elif '你访问的页面不存在' in response.text:
            print('不存在')

            while True:
                meta['cishu'] += 1
                yzma = fujianWord(Referer=response.url,cooikes=cookies[0],cishu=meta['cishu'])
                if not yzma:
                    meta['cishu'] += 1
                    continue
                else:
                    break
            notlist = re.findall("noticelist/(.*?)/\?page=",meta['url'])[0]
            tempUrl = 'http://www.ccgp-fujian.gov.cn/3500/noticelist/{notlist}/?csrfmiddlewaretoken={token}&zone_code=&zone_name=&croporgan_name=&project_no=&fromtime=&endtime=&gpmethod=&agency_name=&title=&notice_type=&open_type=&verifycode={yzma}'
            yzUrl = tempUrl.format(notlist=notlist,token=csrf,yzma=yzma)
            HEA['Referer'] = response.url
            HEA['Upgrade-Insecure-Requests'] = '1'
            yield scrapy.Request(url=yzUrl,callback=self.parse, meta=meta,dont_filter=True,headers=HEA,cookies=scrapy_cookies)


        else:
            a = response.xpath("/html/body/div[2]/div/div/div[3]/div[2]/table/tbody/tr/td/a/text()").extract()
            print(a)
            print(response.text)
