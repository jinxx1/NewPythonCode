# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/6
# import requests
# import urllib3
# import json
#
# urllib3.disable_warnings()
# rq_headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Cookie': 'user=null; JSESSIONID=SIOw0s_lE3WROPEeBFLTl90_raWApGB5A23BB5NZOzKKlPotYc6m!-1203063273',
#     'Host': 'www.szjsjy.com.cn:8001',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'none',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1'
# }
# rs_headers = {
#                 'Accept': 'application/json, text/javascript, */*',
#                 'Accept-Encoding': 'gzip, deflate, br',
#                 'Accept-Language': 'zh-CN,zh;q=0.9',
#                 'Connection': 'keep-alive',
#                 'Content-Type': 'application/json',
#                 'Host': 'www.szjsjy.com.cn:8001',
#                 'Origin': 'https://www.szjsjy.com.cn:8001'
#             }
# r = requests.get('https://www.szjsjy.com.cn:8001/jyw/queryGongGaoList.do?rows=10&page=1',headers=rq_headers,verify=False )
#
# res_str = r.text
# res_obj = res_str[16:-1]
# for row in json.loads(res_obj)['rows']:
#     print(row)
#     detail_link = 'https://www.szjsjy.com.cn:8001/jyw/showGongGao.do?ggGuid=%s&gcbh=&bdbhs='%row['ggGuid']
#     print(detail_link)
#     u = 'https://www.szjsjy.com.cn:8001/jyw/showGongGao.do?ggGuid=2c9e8ac275740a84017596480ca72fd3&gcbh=&bdbhs='
#     q = 'https://www.szjsjy.com.cn:8001/jyw/showGongGao.do?ggGuid=2c9e8ac275ad55240175afdbb09601b0&gcbh=&bdbhs='
#     w = 'https://www.szjsjy.com.cn:8001/jyw/showGongGao.do?ggGuid=2c9e8ac275740a8401758dc6c08523f3&gcbh=&bdbhs='
#     e = 'https://www.szjsjy.com.cn:8001/jyw/showGongGao.do?ggGuid=2c9e8ac275740a840175923874d7291d&gcbh=&bdbhs='
#     r = 'https://www.szjsjy.com.cn:8001/jyw/showGongGao.do?ggGuid=2c9e8ac275740a8401759291b4bc2ad5&gcbh=&bdbhs='
#         # 'https://www.szjsjy.com.cn:8001/jyw/jyw/zbGongGao_View.do?ggguid=2c9e8ac275740a8401759291b4bc2ad5&gcbh=&bdbhs='
#     a = requests.post(url=detail_link,headers=rs_headers,verify=False)
#     print(a.json()['html'])



p = 'asdsf{name}{age}'.format(name = '女子力',age = '18')
print(p)
import re

import re
page = re.findall("\d+","asd1234")
print(page)

for i in range(0,10):
    print(i)
import json
fic = {'message': '成功', 'data': '{"rows":[{"id":"464c451315034327ab3a2ffd062633f3","publishTime":"2020-11-13 09:24","noticeName":"沙角A电厂2021-2023年度汽机压力容器安全阀送外定期检验项目-公开招标公告","evalMethod":"2"},{"id":"6c9b306ea44b4bbabb581780128cf4c2","publishTime":"2020-11-13 09:24","noticeName":"沙角A电厂2021-2023年度机组检修机炉电外围脚手架搭设工程项目-公开招标公告","evalMethod":"2"},{"id":"cba9f0ddd976444b8b0fa5faad20f6db","publishTime":"2020-11-12 23:30","noticeName":"中山大学附属第一医院采购灭菌盒招标项目-公开招标公告","evalMethod":"2"},{"id":"dd557afb26e048bd92740bca3affe75b","publishTime":"2020-11-12 20:19","noticeName":"广东医科大学附属医院药物临床试验机构临床试验GCP信息管理平台项目-公开招标公告","evalMethod":"2"},{"id":"0622d116166640afa7d89874a0c7222b","publishTime":"2020-11-12 20:19","noticeName":"广东医科大学附属医院被服定点采购项目-公开招标公告","evalMethod":"2"},{"id":"a3548d4fdebf4c0faf72b6695e9b7a94","publishTime":"2020-11-12 17:48","noticeName":"中山市小榄人民医院64排螺旋CT系统采购项目-公开招标公告","evalMethod":"2"},{"id":"10b411e3337d407ea4c8bc00c2b22ea6","publishTime":"2020-11-12 17:27","noticeName":"广州信息投资有限公司白云新城商圈片区（齐心路-云霄路）智慧灯杆项目-公开招标公告","evalMethod":"2"},{"id":"26b9de1c424741f0b98e08634c33e9e4","publishTime":"2020-11-12 11:50","noticeName":"南方医科大学珠江医院陪护与送检服务社会化管理项目-公开招标公告","evalMethod":"2"},{"id":"71d4b5b4264f43759bcc65f356e5d655","publishTime":"2020-11-12 11:28","noticeName":"南海长海发电有限公司燃气－蒸汽联合循环冷热电联产改扩建工程项目辅机设备（33）-电力电缆及控制电缆-公开招标公告","evalMethod":"2"},{"id":"5a9493af36834e4f86d9bc5d2adc224a","publishTime":"2020-11-12 11:16","noticeName":"广州市烟草专卖局行动指挥中心项目-公开招标公告","evalMethod":"2"},{"id":"516d21ecf477485d83aca5a9f1af45ae","publishTime":"2020-11-12 09:00","noticeName":"惠州市扫黑除恶专项斗争年度户外宣传广告项目-竞争性磋商公告","evalMethod":"2"},{"id":"ef9092afb9af4dbe8ff306fe07c0f292","publishTime":"2020-11-11 17:54","noticeName":"中山市小榄人民医院高清腹腔镜镜头采购项目-竞争性磋商公告","evalMethod":"2"},{"id":"db05b60d3c0b4e28a9794fa50bfe6eb5","publishTime":"2020-11-11 17:51","noticeName":"广东医科大学附属医院内镜治疗工作站采购项目-公开招标公告","evalMethod":"2"},{"id":"29eb83bdf7a642bfaaede70251959090","publishTime":"2020-11-11 17:51","noticeName":"广东医科大学附属医院电子胃肠镜、超声内镜系统采购项目-公开招标公告","evalMethod":"2"},{"id":"e35c119eb5c841149ee09928e8bd485e","publishTime":"2020-11-11 17:33","noticeName":"广州造纸实业有限公司新产品分厂包装机升级改造项目（第二次）-公开招标公告","evalMethod":"2"}],"footer":[],"total":6954,"pageNumber":1,"pageSize":15}', 'success': True}
w = json.loads(fic['data'])
print(type(w))
print(w['rows'])

for i in range(4,6):
    print(i)