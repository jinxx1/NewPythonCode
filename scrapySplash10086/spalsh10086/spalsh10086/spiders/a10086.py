# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json,pprint,re
from bs4 import BeautifulSoup
from spalsh10086.scrapyParse import *
from spalsh10086.items import Spalsh10086Item
from spalsh10086.mysql_processing import *

class A10086Spider(scrapy.Spider):
    name = '10086_1'
    allowed_domains = ['b2b.10086.cn']
    siteName = '移动'
    subclass = '采购公告'
    start_urls = ['https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2']
    lua_script = '''
    function main(splash, args)
        function focus(sel)
            splash:select(sel):focus()
        end
        splash.images_enabled = false
        splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
        assert(splash:go(args.url))
        assert(splash:wait(3))
        
        splash:select('a[id=caigou]'):mouse_click()
        assert(splash:wait(3))

        focus('input[id=pageNumber]')
        splash:send_text(args.pageNum)
        assert(splash:wait(3))
        splash:select('input[value=GO]'):mouse_click()
        assert(splash:wait(5))
        return {
            html = splash:html(),
            cookies = splash:get_cookies(),
            get_pageNum = args.pageNum
            }
        end
    '''

    def __init__(self, goon=None, spiderName=None,*args, **kwargs):
        super(A10086Spider, self).__init__(*args, **kwargs)
        self.goon = goon
        self.spiderName = spiderName

    def start_requests(self):
        NUM = 1
        with open(self.name + '.txt','w') as f:
            f.write(str(NUM))
            f.flush()
            f.close()
        yield SplashRequest(url=self.start_urls[0],
                            endpoint="execute",
                            args={
                                "wait": 120,
                                "lua_source": self.lua_script,
                                "pageNum": str(NUM)
                            },
                            callback=self.parse,
                            )

    def parse(self,response):
        try:
            article_info = get_IDandTIME(response.data['html'])
            get_pageNum = int(response.data['get_pageNum'])
            print('-----------------------------------------------------------------------', get_pageNum)
        except:
            print('                warning:没有获取到data【html】或【pageNum】      ')
            with open(self.name + '.txt','r') as f:
                get_pageNum = f.read()
                f.close()
            yield SplashRequest(url=self.start_urls[0],
                                endpoint="execute",
                                args={
                                    "wait": 120,
                                    "lua_source": self.lua_script,
                                    "pageNum": str(get_pageNum)
                                },
                                callback=self.parse,
                                )

        noList = depcut(article_info)
        print('第{}页，共有{}篇文章未录入'.format(get_pageNum, len(noList)))

        if not noList and self.goon == 'no':
            return None
        else:
            pandas_insermysql(noList,self.subclass)

        get_pageNum += 1
        with open(self.name + '.txt','w') as f:
            f.write(str(get_pageNum))
            f.flush()
            f.close()
        lua_script1 = '''
        function main(splash, args)
            function focus(sel)
                splash:select(sel):focus()
            end
            splash.images_enabled = false
            splash:init_cookies(args.scookies)
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
            assert(splash:go(args.url))
            assert(splash:wait(3))

            focus('input[id=pageNumber]')
            splash:send_text(args.pageNum)
            assert(splash:wait(3))
            splash:select('input[value=GO]'):mouse_click()
            assert(splash:wait(5))
            return {
                html = splash:html(),
                cookies = splash:get_cookies(),
                get_pageNum = args.pageNum
                }
            end
        '''

        yield SplashRequest(url=self.start_urls[0],
                            endpoint="execute",
                            args={
                                "wait": 120,
                                "lua_source": lua_script1,
                                "pageNum": str(get_pageNum),
                                "scookies": response.data['cookies'],
                            },
                            callback=self.parse,
                            )

    def parseA(self, response):
        item = Spalsh10086Item()
        ddict = get_content(response.text)
        get_pageNum = response.data['get_pageNum']
        if response.status != 200 or not ddict:
            yield SplashRequest(url=self.start_urls[0],
                                endpoint="execute",
                                args={
                                    "wait": 120,
                                    "lua_source": self.lua_script,
                                    "pageNum": get_pageNum
                                },
                                callback=self.parse,
                                )
            return None
        item['get_pageNum'] = response.data['get_pageNum']
        item['issueTime'] = get_timestr(response.data['ttime'], outformat="%Y-%m-%d %H:%M:%S")
        item['url'] = response.url
        item['site'] = self.allowed_domains[0]
        item['subclass'] = self.subclass
        item['title'] = ddict['title']
        item['content'] = ddict['content']

        yield item



