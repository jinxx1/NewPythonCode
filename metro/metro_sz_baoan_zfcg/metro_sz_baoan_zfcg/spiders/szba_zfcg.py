# -*- coding: utf-8 -*-
import scrapy,re,datetime,csv
ttime = str(datetime.datetime.now()).replace(':','_').replace('.','_').replace(' ','---')
pathName = "C:\\PthonCode\\"
if pathName:
    fileName = pathName + ttime + '.csv'
else:
    fileName = ttime + '.csv'

add_info = ['一级分类','二级分类','三级分类','电商()','电商','数量','路径']
csvFile = open(fileName, "a", newline='')
writer = csv.writer(csvFile)
writer.writerow(add_info)
csvFile.close()

class SzbaZfcgSpider(scrapy.Spider):
    name = 'szba_zfcg'
    allowed_domains = ['183.62.155.68']

    listUrl = [{'l0': '强制节能', 'l1': '大家电', 'l2': '空调机', 'url': 'http://183.62.155.68/channel/402'},
               {'l0': '强制节能', 'l1': '大家电', 'l2': '电视机', 'url': 'http://183.62.155.68/channel/405'},
               {'l0': '强制节能', 'l1': '计算机', 'l2': '台式计算机', 'url': 'http://183.62.155.68/channel/187'},
               {'l0': '强制节能', 'l1': '计算机', 'l2': '一体机', 'url': 'http://183.62.155.68/channel/188'},
               {'l0': '强制节能', 'l1': '计算机', 'l2': '便携式计算机', 'url': 'http://183.62.155.68/channel/189'},
               {'l0': '强制节能', 'l1': '计算机', 'l2': '平板电脑', 'url': 'http://183.62.155.68/channel/190'},
               {'l0': '强制节能', 'l1': '打印机', 'l2': '普通激光打印机', 'url': 'http://183.62.155.68/channel/191'},
               {'l0': '强制节能', 'l1': '打印机', 'l2': '工作组激光打印机', 'url': 'http://183.62.155.68/channel/324'},
               {'l0': '强制节能', 'l1': '打印机', 'l2': '多功能一体机', 'url': 'http://183.62.155.68/channel/110'},
               {'l0': '强制节能', 'l1': '打印机', 'l2': '针式打印机', 'url': 'http://183.62.155.68/channel/192'},
               {'l0': '电脑办公', 'l1': '计算机', 'l2': '台式计算机', 'url': 'http://183.62.155.68/channel/187'},
               {'l0': '电脑办公', 'l1': '计算机', 'l2': '一体机', 'url': 'http://183.62.155.68/channel/188'},
               {'l0': '电脑办公', 'l1': '计算机', 'l2': '便携式计算机', 'url': 'http://183.62.155.68/channel/189'},
               {'l0': '电脑办公', 'l1': '计算机', 'l2': '平板电脑', 'url': 'http://183.62.155.68/channel/190'},
               {'l0': '电脑办公', 'l1': '打印机', 'l2': '普通激光打印机', 'url': 'http://183.62.155.68/channel/191'},
               {'l0': '电脑办公', 'l1': '打印机', 'l2': '工作组激光打印机', 'url': 'http://183.62.155.68/channel/324'},
               {'l0': '电脑办公', 'l1': '打印机', 'l2': '多功能一体机', 'url': 'http://183.62.155.68/channel/110'},
               {'l0': '电脑办公', 'l1': '打印机', 'l2': '针式打印机', 'url': 'http://183.62.155.68/channel/192'},
               {'l0': '电脑办公', 'l1': '打印机', 'l2': '彩色喷墨打印机', 'url': 'http://183.62.155.68/channel/178'},
               {'l0': '电脑办公', 'l1': '打印机', 'l2': '一般喷墨打印机', 'url': 'http://183.62.155.68/channel/185'},
               {'l0': '电脑办公', 'l1': '办公设备', 'l2': '传真机', 'url': 'http://183.62.155.68/channel/335'},
               {'l0': '电脑办公', 'l1': '办公设备', 'l2': '扫描仪', 'url': 'http://183.62.155.68/channel/336'},
               {'l0': '电脑办公', 'l1': '办公设备', 'l2': '碎纸机', 'url': 'http://183.62.155.68/channel/337'},
               {'l0': '电脑办公', 'l1': '办公设备', 'l2': '模拟复印机', 'url': 'http://183.62.155.68/channel/334'},
               {'l0': '电脑办公', 'l1': '办公设备', 'l2': '中高速数码复印机', 'url': 'http://183.62.155.68/channel/333'},
               {'l0': '电脑办公', 'l1': '办公设备', 'l2': '速印机', 'url': 'http://183.62.155.68/channel/338'},
               {'l0': '电脑办公', 'l1': '办公设备', 'l2': '投影机', 'url': 'http://183.62.155.68/channel/339'},
               {'l0': '电脑办公', 'l1': '办公设备', 'l2': '投影幕', 'url': 'http://183.62.155.68/channel/340'},
               {'l0': '电脑办公', 'l1': '网络设备', 'l2': '投影机配件', 'url': 'http://183.62.155.68/channel/1010'},
               {'l0': '电脑办公', 'l1': '网络设备', 'l2': '服务器', 'url': 'http://183.62.155.68/channel/354'},
               {'l0': '电脑办公', 'l1': '网络设备', 'l2': '路由器', 'url': 'http://183.62.155.68/channel/356'},
               {'l0': '电脑办公', 'l1': '网络设备', 'l2': '交换机', 'url': 'http://183.62.155.68/channel/357'},
               {'l0': '电脑办公', 'l1': '网络设备', 'l2': '防火墙', 'url': 'http://183.62.155.68/channel/359'},
               {'l0': '电脑办公', 'l1': '计算机外设', 'l2': '不间断电源', 'url': 'http://183.62.155.68/channel/395'},
               {'l0': '电脑办公', 'l1': '计算机外设', 'l2': '空调机', 'url': 'http://183.62.155.68/channel/402'},
               {'l0': '电脑办公', 'l1': '计算机外设', 'l2': '空调配件', 'url': 'http://183.62.155.68/channel/403'},
               {'l0': '电脑办公', 'l1': '计算机外设', 'l2': '空调服务', 'url': 'http://183.62.155.68/channel/404'},
               {'l0': '电脑办公', 'l1': '计算机外设', 'l2': '电视机', 'url': 'http://183.62.155.68/channel/405'},
               {'l0': '电脑办公', 'l1': '计算机外设', 'l2': '电视配件', 'url': 'http://183.62.155.68/channel/320'},
               {'l0': '家用电器', 'l1': '大家电', 'l2': '电视服务', 'url': 'http://183.62.155.68/channel/898'},
               {'l0': '办公用品', 'l1': '办公用纸', 'l2': '复印纸', 'url': 'http://183.62.155.68/channel/123'},
               {'l0': '办公用品', 'l1': '办公用纸', 'l2': '打印纸', 'url': 'http://183.62.155.68/channel/147'},
               {'l0': '办公用品', 'l1': '办公用纸', 'l2': '传真纸', 'url': 'http://183.62.155.68/channel/203'},
               {'l0': '数码通讯', 'l1': '摄影器材', 'l2': '数码照相机', 'url': 'http://183.62.155.68/channel/532'},
               {'l0': '数码通讯', 'l1': '摄影器材', 'l2': '单反相机', 'url': 'http://183.62.155.68/channel/535'},
               {'l0': '数码通讯', 'l1': '摄影器材', 'l2': '运动相机', 'url': 'http://183.62.155.68/channel/536'},
               {'l0': '数码通讯', 'l1': '摄像器材', 'l2': '运动摄像机', 'url': 'http://183.62.155.68/channel/534'},
               {'l0': '数码通讯', 'l1': '摄像器材', 'l2': '数码摄像机', 'url': 'http://183.62.155.68/channel/533'},
               {'l0': '食品生鲜', 'l1': '饮料冲调', 'l2': '饮用水', 'url': 'http://183.62.155.68/channel/830'}]


    def start_requests(self):
        meta = {}
        for i in self.listUrl:
            meta['l0'] = i['l0']
            meta['l1'] = i['l1']
            meta['l2'] = i['l2']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'],callback=self.parse, meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        listWord = response.xpath("//div[@id='filter']/div[@class='filterminlist bbottom']/dl[3]/dd[@class='w130']/a/text()").extract()

        for nn in listWord:
            try:
                meta['Name'] = nn
                try:
                    meta['NumGet'] = re.findall("\((\d{1,10})\)", nn)[0]
                except IndexError:
                    meta['NumGet'] = 0
            except:
                meta['Name'] = '当前页面无数据'
                meta['NumGet'] = '当前页面无数据'
            cutName = '(' + meta['NumGet'] +  ')'
            meta['Name2'] = meta['Name'].replace(cutName,'')
            add_info = [meta['l0'], meta['l1'], meta['l2'], meta['Name'],meta['Name2'],meta['NumGet'],meta['url']]
            csvFile = open(fileName, "a",newline='')
            writer = csv.writer(csvFile)
            writer.writerow(add_info)
            csvFile.close()