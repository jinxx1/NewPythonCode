# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json,pprint,re
from bs4 import BeautifulSoup
from spalsh10086.scrapyParse import *


class T10086Spider(scrapy.Spider):
    name = 't10086'
    allowed_domains = ['b2b.10086.cn']
    siteName = '移动'
    start_urls = ['https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2']

    def start_requests(self):

        lua_script = '''
        function main(splash, args)
            function focus(sel)
                splash:select(sel):focus()
            end
            splash.images_enabled = false
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
            assert(splash:go(args.url))
            assert(splash:wait(3))

            splash:select('a[id=zige]'):mouse_click()
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
                                "lua_source":lua_script,
                                "pageNum":str(1)
                            },
                            callback=self.parse,
                            )

    def parse(self, response):
        get_pageNum = int(response.data['get_pageNum'])
        # if get_pageNum == 3:
        #     return None

        print('-----------------------------------------------------------------------',get_pageNum)

        try:
            article_info = get_IDandTIME(response.data['html'])
        except:
            print('no List html')

        print(article_info[0])
        noList = depcut(article_info)
        print('第{}页，共有{}篇文章未录入'.format(get_pageNum,len(noList)))
        # return None

        article_lua_script = '''
        function main(splash, args)
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
            splash:init_cookies(args.scookies)
            assert(splash:go(args.url))
            assert(splash:wait(3))
        return {
            html = splash:html(),
            ttime = args.ttime
              }
        end
        '''

        if not noList:
            pass
            # return None
        else:
            for n in noList:
                yield SplashRequest(url=n['url'],
                                    endpoint="execute",
                                    args={
                                        "wait": 120,
                                        "lua_source": article_lua_script,
                                        "scookies": response.data['cookies'],
                                        "ttime":n['time']
                                    },
                                    callback=self.parseA,
                                    )


        get_pageNum+=1
        lua_script1 = '''
        function main(splash, args)
            function focus(sel)
                splash:select(sel):focus()
            end
            splash.images_enabled = false
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
            assert(splash:go(args.url))
            assert(splash:wait(3))
            
            splash:select('a[id=zige]'):mouse_click()
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
                                "pageNum": str(get_pageNum)
                            },
                            callback=self.parse,
                            )

    def parseA(self, response):
        ddict = get_content(response.text)
        if not ddict:
            print('--------')
            print(response.url)
            print('no html')
            file = r'fID.txt'
            with open(file, 'a+') as f:
                f.write(response.url + '\n')
            print('--------')


            return None
        ddict['issueTime'] = get_timestr(response.data['ttime'],outformat="%Y-%m-%d %H:%M:%S")
        ddict['url'] = response.url
        ddict['site'] = self.allowed_domains[0]
        ddict['subclass'] = '资格预审公告'

        a = save_api(ddict)
        ddict['content'] = len(ddict['content'])
        pprint.pprint(ddict)
        print(a)
        print('------------------------')
