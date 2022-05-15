# -*- coding: utf-8 -*-
import os.path


import requests
from bs4 import BeautifulSoup
from lxml import etree,html
from html.parser import HTMLParser

def parse(pdfurl):
    '''解析PDF文本，并保存到TXT文件中'''
    fp = requests.get(url=pdfurl)
    # 用文件对象创建一个PDF文档分析器
    pdfFile = 'dnowload.pdf'
    with open(pdfFile,'wb')as file:
        file.write(fp.content)
    fp = open(pdfFile,'rb')
    parser = PDFParser(fp)
    print()
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)


    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:

        raise PDFTextExtractionNotAllowed
    else:

        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()

        # 创建一个PDF设备对象
        laparams = LAParams()

        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():

            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(r'2.txt', 'a') as f:
                        results = x.get_text()
                        print(results)
                        f.write(results + "\n")

def get_Summary(html):
    soup = BeautifulSoup(html, 'lxml')
    noneSummary = ''
    soupList = soup.find_all('p')
    if not soupList:
        print('no p')
        soupList = soup.find_all('a')
    if not soupList:
        print('no a')
        soupList = soup.find_all('span')
    if not soupList:
        print('no span')
        return noneSummary

    allWord = []
    for num,htmlBODY in enumerate(soupList):
        decodeWord = htmlBODY.get_text().replace('\u00A0','').replace('\u0020','').replace('\u3000','').replace('\n','').replace('\t','').replace('\r','')

        allWord.append(decodeWord.strip('，').strip(''))

    decodeWord = ''.join(allWord)
    returnSummaryWord = decodeWord[0:60] + "..."

    if len(returnSummaryWord) > 10:
        return returnSummaryWord.replace('%','%%')
    else:
        return noneSummary


def no_script(htmll):
    scrWord = re.findall("<script.*?>.*?</script>",htmll,re.M|re.S)
    for i in scrWord:
        htmll = htmll.replace(i,'')
    scrWord = re.findall("<link.*?>",htmll,re.M|re.S)
    for i in scrWord:
        htmll = htmll.replace(i,'')
    scrWord = re.findall("<meta.*?>",htmll,re.M|re.S)
    for i in scrWord:
        htmll = htmll.replace(i,'')
    scrWord = re.findall("<style.*?>.*?</style>",htmll,re.M|re.S)
    for i in scrWord:
        htmll = htmll.replace(i,'')
    scrWord = re.findall("<!-.*?>*?->",htmll,re.M|re.S)
    for i in scrWord:
        htmll = htmll.replace(i,'')

    return htmll

def no_Html(wword):
    tagList = ['p','div','a','span','strong','table','tr','td','font','ul','li','hr',
               'ol','dl','dt','dd','em','small','h1','h2','h3','h4','h5','h6','h7',
               'h8','h9','main','article','section']

    wword = no_script(wword)
    for i in tagList:
        wword = re.sub("<{}.*?>".format(i),"<{}>".format(i),wword)
    for n in range(5):
        for i in tagList:
            wword = wword.replace('&nbsp;', '').replace('<br>', '').replace('</br>', '').replace('\n', '')
            wword = re.sub("<{}>\s+".format(i),"<{}>".format(i),wword)
            wword = re.sub(">\s+<","><",wword,re.M|re.S)
            wword = re.sub("<{word}></{word}>".format(word = i),"",wword,re.M|re.S)
    soup = BeautifulSoup(wword,'lxml')
    strHtml = str(soup.prettify())
    return strHtml



