# -*- coding: utf-8 -*-
import scrapy


class CuSpider(scrapy.Spider):
    name = 'cu'
    allowed_domains = ['www.chinaunicombidding.cn']
    st_urls = [{'url':'http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?page=1'}]
    # start_urls = 'http://www.chinaunicombidding.cn/jsp/cnceb/web/index_parent.jsp'
    start_urls = 'http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?type=1&page=1'


    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        # PostDate = {
        #     'type': '1'
        # }
        yield scrapy.Request(url=self.start_urls,callback=self.parse,meta=meta)
        # for i in self.start_urls:
        #     meta['url'] = i['url']

            # yield scrapy.FormRequest(url=meta['url'], callback=self.parse,
            #                      dont_filter=True,
            #                      formdata=PostDate,meta=meta
            #                      )


    def parse(self, response):
        print(response.text)
        print(response.status)

