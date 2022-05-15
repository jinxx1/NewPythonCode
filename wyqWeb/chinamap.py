# -*- coding: utf-8 -*-
import requests
# from pyecharts import Map
import os
# 版本pyecharts 0.5.11







provice = ['浙江', '安徽', '四川', '陕西', '重庆', '甘肃',
           '广西', '宁夏', '新疆', '海南', '山东', '河南',
           '辽宁', '河北', '山西', '内蒙古', '北京', '云南',
           '江西', '湖北', '天津', '吉林', '福建']
values = [37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 4, 4, 4, 4]

map = Map("中国地图",'中国地图', width=1200, height=900)
map.add("", provice, values,
        is_roam=True,   #是否开启鼠标缩放和平移漫游。默认为 True
                        #如果只想要开启缩放或者平移，可以设置成'scale'或者'move'。设置成 True 为都开启
        visual_range=[4, 37],
        is_map_symbol_show=False,#False去掉小红点True保留小红点
        maptype='china',
        # is_selected=True,
        symbol='circle',
        is_visualmap=True,
        visual_text_color='#888',
        symbol_size=15,
        # label_formatter='{b}',
        is_label_show=True,#将名称标注在地图上的
        label_pos="inside")

map.show_config()
map.render()

# with open('render.html','r',encoding='utf-8') as f:
#     hhtml = f.read()
#     f.close()

# hhtml = hhtml.replace('''"mapType": "china",''',''' "mapType": "china","label":{"normal":{"show":true}},''')

# with open('render.html','w',encoding='utf-8') as f:
#     f.write(hhtml)
#     f.flush()
#     f.close()

os.system("render.html")
