# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json,pprint,re
from bs4 import BeautifulSoup
from spalsh10086.scrapyParse import *
from spalsh10086.items import Spalsh10086Item
from spalsh10086.mysql_processing import *
from dateutil.relativedelta import relativedelta

today_get = datetime.datetime.today()
yesterday_get = today_get - relativedelta(days=1)
yesterday_get = yesterday_get.strftime("%Y-%m-%d")

catName = {
    'caigou':{'id':'caigou',
              'subclass':'采购公告'},
    'zige': {'id': 'zige',
               'subclass': '资格预审公告'},
    'jieguo': {'id': 'jieguo',
               'subclass': '候选人公示'},
    'zhongxuan': {'id': 'zhongxuan',
               'subclass': '中选结果公示'},
    'danyi': {'id': 'danyi',
               'subclass': '单一来源采购信息公告'},
}
class FROMTIME10086Spider(scrapy.Spider):
    name = 'fromTime10086'
    allowed_domains = ['b2b.10086.cn']
    siteName = '移动'
    start_urls = ['https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2']
    lua_script_base = '''
    function main(splash, args)
        function focus(sel)
            splash:select(sel):focus()
        end
        splash.resource_timeout = 20
        splash.images_enabled = false
        splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
        assert(splash:go(args.url))
        assert(splash:wait(3))

        splash:select('a[id=jinxiao123456]'):mouse_click()
        assert(splash:wait(3))

        focus('input[id=pageNumber]')
        splash:send_text(args.pageNum)
        assert(splash:wait(3))

        splash:select('input[value=GO]'):mouse_click()
        assert(splash:wait(5))

        return {
            html = splash:html(),
            get_pageNum = args.pageNum
            }
    end'''

    def __init__(self, goon=None, spiderName=None, *args, **kwargs):
        super(FROMTIME10086Spider, self).__init__(*args, **kwargs)
        self.goon = goon
        self.spiderName = spiderName
        self.lua_script = self.lua_script_base.replace('jinxiao123456', catName[spiderName]['id'])
        self.subclass = catName[spiderName]['subclass']


    def start_requests(self):
        NUM = 1
        yield SplashRequest(url=self.start_urls[0],
                            endpoint="execute",
                            args={
                                "wait": 120,
                                # "timeout":3600,
                                # "resource_timeout": 20,
                                "lua_source": self.lua_script,
                                "pageNum": str(NUM)
                            },
                            callback=self.parse,
                            )

    def parse(self, response):
        # //tr[ @ onmouseout = "cursorOut(this)"]/@onclick
        article_info = get_IDandTIME(response.data['html'])
        get_pageNum = int(response.data['get_pageNum'])
        # --------按时间顺序收录文章--开始
        timeMark = 0
        llist = []
        print(yesterday_get)
        for i in article_info:
            if i['time'] != yesterday_get:
                print(i['time'])
                timeMark += 1
                continue
            else:
                llist.append(i)   
        print('《{}》中,第{}页，共有{}篇文章未录入---时间排序的文章'.format(self.subclass, get_pageNum, len(llist)))
        # pandas_insermysql_copy(llist,self.subclass)
        
        # --------按时间顺序收录文章--结束
        
        #---若有未被收录的文章，录到录入库
        # noList_depcutfromMySql = depcut(article_info)
        # print('《{}》中,第{}页，共有{}篇文章未录入---时间排序的文章---剩下的文章'.format(self.subclass, get_pageNum, len(noList_depcutfromMySql)))
        # pandas_insermysql(noList_depcutfromMySql,self.subclass)
        #---若有未被收录的文章，录到录入库

        if timeMark == 20:
            return None
        else:
            get_pageNum += 1
            yield SplashRequest(url=self.start_urls[0],
                            endpoint="execute",
                            args={
                                "wait": 120,
                                # "timeout": 3600,
                                # "resource_timeout": 20,
                                "lua_source": self.lua_script,
                                "pageNum": str(get_pageNum),
                            },
                            callback=self.parse,
                            )