if __name__ == '__main__':

    wword = '''
    <html lang="en"><head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>图片报道2</title>
    <link rel="stylesheet" href="/Tpl/public/cnii/css/base.css">
    <link rel="stylesheet" href="/Tpl/public/cnii/css/index.css">
    <style type="text/css">
        @media screen and (max-width: 1400px) {
            .float-wrap {
                right: 110px !important;
                top: 30%;
                }
        }

        .float-wrap {
            width: 50px;
            position: fixed;
            right:20%;
            top: 300px
        }

    </style>

<style type="text/css" abt="234"></style><link rel="stylesheet" href="http://paper.cnii.com.cn/Tpl/public/cnii/css/laydate/theme/default/laydate.css?v=5.0.9" id="layuicss-laydate"><script>//remove baidu search ad
var _countAA = 0
function doBBBd(){
    var alla = document.getElementsByTagName('a')
    for(var i = 0; i < alla.length; i++){
        if(/baidu.com\/(baidu.php\?url=|adrc.php\?t)/.test(alla[i].href)){
            var _temp = alla[i].parentElement, loop = 0
            while(loop < 5){
                _temp = _temp.parentElement
                loop++
                if(_temp.parentElement.id == 'content_left'){
                    _temp.remove()
                    break
                }
            }
        }
    }
    
    if(_countAA++ < 20){
        setTimeout(doBBBd, 500)
    }
    
}
doBBBd()
document.addEventListener('keyup', function(){_countAA-=10;doBBBd()}, false)
document.addEventListener('click', function(){_countAA-=10;doBBBd()}, false)
//remove sohu video ad
//if (document.URL.indexOf("tv.sohu.com") >= 0){
//    if (document.cookie.indexOf("fee_status=true")==-1){document.cookie='fee_status=true'};
//}
//remove 56.com video ad
//if (document.URL.indexOf("56.com") >= 0){
//    if (document.cookie.indexOf("fee_status=true")==-1){document.cookie='fee_status=true'};
//}
</script></head>
<body id="body">
<!--公共头部开始-->
<style>
    .erwema-login{
        right:9%!important;
        width:auto!important;
        padding-left:10px;
        padding-right:10px;

    }
</style>

<div class="top-navigation">
    <div class="inner-container">
                <ul class="clearfix">
            <li><a href="http://paper.cnii.com.cn" target="_self">人民邮电报</a></li><li><a href="http://paper.cnii.com.cn/home/zgjyb.html" target="_blank">中国集邮报</a></li><li><a href="http://paper.cnii.com.cn/home/zgwxd.html" target="_blank">中国无线电</a></li><li><a href="http://paper.cnii.com.cn/home/txqygl.html" target="_blank">通信企业管理</a></li><li><a href="http://paper.cnii.com.cn/home/zgdxy.html" target="_blank">中国电信业</a></li>        </ul>
                         <a href="https://open.weixin.qq.com/connect/qrconnect?appid=wxed3caae799188172&amp;redirect_uri=http%3A%2F%2Fpaper.cnii.com.cn%2FuserAuth%2F2_rmydb.html&amp;response_type=code&amp;scope=snsapi_login&amp;state=STATE#wechat_redirect" class="login-btn erwema-login">二维码登录</a> 
        <a href="/user/login/rmydb.html" class="login-btn">登录</a>

            </div>
</div>
<div class="sub-nav">
    <a href="/home/rmydb.html" class="logo"><img src="/Public/Uploads/logo_imgs/1/1572500637.png" alt=""></a>
    <ul class="clearfix">
        <li>2020年09月30日第7446期 星期三</li>
        <li><a href="/item/rmydb_2020_9_30_1.html">返回头版</a></li>
        <li class="bmdh">
            <span>版面导航</span>
            <div class="bmList mCustomScrollbar _mCS_1 mCS_no_scrollbar"><div id="mCSB_1" class="mCustomScrollBox mCS-light mCSB_vertical mCSB_inside" tabindex="0"><div id="mCSB_1_container" class="mCSB_container mCS_y_hidden mCS_no_scrollbar_y" style="position:relative; top:0; left:0;" dir="ltr">
                <table>
                    <tbody>
                        <tr>
                                <td><a href="/item/rmydb_2020_9_30_1.html">第01版：头版</a>
                                </td>
                            </tr><tr>
                                <td><a href="/item/rmydb_2020_9_30_2.html">第02版：综合新闻</a>
                                </td>
                            </tr><tr>
                                <td><a href="/item/rmydb_2020_9_30_3.html">第03版：工业互联网</a>
                                </td>
                            </tr><tr>
                                <td><a href="/item/rmydb_2020_9_30_4.html">第04版：专题报道</a>
                                </td>
                            </tr>                    </tbody>
                </table>
            </div><div id="mCSB_1_scrollbar_vertical" class="mCSB_scrollTools mCSB_1_scrollbar mCS-light mCSB_scrollTools_vertical" style="display: none;"><div class="mCSB_draggerContainer"><div id="mCSB_1_dragger_vertical" class="mCSB_dragger" style="position: absolute; min-height: 0px; top: 0px;" oncontextmenu="return false;"><div class="mCSB_dragger_bar" style="line-height: 0px;"></div></div><div class="mCSB_draggerRail"></div></div></div></div></div>
        </li>
        <li class="btdh">
            <span>标题导航</span>
            <div class="btList mCustomScrollbar _mCS_2 mCS_no_scrollbar"><div id="mCSB_2" class="mCustomScrollBox mCS-light mCSB_vertical mCSB_inside" tabindex="0"><div id="mCSB_2_container" class="mCSB_container mCS_y_hidden mCS_no_scrollbar_y" style="position:relative; top:0; left:0;" dir="ltr">
                <h3><a href="/item/rmydb_2020_9_30_1.html">第01版：头版</a>
                    </h3>
                    <ul>
                        <li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295989.html">刘烈宏：继续大力推进5G应用创新</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295990.html">让“浑源电商”成为当地经济增长新引擎</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295991.html">中国电信新推客户品牌“青年一派”</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295992.html">图片报道1</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295993.html">中国移动原创性传输技术体系正式确立</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295994.html">中国移动党组理论学习中心组专题学习研讨《习近平谈治国理政》第三卷</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295995.html">我国网民规模达9.4亿 手机网民占99.2%</a>
                            </li>                    </ul><h3><a href="/item/rmydb_2020_9_30_2.html">第02版：综合新闻</a>
                    </h3>
                    <ul>
                        <li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295996.html">有难事，找新疆电信“访聚惠”驻村工作队</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295997.html">图片报道2</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295998.html">丽江移动打造智慧校园网络</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_295999.html">电信扶贫队长忙赶集</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296000.html">新基建牵引智慧教育陕西电信与西安交大合作5G应用</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296001.html">中国联通研究院获中国SDN大会最佳案例奖</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296002.html">河北移动携手中车唐山公司打造“5G+智能制造”唐山样板</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296003.html">金川集团选矿厂“5G智慧车间”运行</a>
                            </li>                    </ul><h3><a href="/item/rmydb_2020_9_30_3.html">第03版：工业互联网</a>
                    </h3>
                    <ul>
                        <li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296004.html">上海：3年内建设100家智能工厂</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296005.html">江苏：出台交通运输新基建行动方案</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296006.html">山东：打造“四张网”，建设省级工业互联网综合服务平台</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296007.html">“5G+工业互联网”赋能水泥行业数字化转型</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296008.html">“智能+”时代催生新型工业互联网</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296009.html">安全是发展工业互联网的先决条件</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296010.html">科技服务业是制造业数字化转型方向之一</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296011.html">中小企业开创工业互联网发展的春天</a>
                            </li>                    </ul><h3><a href="/item/rmydb_2020_9_30_4.html">第04版：专题报道</a>
                    </h3>
                    <ul>
                        <li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296012.html">浙江移动实现 5G SA 规模应用</a>
                            </li><li style=" list-style:none; text-indent:10px;">
                                <a href="/article/rmydb_15749_296013.html">从贫困村到幸福村</a>
                            </li>                    </ul>            </div><div id="mCSB_2_scrollbar_vertical" class="mCSB_scrollTools mCSB_2_scrollbar mCS-light mCSB_scrollTools_vertical" style="display: none;"><div class="mCSB_draggerContainer"><div id="mCSB_2_dragger_vertical" class="mCSB_dragger" style="position: absolute; min-height: 0px; top: 0px; height: 0px;" oncontextmenu="return false;"><div class="mCSB_dragger_bar" style="line-height: 0px;"></div></div><div class="mCSB_draggerRail"></div></div></div></div></div>
        </li>
        <li>
            <span id="pastPaper" lay-key="1">往期报纸</span>
            <input type="text" id="pastInput" style="position:relative;visibility: hidden" lay-key="1">
        </li>
    </ul>
</div>
<!--公共头部结束-->
<div class="main-container clearfix">
    <div class="left">
        <div class="newspaper" id="newspaper">
            <img src="http://szbpic.cnii.com.cn/data/newspaper/78/38478/49/15749/image/2.jpg" alt="map" usemap="#news" border="0">
            <map name="news" id="news">
          
                 <area shape="rect" coords="5,40,215,141" href="/article/rmydb_15749_295996.html" data-href="/article/rmydb_15749_295996.html" target="_blank"><area shape="rect" coords="100,149,214,251" href="/article/rmydb_15749_295997.html" data-href="/article/rmydb_15749_295997.html" target="_blank"><area shape="rect" coords="100,261,215,299" href="/article/rmydb_15749_295998.html" data-href="/article/rmydb_15749_295998.html" target="_blank"><area shape="rect" coords="5,318,215,426" href="/article/rmydb_15749_295999.html" data-href="/article/rmydb_15749_295999.html" target="_blank"><area shape="rect" coords="223,44,305,138" href="/article/rmydb_15749_296000.html" data-href="/article/rmydb_15749_296000.html" target="_blank"><area shape="rect" coords="225,145,305,247" href="/article/rmydb_15749_296001.html" data-href="/article/rmydb_15749_296001.html" target="_blank"><area shape="rect" coords="225,253,303,335" href="/article/rmydb_15749_296002.html" data-href="/article/rmydb_15749_296002.html" target="_blank"><area shape="rect" coords="225,344,304,426" href="/article/rmydb_15749_296003.html" data-href="/article/rmydb_15749_296003.html" target="_blank">
            </map>
            <div id="hotArea">
                <div style="height:100%;"></div>
            </div>
            
               <a href="/item/rmydb_2020_9_30_1.html" class="btn prev"><span>上<br>一<br>版</span></a>                
                <a href="/item/rmydb_2020_9_30_3.html" class="btn next"><span>下<br>一<br>版</span></a>

        </div>
        <div class="title">第02版：综合新闻</div>
    </div>
    <div class="detail-content">
        <div class="title-container">
        	<h4></h4>
            <h2>图片报道2</h2>
            <h3></h3>
            <span class="date">
                          作者：黄彩琴 赵海燕/摄影报道   
             
            </span>
            <p class="date">
             出版时间：2020-09-30            </p>
            <p class="date">
             全文共260字
            </p>
           
            <p>
                <span class="decrease decrease-disable">A-</span>
                <span class="increase">A+</span>
            </p>
        </div>
        <div class="text">
            <div align="center"><br><font color="#008000" face="宋体"><img src="http://szbpic.cnii.com.cn/data/newspaper//78/38478/49/15749/article_images/6b2756f9d148d4cf8b9f2cd1fcaae246.jpg"><br><br></font></div><div align="left"><font color="#000000" face="宋体">　　近日，中国电信湖北鄂州分公司团委组织开展“网络改变生活”公益课堂进校园活动。在鄂州市鄂城区华山小学，电信团员青年讲解由“烽火传书”到5G时代的通信发展史，近百名留守学生踊跃举手发言，畅谈各自心中的5G未来时代。该校校长兴奋地说：“你们这个授课方式非常新颖，不但可以引导孩子健康使用网络，还可以培养孩子学习新科技的兴趣，这样的课程对孩子非常有益。”在这次主题为“天翼有爱翼起守护”手拉手“团建翼联”实践活动中，鄂州电信团委还向学校捐赠了课外书籍，鼓励同学们养成读好书、好读书的习惯。图为学生代表为青年团员佩戴红领巾。 </font></div>        </div>
        <div class="wxqrcode">
            <!-- <img src="/Tpl/public/cnii/img/1.png" alt="">
            <p>扫一扫，分享到微信朋友圈</p> -->
        </div>
        <p class="like">
            <!-- <span class="like-btn">0</span>
            <span class="unlike-btn">0</span> -->
        </p>
        <div class="detail-bottom">
            <!-- <div class="share">
                <a href="#"><img src="/Tpl/public/cnii/img/mulShare.png" alt=""></a>
                <a href="#"><img src="/Tpl/public/cnii/img/space.png" alt=""></a>
                <a href="#"><img src="/Tpl/public/cnii/img/sina.png" alt=""></a>
                <a href="#"><img src="/Tpl/public/cnii/img/baidu.png" alt=""></a>
                <a href="#"><img src="/Tpl/public/cnii/img/renren.png" alt=""></a>
            </div> -->
            <!-- <div class="print">
                <span class="print-file">打印正文</span>
            </div> -->
        </div>

    </div>
    <div class="float-wrap">
        <div>
            <a href="/home/rmydb.html"><img src="/Tpl/public/cnii/img/index-icon.png" alt=""></a>
        </div>
        <div>
            <img src="/Tpl/public/cnii/img/phone-icon.png" alt="">
            <p class="phone">(010)64963755</p>
        </div>
        <!-- <div>
            <img src="/Tpl/public/cnii/img/wx-icon.png" alt="">
            <p class="wx-code"><img src="/Tpl/public/cnii/img/1.png" alt=""></p>
        </div> -->
        <div class="top"><img src="/Tpl/public/cnii/img/to-top.png" alt=""></div>
    </div>
</div>


<div class="bmInfor" id="bmInfor">
    <ul>
        <li data-src="/article/rmydb_15749_295996.html">
                <span>有难事，找新疆电信“访聚惠”驻村工作队</span>
            </li><li data-src="/article/rmydb_15749_295997.html">
                <span>图片报道2</span>
            </li><li data-src="/article/rmydb_15749_295998.html">
                <span>丽江移动打造智慧校园网络</span>
            </li><li data-src="/article/rmydb_15749_295999.html">
                <span>电信扶贫队长忙赶集</span>
            </li><li data-src="/article/rmydb_15749_296000.html">
                <span>新基建牵引智慧教育陕西电信与西安交大合作5G应用</span>
            </li><li data-src="/article/rmydb_15749_296001.html">
                <span>中国联通研究院获中国SDN大会最佳案例奖</span>
            </li><li data-src="/article/rmydb_15749_296002.html">
                <span>河北移动携手中车唐山公司打造“5G+智能制造”唐山样板</span>
            </li><li data-src="/article/rmydb_15749_296003.html">
                <span>金川集团选矿厂“5G智慧车间”运行</span>
            </li>    </ul>
</div>
<!--公共尾部开始-->
<div class="footer">
    <div class="bottom-content">
        <div class="link">
        	<a href="http://www.miit.gov.cn/" target="_blank">中华人民共和国工业和信息化部 </a> | 
        	<a href="http://www.cac.gov.cn/" target="_blank">中共中央网络安全和信息化委员会办公室</a> | 
        	<a href="http://www.caict.ac.cn/" target="_blank">中国信息通信研究院</a> | 
        	<a href="http://www.caict.ac.cn/" target="_blank">中国通信企业协会</a> | 
        	<a href="http://www.china-cic.cn/" target="_blank">中国通信学会</a>     
        </div>
        <div class="link">
        	<a href="http://www.cnii.com.cn/sy/adRights/201910/t20191021_124860.html" target="_blank">广告服务</a>|
        	 <a href="http://www.cnii.com.cn/sy/adRights/201910/t20191021_124861.html" target="_blank">关于我们</a>|        
            <a href="http://www.cnii.com.cn/sy/adRights/201910/t20191021_124859.html" target="_blank">版权信息</a>|
            <a href="/user/register/rmydb.html">用户注册</a>|
            <a href="/buy/index/rmydb.html">购买阅读卡</a>
        </div>  
 		<div class="link">
        	 <a href="http://report.12377.cn:13225/toreportinputNormal_anis.do" target="_blank">网上有害信息举报专区</a>
            <a href="http://www.cyberpolice.cn/wfjb/" target="_blank">公安部网络违法犯罪举报网站 </a>        
        </div>
    </div>
    
   <div class="note">
         <p>版权所有2000-2020 &nbsp;&nbsp;人民邮电报社 &nbsp;&nbsp;服务电话：(010)64963755&nbsp;&nbsp; 违法和不良信息举报电话：(010)64963027&nbsp;&nbsp;   京ICP备19055921号-1</p>
  
   </div>
</div>

<script src="/Tpl/public/cnii/js/jquery-2.1.4.min.js"></script>
<script src="/Tpl/public/cnii/js/mCustomScrollbar.js"></script>
<script src="/Tpl/public/cnii/css/laydate/laydate.js"></script>
<script id="_trs_ta_js" src="//ta.trs.cn/c/js/ta.js?mpid=3218" async="async" defer="defer"></script>

<script>

        (function($){
            $(".content,.bmList,.btList").mCustomScrollbar({
                scrollInertia:80,
            });
    
            var nowDate = new Date();
            var year = nowDate.getFullYear();
            var month = nowDate.getMonth()+1;
            var date = nowDate.getDate();
            var orgname = 'rmydb';
          
           
    
            laydate.render({
                elem: '#pastInput',
                eventElem: '#pastPaper',
                max:'year+"-"+month+"-"+date',
                trigger: 'mouseover',
                showBottom:false,
                 value: "2020-09-30",
                isInitValue: true, 
                change:function(value,date){
                    var elem = $(".layui-laydate-content");
                    var temp_year = date.year;
                    var temp_month = date.month;
                    $.ajax({
                        type:"post",
                        url:"/home/index/getHistoryList",
                        data:{item_year:temp_year,item_month:temp_month},
                        dataType:"json",
                        success:function(data){
                            
                            if(data){
                                $.each(elem.find('tr'),function(trIndex,trElem){
                                $.each($(trElem).find('td'),function(tdIndex,tdElem){
                                    var ymd = $(tdElem).attr('lay-ymd');                          
                                    var index = $.inArray(ymd,data);
                                       if(index < 0){
                                           $(tdElem).addClass('laydate-disabled');
                                       }

                                })
                             })
                            }
                            
                         
                        }
                    })       
                },
                ready:function(value,date){
                    var pub_list = transArr([]);
                    var elem = $(".layui-laydate-content");
                    $.each(elem.find('tr'),function(trIndex,trElem){
                        $.each($(trElem).find('td'),function(tdIndex,tdElem){

                             var ymd = $(tdElem).attr('lay-ymd');                          
                               var index = $.inArray(ymd,pub_list);
                               if(index < 0){
                                   $(tdElem).addClass('laydate-disabled');
                               }

                        })
                    })
                },
                done:function(value,date){
                    var temp_array= [];
                    temp_array = value.split('-');
                   
                    var years = temp_array[0];
                    var month = temp_array[1];
                    var days = temp_array[2];
                    var url = '/item/'+orgname+'_'+years+'_'+month+'_'+days+'_1.html';

                    window.location.href = url;
    
                }
            });


            laydate.render({
                elem: '#past',
                eventElem: '#secpast',
                max:'year+"-"+month+"-"+date',
                trigger: 'mouseover',
                showBottom:false,
                value: "2020-09-30",
                isInitValue: true, 
                change:function(value,date){
                    var elem = $(".layui-laydate-content");
                    var temp_year = date.year;
                    var temp_month = date.month;
                    $.ajax({
                        type:"post",
                        url:"/home/index/getHistoryList",
                        data:{item_year:temp_year,item_month:temp_month},
                        dataType:"json",
                        success:function(data){
                            
                            if(data){
                                $.each(elem.find('tr'),function(trIndex,trElem){
                                $.each($(trElem).find('td'),function(tdIndex,tdElem){
                                    var ymd = $(tdElem).attr('lay-ymd');                          
                                    var index = $.inArray(ymd,data);
                                       if(index < 0){
                                           $(tdElem).addClass('laydate-disabled');
                                       }

                                })
                             })
                            }
                         
                        }
                    })       
            
                },
                ready:function(value){
                    var pub_list = transArr([]);
                    var elem = $(".layui-laydate-content");
                    $.each(elem.find('tr'),function(trIndex,trElem){
                        $.each($(trElem).find('td'),function(tdIndex,tdElem){

                             var ymd = $(tdElem).attr('lay-ymd');                          
                               var index = $.inArray(ymd,pub_list);
                               if(index < 0){
                                   $(tdElem).addClass('laydate-disabled');
                               }

                        })
                    })
                   
            
                },
                done:function(value,date){
                    var temp_array= [];
                    temp_array = value.split('-');
                    var years = temp_array[0];
                    var month = temp_array[1];
                    var days = temp_array[2];
                    var url = '/item/'+orgname+'_'+years+'_'+month+'_'+days+'_1.html';

                    window.location.href = url;
    
                }
            });
    
    
        })(jQuery);

 
        function transArr(obj) {
                var tem=[];
                $.each(obj, function(i) {
                    tem[i]=obj[i];
                });
                return tem;
            } 

    </script>


<script src="/Tpl/public/cnii/js/map.js"></script>
<script src="/Tpl/public/cnii/css/laydate/laydate.js"></script>
<!--公共尾部结束-->
<script>

    (function($){
        var fontSize = 15;
        $('.decrease').on('click',function(){
            $('.increase').removeClass('increase-disable');
            if(fontSize>15){
                fontSize-=2;
            }
            if(fontSize<=15){
                $(this).addClass('decrease-disable');
            }
            $('.text').css({'font-size':fontSize+'px'})
        });
        $('.increase').on('click',function(){
            $('.decrease').removeClass('decrease-disable');
            if(fontSize<19){
                fontSize+=2;
            }
            if(fontSize>=19){
                $(this).addClass('increase-disable');
            }
            $('.text').css({'font-size':fontSize+'px'})
        });

        //鼠标移入移出
        $('.float-wrap div').on('mouseover', function() {
            $(this).addClass('blue')
            $(this).find('p').show()
        })
        $('.float-wrap div').on('mouseout', function() {
            $(this).removeClass('blue');
            $(this).find('p').hide();
        })
        //返回顶部
        window.onscroll = function() {
            var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            if (scrollTop > 200) {
                $('.top').css('display', 'flex')
            } else {
                $('.top').hide()
            }
        }
        $('.top').on('click', function() {
            $('body,html').animate({
                scrollTop: 0
            }, 300)
        })
        //点赞
        $('.like-btn').on('click',function(){
            $(this).attr('disabled',true)
        });

        $('.unlike-btn').on('click',function(){
            $(this).attr('disabled',true)
        });
        //打印
        $('.print-file').on('click',function(){
            window.print()
        });

        var nowDate = new Date();
        var year = nowDate.getFullYear();
        var month = nowDate.getMonth()+1;
        var date = nowDate.getDate();

        laydate.render({
            elem: '#pastInput',
            eventElem: '#pastPaper',
            min:'2010-01-01',
            max:'year+"-"+month+"-"+date',
            trigger: 'click',
            done:function(value,date){
                alert(value)

            }
        });


    })(jQuery);

</script>

</body></html>
    
    '''
    import re
    brow = re.findall("出版时间：(\d{4}-\d{2}-\d{2})",wword)
    print(brow)

