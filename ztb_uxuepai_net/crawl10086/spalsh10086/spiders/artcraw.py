# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json,pprint,re
from bs4 import BeautifulSoup
from spalsh10086.scrapyParse import *
from spalsh10086.items import Spalsh10086Item
from spalsh10086.mysql_processing import *
from spalsh10086.settings import MYSQLINFO
import sqlalchemy

conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO[
                                                                                               'DBNAME'])
mysqlcon = sqlalchemy.create_engine(conStr)

class A100862Spider(scrapy.Spider):
    name = 'artcraw'
    allowed_domains = ['b2b.10086.cn']
    siteName = '移动'
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
        try:
            article_info = get_IDandTIME(response.data['html'])
        except:
            print('no List html')

        print(article_info[0])

        ddict = mysqlcon.execute("select id,page_url,subclass,issue_time from temp10086url where process_status = 0")
        for i in ddict:
            art_id = str(i[0])
            art_url = i[1]
            art_sub = i[2]
            art_time = str(i[3])


            article_lua_script = '''
            function main(splash, args)
                splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
                splash:init_cookies(args.scookies)
                assert(splash:go(args.url))
                assert(splash:wait(3))
            return {
                html = splash:html(),
                art_time = args.art_time,
                art_id = args.art_id,
                art_sub = args.art_sub,
                  }
            end
            '''

            yield SplashRequest(url=art_url,
                                endpoint="execute",
                                args={
                                    "wait": 120,
                                    "lua_source": article_lua_script,
                                    "scookies": response.data['cookies'],
                                    "art_time": art_time,
                                    "art_id": art_id,
                                    "art_sub":art_sub,

                                },
                                callback=self.parseA,
                                )


    def parseA(self, response):


        if response.status != 200:
            import random
            art_pageNum = random.randint(2,70)

            yield SplashRequest(url=self.start_urls[0],
                                endpoint="execute",
                                args={
                                    "wait": 120,
                                    "lua_source": self.lua_script,
                                    "pageNum": str(art_pageNum)
                                },
                                callback=self.parse,
                                )
            # print('cookie失效关闭爬虫88888888888888888888888888888888888888')
            # self.crawler.engine.close_spider(self, 'cookie失效关闭爬虫')
            return None

        art_time = response.data['art_time']
        art_id = response.data['art_id']
        art_sub = response.data['art_sub']
        ddict = get_content(response.text)

        ddict['issueTime'] = get_timestr(art_time, outformat="%Y-%m-%d %H:%M:%S")
        ddict['url'] = response.url
        ddict['site'] = self.allowed_domains[0]
        ddict['subclass'] = art_sub
        a = save_api(ddict)

        if a['msg'] == 'success' or a['msg'] == '该链接已经存在了':
            mysql_update = "UPDATE temp10086url SET process_status=1 where id ={}".format(art_id)
            mysqlcon.execute(mysql_update)
            print('{}----录入结束'.format(ddict['title']))
        else:
            return None

