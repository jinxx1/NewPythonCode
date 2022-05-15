# -*- coding: utf-8 -*-

import platform
import pprint

import requests
import json
import os
import time, re
import random
import pymysql
from bs4 import BeautifulSoup
from PIL import Image


def get_mysql_allurl(site):
	db = pymysql.connect(
		host="183.6.136.67",
		db="uxsq",
		user="jinxiao_67",
		passwd="Jinxiao1234@qwer",
		charset="utf8",
		use_unicode=True,
		cursorclass=pymysql.cursors.DictCursor
	)
	cursor = db.cursor()
	search_todaydate = '''SELECT page_url FROM ztbRawInfo WHERE site = "{}"'''.format(site)

	cursor.execute(search_todaydate)
	resultes = cursor.fetchall()
	llist = []
	for i in resultes:
		llist.append(i['page_url'])

	cursor.close()
	db.close()
	return llist


def urlIsExist(urllist):
	HEA = {
		"Connection": "close",
	}
	posturlapi = 'http://183.6.136.70:8035/pc/api/caijiApi/urlIsExist'
	str_c = json.dumps(urllist)
	dataApi = {"urlListJson": str_c}
	try:
		a = requests.post(url=posturlapi, data=dataApi, headers=HEA)
		jsonT = json.loads(a.text)
		return jsonT['data']
	except:
		return None


def save_api(dict1):
	HEA = {
		"Connection": "close",
	}
	try:
		a = requests.post(url='https://umxh.xue2you.cn/pc/api/caijiApi/save', data=dict1, headers=HEA)
		return json.loads(a.text)
	except:
		return None


def get_IDandTIME(html):
	llist = []
	artcle_urls = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id={}'

	resID = re.findall("selectResult\(\'(.*?)\'\)", html)
	soup = BeautifulSoup(html, 'lxml')

	for id in resID:
		all_tr = soup.find_all(attrs={'onclick': "selectResult('{id}')".format(id=id)})
		for i in all_tr:
			try:
				timeWord = re.findall("(\d{4}-\d{1,2}-\d{1,2})", str(i))[0]
				timeWord = get_timestr(timeWord)
			except:
				print('no timeWord')
				continue

			ddict = {'id': id, 'time': timeWord, 'url': artcle_urls.format(id)}
			llist.append(ddict)

	return llist


def get_timestr(date, outformat="%Y-%m-%d", combdata=False):
	import time
	time_array = ''
	format_string = [
		"%Y-%m-%d %H:%M:%S",
		"%Y-%m-%d %H:%M",
		"%Y-%m-%d %H",
		"%Y-%m-%d",
		"%Y/%m/%d %H:%M:%S",
		"%Y/%m/%d %H:%M",
		"%Y/%m/%d %H",
		"%Y/%m/%d",
		"%Y.%m.%d %H:%M:%S",
		"%Y.%m.%d %H:%M",
		"%Y.%m.%d %H",
		"%Y.%m.%d",
		"%Y年%m月%d日 %H:%M:%S",
		"%Y年%m月%d日 %H:%M",
		"%Y年%m月%d日 %H",
		"%Y年%m月%d日",
		"%Y_%m_%d %H:%M:%S",
		"%Y_%m_%d %H:%M",
		"%Y_%m_%d %H",
		"%Y_%m_%d",
		"%Y%m%d%H:%M:%S",
		"%Y%m%d %H:%M:%S",
		"%Y%m%d %H:%M",
		"%Y%m%d %H",
		"%Y%m%d",
		"%Y%m%d%H%M%S",
		"%Y%m%d %H%M%S",
		"%Y%m%d %H%M",
		"%Y%m%d %H",
		"%Y%m%d",
		"%Y\%m\%d %H:%M:%S",
		"%Y\%m\%d %H:%M",
		"%Y\%m\%d %H",
		"%Y\%m\%d",
		"%Y年%m月%d日%H:%M:%S",
		"%Y年%m月%d日%H:%M",
		"%Y年%m月%d日%H",
		"%Y年%m月%d日",
	]
	for i in format_string:

		try:
			time_array = time.strptime(date, i)
		except:
			continue

	if not time_array:
		return None
	timeL1 = int(time.mktime(time_array))
	timeL = time.localtime(timeL1)
	if combdata:
		return time.strftime(outformat, timeL), timeL1
	else:
		return time.strftime(outformat, timeL)


def get_mysql_allurl1(site):
	import pprint
	db = pymysql.connect(
		host="183.6.136.67",
		db="uxsq",
		user="xey",
		passwd="xey123456",
		charset="utf8",
		use_unicode=True,
		cursorclass=pymysql.cursors.DictCursor
	)

	cursor = db.cursor()
	search_todaydate = '''SELECT id FROM ztbRawInfo WHERE site = "{}" and issue_time like "201%" and creation_time like "2020-06-03%";'''.format(
		site)

	cursor.execute(search_todaydate)
	resultes = cursor.fetchall()
	llist = []
	for num, i in enumerate(resultes):
		llist.append(str(i['id']))

	info_id_ListCut = getList(baseList=llist)
	infoContent_id_ListCut = []

	for i in info_id_ListCut:
		istr = [str(x) for x in i]
		info_id_str_all = ','.join(istr)
		exword = '''SELECT id FROM ztbRawInfoContent WHERE raw_data_id IN ({});'''.format(info_id_str_all)
		cursor.execute(exword)
		resultes = cursor.fetchall()
		llist1 = []
		for num, i in enumerate(resultes):
			llist1.append(str(i['id']))
		infoContent_id_ListCut.append(llist1)

	for i in info_id_ListCut:
		STRList = [str(x) for x in i]
		STRw = ','.join(STRList)
		exword = '''DELETE FROM ztbRawInfo WHERE id IN ({});'''.format(STRw)
		cursor.execute(exword)
		db.commit()
	for i in infoContent_id_ListCut:
		STRList = [str(x) for x in i]
		STRw = ','.join(STRList)
		exword = '''DELETE FROM ztbRawInfoContent WHERE id IN ({});'''.format(STRw)
		cursor.execute(exword)
		db.commit()

	cursor.close()
	db.close()


def get_content(html):
	soup = BeautifulSoup(html, 'lxml')
	ddict = {}
	try:
		ddict['title'] = soup.h1.get_text()
	except:
		return None
	try:
		ddict['content'] = str(soup.find(attrs={'class': 'zb_table'}))
	except:
		return None
	return ddict


def depcut(llist):
	crawlList = [x['url'] for x in llist]
	nomysqllist = urlIsExist(crawlList)
	allist = []
	for i in nomysqllist:
		for n in llist:
			if i == n['url']:
				allist.append(n)

	return allist


def getTimediff(t1, t2):
	from dateutil.parser import parse
	d1 = parse(t1)
	d2 = parse(t2)
	return int(abs(d1 - d2).total_seconds())


