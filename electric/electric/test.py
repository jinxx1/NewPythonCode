import pprint
import re
import json
import datetime, time

dictTemp = [{'components': {}, 'isHover': False, 'childSpan': [8, 16], 'children': [{'components': {
    'icon': 'iconicon-21', 'name': '嵌入代码', 'id': 'e7e80241aee203f0e20a008306305793', 'type': 'ItemInnerCode',
    'option': {
        'code': '<h1class="logo">\n\t\t\t<ahref="Default.html">\n\t\t\t\t<imgsrc="${siteHost}/images/a_03.png"/>\n\t\t\t\t<h2>电子商务平台</h2>\n\t\t\t\t<p>E-commerceplatform</p>\n\t\t\t</a>\n\t\t</h1>',
        'data': {'dataId': '', 'hasClassify': False, 'dataConnId': '', 'dataType': 'internalData', 'dataClassName': '',
                 'query': '', 'pageSize': 10, 'detailId': '', 'sort': [], 'mapFields': [], 'dataClassId': ''},
        'partTitle': '', 'fields': [], 'partType': 'default'}}, 'isHover': False, 'childSpan': [24], 'children': [],
                                                                                     'width': 100, 'lv': 2,
                                                                                     'type': 'components',
                                                                                     'widthType': '%', 'span': 8},
                                                                                    {'components': {}, 'isHover': False,
                                                                                     'childSpan': [24], 'children': [{
                                                                                                                         'components': {
                                                                                                                             'icon': 'iconicon-21',
                                                                                                                             'name': '嵌入代码',
                                                                                                                             'id': '50a0438ec132301fccab8c287809aa8f',
                                                                                                                             'type': 'ItemInnerCode',
                                                                                                                             'option': {
                                                                                                                                 'code': '<divclass="ssk">\n<divclass="yzcz">\n\t\t\t\t\t<p>中文</p>\n\t\t\t\t\t<ul>\n\t\t\t\t\t\t<li><ahref="${siteHost}/enus/default.html">English</a></li>\n\t\t\t\t\t\t<li><ahref="${siteHost}/default.html">中文</a></li>\n\t\t\t\t\t</ul>\n\t\t\t\t</div>\n\t\t\t\t<divclass="sskbox">\n\t\t\t\t\t<inputtype="text"class="wby1"placeholder="搜索关键字"/>\n\t\t\t\t\t<buttontype="button"class="btn1search-btn"></button>\n\t\t\t\t</div>\n\t\t\t\t<divclass="clear"></div>\n\t\t\t</div>',
                                                                                                                                 'data': {
                                                                                                                                     'dataId': '',
                                                                                                                                     'hasClassify': False,
                                                                                                                                     'dataConnId': '',
                                                                                                                                     'dataType': 'internalData',
                                                                                                                                     'dataClassName': '',
                                                                                                                                     'query': '',
                                                                                                                                     'pageSize': 10,
                                                                                                                                     'detailId': '',
                                                                                                                                     'sort': [],
                                                                                                                                     'mapFields': [],
                                                                                                                                     'dataClassId': ''},
                                                                                                                                 'partTitle': '',
                                                                                                                                 'fields': [],
                                                                                                                                 'partType': 'default'}},
                                                                                                                         'isHover': False,
                                                                                                                         'childSpan': [
                                                                                                                             24],
                                                                                                                         'children': [],
                                                                                                                         'width': 100,
                                                                                                                         'lv': 3,
                                                                                                                         'type': 'components',
                                                                                                                         'widthType': '%',
                                                                                                                         'span': 24},
                                                                                                                     {
                                                                                                                         'components': {
                                                                                                                             'icon': 'iconicon-14',
                                                                                                                             'name': '新闻列表',
                                                                                                                             'id': '21eadaeaa251eabcd8a5ff96ed169653',
                                                                                                                             'type': 'ItemList',
                                                                                                                             'option': {
                                                                                                                                 'dataUrl': '',
                                                                                                                                 'data': {
                                                                                                                                     'dataId': '01e29646bcb245f6a80b670f8a54116d',
                                                                                                                                     'hasClassify': False,
                                                                                                                                     'dataConnId': '',
                                                                                                                                     'dataType': 'internalData',
                                                                                                                                     'dataClassName': '',
                                                                                                                                     'query': '',
                                                                                                                                     'pageSize': 10,
                                                                                                                                     'sort': [],
                                                                                                                                     'mapFields': [
                                                                                                                                         'SystemName',
                                                                                                                                         'Url',
                                                                                                                                         'ShowCategory'],
                                                                                                                                     'dataClassId': ''},
                                                                                                                                 'icon': '',
                                                                                                                                 'moreUrlType': '2',
                                                                                                                                 'partTitle': '',
                                                                                                                                 'className': '',
                                                                                                                                 'templateCode': '<divclass="of-site-components${className}"style="${width}">\n\t<divclass="rmbq">\n\t\t<ulid="${id}">\n\t\t\t<!--tmpl-start-->\n\t\t\t{{each(i,item)data}}\n\t\t\t{{if(item.ShowCategory==\'Intranet\'&&funGetNetWork()==\'Intranet\')||item.ShowCategory!=\'Intranet\'}}\n\t\t\t<li><ahref="${getLanguageValue(item.Url)}"target="_blank">${getLanguageValue(item.SystemName)}</a></li>\n\t\t\t{{/if}}\n\t\t\t{{/each}}\n\t\t\t<!--tmpl-end-->\n\t\t</ul>\n\t</div>\n</div>',
                                                                                                                                 'templateId': '01c7f49f-1c20-4203-bd6e-ea1439f74acc',
                                                                                                                                 'title': '',
                                                                                                                                 'dataUrlType': '1',
                                                                                                                                 'templateName': 'ECP-系统链接入口',
                                                                                                                                 'showTitle': True,
                                                                                                                                 'iconType': '1',
                                                                                                                                 'moreUrl': '',
                                                                                                                                 'partType': 'default',
                                                                                                                                 'showIcon': False}},
                                                                                                                         'isHover': False,
                                                                                                                         'childSpan': [
                                                                                                                             24],
                                                                                                                         'children': [],
                                                                                                                         'width': 100,
                                                                                                                         'lv': 3,
                                                                                                                         'type': 'components',
                                                                                                                         'widthType': '%',
                                                                                                                         'span': 24}],
                                                                                     'width': 100, 'lv': 2,
                                                                                     'type': 'layout', 'widthType': '%',
                                                                                     'span': 16}], 'width': '100',
             'layoutType': 2, 'lv': 1, 'className': 'header', 'type': 'layout', 'widthType': '%', 'span': 24}, {
                'components': {'icon': 'iconicon-14', 'name': '新闻列表', 'id': '781da2407fac1f8d006fa129b50af5d2',
                               'type': 'ItemList', 'option': {'dataUrl': '',
                                                              'data': {'dataId': 'a1b2b9c17c0745e5b7052c4e4577dade',
                                                                       'hasClassify': False, 'dataConnId': '',
                                                                       'dataType': 'internalData', 'dataClassName': '',
                                                                       'query': '', 'pageSize': 999, 'sort': [
                                                                      {'fieldName': 'UpdateTime', 'sort': 'desc'}],
                                                                       'mapFields': ['CreateTime', 'CreateUserName',
                                                                                     'UpdateTime', 'UpdateUserName',
                                                                                     'Title', 'ContentStoreId',
                                                                                     'CreateUserId', 'Five',
                                                                                     'FiveMatching', 'FiveUrl', 'Four',
                                                                                     'FourMatching', 'FourUrl', 'One',
                                                                                     'OneUrl', 'SiteId', 'Three',
                                                                                     'ThreeMatching', 'ThreeUrl', 'Two',
                                                                                     'TwoMatching', 'TwoUrl',
                                                                                     'UpdateUserId'],
                                                                       'dataClassId': ''}, 'icon': '',
                                                              'moreUrlType': '1', 'partTitle': '', 'className': '',
                                                              'templateCode': '\n<divclass="of-site-components${className}site-navigationhide"style="${width}">\n<divclass="site-crumbsclearfix">\n\n{{ifpartTitle}}\n<divclass="crumbs-title">${partTitle}</div>\n{{/if}}\n\n<ulid="${id}">\n\n<!--tmpl-start-->\n{{ifdata}}\n\n{{each(i,item)funCheckNavigation(data)}}\n\n{{ifitem&&item.Current==true}}\n\n{{ifitem.One&&item.OneUrl==\'\'}}\n<liclass="active">\n<iclass="fasfa-home-lg-alt"></i>${getLanguageValue(item.One)}\n</li>\n{{elseitem.One}}\n<li>\n\n<iclass="fasfa-home-lg-alt"></i><ahref="${item.OneUrl}"target="_blank">${getLanguageValue(item.One)}</a>\n</li>\n{{/if}}\n\n\n{{ifitem.Two&&item.TwoUrl==\'\'}}\n<liclass="active">${getLanguageValue(item.Two)}</li>\n{{elseitem.Two}}\n<li>\n<ahref="${item.TwoUrl}"target="_blank">${getLanguageValue(item.Two)}</a>\n</li>\n{{/if}}\n\n\n{{ifitem.Three&&item.ThreeUrl==\'\'}}\n<liclass="active">${getLanguageValue(item.Three)}</li>\n{{elseitem.Three}}\n<li>\n<ahref="${item.ThreeUrl}"target="_blank">${getLanguageValue(item.Three)}</a>\n</li>\n{{/if}}\n\n{{ifitem.Four&&item.FourUrl==\'\'}}\n<liclass="active">${getLanguageValue(item.Four)}</li>\n{{elseitem.Four}}\n<li>\n<ahref="${item.FourUrl}"target="_blank">${getLanguageValue(item.Four)}</a>\n</li>\n{{/if}}\n\n{{ifitem.Five&&item.FiveUrl==\'\'}}\n<liclass="active">${getLanguageValue(item.Five)}</li>\n{{elseitem.Five}}\n<li>\n<ahref="${item.FiveUrl}"target="_blank">${getLanguageValue(item.Five)}</a>\n</li>\n{{/if}}\n\n{{/if}}\n{{/each}}\n\n{{/if}}\n<!--tmpl-end-->\n</ul>\n\n</div>\n</div>\n',
                                                              'templateId': 'cb02ce8a-8800-48bc-9719-bae7913c1f2a',
                                                              'title': '', 'dataUrlType': '1',
                                                              'templateName': '通用-网站导航-1', 'showTitle': False,
                                                              'iconType': '1', 'moreUrl': '', 'partType': 'default',
                                                              'showIcon': False}}, 'isHover': True, 'childSpan': [24],
                'children': [], 'width': '1240', 'layoutType': 2, 'lv': 1, 'type': 'components', 'widthType': '%',
                'span': 24}, {'components': {}, 'sideWrapper': {
    'left': {'components': {}, 'menuwidthHide': True, 'childSpan': [24], 'children': [], 'width': 100, 'lv': 0,
             'widthType': '%', 'span': 24},
    'right': {'components': {}, 'menuwidthHide': True, 'childSpan': [24], 'children': [], 'width': 100, 'lv': 0,
              'widthType': '%', 'span': 24}}, 'isHover': False, 'childSpan': [24], 'children': [
    {'components': {}, 'isHover': False, 'childSpan': [6, 18], 'children': [{'components': {'icon': 'iconicon-14',
                                                                                            'name': '新闻列表',
                                                                                            'id': 'ba0edaba5ef68ca771839209873f520b',
                                                                                            'type': 'ItemList',
                                                                                            'option': {'dataUrl': '',
                                                                                                       'data': {
                                                                                                           'dataId': '1bcf75cf3e1a4b768df2edeed59ba4dd',
                                                                                                           'hasClassify': False,
                                                                                                           'dataConnId': '',
                                                                                                           'dataType': 'internalData',
                                                                                                           'dataClassName': '',
                                                                                                           'query': "Category='招标信息'",
                                                                                                           'pageSize': 10,
                                                                                                           'sort': [{
                                                                                                                        'fieldName': 'SerialNumber',
                                                                                                                        'sort': 'asc'}],
                                                                                                           'mapFields': [
                                                                                                               'CreateTime',
                                                                                                               'CreateUserName',
                                                                                                               'UpdateTime',
                                                                                                               'UpdateUserName',
                                                                                                               'Title',
                                                                                                               'Category',
                                                                                                               'ListUrl',
                                                                                                               'SerialNumber',
                                                                                                               'Url'],
                                                                                                           'dataClassId': ''},
                                                                                                       'icon': '',
                                                                                                       'moreUrlType': '1',
                                                                                                       'partTitle': '招标信息',
                                                                                                       'className': '',
                                                                                                       'templateCode': '<divclass="of-site-components${className}"style="${width}">\n\n<divclass="of-site-components">\n<divclass="site-boxsite-list-menu">\n{{ifpartTitle}}\n<divclass="list-menu-title">${partTitle}</div>\n{{/if}}\n<ulid="${id}">\n<!--tmpl-start-->\n{{each(i,item)data}}\n\n{{if(item.ListUrl.indexOf(\'nbtz.html\')==-1)||funGetNetWork()==\'Intranet\'}}\n\n<ahref="${item.ListUrl}">\n{{ifwindow.location.href.toUpperCase().indexOf(data[i].ListUrl.toUpperCase())>-1}}\n\n<liclass="active">\n${getLanguageValue(item.Title)}\n</li>\n\n{{else}}\n<li>\n${getLanguageValue(item.Title)}\n</li>\n{{else}}\n{{/if}}\n\n</a>\n\n{{/if}}\n\n{{/each}}\n<!--tmpl-end-->\n\n</ul>\n</div>\n</div>\n\n</div>',
                                                                                                       'templateId': '5276743c-0935-4ae6-9ab4-955cae9ebfb5',
                                                                                                       'title': '',
                                                                                                       'dataUrlType': '1',
                                                                                                       'templateName': 'ECP-新闻中心-1',
                                                                                                       'showTitle': False,
                                                                                                       'iconType': '1',
                                                                                                       'moreUrl': '',
                                                                                                       'partType': 'default',
                                                                                                       'showIcon': False}},
                                                                             'isHover': False, 'childSpan': [24],
                                                                             'children': [], 'width': 100, 'lv': 2,
                                                                             'type': 'components', 'widthType': '%',
                                                                             'span': 6}, {
                                                                                'components': {'icon': 'iconicon-14',
                                                                                               'name': '新闻更多',
                                                                                               'id': '350ea2d859f7a2797c9be4b6cb3b5ebe',
                                                                                               'type': 'ItemListMore',
                                                                                               'option': {
                                                                                                   'dataUrl': 'Details.html',
                                                                                                   'data': {
                                                                                                       'dataId': 'aa2e86adfa624027b1cf9d1598fb90b6',
                                                                                                       'hasClassify': False,
                                                                                                       'dataConnId': '',
                                                                                                       'dataType': 'internalData',
                                                                                                       'dataClassName': '',
                                                                                                       'query': "Status='passed'\nAND(Titlelike${Key|%%}ORBidInvitingPartylike${Key|%%}ORTenderNolike${Key|%%})\nAND(DATE(IssueTime)>=${StartDate|1949-10-10})\nAND(DATE(IssueTime)<=${EndDate|2100-10-10})\n",
                                                                                                       'pageSize': 15,
                                                                                                       'sort': [{
                                                                                                                    'fieldName': 'IssueTime',
                                                                                                                    'sort': 'desc'}],
                                                                                                       'mapFields': [
                                                                                                           'CreateTime',
                                                                                                           'CreateUserName',
                                                                                                           'UpdateTime',
                                                                                                           'UpdateUserName',
                                                                                                           'Title',
                                                                                                           'BidEndTime',
                                                                                                           'BidInvitingParty',
                                                                                                           'BidStartTime',
                                                                                                           'IssueTime',
                                                                                                           'IsTop',
                                                                                                           'NewExpireTime',
                                                                                                           'TenderNo'],
                                                                                                       'dataClassId': ''},
                                                                                                   'icon': '',
                                                                                                   'partTitle': '中标候选人公示',
                                                                                                   'className': '',
                                                                                                   'templateCode': '<divclass="of-site-components${className}"style="${width}">\r\n<divclass="content-box-maincontent-box-list">\r\n<divclass="zbgs">\r\n<divclass="zbgs_tit">\r\n<divclass="zbpx">\r\n<pid="sortName">按发布日期排序</p>\r\n<divclass="sxj">\r\n<spanclass="topbtn"></span><spanclass="bottombtn"></span>\r\n</div>\r\n<divclass="pxxz">\r\n<divclass="sxj"style="top:10px;right:15px">\r\n<spanclass="topbtn"></span><spanclass="bottombtn"></span>\r\n</div>\r\n<ul>\r\n<li><aonclick="funOrdereByList(\'BidInvitingParty\',\'asc\');returnfalse;">按招标人排序</a></li>\r\n<li><aonclick="funOrdereByList(\'TenderNo\',\'asc\');returnfalse;">按招标编号排序</a></li>\r\n<li><aonclick="funOrdereByList(\'IssueTime\',\'desc\');returnfalse;">按发布日期排序</a></li>\r\n<li><aonclick="funOrdereByList(\'BidStartTime\',\'desc\');returnfalse;">按公示起始日期排序</a>\r\n</li>\r\n<li><aonclick="funOrdereByList(\'BidEndTime\',\'desc\');returnfalse;">按公示结束日期排序</a>\r\n</li>\r\n</ul>\r\n</div>\r\n</div>\r\n<h2>${partTitle}</h2>\r\n</div>\r\n\r\n<divclass="nybt">\r\n<ulstyle="border:none;">\r\n<li>\r\n<b>关键词</b>\r\n<inputtype="text"class="wby2"placeholder="请输入关键词搜索"id="${id}_Key"\r\nvalue="${getNoLike(getPageParam(\'Key\')||\'\')}"\r\nonkeypress="event.keyCode===13?funBindArticleListQuery(\'${id}\'):\'\'">\r\n</li>\r\n<li>\r\n<b>发布日期</b>\r\n<inputtype="text"name="date"class="ECalendarStartDate"id="${id}_StartDate"\r\nvalue="${getNoLike(getPageParam(\'StartDate\')||\'\')}"\r\nonkeypress="event.keyCode===13?funBindArticleListQuery(\'${id}\'):\'\'">\r\n<em>~</em>\r\n<inputtype="text"name="date"class="ECalendarEndDate"id="${id}_EndDate"\r\nvalue="${getNoLike(getPageParam(\'EndDate\')||\'\')}"\r\nonkeypress="event.keyCode===13?funBindArticleListQuery(\'${id}\'):\'\'">\r\n</li>\r\n<li>\r\n<buttontype="submit"class="btn5"onclick="funBindArticleListQuery(\'${id}\');">查询</button>\r\n</li>\r\n</ul>\r\n</div>\r\n\r\n<scripttype="text/javascript">\r\n$(function(){\r\n$(".StartDate").ECalendar({\r\ntype:"date",\r\nskin:"#005287",\r\noffset:[0,2]\r\n});\r\n$(".EndDate").ECalendar({\r\ntype:"date",\r\nskin:"#005287",\r\noffset:[0,2]\r\n});\r\n\r\n});\r\n\r\nfunctionloadSortName(){\r\nvarurl=window.location.href;\r\nvarstart=url.lastIndexOf("=",(url.lastIndexOf("=")-1))+1;\r\nvarend=url.lastIndexOf("&");\r\nvarname=url.substring(start,end);\r\nif(name=="BidInvitingParty"){\r\n$("#sortName").text("按招标人排序");\r\n}elseif(name=="TenderNo"){\r\n$("#sortName").text("按招标编号排序");\r\n}elseif(name=="BidStartTime"){\r\n$("#sortName").text("按公示起始日期排序");\r\n}elseif(name=="BidEndTime"){\r\n$("#sortName").text("按 公示结束日期排序");\r\n}else{\r\n$("#sortName").text("按发布日期排序");\r\n}\r\n}\r\nwindow.onload=loadSortName();\r\n&lt;/script&gt;\r\n\r\n\r\n<divid="${id}">\r\n<!--tmpl-start-->\r\n<divclass="box-content">\r\n{{ifdata&&data.list}}\r\n{{each(i,item)data.list}}\r\n<divclass="zbnr">\r\n<divclass="zbnr_left"style="width:calc(100%-290px);">\r\n<atitle="${getLanguageValue(item.Title)}"href="${dataUrl+item.Id}"target="_blank">\r\n<h2>\r\n<i>${getLanguageValue(item.Title)}</i>\r\n{{ifitem._IsTop!=\'1\'&&getIsNewArticle(item.NewExpireTime)==\'1\'}}\r\n<spanclass="bq2"></span>\r\n{{/if}}\r\n{{ifitem._IsTop==\'1\'}}\r\n<spanclass="bq3"></span>\r\n{{/if}}\r\n</h2>\r\n<p><span>招标人：${getLanguageValue(item.BidInvitingParty)}</span>&nbsp;&nbsp;&nbsp;&nbsp;招标编号：${item.TenderNo}\r\n</p>\r\n</a>\r\n</div>\r\n<divclass="zbnr_right"style="width:270px;">\r\n<dl>\r\n<dt>\r\n<p>公示起始日期</p>\r\n<h2style="color:#999999">${getFormatYearMonthDay(item.BidStartTime)}</h2>\r\n</dt>\r\n<dt>\r\n<p>公示结束日期</p>\r\n<h2style="color:#999999">${getFormatYearMonthDay(item.BidEndTime)}</h2>\r\n</dt>\r\n</dl>\r\n</div>\r\n<divclass="clear"></div>\r\n</div>\r\n{{/each}}\r\n{{/if}}\r\n</div>\r\n\r\n<divclass="list-more-footerclearfix">\r\n<divclass="site-paginationright">\r\n<spanclass="pagination-total">共${data?data.total||0:0}条</span>\r\n<spanclass="pagination-sizes">\r\n<selectclass="site-form-control"onchange="setPageSize(this.value)">\r\n\r\n{{ifgetPageSize(pageSize)===15}}\r\n<optionselectedvalue="15">15条/页</option>\r\n{{else}}\r\n<optionvalue="15">15条/页</option>\r\n{{/if}}\r\n\r\n{{ifgetPageSize(pageSize)===30}}\r\n<optionselectedvalue="30">30条/页</option>\r\n{{else}}\r\n<optionvalue="30">30条/页</option>\r\n{{/if}}\r\n\r\n{{ifgetPageSize(pageSize)===50}}\r\n<optionselectedvalue="50">50条/页</option>\r\n{{else}}\r\n<optionvalue="50">50条/页</option>\r\n{{/if}}\r\n\r\n{{ifgetPageSize(pageSize)===100}}\r\n<optionselectedvalue="100">100条/ 页</option>\r\n{{else}}\r\n<optionvalue="100">100条/页</option>\r\n{{/if}}\r\n\r\n</select>\r\n</span>\r\n<buttontype="button"${getPageIndex()<=1?\'disabled\':\'\'}class="btn-prev"\r\nonclick="setPageIndex(${getPageIndex()-1})">\r\n<iclass="fafa-angle-left"></i>\r\n</button>\r\n<ulclass="pager">\r\n{{each(i,item)getPages(data?data.total||0:0,pageSize)}}\r\n{{ifitem===\'...\'}}\r\n<lionclick="setPageIndex(${i<5?getPageIndex()-5:getPageIndex()+5})">${item}</li>\r\n{{else}}\r\n<liclass="${getPageIndex()===item?\'active\':\'\'}"\r\nonclick="$(this).hasClass(\'active\')?\'\':setPageIndex(${item})">${item}</li>\r\n{{/if}}\r\n{{/each}}\r\n</ul>\r\n<buttontype="button"${getPageIndex()<getPageCount(data?data.total||0:0,\r\ngetPageSize(pageSize))?\'\':\'disabled\'}class="btn-prev"\r\nonclick="setPageIndex(${getPageIndex()+1})">\r\n<iclass="fafa-angle-right"></i>\r\n</button>\r\n<spanclass="pagination-jump">\r\n前往<inputclass="site-form-control"type="text"value="1"\r\nonkeypress="event.keyCode===13?setPageIndex(this.value):\'\'">页\r\n</span>\r\n</div>\r\n</div>\r\n<!--tmpl-end-->\r\n</div>\r\n\r\n</div>\r\n</div>\r\n</div>',
                                                                                                   'templateId': '92e27b27-e973-46b0-a5f8-5c06c63cf974',
                                                                                                   'title': '',
                                                                                                   'dataUrlType': '1',
                                                                                                   'templateName': 'ECP-新闻更多-3',
                                                                                                   'showTitle': False,
                                                                                                   'iconType': '1',
                                                                                                   'partType': 'page',
                                                                                                   'showIcon': False}},
                                                                                'isHover': False, 'childSpan': [24],
                                                                                'children': [], 'width': 100, 'lv': 2,
                                                                                'type': 'components', 'widthType': '%',
                                                                                'span': 18}], 'width': '1200',
     'layoutType': 2, 'lv': 1, 'className': 'list-more-layout', 'type': 'layout', 'widthType': 'px', 'span': 24}],
                              'width': 100, 'lv': 0, 'type': 'layout', 'widthType': '%', 'span': 24}, {
                'components': {'icon': 'iconicon-21', 'name': '嵌入代码', 'id': 'ed772cf761fd7d9505614293ac77c4d4',
                               'type': 'ItemInnerCode', 'option': {
                        'code': '<divclass="footer">\n\t<p><span>总访问量：<b>388228</b></span><span>今日访问量：<b>14755</b></span></p>\n\t<h3><span>版权所有：中国广核集团有限公司</span><ahref="https://beian.miit.gov.cn/"target="_blank"style="color:#666666"><span><imgsrc="${siteHost}/images/a_59.png"/>粤ICP备08132407号-20</span></a></h3>\n{{iffunGetNetWork()==\'Intranet\'}}\n<ahref="https://nep.gnpjvc.cgnpc.com.cn/portal/index.html#/task"target="_blank"><iclass="fafa-file-import"></i>审批入口</a>\n<ahref="manage.html"target="_blank"><iclass="farfa-sliders-h-square"></i>网站管理</a>\n{{/if}}\n</div>',
                        'data': {'dataId': '', 'hasClassify': False, 'dataConnId': '', 'dataType': 'internalData',
                                 'dataClassName': '', 'query': '', 'pageSize': 10, 'detailId': '', 'sort': [],
                                 'mapFields': [], 'dataClassId': ''}, 'partTitle': '', 'fields': [],
                        'partType': 'default'}}, 'isHover': False, 'childSpan': [24], 'children': [], 'width': 100,
                'lv': 1, 'type': 'components', 'widthType': '%', 'span': 24}, {
                'components': {'icon': 'iconicon-21', 'name': '嵌入代码', 'id': '85ed1d5a32c6ae3fb653684e6aafc346',
                               'type': 'ItemInnerCode', 'option': {
                        'code': "<scripttype='text/javascript'>\n$(document).on('mouseenter','.box-title.tabs-barli',function(){\n$(this).click();\n});\n&lt;/script&gt;\n",
                        'data': {'dataId': '', 'hasClassify': False, 'dataConnId': '', 'dataType': 'internalData',
                                 'dataClassName': '', 'query': '', 'pageSize': 10, 'detailId': '', 'sort': [],
                                 'mapFields': [], 'dataClassId': ''}, 'partTitle': '', 'fields': [],
                        'partType': 'default'}}, 'isHover': False, 'childSpan': [24], 'children': [], 'width': 100,
                'lv': 1, 'type': 'components', 'widthType': '%', 'span': 24}]


