# -*- coding: utf-8 -*-
import json
import re
import requests

hhtml = '''
<html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>烟草行业招投标信息平台</title>
<link rel="stylesheet" type="text/css" href="css/css.css">
<style type="text/css" abt="234"></style></head>
<body>
<!-------------------------头部--------------------------->

		<script>
	function keysearch() {
		var key = document.getElementById("key");
		var kgaoji = document.getElementById("kgaoji");
		kgaoji.href="https://search.tobaccobid.com/keyTender.action?keyName="+key.value+"&area=0&type=0&date=&infoType=1";
	}

	function allsearch() {
		var area = document.getElementById("area");
		var type = document.getElementById("type");
		var date = document.getElementById("date");
		var keyName = document.getElementById("keyName");
		var allgaoji = document.getElementById("allgaoji");
		allgaoji.href="https://search.tobaccobid.com/allTender.action?keyName="+keyName.value+"&area="+area.value+"&type="+type.value+"&date="+date.value+"&infoType=1";
	}
	function Login(){
		var checkbox1 = document.getElementById("checkbox1");
		var checkbox2 = document.getElementById("checkbox2");
		var username = document.getElementById("username").value;
		var password = document.getElementById("password").value;
		var code = document.getElementById("code").value;
		var yzm = document.getElementById("yzm").value;
		if(username==""){
			alert("请输入用户名！");
		}else if(password==""){
			alert("请输入密码！");
		}else if(yzm==""||code!=yzm){
			alert("验证码不正确！");
		}else{
			if(checkbox1.checked==true){
				setCookie("tendername",username);
			}
			if(checkbox1.checked==false){
				delCookie("tendername",username);
			}
			 
			if(checkbox2.checked==true){
				setCookie("tendername2",username);
				setCookie("tenderpwd2",password);
			}
			
			document.form1.submit();
		}
	}
	function loginout(){
		delCookie('tendername2');
		delCookie('tenderpwd2');
		document.getElementById("loginout").href="Loginout.action";
		}
	//两个参数，一个是cookie的名子，一个是值
	function setCookie(name,value){
		var Days = 30; //此 cookie 将被保存 30 天
		var exp = new Date(); //new Date("December 31, 9998");
		exp.setTime(exp.getTime() + Days*24*60*60*1000);
		document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
	}
	 //取cookies函数
	function getCookie(name){
		var arr = document.cookie.match(new RegExp("(^| )"+name+"=([^;]*)(;|$)"));
		if(arr != null) {
			return unescape(arr[2]); 
		}else{
			return null;
		}
	}
	//删除cookie
	function delCookie(name){
		var exp = new Date();
		exp.setTime(exp.getTime() );
		var cval=getCookie(name);
		if(cval!=null) {
			document.cookie= name + "="+cval+";expires="+exp.toGMTString();
		}
	}
	function creatcode(){
		var code ; //在全局 定义验证码   
	      code = "";   
	      var codeLength = 4;//验证码的长度   
	      var checkCode = document.getElementById("checkCode");   
	      var selectChar = new Array(0,1,2,3,4,5,6,7,8,9);//所有候选组成验证码的字符，当然也可以用中文的   
	          
	      for(var i=0;i<codeLength;i++){   
		    var charIndex = Math.floor(Math.random()*10);   
			code +=selectChar[charIndex];   
			document.getElementById("yz"+(i+1)).src="../images/"+selectChar[charIndex]+".jpg";
	      } 
	      document.getElementById("code").value=code;
		}
</script>



<div id="header">
	<div class="hy"><div class="y fr"><a href="#" class="hrefs" onclick="this.style.behavior='url(#default#homepage)';this.setHomePage('http://www.tobaccochina.com/');">设为首页</a><a href="mailto:ztb@tobaccochina.com">联系我们</a><a href="tencent://message/?uin=2654420072&amp;Site=&amp;Menu=yes" target="_blank">在线咨询</a></div><h3>欢迎访问烟草行业招投标信息平台! 
	 请<a href="http://WWW.tobaccobid.com/login.action">登录</a> <a href="https://search.tobaccobid.com/reg.jsp">免费注册</a>!  <a href="http://www.tobaccobid.com/ztb/www.tobaccobid.com/indexses.html">招标资料列表</a>
	
</h3></div>
<!-- <div style="width:1003px; height:90px; margin:0px auto 0px;" ><img src="../2014chunjie.jpg" width="1003" height="90" /></div>-->
    <div class="seach">
    <div class="logo fl"><a href="http://www.tobaccobid.com/web/index.html"><img src="../images/logo.jpg"></a></div>
        <div class="logo_r fr">
        	<div class="box">
            	<div id="tabs">
                	<ul>
                        <li onmouseover="change(0)" class="bg"><a href="#">全部</a></li>
                        <li onmouseover="change(1)"><a href="#">关键字</a></li> <li><a href="https://list.tobaccobid.com/allTender.action?keyName=&amp;area=0&amp;type=0&amp;date=0&amp;infoType=3"><b>中标搜索</b></a>
                    </li></ul>
                </div>
                <script language="javascript">
					function change(num){
						for(i=0;i<2;i++){
							document.getElementById("newsContents"+i).className="newsContents";
							document.getElementById("tabs").getElementsByTagName("li")[i].className="";
						}//在切换之前，用循环把所有的隐藏
						document.getElementById("newsContents"+num).className="newsContents blocks";//根据num的取值，把对应的显示
						document.getElementById("tabs").getElementsByTagName("li")[num].className="bg"
					}	
			    </script>
                 <div class="box1"><div id="newsContents0" class="newsContents blocks"><div class="xuan fl"><select name="area" id="area">
				    		<option value="0">-按地区-</option>
    		<option value="1">-上海-</option>
    		<option value="2">-江苏-</option>
    		<option value="3">-浙江-</option>
    		<option value="4">-安徽-</option>
    		<option value="5">-福建-</option>
    		<option value="6">-江西-</option>
    		<option value="7">-山东-</option>
    		
    		<option value="8">-北京-</option>
    		<option value="9">-天津-</option>
    		<option value="10">-河北-</option>
    		<option value="11">-内蒙古-</option>
    		<option value="12">-山西-</option>
    		
    		<option value="13">-黑龙江-</option>
    		<option value="14">-辽宁-</option>
    		<option value="15">-吉林-</option>
    		
    		<option value="16">-河南-</option>
    		<option value="17">-湖南-</option>
    		<option value="18">-湖北-</option>
    		
    		<option value="19">-云南-</option>
    		<option value="20">-西藏-</option>
    		<option value="21">-贵州-</option>
    		<option value="22">-重庆-</option>
    		<option value="23">-四川-</option>
    		
    		<option value="24">-甘肃-</option>
    		<option value="25">-宁夏-</option>
    		<option value="26">-青海-</option>
    		<option value="27">-陕西-</option>
    		<option value="28">-新疆-</option>
    		
    		<option value="29">-广东-</option>
    		<option value="30">-广西-</option>
    		<option value="31">-海南-</option>
				    	</select>
                        <select name="type" id="type">
						    <option value="0">-按招标类型-</option>
	    <option value="1">-工程基建-</option>
	    <option value="2">-信息化服务-</option>
	    <option value="3">-宣传促销-</option>
	    <option value="4">-辅料及配件-</option>
	    <option value="5">-农用物资-</option>
	    <option value="6">-办公用品-</option>
	    <option value="7">-消防器材-</option>
	    <option value="8">-劳保用品-</option>
		  <option value="9">-物流运输-</option>
							    <option value="10">-印刷设计-</option>
								  <option value="11">-物业安保-</option>
								  <option value="13">-机电设备-</option>
								    <option value="12">-其他-</option>
					    </select>
                        <select name="date" id="date">
				    	<option value="0">-按时间-</option>
				    	<option value="1">-一周内-</option>
				    	<option value="2">-一个月内-</option>
				    	<option value="3">-三个月内-</option>
				    	</select>
                        <input type="text" name="keyName" id="keyName" class="inputw">
                        </div>
                       <div class="sousuo fl"><a href="https://search.tobaccobid.com/" onclick="allsearch()" id="allgaoji"><img src="/images/sousuo-img.jpg"></a></div>
                      <div class="gao fr"><a href="https://search.tobaccobid.com/allTender.action?keyName=&amp;area=0&amp;type=0&amp;date=0&amp;infoType=1" target="_blank"><strong><b><u>高级搜索</u></b></strong></a><br></div>
                    </div>
                    <div id="newsContents1" class="newsContents">
                        <div class="xuan fl"><input type="text" value="" id="key" class="inputc"></div>
                       <div class="sousuo fl"><a href="https://search.tobaccobid.com/" onclick="keysearch()" id="kgaoji"><img src="/images/sousuo-img.jpg"></a></div>
           <div class="gao fr"><a href="http://search.tobaccobid.com/search.action?infoType=1" target="_blank"><strong><b><big><u>高级搜索</u></big></b></strong></a><br></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <ul class="nav">
    	<li><a href="http://www.tobaccobid.com/web/index.html">网站首页</a></li>
        <li><a href="http://www.tobaccobid.com/web/listsestb1.html">招标公告</a></li>
        <li><a href="http://info.TOBACCOBID.COM/listConsult.action?consultType=1">招标动态</a></li>
        <li><a href="http://www.tobaccobid.com/web/listseszb1.html">中标公示</a></li>
        <li><a href="http://info.TOBACCOBID.COM/listConsult.action?consultType=3">资料下载</a></li>
        <li><a href="http://info.TOBACCOBID.COM/listConsult.action?consultType=2">政策法规</a></li>
    </ul>
    <div class="box2">
    <script>
    	onload = function() {
   	 var code ; //在全局 定义验证码   
      code = "";   
      var codeLength = 4;//验证码的长度   
      var checkCode = document.getElementById("checkCode");   
      var selectChar = new Array(0,1,2,3,4,5,6,7,8,9);//所有候选组成验证码的字符，当然也可以用中文的   
          
      for(var i=0;i<codeLength;i++){   
	    var charIndex = Math.floor(Math.random()*10);   
		code +=selectChar[charIndex];   
		document.getElementById("yz"+(i+1)).src="../images/"+selectChar[charIndex]+".jpg";
      } 
      document.getElementById("code").value=code;
		var username = getCookie("tendername");
		var username2 = getCookie("tendername2");
		var password2 = getCookie("tenderpwd2");
		if(username!=null){
			document.getElementById("checkbox1").checked=true;
			document.getElementById("username").value=username;
		}
		if(username2!=null){
			//document.getElementById("checkbox1").checked=true;
			document.getElementById("username").value=username2;
			document.getElementById("password").value=password2;
			document.form1.submit();
		}
	}
</script>
										

	    <a href="http://www.tobaccobid.com/login.action"><img src="../images/dl.jpg" class="yz"></a>&nbsp;
	    <a href="http://reg.tobaccobid.com/reg.jsp" target="_blank"><img src="/images/zc.jpg" class="yz"></a>
	 
    
    </div>
</div>

<!-------------------------内容--------------------------->
<div id="mainbody1">
	<div class="nr17">
    	<div class="lef fl">
        	<div class="zbbg">
            	<div class="bt6"><a href="list.action?type=2&amp;tenderType=" class="fr">更多&gt;&gt;</a><h3>招标变更</h3></div>
                <ul class="n3">
                	<li><a href="detailChange.action?id=5272" target="_blank">吉林省烟草公司长春市公司七氟丙烷...</a></li>
                	<li><a href="detailChange.action?id=5271" target="_blank">湖北省烟草公司仙桃市公司基于“图...</a></li>
                	<li><a href="detailChange.action?id=5270" target="_blank">湖北省烟草公司仙桃市公司基于跨界...</a></li>
                	<li><a href="detailChange.action?id=5269" target="_blank">湖南省烟草公司郴州市公司关于物流...</a></li>
                	<li><a href="detailChange.action?id=5268" target="_blank">2021年门店牌匾标识更换工程终...</a></li>
                	<li><a href="detailChange.action?id=5267" target="_blank">广东烟草惠州市有限责任公司博罗县...</a></li>
                </ul>
            </div>
            <div class="zbbg1">
            	<div class="bt6"><a href="listConsult.action?consultType=1" class="fr">更多&gt;&gt;</a><h3>招标动态</h3></div>
                <ul class="n3">
                    	<li><a href="detailConsult.action?id=258&amp;consultType=1" target="_blank">江西中烟工业有限责任公司矿泉水采...</a></li>
                    	<li><a href="detailConsult.action?id=252&amp;consultType=1" target="_blank">江西中烟工业有限责任公司广丰卷烟...</a></li>
                    	<li><a href="detailConsult.action?id=251&amp;consultType=1" target="_blank">广东烟草河源市有限责任公司201...</a></li>
                    	<li><a href="detailConsult.action?id=240&amp;consultType=1" target="_blank">甘肃省局抓创新求突破着力推动规范...</a></li>
                    	<li><a href="detailConsult.action?id=239&amp;consultType=1" target="_blank">红云红河集团进一步加强工会采购规...</a></li>
                    	<li><a href="detailConsult.action?id=241&amp;consultType=1" target="_blank">江西中烟完成2016年度采购计划...</a></li>
                </ul>
            </div>
            
        </div>
        <div class="righ1 fr">
        	<div class="y2">
        	<h3>您当前位置：<a href="index.html">首页</a> &gt; 
        	招标公告
        	</h3></div>
          <div class="y3"><p><span>2020-2022年自主品牌条、盒包装纸（一）GXYLG20191070-N招标公告</span></p></div>
            
			<div style="border-bottom: 1px #FC6 solid; margin:4px 30px;text-align: right; padding-bottom:5px; padding-right:70px;">开标日期：2019-11-22   &nbsp;发布日期：2019-11-01</div>
			<div class="y4"><p><strong>招标代理：</strong><span>云之龙招标集团有限公司</span></p></div>
			
			<div class="y4"><p><strong>招标类型：</strong><span>其他</span></p></div>
            <div class="y4"><p style="text-indent:28px"><span style="font-family: 宋体">&nbsp;</span></p><p style="margin-left:6px;text-indent:28px"><span style="font-family: 宋体">云之龙招标集团有限公司受广西中烟工业有限责任公司的委托，拟对2020-2022年自主品牌条、盒包装纸（一）进行国内公开招标，现将有关事项公告如下： </span></p><h3 style="line-height:normal"><span style="font-size: 14px;font-family: 宋体">．</span><span style="font-size: 14px;font-family: 宋体">招标项目名称及内容</span></h3><p style="text-indent:28px"><span style="font-family: 宋体">项目名称：2020-2022年自主品牌条、盒包装纸（一）</span></p><p style="text-indent:28px"><span style="font-family: 宋体">项目编号：GXYLG20191070-N</span></p><p style="text-indent:28px"><span style="font-family: 宋体">招标内容：自主品牌条、盒包装纸一批</span><span style="font-family: 宋体">，</span><span style="font-family: 宋体">具体内容详见招标文件。</span></p><h3 style="line-height:normal"><span style="font-size: 14px;font-family: 宋体">．投标人资格要求</span></h3><p><span style="font-family: 宋体">2.1 </span><span style="font-family: 宋体">本次招标要求投标人须具备以下资格。</span></p><p><span style="font-family: 宋体">2.1.1</span><span style="font-family: 宋体">投标人必须是中华人民共和国境内注册（指按国家有关规定要求注册的），生产或经营本次招标货物，具备独立法人资格的供应商。</span></p><p><span style="font-family: 宋体">2.1.2</span><span style="font-family: 宋体">本次招标要求投标人须提供有效的企业法人营业执照，印刷许可证。</span></p><p><span style="font-family: 宋体">2.1.3</span><span style="font-family: 宋体">生产制造设备和专业技术能力必须达到招标项目生产工艺要求；具备保障烟标及其相关原材料的质量检测设备和检测人员的质量保障能力，产品必须达到规定的技术要求和质量要求。</span></p><p><span style="font-family: 宋体">2.2</span><span style="font-family: 宋体">法定代表人为同一个人的两个或两个以上法人、母公司及其全资子公司或其控股子公司，只能有一家单位参加投标，否则均按无效投标处理。</span></p><p><span style="font-family: 宋体">2.3</span><span style="font-family: 宋体">投标人的投标标的如果涉及知识产权（包括专利、商标和著作等）使用，投标人应在投标文件中提供相关知识产权的权属证明或合法使用证明复印件。</span></p><p><span style="font-family: 宋体">2.4</span><span style="font-family: 宋体">本次招标不接受联合体投标，</span><span style="font-family: 宋体">并不得转包或非法分包</span><span style="font-family: 宋体">。</span></p><h3 style="line-height:normal"><span style="font-size: 14px;font-family: 宋体">．招标文件的获取</span></h3><p><span style="font-family: 宋体">3.1 </span><span style="font-family: 宋体">凡有意参加投标者，请于2019年11月1日至2019年11月8日（法定公休日、法定节假日除外），每日上午8时至12时，下午3时至6时（北京时间，下同）, 持单位介绍信、</span><span style="font-family: 宋体">法</span><span style="font-family: 宋体">人授权委托书原件和委托代理人身份证复印件（委托代理时），法定代表人身份证、营业执照副本、2.1条款要求的其他资质证明材料</span><span style="font-family: 宋体">（以上资料均为</span><span style="font-family: 宋体">复印件，</span><span style="font-family: 宋体">要求加盖公章）</span><span style="font-family: 宋体">到到云之龙招标集团有限公司（广西南宁市新民路34-18号中明大厦11楼A座）购买招标文件。</span></p><p><span style="font-family: 宋体">3.2 </span><span style="font-family: 宋体">招标文件每套售价300元，售后不退。</span></p><p><span style="font-family: 宋体">3.3 </span><span style="font-family: 宋体">邮购招标文件的，需另加手续费（含邮费）50元。招标人在收到3.1条款要求的全部报名资料并审核通过和邮购款（含手续费）后2个工作日内寄送。</span></p><h3 style="line-height:normal"><span style="font-size: 14px;font-family: 宋体">．投标文件的递交</span></h3><p><span style="font-family: 宋体">4.1 </span><span style="font-family: 宋体">投标文件递交的截止时间（投标截止时间，下同）为2019年11月22 日9时00分，地点为广西南宁市新民路34-18号中明大厦11楼E座云之龙招标集团有限公司。</span></p><p><span style="font-family: 宋体">4.2 </span><span style="font-family: 宋体">逾期送达的或者未送达指定地点的投标文件，招标人不予受理。</span></p><h3 style="line-height:normal"><span style="font-size: 14px;font-family: 宋体">．发布公告的媒介</span></h3><p><span style="font-family: 宋体">本本次招标公告同时在中国采购与招标网www.chinabidding.com.cn、广西中烟工业有限责任公司网www.gxzygygs.com、烟草行业招投标信息平台www.tobaccochina.net、云之龙招标集团网www.gxyunlong.cn上发布。</span></p><h3 style="line-height:normal"><span style="font-size: 14px;font-family: 宋体">．</span><span style="font-size: 14px;font-family: 宋体">代理招标机构其他信息</span></h3><p style="text-indent:28px"><span style="font-family: 宋体">&nbsp; </span><span style="font-family: 宋体">招标代理机构：云之龙招标集团有限公司</span></p><p style="text-indent:28px"><span style="font-family: 宋体">&nbsp; </span><span style="font-family: 宋体">地&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 址：南宁市新民路34-18号中明大厦12楼D座</span></p><p style="text-indent:42px"><span style="font-family: 宋体">邮&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 编：530012</span></p><p style="text-indent:28px"><span style="font-family: 宋体">&nbsp; </span><span style="font-family: 宋体">联&nbsp;&nbsp; 系&nbsp;&nbsp; 人：何玫、黄及红&nbsp;&nbsp; </span></p><p style="text-indent:28px"><span style="font-family: 宋体">&nbsp; </span><span style="font-family: 宋体">电&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 话：0771-2618118、2618199</span></p><p style="text-indent:28px"><span style="font-family: 宋体">&nbsp; </span><span style="font-family: 宋体">传&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 真：0771-2808596</span></p><p style="text-indent:28px"><span style="font-family: 宋体">&nbsp; </span><span style="font-family: 宋体">开 户 银 行：</span><span style="font-family: 宋体">中国银行广西南宁市民主支行</span></p><p style="text-indent:43px"><span style="font-family: 宋体">开户名称：云之龙招标集团有限公司</span></p><p style="text-indent:43px"><span style="font-family: 宋体">账号：623660979180（此账户为购买招标文件和交纳服务费专用）</span></p><p style="text-indent:42px"><span style="font-family: 宋体">开户行行号：104611010017</span></p><p style="text-indent:28px"><span style="font-family: 宋体">&nbsp;</span></p><p style="text-indent:28px"><span style="font-family: 宋体">&nbsp;</span></p><p style="text-indent:28px"><span style="font-family: 宋体">&nbsp; </span></p><p style="text-align:center;text-indent:28px"><span style="font-family: 宋体">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2019</span><span style="font-family: 宋体">年11 月1 日</span></p><p><span style="font-family: 宋体">&nbsp;</span></p><p><br></p></div>
        </div>
    </div>
</div>
<!-------------------------脚步--------------------------->
﻿
<div id="footer"><div class="nr16"><div class="log fl"><a href="http://www.tobaccochina.com"><img src="../images/yc.jpg"></a></div><div class="rig fl">Copyright@1997-2021 by <a href="http://www.tobaccochina.com">TobaccoChina Online LLC.</a>本网站所有内容均受版权保护<br>未经版权所有人明确的书面许可，不得以任何方式或媒体翻印或转载本网站的部分或全部内容</div></div>
	<span class="date" style="position:relative; top:-10px;">       <a href="http://www.beian.miit.gov.cn">京ICP备17042229号-2</a>    <a href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11011502003946" target="_blank"> 京公网安备11011502003946</a></span>
</div>


</body></html>
'''

if __name__ == '__main__':
	import datetime, time

	start = time.perf_counter()
	hhtml.replace('Content-Type', '')

	end = time.perf_counter()
	result = end - start
	print(result*1000)
