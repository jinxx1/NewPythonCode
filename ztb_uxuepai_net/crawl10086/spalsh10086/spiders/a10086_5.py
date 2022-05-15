# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json,pprint,re
from bs4 import BeautifulSoup
from spalsh10086.scrapyParse import *
from spalsh10086.items import Spalsh10086Item
from spalsh10086.mysql_processing import *




class A100862Spider(scrapy.Spider):
    name = '10086_5'
    allowed_domains = ['b2b.10086.cn']
    siteName = '移动'
    subclass = '单一来源信息公告'
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

        splash:select('a[id=danyi]'):mouse_click()
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

    def start_requests(self):
        yield SplashRequest(url=self.start_urls[0],
                            endpoint="execute",
                            args={
                                "wait": 120,
                                "lua_source": self.lua_script,
                                "pageNum": str(1)
                            },
                            callback=self.parse,
                            )

    def parse(self, response):
        get_pageNum = int(response.data['get_pageNum'])
        if get_pageNum ==10:
            return None
        print('-----------------------------------------------------------------------', get_pageNum)
        try:
            article_info = get_IDandTIME(response.data['html'])
        except:
            print('no List html')

        print(article_info[0])
        noList = depcut(article_info)
        print('第{}页，共有{}篇文章未录入'.format(get_pageNum, len(noList)))



        if not noList:
            return None
        else:
            article_lua_script = '''
            function main(splash, args)
                splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
                splash:init_cookies(args.scookies)
                assert(splash:go(args.url))
                assert(splash:wait(3))
            return {
                html = splash:html(),
                ttime = args.ttime,
                get_pageNum = args.pageNum
                  }
            end
            '''
            for n in noList:
                yield SplashRequest(url=n['url'],
                                    endpoint="execute",
                                    args={
                                        "wait": 120,
                                        "lua_source": article_lua_script,
                                        "scookies": response.data['cookies'],
                                        "ttime": n['time'],
                                        "pageNum": str(get_pageNum),
                                    },
                                    callback=self.parseA,
                                    )


        if len(noList) < len(article_info):
            return None
        get_pageNum += 1
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

            splash:select('a[id=danyi]'):mouse_click()
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