def key_process(keyName, dic, lists=[]):
    from collections import Iterable

    for num, key in enumerate(dic.keys()):
        if keyName == key:
            lists.append(keyName)
        elif isinstance(key, (list, tuple)):
            pass

    if key in dic.keys():
        tmp_list.append(dic[key])


def findAllDict(seach_value, purpose, dic):
    if purpose not in ['key', 'value']:
        raise ValueError('''purpose传参必须是key或value。比如purpose="key"''')
    if not isinstance(dic, dict) or not isinstance(dic, list):
        raise ValueError('''输入的dic格式不对，必须为dict或list''')
        # 以上对传入数据进行格式校验

    if purpose == 'key':
        a = key_process(seach_value, dic)
    else:
        pass


def f(x):
    return str(x) + "_" + str(x)


class vidict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
    def walk(self):
        for key, value in self.items():
            if isinstance(value, vidict):
                for tup in value.walk():
                    yield (key,) + tup
            else:
                yield key, value

def vidict_func(dic):
    for nn in dic.walk():
        print(nn[0])
        print(type(nn[0]))
        print(nn[1])
        print(str(type(nn[1])))
        print(isinstance(nn[1], (list, tuple)))
        print('---------------------')


if __name__ == '__main__':
    # dictTemp
    pprint.pprint(dictTemp)

    from functools import reduce

    # aa = map(f, (1, 2, 3, 4, 5, 6, 7))
    # for i in aa:
    #     print(i)
    # print(aa)

exit()
ww = '''招标信息_招标公告	https://ecp.cgnpc.com.cn/zbgg.html?pageIndex={}	145
招标信息_资格预审公告	https://ecp.cgnpc.com.cn/zgysgg.html?pageIndex={}	14
招标信息_中标候选人公示	https://ecp.cgnpc.com.cn/zbhxrgs.html?pageIndex={}	110
招标信息_中标结果公示	https://ecp.cgnpc.com.cn/zbjggs.html?pageIndex={}	55
招标信息_变更公告	https://ecp.cgnpc.com.cn/bggg.html?pageIndex={}	21
非招标采购信息_采购启动公示	https://ecp.cgnpc.com.cn/cgqdgs.html?pageIndex={}	905
非招标采购信息_采购结果公示	https://ecp.cgnpc.com.cn/cgjggs.html?pageIndex={}	397'''.split('\n')
llist = []
for i in ww:
    cut = i.split('\t')
    ddict = {}
    ddict['catName'] = cut[0]
    ddict['baseUrl'] = cut[1]
    ddict['allPage'] = int(cut[2])
    llist.append(ddict)
pprint.pprint(llist)

print(llist)