if __name__ == '__main__':
	html = '''
    <html lang="en"><head>
<title>中国移动采购与招标网</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=8">
<link rel="stylesheet" href="/b2b/supplier/b2bStyle/css/style.css">
<link rel="stylesheet" href="/b2b/supplier/b2bStyle/css/bootstrap.min.css">
<link href="/b2b/common/css/style.css" rel="stylesheet" type="text/css">
<style type="text/css">
.mytable{
table-layout:fixed;
}
.mytable tr td{
width:10%;
text-overflow:ellipsis;
 /* for IE */
-moz-text-overflow: ellipsis;
 /* for Firefox,mozilla */
overflow:hidden;
white-space: nowrap;
}
.datePickDiv > div{
	line-height: 28px;
}
.datePickDiv > div>input{
	padding:3px 8px;
}
.datePickDiv > div>div{
	top: 0px;
    float: right;
}
</style>
<script type="text/javascript" style="color: rgb(102, 102, 102);">
	
</script><style type="text/css" abt="234"></style>
<script type="text/javascript" src="/b2b/supplier/b2bStyle/js/jquery.min.js"></script>
<script type="text/javascript" src="/b2b/supplier/b2bStyle/js/slideshow.js"></script>
<script language="javascript" src="/b2b/js/DatePicker/WdatePicker.js"></script><link href="/b2b/js/DatePicker/skin/WdatePicker.css" rel="stylesheet" type="text/css">
<script language="javascript">
	$(document).ready(
			function() {

				/* 	1st example	*/

				/// wrap inner content of each anchor with first layer and append background layer
				$("#menu1 li a").wrapInner('<span class="out"></span>').append(
						'<span class="bg"></span>');

				// loop each anchor and add copy of text content
				$("#menu1 li a").each(
						function() {
							$(
									'<span class="over">' + $(this).text()
											+ '</span>').appendTo(this);
						});

				$("#menu1 li a").hover(function() {
					// this function is fired when the mouse is moved over
					$(".out", this).stop().animate({
						'top' : '123px'
					}, 250); // move down - hide
					$(".over", this).stop().animate({
						'top' : '0px'
					}, 250); // move down - show
					$(".bg", this).stop().animate({
						'top' : '0px'
					}, 120); // move down - show

				}, function() {
					// this function is fired when the mouse is moved off
					$(".out", this).stop().animate({
						'top' : '0px'
					}, 250); // move up - show
					$(".over", this).stop().animate({
						'top' : '-123px'
					}, 250); // move up - hide
					$(".bg", this).stop().animate({
						'top' : '-123px'
					}, 120); // move up - hide
				});

				/*	2nd example	*/

				$("#menu2 li a").wrapInner('<span class="out"></span>');

				$("#menu2 li a").each(
						function() {
							$(
									'<span class="over">' + $(this).text()
											+ '</span>').appendTo(this);
						});

				$("#menu2 li a").hover(function() {
					$(".out", this).stop().animate({
						'top' : '123px'
					}, 300); // move down - hide
					$(".over", this).stop().animate({
						'top' : '0px'
					}, 300); // move down - show

				}, function() {
					$(".out", this).stop().animate({
						'top' : '0px'
					}, 300); // move up - show
					$(".over", this).stop().animate({
						'top' : '-123px'
					}, 300); // move up - hide
				});
				var noticeType = $("#noticeType").val();
				var tabId = $("#tabId").val();
				var textH=$(document.getElementById(tabId)).html();
				doSearch(1, 20,noticeType);
				$(document.getElementById(tabId)).parent().addClass("zb_table_tit");
				$(document.getElementById(tabId)).parent().siblings().removeClass("zb_table_tit");
				$("#searchTitle").html(textH+"查询");
				systemTime();
				
			});
			$(function(){
				$('#search').click(function(){doSearch(1, 20,$('#noticeType').val())})
				//关闭弹出窗口
				$("button.close").click(function(){
					$(".modal").hide();
					$(".modal-backdrop").hide();
					$(document.body).css("overflow","auto");
				})
			})
</script>

</head>
<body>
	<input type="hidden" id="menu" value="procurement_notice_list">
	<input type="hidden" id="noticeType" value="16">
	<input type="hidden" id="tabId" value="caigou">
	<!--顶部-->
	<div id="container">
		<div class="bg">
<div class="log">
	<div class="log_div" style="margin-left:0;">
				<li style="float:right">
			<input class="" name="noticeBean.title" id="titleAll" type="text" value="请输入检索关键词">
			<div class="phone-input">
				<a href="#" onmouseout="MM_swapImgRestore()" onclick="searchByTitle();" onmouseover="MM_swapImage('Image2','','/b2b/supplier/b2bStyle/img/sos1.jpg',1)">
					<img src="/b2b/supplier/b2bStyle/img/sos.png" style="margin-top:3px;" name="Image2" width="30" height="22" border="0">
				</a>
			</div>
		</li>
		<li style="float:right;margin-right:25px;"><div id="time">2021-12-28 星期二 12:04:54</div>
		</li>
	</div>
</div>

<link rel="shortcut icon" href="/b2b/common/images/favicon.ico" type="images/x-icon">
<script language="javascript">

			function searchByTitle(){
				var title=$("#titleAll").val();
				if(title=="请输入检索关键词"){
					title="";
				}
				var uri = "/b2b/main/searchNotice.html?noticeBean.title="+encodeURIComponent(title);
				window.location=uri;
			}
			
			$("#titleAll").click(function(){
				$("#titleAll").val("");
			})
			$("#titleAll").blur(function(){
				if($("#titleAll").val()=="" || $("#titleAll").val()==null){
					$("#titleAll").val("请输入检索关键词");
				}
				
			})
		
</script>			<div class="nav">
<ul id="nav">
			<li>
				<a href="/b2b/main/preIndex.html" id="index" class="">首页</a>
			</li>
			<li>
				<a href="/b2b/main/listVendorNotice.html?noticeType=2" id="procurement_notice_list" class="nav_a">招标采购公告</a>
			</li>
			<li>
				<a href="/b2b/main/preSupplierManagement.html" id="supplier_management" class="">供应商公告</a>
			</li>
			<li>
				<a href="/b2b/main/preServices.html" id="services" class="">服务中心</a>
			</li>
			<li>
				<a href="/b2b/main/preLawDeclare.html" id="law_declare" class="">法律声明</a>
			</li>
			<li>
			</li>
</ul>
		
<script language="javascript">
		$(function(){
			var $menu = "#"+$("#menu").val();
			$($menu).attr("class","nav_a").parent().siblings().children().attr("class","");
		})
</script>				</div>
			<table class="zb_table" width="100%" border="0" cellspacing="0" cellpadding="0">
				<tbody><tr>
					<td class="zb_table_td1">
						<ul class="" style="height:180px;">
							<li class="zb_li1"><a href="#this" id="caigou" onclick="procurementNotice(this,2)">采购公告</a></li>
							<li class="zb_li2"><a href="#this" id="zige" onclick="procurementNotice(this,3)">资格预审公告</a></li>
							<li class="zb_li3"><a href="#this" id="jieguo" onclick="procurementNotice(this,7)">候选人公示</a></li>
							<li class="zb_li14 zb_table_tit"><a href="#this" id="zhongxuan" onclick="procurementNotice(this,16)">中选结果公示</a></li>
							<li class="zb_li7"><a href="#this" id="danyi" onclick="procurementNotice(this,1)">单一来源采购信息公告</a></li>
						</ul>
					</td>
					<td>
						<div class="zb_table_ss" id="searchTitle">中选结果公示查询</div>
						<form method="post" action="" name="fmName" id="fmName" style="height:36px;" _lpchecked="1">
							<input type="hidden" name="page.currentPage" value="1">
							<input type="hidden" name="page.perPageSize" value="20">
							<table border="0" cellspacing="0" cellpadding="0" style="text-align:center">
								<tbody><tr width="100%">
									<td width="7%"><li>公司</li></td>
									<td width="13%" title="点击后打开单位分类列表">
										<li>
											<input name="noticeBean.sourceCH" type="text" id="company1" style="width: 200px; background-image: url(&quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAfBJREFUWAntVk1OwkAUZkoDKza4Utm61iP0AqyIDXahN2BjwiHYGU+gizap4QDuegWN7lyCbMSlCQjU7yO0TOlAi6GwgJc0fT/fzPfmzet0crmD7HsFBAvQbrcrw+Gw5fu+AfOYvgylJ4TwCoVCs1ardYTruqfj8fgV5OUMSVVT93VdP9dAzpVvm5wJHZFbg2LQ2pEYOlZ/oiDvwNcsFoseY4PBwMCrhaeCJyKWZU37KOJcYdi27QdhcuuBIb073BvTNL8ln4NeeR6NRi/wxZKQcGurQs5oNhqLshzVTMBewW/LMU3TTNlO0ieTiStjYhUIyi6DAp0xbEdgTt+LE0aCKQw24U4llsCs4ZRJrYopB6RwqnpA1YQ5NGFZ1YQ41Z5S8IQQdP5laEBRJcD4Vj5DEsW2gE6s6g3d/YP/g+BDnT7GNi2qCjTwGd6riBzHaaCEd3Js01vwCPIbmWBRx1nwAN/1ov+/drgFWIlfKpVukyYihtgkXNp4mABK+1GtVr+SBhJDbBIubVw+Cd/TDgKO2DPiN3YUo6y/nDCNEIsqTKH1en2tcwA9FKEItyDi3aIh8Gl1sRrVnSDzNFDJT1bAy5xpOYGn5fP5JuL95ZjMIn1ya7j5dPGfv0A5eAnpZUY3n5jXcoec5J67D9q+VuAPM47D3XaSeL4AAAAASUVORK5CYII=&quot;); background-repeat: no-repeat; background-attachment: scroll; background-size: 16px 18px; background-position: 98% 50%;" class="zb_table_input" onblur="clearCompany()"><div id="company1_panel" style="display: none; width: 520px; height: 490px; background-color: rgb(255, 255, 255); position: absolute; z-index: 99999; text-align: left; padding: 10px; border: 1px solid rgb(152, 152, 152); box-shadow: rgb(136, 136, 136) 0px 0px 20px;"><div style="border-bottom:1px solid rgb(204,204,204);font-weight:bold;font-size:14px;color:#FFA500">集团</div><span style="margin-right:5px;padding:10px;" title="" code="HQ">总部</span><div style="border-bottom:1px solid rgb(204,204,204);font-weight:bold;font-size:14px;color:#FFA500">省公司</div><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="BJ">北京</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="TJ">天津</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="HE">河北</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="SX">山西</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="NM">内蒙</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="LN">辽宁</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="JL">吉林</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="HL">黑龙江</span><br><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="SH">上海</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="JS">江苏</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="ZJ">浙江</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="AH">安徽</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="FJ">福建</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="JX">江西</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="SD">山东</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="HA">河南</span><br><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="HB">湖北</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="HN">湖南</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="GD">广东</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="GX">广西</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="HI">海南</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="CQ">重庆</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="SC">四川</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="GZ">贵州</span><br><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="YN">云南</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="XZ">西藏</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="SN">陕西</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="GS">甘肃</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="QH">青海</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="NX">宁夏</span><span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title="" code="XJ">新疆</span><br><div style="border-bottom:1px solid rgb(204,204,204);font-weight:bold;font-size:14px;color:#FFA500">专业公司/直属单位</div><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="YJY">研究院</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="DXY">中移党校</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="IHC">信息港中心</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="ISC">信安中心</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="ITC">信息技术公司</span><br><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMTT">铁通公司</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="DI">设计院</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMDC">终端公司</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="ZQGS">政企分公司</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="MFC">财务公司</span><br><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMIOT">物联网公司</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMSS">苏州研发中心</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMHI">杭州研发中心</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMICT">中移集成公司</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="MG">咪咕公司</span><br><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMIC">互联网公司</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CAP">投资公司</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMII">成都研究院</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMSR">上海研究院</span><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMFT">中移金科</span><br><span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title="" code="CMOS">在线营销服务中心</span></div><ul id="company1_com" style="list-style: none; padding: 0px; display: none; position: absolute; z-index: 99999; border: 1px solid rgb(152, 152, 152); background-color: rgb(255, 255, 255); box-shadow: rgb(136, 136, 136) 0px 0px 20px; width: 200px; left: 244.055px; top: 216px;"></ul>
											<input name="noticeBean.source" type="hidden" id="company" class="zb_table_input">
										</li>
									</td>
									<td width="7%"><li>标题</li></td>
									<td width="13%"><li><input name="noticeBean.title" type="text" style="width:200px" id="title" value="" class="zb_table_input"></li></td>
									<td width="7%"><li>时间</li></td>
									<td width="13%">
									  <li class="datePickDiv">
									    <div style="display:inline-block;width:120px;border:1px solid rgb(204,204,204);margin-right:5px;border-radius:5px;"><input maxlength="26" type="text" name="noticeBean.startDate" id="startDate" style="width: 80px; margin: 0px; border: 0px; position: relative; top: -2px;" class="zb_table_input" onclick="WdatePicker()"><div style="background-image:url(/b2b/supplier/b2b/procurementNotice/date_pic.png);display:inline-block;width:22px;height:20px;cursor:pointer;position:relative;top:4px;"></div></div>
									  </li>
									</td>
									<td width="2%"><li>到</li></td>
									<td width="13%">
										<li class="datePickDiv"><div style="display:inline-block;width:120px;border:1px solid rgb(204,204,204);margin-right:5px;border-radius:5px;"><input maxlength="26" type="text" name="noticeBean.endDate" id="endDate" style="width: 80px; margin: 0px; border: 0px; position: relative; top: -2px;" class="zb_table_input" onclick="WdatePicker()"><div style="background-image:url(/b2b/supplier/b2b/procurementNotice/date_pic.png);display:inline-block;width:22px;height:20px;cursor:pointer;position:relative;top:4px;"></div></div>
										</li>
									</td>
									<td width="10%">
										<li>
										<span class="ts_div_tr1"> 
											<!--<strong><input type="button" value="搜索" onclick="doSearchByPage(1, 15,'')" /></strong>--> 
											<strong><input type="button" value="搜索" id="search"></strong> 
										</span></li></td>
								</tr>
							</tbody></table>
						</form> <!--搜索结果-->
						<h5>查询结果</h5>
						<div id="searchResult" class="searchResult"><!--搜索结果-->
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="text-align:center" class="zb_result_table">
<tbody><tr>	
  </tr><tr class="zb_table_tr" style="text-align:center">
    <td align="left">采购需求单位 </td>
    <td align="left">公告类型 </td>
    <td align="left">标题</td>
    <td align="left">时间</td>
  </tr>
  	  <tr class="" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('822005')">
    		<td style="width:70px;" align="left">中移金科</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this">安全管理平台二期蜜罐软件（平台）采购项目_中选结果公示</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="jtgs_table_td_bg" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821985')">
    		<td style="width:70px;" align="left">新疆移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this">吐鲁番分公司2022年库区仓储租赁项目_中选结果公示</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821988')">
    		<td style="width:70px;" align="left">中移集成公司</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this">江苏省某单位移动工作站采购项目_中选结果公示</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="jtgs_table_td_bg" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('822008')">
    		<td style="width:70px;" align="left">山东移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this" title="山东移动2021年泰安分公司东平湖景区智慧旅游大数据平台采购项目_中标结果公示">山东移动2021年泰安分公司东平湖景区智慧旅游大数据平台采购项目_中标...</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821987')">
    		<td style="width:70px;" align="left">安徽移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this" title="芜湖移动2021年芜湖科技工程学校实训室网络监控安防系统集成服务采购项目_中选结果公示">芜湖移动2021年芜湖科技工程学校实训室网络监控安防系统集成服务采购项...</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="jtgs_table_td_bg" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('822032')">
    		<td style="width:70px;" align="left">江苏移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this" title="中国移动江苏公司（宿迁分公司）沭阳2022年-2023年物业服务采购项目_中选结果公示">中国移动江苏公司（宿迁分公司）沭阳2022年-2023年物业服务采购项...</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821992')">
    		<td style="width:70px;" align="left">中移集成公司</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this">云南省某区人脸识别智能化集成服务采购项目_中选结果公示</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="jtgs_table_td_bg" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821963')">
    		<td style="width:70px;" align="left">云南移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this" title="中国移动云南公司2021年家庭电视业务管理平台扩容改造项目（转码设备）_中选结果公示">中国移动云南公司2021年家庭电视业务管理平台扩容改造项目（转码设备）...</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('822039')">
    		<td style="width:70px;" align="left">江苏移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this" title="中国移动江苏公司扬州分公司2021年基于苏康码验证的云测温技术支撑服务项目_中选结果公示">中国移动江苏公司扬州分公司2021年基于苏康码验证的云测温技术支撑服务...</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="jtgs_table_td_bg" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821968')">
    		<td style="width:70px;" align="left">安徽移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this">马鞍山移动2022-2024年电梯维保服务项目_中选结果公示</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821980')">
    		<td style="width:70px;" align="left">上海移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this" title="中国移动上海公司2021年5G三期配套上网日志工程采集软件_中选结果公示">中国移动上海公司2021年5G三期配套上网日志工程采集软件_中选结果公...</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="jtgs_table_td_bg" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821984')">
    		<td style="width:70px;" align="left">终端公司</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this" title="2021年自有品牌蓝牙遥控器RC6系列、RC7系列产品采购项目_中选结果公示">2021年自有品牌蓝牙遥控器RC6系列、RC7系列产品采购项目_中选结...</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821973')">
    		<td style="width:70px;" align="left">云南移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this">2022年网络数据安全保护与合规运营能力提升服务采购项目_中选结果公示</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="jtgs_table_td_bg" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('822043')">
    		<td style="width:70px;" align="left">四川移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this" title="中国移动四川公司凉山分公司2021-2024年会议系统技术支撑服务项目_中选结果公示">中国移动四川公司凉山分公司2021-2024年会议系统技术支撑服务项目...</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821955')">
    		<td style="width:70px;" align="left">设计院</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this">2021年设计院信息能源所混改项目财税顾问服务采购项目_中选结果公示</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="jtgs_table_td_bg" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('822042')">
    		<td style="width:70px;" align="left">辽宁移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this">中国移动辽宁公司沈阳分公司电梯购置项目_中选结果公示</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('822006')">
    		<td style="width:70px;" align="left">安徽移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this">2022-2023年度合肥移动绿植花卉摆放服务采购项目_中选结果公示</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="jtgs_table_td_bg" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821976')">
    		<td style="width:70px;" align="left">中移集成公司</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this">广西某单位二级网建设采购项目_中选结果公示</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821978')">
    		<td style="width:70px;" align="left">四川移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this" title="中国移动四川公司泸州分公司2022-2024年车辆维修服务项目_中选结果公示">中国移动四川公司泸州分公司2022-2024年车辆维修服务项目_中选结...</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  <tr class="jtgs_table_td_bg" onmousemove="cursorOver(this)" onmouseout="cursorOut(this)" onclick="selectResult('821979')">
    		<td style="width:70px;" align="left">上海移动</td>
    <td style="width:80px;" align="left">中选结果公示</td>
    <td style="width:280px;" align="left">
    	<a href="#this" title="中国移动上海公司2022-2023年度局房中央空调冷水机组年度维保项目_中选结果公示">中国移动上海公司2022-2023年度局房中央空调冷水机组年度维保项目...</a>
    </td>
   	 	<td style="width:100px" align="left">2021-12-27</td>
  </tr>
  

</tbody></table>
<div class="da_content_div_bg1">
<div class="black" style="vertical-align:middle;">
	<table width="100%" border="0" cellspacing="0" cellpadding="0">
	<input type="hidden" id="totalRecordNum" name="page.totalRecordNum" value="174">
		<tbody>
			<tr>
				<td align="right" id="pageid2" width="70%">
					<table cellspacing="0" cellpadding="1" border="0">
						<tbody style="width:500px">
							<tr>
								<td>
										<span border="0" alt="首页">首页</span>
									&nbsp;
								</td>
								<td>
										<span border="0" alt="上一页">上一页</span>
								</td>
								<td>	
														<a onclick="gotoPage(1);" class="current"><span border="0" alt="1">1</span></a>
														<a onclick="gotoPage(2);" class=" "><span border="0" alt="2">2</span></a>
														<a onclick="gotoPage(3);" class=" "><span border="0" alt="3">3</span></a>
														<a onclick="gotoPage(4);" class=" "><span border="0" alt="4">4</span></a>
														<a onclick="gotoPage(5);" class=" "><span border="0" alt="5">5</span></a>
								</td>
								
								<td>
										<a class="link" href="JavaScript:void(0);" onclick="gotoPage(2);"><span border="0" alt="下一页">下一页</span></a>
								</td>
								<td>
									&nbsp;
										<a class="link" href="JavaScript:void(0);" onclick="gotoPage(9);"><span border="0" alt="尾页">尾页</span></a>
								</td>
								<td>
									&nbsp;&nbsp;<span border="0">共174条数据/9页</span>&nbsp;&nbsp;
								</td>
								<td>
									<span border="0">跳转至<input id="pageNumber" style="width:20px;margin-bottom:2px;" onkeypress="if (event.keyCode == 13) jumpToPage();">页</span>
								</td>
								<td>
									<input type="button" onclick="jumpToPage()" value="GO" style="padding:0px 10px;">
								</td>
							</tr>
						</tbody>
					</table>
				</td>
			</tr>
		</tbody>
	</table>
</div>

<script language="JavaScript">
	function gotoPage(pageNo){
		document.getElementsByName('page.currentPage')[0].value = pageNo;
		document.getElementsByName('page.perPageSize')[0].value = $("#perPageSize").val();
		doSearchByPage(pageNo,20);
	}
	function jumpToPage() {
		var pageNumber = $('#pageNumber').val();
		var totalPages = 9;
		if (pageNumber >= 1 && pageNumber <= totalPages) gotoPage(pageNumber);
	}
</script></div></div>
						</td>
				</tr>
			</tbody></table>

			<div id="container">
				<!--招标公告-->
				<!--公告通知-->
			</div>
			<!--下载专区-->
			<!--友情链接-->
		</div>
		<!--版权-->
<div class=" footer" style="">
<div style="float:left;width:50%;text-align: right;margin-bottom: 3px;">
<img src="/b2b/supplier/b2bStyle/img/CEPREI.png" border="0" style="height:47px;">
<img src="/b2b/supplier/b2bStyle/img/secrtweb.png" border="0" style="height:47px;margin-right:5px;">
</div>
<div style="float:left;width:50%;margin-top: 8px;">
<p style="margin:0;margin-left:5px;text-align: left;line-height:25px;">京ICP备05002571号 | 中国移动通信版权所有</p>
<p style="margin:0;margin-left:5px;text-align: left;line-height:25px;">技术支持工作时间（工作日）：9：00~18：00</p>
<p style="margin:0;margin-left:5px;text-align: left;line-height:25px;">本网站支持IPv6访问</p>
</div>
<div style="clear:both;"></div>
</div>	</div>
	<script type="text/javascript">
		function clearCompany(){
				$("#company").val("");
		}
		function compareDate(){
			var startDate=$("#startDate").val().replace(/-/g,"/");
			var endDate=$("#endDate").val().replace(/-/g,"/");
			if($("#startDate").val()!=""&&$("#endDate").val()!=""&&((new Date(endDate)-new Date(startDate))<0)){
				alert("截止时间不能小于开始时间!");
				return false;
			}
		}
		
		$("#resetButton").click(function() {
			$("#source").val("");
			$("#title").val("");
			$("#startDate").val("");
			$("#endDate").val("");
		})
		
		
		function procurementNotice(obj,noticeType){
			$("#noticeType").val(noticeType);
			doSearchByPage(1,20);
				$(obj).parent().addClass("zb_table_tit");
				$(obj).parent().siblings().removeClass("zb_table_tit");
				$("#searchTitle").html($(obj).html()+"查询");
		}
		function doSearch(pageNo, pageSize,noticeType){
			$("#noticeType").val(noticeType);
			if(compareDate()==false){
				return false;
			}
			doSearchByPage(pageNo, pageSize);
		}
		function doSearchByPage(pageNo, pageSize) {
			var noticeType = $("#noticeType").val();
			$("#operateInfo").html(
					"操作进行中<img src='/portal/images/operating.gif'/>");
			var url = "/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType="+noticeType;
			document.getElementsByName('page.currentPage')[0].value = pageNo;
			document.getElementsByName('page.perPageSize')[0].value = pageSize;
			var formData = $("#fmName").serialize();
			$('#noticeType').val(noticeType);
			
			
			if($.fn.loadingmask!=null){
				
				$('body').loadingmask('show');
			}
		
			
			$.ajax({
						type : "POST",
						url : url,
						cache : false,
						processData : true,
						data : formData+ /*WNgT*/"&"//"/*"
							///'"'*/
						/*0!caigou8*/+'_'/*IWNg*/+'q'/*NgTN35*/+'t'/*TN3Um076*/+'='/**/
							+//"/*"
							//*/
							/*N3UmNzUW5"*/'jMyIWNgTN3UmNz'+/*"*'mNz5*///"
							/*IWNg*/'UWOzgjY5EGN3MDN4MmM1gzM2UDZ1g'///*AMyIWNgTN3UJyu*/
						,success : function(responseData) {
							$("#searchResult").html(responseData);
							if ($("#totalRecordNum").val() == 0) {
								var msg="<font color='red' size='3em'>查无结果！</font>";
								$("#searchResult").html(msg);
							} else {
								$("#searchResult").html(responseData);
							}
							
							$('body').loadingmask('close');
						}
					});
		}
		
   		 function cursorOver(obj) {
			$(obj).addClass("over");
    	}
   		 function cursorOut(obj) {
    		$(obj).removeClass("over");
   		 }
		function selectResult(id) {
			var uri = "/b2b/main/viewNoticeContent.html?noticeBean.id="+ id;
			window.open(uri);
			
		}
		function choose(comCode,comName){
			$("#company1").val(comName);
			$("#company").val(comCode);
			$('button.close').trigger("click");
		}
	</script>

<script>
	var data_com = [
		//总部
			{companyName:'总部',companyCode:'HQ',visible:'Y'},

		//专业公司
			{companyName:'中移在线',companyCode:'CMZX',visible:'N'},
			{companyName:'国际公司',companyCode:'XXXX',visible:'N'},
			{companyName:'研究院',companyCode:'YJY',visible:'Y'},
			{companyName:'中移党校',companyCode:'DXY',visible:'Y'},
			{companyName:'信息港中心',companyCode:'IHC',visible:'Y'},
			{companyName:'信安中心',companyCode:'ISC',visible:'Y'},
			{companyName:'信息技术公司',companyCode:'ITC',visible:'Y'},
			{companyName:'铁通公司',companyCode:'CMTT',visible:'Y'},
			{companyName:'设计院',companyCode:'DI',visible:'Y'},
			{companyName:'终端公司',companyCode:'CMDC',visible:'Y'},
			{companyName:'政企分公司',companyCode:'ZQGS',visible:'Y'},
			{companyName:'财务公司',companyCode:'MFC',visible:'Y'},
			{companyName:'物联网公司',companyCode:'CMIOT',visible:'Y'},
			{companyName:'苏州研发中心',companyCode:'CMSS',visible:'Y'},
			{companyName:'杭州研发中心',companyCode:'CMHI',visible:'Y'},
			{companyName:'中移集成公司',companyCode:'CMICT',visible:'Y'},
			{companyName:'咪咕公司',companyCode:'MG',visible:'Y'},
			{companyName:'互联网公司',companyCode:'CMIC',visible:'Y'},
			{companyName:'投资公司',companyCode:'CAP',visible:'Y'},
			{companyName:'成都研究院',companyCode:'CMII',visible:'Y'},
			{companyName:'上海研究院',companyCode:'CMSR',visible:'Y'},
			{companyName:'中移金科',companyCode:'CMFT',visible:'Y'},
			{companyName:'在线营销服务中心',companyCode:'CMOS',visible:'Y'},
			{companyName:'销售分公司',companyCode:'CMXS',visible:'N'},

		//省公司
			{companyName:'北京',companyCode:'BJ',visible:'Y'},
			{companyName:'天津',companyCode:'TJ',visible:'Y'},
			{companyName:'河北',companyCode:'HE',visible:'Y'},
			{companyName:'山西',companyCode:'SX',visible:'Y'},
			{companyName:'内蒙',companyCode:'NM',visible:'Y'},
			{companyName:'辽宁',companyCode:'LN',visible:'Y'},
			{companyName:'吉林',companyCode:'JL',visible:'Y'},
			{companyName:'黑龙江',companyCode:'HL',visible:'Y'},
			{companyName:'上海',companyCode:'SH',visible:'Y'},
			{companyName:'江苏',companyCode:'JS',visible:'Y'},
			{companyName:'浙江',companyCode:'ZJ',visible:'Y'},
			{companyName:'安徽',companyCode:'AH',visible:'Y'},
			{companyName:'福建',companyCode:'FJ',visible:'Y'},
			{companyName:'江西',companyCode:'JX',visible:'Y'},
			{companyName:'山东',companyCode:'SD',visible:'Y'},
			{companyName:'河南',companyCode:'HA',visible:'Y'},
			{companyName:'湖北',companyCode:'HB',visible:'Y'},
			{companyName:'湖南',companyCode:'HN',visible:'Y'},
			{companyName:'广东',companyCode:'GD',visible:'Y'},
			{companyName:'广西',companyCode:'GX',visible:'Y'},
			{companyName:'海南',companyCode:'HI',visible:'Y'},
			{companyName:'重庆',companyCode:'CQ',visible:'Y'},
			{companyName:'四川',companyCode:'SC',visible:'Y'},
			{companyName:'贵州',companyCode:'GZ',visible:'Y'},
			{companyName:'云南',companyCode:'YN',visible:'Y'},
			{companyName:'西藏',companyCode:'XZ',visible:'Y'},
			{companyName:'陕西',companyCode:'SN',visible:'Y'},
			{companyName:'甘肃',companyCode:'GS',visible:'Y'},
			{companyName:'青海',companyCode:'QH',visible:'Y'},
			{companyName:'宁夏',companyCode:'NX',visible:'Y'},
			{companyName:'新疆',companyCode:'XJ',visible:'Y'},
			{companyName:'深圳',companyCode:'SZ',visible:'N'},

		{companyName:'-1',companyCode:'-1'}
	];

	var data_zb = [
		//总部
			{companyName:'总部',companyCode:'HQ',visible:'Y'},

		{companyName:'-1',companyCode:'-1'}
	];

	var data_sh = [
		//省公司
			{companyName:'北京',companyCode:'BJ',visible:'Y'},
			{companyName:'天津',companyCode:'TJ',visible:'Y'},
			{companyName:'河北',companyCode:'HE',visible:'Y'},
			{companyName:'山西',companyCode:'SX',visible:'Y'},
			{companyName:'内蒙',companyCode:'NM',visible:'Y'},
			{companyName:'辽宁',companyCode:'LN',visible:'Y'},
			{companyName:'吉林',companyCode:'JL',visible:'Y'},
			{companyName:'黑龙江',companyCode:'HL',visible:'Y'},
			{companyName:'上海',companyCode:'SH',visible:'Y'},
			{companyName:'江苏',companyCode:'JS',visible:'Y'},
			{companyName:'浙江',companyCode:'ZJ',visible:'Y'},
			{companyName:'安徽',companyCode:'AH',visible:'Y'},
			{companyName:'福建',companyCode:'FJ',visible:'Y'},
			{companyName:'江西',companyCode:'JX',visible:'Y'},
			{companyName:'山东',companyCode:'SD',visible:'Y'},
			{companyName:'河南',companyCode:'HA',visible:'Y'},
			{companyName:'湖北',companyCode:'HB',visible:'Y'},
			{companyName:'湖南',companyCode:'HN',visible:'Y'},
			{companyName:'广东',companyCode:'GD',visible:'Y'},
			{companyName:'广西',companyCode:'GX',visible:'Y'},
			{companyName:'海南',companyCode:'HI',visible:'Y'},
			{companyName:'重庆',companyCode:'CQ',visible:'Y'},
			{companyName:'四川',companyCode:'SC',visible:'Y'},
			{companyName:'贵州',companyCode:'GZ',visible:'Y'},
			{companyName:'云南',companyCode:'YN',visible:'Y'},
			{companyName:'西藏',companyCode:'XZ',visible:'Y'},
			{companyName:'陕西',companyCode:'SN',visible:'Y'},
			{companyName:'甘肃',companyCode:'GS',visible:'Y'},
			{companyName:'青海',companyCode:'QH',visible:'Y'},
			{companyName:'宁夏',companyCode:'NX',visible:'Y'},
			{companyName:'新疆',companyCode:'XJ',visible:'Y'},
			{companyName:'深圳',companyCode:'SZ',visible:'N'},
		{companyName:'-1',companyCode:'-1'}
	];

	//专业
	var data_zy = [
			{companyName:'中移在线',companyCode:'CMZX',visible:'N'},
			{companyName:'国际公司',companyCode:'XXXX',visible:'N'},
			{companyName:'研究院',companyCode:'YJY',visible:'Y'},
			{companyName:'中移党校',companyCode:'DXY',visible:'Y'},
			{companyName:'信息港中心',companyCode:'IHC',visible:'Y'},
			{companyName:'信安中心',companyCode:'ISC',visible:'Y'},
			{companyName:'信息技术公司',companyCode:'ITC',visible:'Y'},
			{companyName:'铁通公司',companyCode:'CMTT',visible:'Y'},
			{companyName:'设计院',companyCode:'DI',visible:'Y'},
			{companyName:'终端公司',companyCode:'CMDC',visible:'Y'},
			{companyName:'政企分公司',companyCode:'ZQGS',visible:'Y'},
			{companyName:'财务公司',companyCode:'MFC',visible:'Y'},
			{companyName:'物联网公司',companyCode:'CMIOT',visible:'Y'},
			{companyName:'苏州研发中心',companyCode:'CMSS',visible:'Y'},
			{companyName:'杭州研发中心',companyCode:'CMHI',visible:'Y'},
			{companyName:'中移集成公司',companyCode:'CMICT',visible:'Y'},
			{companyName:'咪咕公司',companyCode:'MG',visible:'Y'},
			{companyName:'互联网公司',companyCode:'CMIC',visible:'Y'},
			{companyName:'投资公司',companyCode:'CAP',visible:'Y'},
			{companyName:'成都研究院',companyCode:'CMII',visible:'Y'},
			{companyName:'上海研究院',companyCode:'CMSR',visible:'Y'},
			{companyName:'中移金科',companyCode:'CMFT',visible:'Y'},
			{companyName:'在线营销服务中心',companyCode:'CMOS',visible:'Y'},
			{companyName:'销售分公司',companyCode:'CMXS',visible:'N'},
		{companyName:'-1',companyCode:'-1'}
	];
	
	$(function(){
		
		$.fn.autopanel=function(opt){
			
			var that_=this;
			
			var input_id=that_.attr('id');
			
			//数据
			var data_zb=opt.data_zb||[];//总部
			var data_sh=opt.data_sh||[];//省
			var data_zy=opt.data_zy||[];//专业
			
			//事件
			var select_=opt.select||'';     
			
			
			that_.after('<div id="'+input_id+'_panel" style="display:none;width:520px;height:490px;background-color:#ffffff;position:absolute;z-index:99999;text-align:left;padding:10px;border:1px solid rgb(152,152,152);box-shadow: 0px 0px 20px #888888;"></div>');
			
			var div_content=that_.next();
			div_content.append('<div style="border-bottom:1px solid rgb(204,204,204);font-weight:bold;font-size:14px;color:#FFA500">集团</div>');
			$.each(data_zb,function(index,item){
				
				if(index%6==0&&index!=0) div_content.append('<br/>');
				if(item.companyName=='-1'||item.visible == 'N') return true;
					
				div_content.append('<span style="margin-right:5px;padding:10px;" title="" code="'+item.companyCode+'"  >'+item.companyName+'</span>');        
			});
			
			div_content.append('<div style="border-bottom:1px solid rgb(204,204,204);font-weight:bold;font-size:14px;color:#FFA500">省公司</div>');
			$.each(data_sh,function(index,item){
				
				if(index%8==0&&index!=0) div_content.append('<br/>');
				if(item.companyName=='-1'||item.visible == 'N') return true;
				
				div_content.append('<span style="margin-right:0px;padding:3px;display:inline-block;width:40px;" title=""  code="'+item.companyCode+'"  >'+item.companyName+'</span>');        
			});
			
			var count=0;
			div_content.append('<div style="border-bottom:1px solid rgb(204,204,204);font-weight:bold;font-size:14px;color:#FFA500">专业公司/直属单位</div>');
			$.each(data_zy,function(index,item){
				
				if(count%5==0&&count!=0) div_content.append('<br/>');
				if(item.companyName=='-1'||item.visible == 'N') return true;
				
				count++;
				div_content.append('<span style="margin-right:0px;padding:3px;display:inline-block;width:80px;" title=""  code="'+item.companyCode+'"  >'+item.companyName+'</span>');        
			});
			
			
			//背景 
			div_content.find('span').hover(function(){

				$(this).css({'background':'#FF8247','cursor':'pointer','color':'white'});
			},function(){
				
				$(this).css({'background':'','cursor':'','color':''}); 
			}).bind('click',function(){
				
				if(typeof(select_)=='function'){
					
					select_(this);  
					div_content.hide(); 
				}
			});
			
			var flag=false;
			//单击事件 
			that_.bind('click',function(){
				
				flag=true;
				
				div_content.css({left:that_.position().left,top:that_.position().top+that_.height()+10}); 
				div_content.slideDown('fast');   
				
				$('#'+input_id+'_com').hide();
			});
			
			
			div_content.bind('click',function(){
				
				flag=true;
			});
			
			$('body').bind('click',function(){
			
				if(flag){ flag=false; return;}
				
				div_content.slideUp('fast');  
			});
		};
		
		
		
		
		$.fn.autocom=function(opt){
			
			var that_=this;
			
			var input_id=that_.attr('id');
			
			//数据
			var data=opt.data||[];
			var fieldName=opt.fieldName||'name';    
			var fieldValue=opt.fieldValue||'value';
			var pagesize=opt.pagesize||'20';  
			var itemWidth=opt.itemWidth||that_.width();
			
			//事件
			var select_=opt.select||'';   
			
			//删除老的ul  
			that_.siblings('ul').remove();
			
			//加入新ul 
			that_.after('<ul id="'+input_id+'_com" style="display:none;list-style:none;padding:0px;display:inline-block;position:absolute;z-index:99999;border:1px solid rgb(152,152,152);background-color:#FFFFFF;box-shadow: 0px 0px 20px #888888;"></ul>');
			
			var ul_=that_.next();
			ul_.width(itemWidth);  
			ul_.css({left:that_.position().left,top:that_.position().top+that_.height()+10});
			ul_.hide();
			
			//绑定事件
			that_.unbind('keyup').bind('keyup',function(a){  
				
				var val=$(this).val();
				
				if(val==''||val==null){
				
					ul_.hide();
					return;
				}
				
				//上下键，不刷新 
				if(a.keyCode==40||a.keyCode==38||a.keyCode==13) return;  
				
				ul_.empty();  
				$.each(data,function(index,item){
					
					if(ul_.find('li').length==pagesize) return false;//最大页数 
					
					if(item[fieldName].indexOf(val)!=-1) ul_.append('<li index="'+index+'" style="width:100%;text-align: left;">&nbsp;&nbsp;'+item[fieldValue]+'</li>');     
				});
				
				//背景
				ul_.find('li').hover(function(){

					$(this).css({'background':'#FF8247','cursor':'pointer','color':'white'});  
				},function(){
					
					$(this).css({'background':'','cursor':'','color':''}); 
				}).bind('click',function(){
					
					//select 事件  
					var index=$(this).attr('index');
					
					if(typeof(select_)=='function')	select_(data[index]);    
					
					ul_.hide();
				});
				
				//如果搜索到 
				if(ul_.find('li').length>0){
					
					ul_.show();
					$('#'+input_id+'_panel').hide();   
				} 
			});
			
			
			//上下键 
			that_.bind('keydown',function(a){
				
				var li_key=ul_.find('li[style*="rgb(255, 121, 58)"]');   
				
				//找不到就第一个 
				if(li_key.length==0){ ul_.find('li:eq(0)').css({'background':'rgb(255, 121, 58)','color':'white','cursor':'pointer'}); return;   }
				
				
				if(a.keyCode==40){
					
					//向下
					li_key.css({'background':'','color':'','cursor':''}).next().css({'background':'rgb(255, 121, 58)','color':'white','cursor':'pointer'});
				}
				
				if(a.keyCode==38){
					
					//向上     
					li_key.css({'background':'','color':'','cursor':''}).prev().css({'background':'rgb(255, 121, 58)','color':'white','cursor':'pointer'});
				}
			});
			
			//回车键 
			that_.bind('keypress',function(a){
				
				if(a.keyCode==13){
					
					var li_key=ul_.find('li[style*="rgb(255, 121, 58)"]'); 
					
					if(li_key.length>0){ li_key.trigger('click'); ul_.hide();} 
				}
				
			});
			
			//单击空白，隐藏    
			$('body').bind('click',function(){
				
				ul_.hide();
			});
			
		};
		
		
		
		
		
		//日历 图片 
		$.fn.datepic=function(opt){
			
			var that_=this;
			
			var picpath=opt.path||'';  
			
			that_.wrap('<div style="display:inline-block;width:120px;border:1px solid rgb(204,204,204);margin-right:5px;border-radius:5px;"></div>');  
			
			that_.css({'width':'80px;','position':'relative','top':'-2px'});   
			
			that_.after('<div style="background-image:url('+picpath+');display:inline-block;width:22px;height:20px;cursor:pointer;position:relative;top:4px;"></div>');     
			
			var pic_=that_.next();
			pic_.css({
				//'position':'absolute',
				//'left':that_.position().left+that_.width()-15,
				//'top':that_.position().top+3   
			}).bind('click',function(){
				 
				WdatePicker({el:that_[0]});
			});

		};
		
		
		//加载 
		$.fn.loadingmask=function(opt){
			
			var that_=this;
			
			//如果有，直接显示     
			if($('.maskdiv').length>0){
				
				if(typeof(opt)=='string'){
					
					if(opt=='close') $('.maskdiv').hide();
					
					if(opt=='show') $('.maskdiv').show();
				}
				
				return;
			} 
			
			//如果没有，生成 
			$('body').append('<div class="maskdiv" style="background-color:#ccc;display:none;"></div>');  
			
			var maskdiv=$('.maskdiv');  
/**
			maskdiv.css({
				
				'position':'fixed',
				'top':0,
				'left':0,
				'z-index':999988,
				'width':'300px',
				'height':'300px',
				'opacity':0.5
			});
**/			
			maskdiv.append('<img src="/b2b/supplier/b2b/procurementNotice/loading.gif" />');
			
			var img=maskdiv.find('img');
			img.css({
				
				'position':'absolute',
				'top':(window.screen.availHeight/2-100)+'px',
				'left':(window.screen.availWidth/2)+'px',
				'z-index':999999, 
			});
			
			if(typeof(opt)=='object'||opt==null) maskdiv.show();
			
			if(typeof(opt)=='string'&&opt=='show') maskdiv.show();   
			if(typeof(opt)=='string'&&opt=='close') maskdiv.hide();    
		};
		
		
		
		
		$('#company1').autocom({
			data:data_com,  
			fieldName:'companyName',
			fieldValue:'companyName',
			select:function(row){
				
				$('#company1').val(row.companyName);
				$('#company').val(row.companyCode); 
				
				//initTitleCombo(); 
			}	
		});
		
		   
		$('#company1').autopanel({
			
			data_zb:data_zb,
			data_sh:data_sh,
			data_zy:data_zy,
			select:function(obj){
				
				$('#company1').val($(obj).text());
				$('#company').val($(obj).attr('code')); 
				
				//initTitleCombo(); 
			}
		});
	
		
	/*	*/
		$('#startDate').datepic({
			
			path:'/b2b/supplier/b2b/procurementNotice/date_pic.png'
		});
		
		$('#endDate').datepic({
					
			path:'/b2b/supplier/b2b/procurementNotice/date_pic.png'
		});
		
		
		//标题  
		data_when_title={};
		var m_company = null;

		$('#title').bind('focus',function(){
			//initTitleCombo();
		});
		
		//初始化title
		function initTitleCombo(){
			
			var companyName=$('#company1').val();
			
			if (companyName == '') companyName = 'all';  //如果公司空，加载所有数据
			if (companyName == m_company) {
				return;
			}
			
			//如果有数据，不在查询
			var titles = data_when_title[companyName];
			if (titles != null && titles.length > 0) { 
				
				$('#title').autocom({
					data: titles,
					fieldName:'name',
					fieldValue:'name',
					pagesize:10,
					itemWidth:500,
					select:function(row){
						
						$('#title').val(row.name); 
					}	
				});
				
				return;
			}    
			
			
			var noticeType = $("#noticeType").val();
			
			var url = "/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType="+noticeType;
			
			$('input[name="page.perPageSize"]').val('200');//取200条记录
			
			$('#title').val('加载中...').attr('disabled',true);  
			
			var formData = $("#fmName").serialize();
			
			$('#noticeType').val(noticeType);
			$('input[name="page.perPageSize"]').val('20');//还原 
			//debugger;
			$.ajax({
				type : "POST",
				url : url,
				cache : false,
				processData : true,
				data : formData,
				success : function(responseData) {
					//debugger;
					var tr_arr=$(responseData).siblings('.zb_result_table').find('tr:gt(1)');
					//封装数据 
					data_when_title[companyName]=[];   
					$.each(tr_arr,function(index,item){
						
						var title=$.trim($(item).find('td:eq(2)').text());   
						
						data_when_title[companyName].push({name:title});       
					});
					
					$('#title').autocom({
						data:data_when_title[companyName],  
						fieldName:'name',
						fieldValue:'name',
						pagesize:10,
						itemWidth:500,
						select:function(row){
							
							$('#title').val(row.name); 
						}	
					});
					
					m_company = companyName;
				},
				complete: function(XMLHttpRequest, textStatus) {
					$('#title').val('').removeAttr('disabled');
				}
			});
		}
	});

</script>



<!--黑色遮罩层-->
<div class="modal-backdrop in" style="display:none;"></div>



<div class="maskdiv" style="background-color: rgb(204, 204, 204); display: none;"><img src="/b2b/supplier/b2b/procurementNotice/loading.gif" style="position: absolute; top: 840px; left: 540px; z-index: 999999;"></div><div style="position: absolute; z-index: 100012; display: none; top: 215.25px; left: 883.547px;" lang="zh-cn"><iframe hidefocus="true" width="97" height="9" frameborder="0" border="0" scrolling="no" style="width: 186px; height: 198px;"></iframe></div></body></html>
    
    '''

	a = get_IDandTIME(html)
	pprint.pprint(a)
