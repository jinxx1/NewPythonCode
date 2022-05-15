import os
import re

from crawltools import getBetweenDayList
from bs4 import BeautifulSoup


wordd = '''<div class="protect" id="noticeArea">
<style type="text/css">
        #noticeArea { line-height:32px; font-size: 16px;text-align: justify;font-family: '宋体';word-break: break-all;}
        #noticeArea h1, #noticeArea h2, #noticeArea h3, #noticeArea h4, #noticeArea h5, #noticeArea h6{ line-height:2; }
        #noticeArea  *{padding:0; margin:0;}
        #noticeArea  .focuscontent{ color:#337ab7;}
        #noticeArea  strong{ font-weight: bold;}
        #noticeArea  h2{font-size: 24px; text-align: center; margin-bottom: 20px;text-align: left;}
        #noticeArea  h3{font-size: 18px;font-weight: normal; text-align: left;}
        #noticeArea  h4{font-size: 16px;font-weight: normal; line-height: 50px; margin-top: 10px; text-align: left;}
        #noticeArea  h5{text-indent: 32px;font-size: 16px;font-weight: normal; text-align: left;}
        #noticeArea  h6{font-size: 16px;font-weight: normal; text-align: left;}
        #noticeArea  pre{font-size: 16px;background: none;border: none;line-height: 32px;}
        #noticeArea  p{ text-indent: 32px; font-size: 16px; line-height: 32px;}
        #noticeArea  table{font-size: 16px;border-collapse: collapse; border-spacing: 0; width:100%;margin:10px auto; word-break: normal; line-height: 24px;}
        #noticeArea  table tr td{border-collapse: collapse; border:1px solid #333;text-align: center;padding: 5px 8px; word-break: break-all;}
        #noticeArea  table tr th{ font-weight: bold; text-align: center; border:1px solid #333;padding: 5px 8px; word-break: break-all;}
        #noticeArea  table tr{height: 32px; word-break: break-all;}
        #noticeArea .innercontent{padding-left: 32px;}
        #noticeArea .cleardom{clear: both;height: 0;line-height: 0;overflow: hidden;}
        #noticeArea .alignright{ text-align: right;word-break: normal;}
        @media print {
            #noticeArea { font-family: '宋体'; line-height:1.8; font-size: 18px;text-align: justify;word-break: break-all;}
            #noticeArea  *{padding:0; margin:0;}
            #noticeArea h1, #noticeArea h2, #noticeArea h3, #noticeArea h4, #noticeArea h5, #noticeArea h6{ line-height: 2; }
            #noticeArea  .focuscontent{ color:#337ab7;}
            #noticeArea  h2{font-size: 34px; text-align: center; margin-bottom: 25px;font-family: SimHei; text-align: left;}
            #noticeArea  h3{font-size: 24px; font-weight: normal; text-align: left;}
            #noticeArea  h4{font-size: 21px; font-weight: normal; text-align: left;}
            #noticeArea  h5{font-size: 18px; text-indent: 36px; font-weight: normal; text-align: left;}
            #noticeArea  h6{font-size: 16px;font-weight: normal; text-align: left;}
                  #noticeArea  pre{font-size: 18px;background: none;border: none;line-height: 1.8;}
            #noticeArea  p{ text-indent: 36px; font-size: 18px; line-height: 32px;}
            #noticeArea  table{font-size: 16px;border-collapse: collapse; border-spacing: 0; width:100%;margin:15px auto; word-break: normal; line-height: 24px;}
            #noticeArea  table tr td{border-collapse: collapse; border:1px solid #333;text-align: center;padding: 2px 6px; word-break: break-all;}
            #noticeArea  table tr th{ font-weight: bold; text-align: center;padding: 2px 6px; word-break: break-all;}
            #noticeArea  table tr{height: 32px; word-break: break-all;}
            #noticeArea .innercontent{padding-left: 32px;}
            #noticeArea .cleardom{clear: both;height: 0;line-height: 0;overflow: hidden;}
            #noticeArea .alignright{ text-align: right;word-break: normal;}
            }
#noticeArea { }
@media print {
#noticeArea { }
}
</style>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<p data-v-6b13d514=""></p>
<h4><strong>一、项目基本情况</strong></h4>
<p>原公告的采购项目编号：BTZCQSS-C-G-220014</p>
<p>原公告的采购项目名称：二零二北环路整体罩面工程</p>
<p>首次公告日期：2022年03月19日  </p>
<h4><strong>二、更正信息：</strong></h4>
<p></p><p style="text-indent:32px;">更正事项：采购公告</p>
<div style="text-indent:32px; float: left;">更正原因：</div>
<div style="float: none;margin-left: 110px;">
	<span>因疫情反复原因变更开标方式</span>
</div>
<div class="cleardom"></div>
<p style="text-indent:32px;">更正内容：</p>

<div class="innercontent"><p>开标方式变由现场网上开标变更为远程开标</p>
</div>
<p style="text-indent:32px;">其他内容不变</p>
<p style="text-indent:32px;">更正日期：<span name="releaseDateSpan">2022年03月23日</span></p><p></p>                 
<h4><strong>三、其他补充事项</strong></h4>
<div class="otherSupplement-otherSupplement _notice_content_otherSupplement-otherSupplement dynamic-form-editor" id="_notice_content_otherSupplement-otherSupplement">
	
	<div><p>无</p>
</div>
	
</div>
<h4><strong>四、凡对本次公告内容提出询问，请按以下方式联系。</strong></h4>
<div class="innercontent">
<h6>1.釆购人信息</h6>
<p>名称：<span class="u-content noticePurchase-purchaserOrgName _notice_content_noticePurchase-purchaserOrgName dynamic-form-editor" id="_notice_content_noticePurchase-purchaserOrgName">包头市青山区住房和城乡建设局</span></p>
<p>地址：<span class="u-content noticePurchase-purchaserOrgAddress _notice_content_noticePurchase-purchaserOrgAddress dynamic-form-editor" id="_notice_content_noticePurchase-purchaserOrgAddress">青东路与文学道交叉口</span></p>
<p>联系方式：<span class="u-content noticePurchase-purchaserLinkTel _notice_content_noticePurchase-purchaserLinkTel dynamic-form-editor" id="_notice_content_noticePurchase-purchaserLinkTel">0472-3612285</span></p>
<h6>2.釆购代理机构信息</h6>
<p>名称：<span class="u-content noticeAgency-agencyName _notice_content_noticeAgency-agencyName dynamic-form-editor" id="_notice_content_noticeAgency-agencyName">内蒙古金晨建设项目管理有限公司</span></p>
<p>地址：<span class="u-content noticeAgency-agentAddress _notice_content_noticeAgency-agentAddress dynamic-form-editor" id="_notice_content_noticeAgency-agentAddress">内蒙古自治区包头市青山区少先路2号商会大厦2008</span></p>
<p>联系方式：<span class="u-content noticeAgency-agentLinkTel _notice_content_noticeAgency-agentLinkTel dynamic-form-editor" id="_notice_content_noticeAgency-agentLinkTel">18247245248</span></p>
<h6>3.项目联系方式 </h6>
<p>项目联系人：<span class="u-content projectContact-managerName _notice_content_projectContact-managerName dynamic-form-editor" id="_notice_content_projectContact-managerName">徐工</span></p>
<p>电话：<span class="u-content projectContact-managerLinkPhone _notice_content_projectContact-managerLinkPhone dynamic-form-editor" id="_notice_content_projectContact-managerLinkPhone">18247245248</span></p>
</div>
<p style="text-align: right; ">内蒙古金晨建设项目管理有限公司</p>
<p style="text-align: right; "></p><p style="text-align:right;" name="releaseDateSpan">2022年03月23日</p><br><p></p>
</div><div>
	<style type="text/css">
		a {color: #337ab7;text-decoration: none;transition: 0.5 s;background-color: transparent;
		a:focus,a:hover {text-decoration: none;color: #23527c;}
		a:focus {outline: 5px auto -webkit-focus-ring-color;outline-offset: -2px;}
		a:active, a:hover {outline: 0;}
	</style>
  <span style="margin-left: 4px;">相关附件：</span> 
  <br> 
  <div style="margin-left: 22px;"> 
    <a href="http://39.104.85.103/gpx-bid-file/150204/gpx-tender/2022/3/14/402881cd7f828544017f8612f1cb358f.zip?accessCode=8c8028d694353382f3f361d1fd9b75b9">二零二北环路整体罩面工程--清单导出件.zip</a> 
  </div> 
  <div style="margin-left: 22px;"> 
    <a href="http://39.104.85.103/gpx-bid-file/150204/gpx-tender/2022/3/14/402881cc7f82850a017f8613f97647b4.zip?accessCode=e4c5146573f84d115979b44df4a34c1c">图纸.zip</a> 
  </div> 
</div></div>
                                <hr style="margin-top:30px;">
                <div class="title-box">
                    <p>包头市青山区住房和城乡建设局二零二北环路整体罩面工程竞争性磋商公告</p>
                </div>
                <div><div class="protect" id="noticeArea">
<style type="text/css">
        #noticeArea { line-height:32px; font-size: 16px;text-align: justify;font-family: '宋体';word-break: break-all;}
        #noticeArea h1, #noticeArea h2, #noticeArea h3, #noticeArea h4, #noticeArea h5, #noticeArea h6{ line-height:2; }
        #noticeArea  *{padding:0; margin:0;}
        #noticeArea  .focuscontent{ color:#337ab7;}
        #noticeArea  strong{ font-weight: bold;}
        #noticeArea  h2{font-size: 24px; text-align: center; margin-bottom: 20px;text-align: left;}
        #noticeArea  h3{font-size: 18px;font-weight: normal; text-align: left;}
        #noticeArea  h4{font-size: 16px;font-weight: normal; line-height: 50px; margin-top: 10px; text-align: left;}
        #noticeArea  h5{text-indent: 32px;font-size: 16px;font-weight: normal; text-align: left;}
        #noticeArea  h6{font-size: 16px;font-weight: normal; text-align: left;}
        #noticeArea  pre{font-size: 16px;background: none;border: none;line-height: 32px;}
        #noticeArea  p{ text-indent: 32px; font-size: 16px; line-height: 32px;}
        #noticeArea  table{font-size: 16px;border-collapse: collapse; border-spacing: 0; width:100%;margin:10px auto; word-break: normal; line-height: 24px;}
        #noticeArea  table tr td{border-collapse: collapse; border:1px solid #333;text-align: center;padding: 5px 8px; word-break: break-all;}
        #noticeArea  table tr th{ font-weight: bold; text-align: center; border:1px solid #333;padding: 5px 8px; word-break: break-all;}
        #noticeArea  table tr{height: 32px; word-break: break-all;}
        #noticeArea .innercontent{padding-left: 32px;}
        #noticeArea .cleardom{clear: both;height: 0;line-height: 0;overflow: hidden;}
        #noticeArea .alignright{ text-align: right;word-break: normal;}
        @media print {
            #noticeArea { font-family: '宋体'; line-height:1.8; font-size: 18px;text-align: justify;word-break: break-all;}
            #noticeArea  *{padding:0; margin:0;}
            #noticeArea h1, #noticeArea h2, #noticeArea h3, #noticeArea h4, #noticeArea h5, #noticeArea h6{ line-height: 2; }
            #noticeArea  .focuscontent{ color:#337ab7;}
            #noticeArea  h2{font-size: 34px; text-align: center; margin-bottom: 25px;font-family: SimHei; text-align: left;}
            #noticeArea  h3{font-size: 24px; font-weight: normal; text-align: left;}
            #noticeArea  h4{font-size: 21px; font-weight: normal; text-align: left;}
            #noticeArea  h5{font-size: 18px; text-indent: 36px; font-weight: normal; text-align: left;}
            #noticeArea  h6{font-size: 16px;font-weight: normal; text-align: left;}
                  #noticeArea  pre{font-size: 18px;background: none;border: none;line-height: 1.8;}
            #noticeArea  p{ text-indent: 36px; font-size: 18px; line-height: 32px;}
            #noticeArea  table{font-size: 16px;border-collapse: collapse; border-spacing: 0; width:100%;margin:15px auto; word-break: normal; line-height: 24px;}
            #noticeArea  table tr td{border-collapse: collapse; border:1px solid #333;text-align: center;padding: 2px 6px; word-break: break-all;}
            #noticeArea  table tr th{ font-weight: bold; text-align: center;padding: 2px 6px; word-break: break-all;}
            #noticeArea  table tr{height: 32px; word-break: break-all;}
            #noticeArea .innercontent{padding-left: 32px;}
            #noticeArea .cleardom{clear: both;height: 0;line-height: 0;overflow: hidden;}
            #noticeArea .alignright{ text-align: right;word-break: normal;}
            }
#noticeArea { }
@media print {
#noticeArea { }
}
</style>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<p data-v-6b13d514=""></p>

<div style="border: 1px solid black;padding: 12px;border-collapse:collapse;line-height: 28px;width: 98%;margin: 10px auto">
<h6><strong>
项目概况
</strong>
</h6>
<p>
<span>二零二北环路整体罩面工程</span>采购项目的潜在供应商应在<span class="noticeGetFile-getBidFileAddress _notice_content_noticeGetFile-getBidFileAddress content dynamic-form-editor">内蒙古自治区政府采购网</span>获取采购文件，并于<span class="noticePurchaseTime-noticePurchaseTime _notice_content_noticePurchaseTime-noticePurchaseTime bidFileSubmitTime dynamic-form-editor">
	
	2022年03月31日 09时50分
</span>（北京时间）前提交响应文件。
</p>
</div>
<h4><strong>一、项目基本情况</strong></h4>
<p>项目编号：BTZCQSS-C-G-220014</p>
<p>项目名称：二零二北环路整体罩面工程</p>
<p>采购方式：竞争性磋商</p>
<p>预算金额：1,508,658.00元</p>
<p>采购需求：</p>
<div class="noticeDemandExternal-noticeDemandExternal _notice_content_noticeDemandExternal-noticeDemandExternal dynamic-form-editor" id="_notice_content_noticeDemandExternal-noticeDemandExternal">
	<div id="noticeDemandExternal">
	<style type="text/css">
        #noticeDemandExternal { line-height:32px; font-size: 16px;text-align: justify;font-family: '宋体';}
        #noticeDemandExternal h1, #noticeDemandExternal h2, #noticeDemandExternal h3, #noticeDemandExternal h4, #noticeDemandExternal h5, #noticeDemandExternal h6{ line-height:2; }
        #noticeDemandExternal  *{padding:0; margin:0;}
        #noticeDemandExternal  .focuscontent{ color:#337ab7;}
        #noticeDemandExternal  strong{ font-weight: bold;}
        #noticeDemandExternal  h2{font-size: 24px; text-align: center; margin-bottom: 20px;}
        #noticeDemandExternal  h3{font-size: 18px;font-weight: normal;}
        #noticeDemandExternal  h4{font-size: 16px;font-weight: normal; line-height: 50px; margin-top: 10px;}
        #noticeDemandExternal  h5{text-indent: 32px;font-size: 16px;font-weight: normal;}
        #noticeDemandExternal  h6{font-size: 16px;font-weight: normal;}
        #noticeDemandExternal  pre{font-size: 16px;background: none;border: none;line-height: 32px;}
        #noticeDemandExternal  p{ text-indent: 32px; font-size: 16px; line-height: 32px;}
        #noticeDemandExternal  table{font-size: 16px;border-collapse: collapse; border-spacing: 0; width:100%;margin:10px auto;word-break: normal; line-height: 24px;}
        #noticeDemandExternal  table tr td{border-collapse: collapse; border:1px solid #333;text-align: center;padding: 5px 8px;}
        #noticeDemandExternal  table tr th{ font-weight: bold; text-align: center; border:1px solid #333;padding: 5px 8px;}
        #noticeDemandExternal  table tr{
        height: 32px;}
        #noticeDemandExternal .innercontent{padding-left: 32px;}
        #noticeDemandExternal .cleardom{clear: both;height: 0;line-height: 0;overflow: hidden;}
        #noticeDemandExternal .alignright{ text-align: right;word-break: normal;}
        @media print {
            #noticeDemandExternal { font-family: '宋体'; line-height:1.8; font-size: 18px;text-align: justify;}
            #noticeDemandExternal  *{padding:0; margin:0;}
            #noticeDemandExternal h1, #noticeDemandExternal h2, #noticeDemandExternal h3, #noticeDemandExternal h4, #noticeDemandExternal h5, #noticeDemandExternal h6{ line-height: 2; }
            #noticeDemandExternal  .focuscontent{ color:#337ab7;}
            #noticeDemandExternal  h2{font-size: 34px; text-align: center; margin-bottom: 25px;font-family: SimHei; }
            #noticeDemandExternal  h3{font-size: 24px; font-weight: normal;}
            #noticeDemandExternal  h4{font-size: 21px; font-weight: normal;}
            #noticeDemandExternal  h5{font-size: 18px; text-indent: 36px; font-weight: normal;}
            #noticeDemandExternal  h6{font-size: 16px;font-weight: normal;}
                  #noticeDemandExternal  pre{font-size: 18px;background: none;border: none;line-height: 1.8;}
            #noticeDemandExternal  p{ text-indent: 36px; font-size: 18px; line-height: 32px;}
            #noticeDemandExternal  table{font-size: 16px;border-collapse: collapse; border-spacing: 0; width:100%;margin:15px auto; word-break: normal; line-height: 24px;}
            #noticeDemandExternal  table tr td{border-collapse: collapse; border:1px solid #333;text-align: center;padding: 2px 6px; }
            #noticeDemandExternal  table tr th{ font-weight: bold; text-align: center;padding: 2px 6px;}
            #noticeDemandExternal  table tr{
                height: 32px;}
            #noticeDemandExternal .innercontent{padding-left: 32px;}
            #noticeDemandExternal .cleardom{clear: both;height: 0;line-height: 0;overflow: hidden;}
            #noticeDemandExternal .alignright{ text-align: right;word-break: normal;}
            }
    </style>
	<div class="innercontent">
	<p class="u-content">合同包1(二零二北环路 整体罩面工程):</p>
	<p style="text-indent:42px;">合同包预算金额：<span class="u-content">1,508,658.00元</span></p>
	
	<table width="100%" border="1" cellspacing="0">
		<thead>
			<tr style="height:36.4pt">
				<th style="width:80px;">品目号</th>
				<th style="width:300px;">品目名称</th>
				<th style="width:300px;">采购标的</th>
				<th style="width:100px;">数量（单位）</th>
				<th style="width:200px;">技术规格、参数及要求</th>
				<th style="width:120px;">品目预算(元)</th>
				<th style="width:120px;">最高限价(元)</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>1-1</td>
				<td>其他建筑工程</td>
				<td>1508658.00</td>
				<td>1(项)</td>
				<td>详见采购文件</td>
				<!-- 品目预算 -->
				<td class="alignright">
					
					<span>1,508,658.00</span>
				</td>
				<!-- 最高限价 -->
				<td class="alignright">
					<span>-</span>
					
				</td>
			</tr>
		</tbody>
	</table>
	<div>
		
		
	</div>
	<div>
		
		<p style="text-indent:42px;">
			本合同包<span class="u-content">不接受</span>联合体投标
		</p>
	</div>
	<div>
		<p style="text-indent:42px;">
			合同履行期限：<span class="u-content">自合同签订之日起13个月</span>
		</p>
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
</div>
</div>
	</div>
<h4><strong>二、申请人的资格要求：</strong></h4>
<div class="clauseLegalPackage-clauseLegalPackage _notice_content_clauseLegalPackage-clauseLegalPackage dynamic-form-editor" id="_notice_content_clauseLegalPackage-clauseLegalPackage">
<p>1.满足《中华人民共和国政府釆购法》第二十二条规定：</p>
<p>（1）具有独立承担民事责任的能力；</p>
<p>（2）具有良好的商业信誉和健全的财务会计制度；</p>
<p>（3）具有履行合同所必需的设备和专业技术能力；</p>
<p>（4）有依法缴纳税收和社会保障资金的良好记录；</p>
<p>（5）参加政府采购活动前三年内，在经营活动中没有重大违法记录；</p>
<p>（6）法律、行政法规规定的其他条件。</p>
<p>2.落实政府采购政策需满足的资格要求：

<span class="u-content">无。</span>
</p>
<p>3.本项目的特定资格要求：</p><div class="innercontent">
  <p>合同包1(二零二北环路 整体罩面工程)特定资格要求如下:</p>
  <div>
	<p>(1)响应供应商资质：需具有市政公用工程施工总承包三级及以上资质并具有有效的安全生产许可证。 项目负责人资质：需具有市政工程注册二级建造师并具有有效的安全考核证书。</p>
  </div>
</div><p></p>
</div>
<h4><strong>三、获取采购文件</strong></h4>
<p>时间：<span class="noticePurchaseTime-noticePurchaseTime _notice_content_noticePurchaseTime-noticePurchaseTime dynamic-form-editor" id="_notice_content_noticePurchaseTime-noticePurchaseTime"><span class="u-content">
	
	2022年03月19日
</span>至<span class="u-content">
	
	2022年03月25日
</span>，每天上午<span class="u-content">
	
	00:00:00
</span>至<span class="u-content">
	
	12:00:00
</span>，下午<span class="u-content">
	
	12:00:00
</span>至<span class="u-content">
	
	23:59:59
</span>（北京时间,法定节假日除外）</span></p>
<p>地点：<span class="u-content noticeGetFile-getBidFileAddress _notice_content_noticeGetFile-getBidFileAddress dynamic-form-editor" id="_notice_content_noticeGetFile-getBidFileAddress">内蒙古自治区政府采购网</span></p>
<p>方式：在线获取。获取采购文件时，需登录“政府采购云平台”，按照“执行交易→应标→项目应标→未参与项目”步骤，填写联系人相关信息确认参与后，即为成功“在线获取”。</p>
<p>售价：<span class="u-content noticeGetFile-bidFilePrice _notice_content_noticeGetFile-bidFilePrice dynamic-form-editor" id="_notice_content_noticeGetFile-bidFilePrice">
	
	免费获取
	
</span></p>
<h4><strong>四、响应文件提交</strong></h4>
<p>截止时间：<span class="u-content noticePurchaseTime-noticePurchaseTime _notice_content_noticePurchaseTime-noticePurchaseTime bidFileSubmitTime3 dynamic-form-editor">
	
	2022年03月31日 09时50分00秒
</span>（北京时间）</p>
<p>地点：<span class="u-content noticeBidTime-bidFileSubmitAddress _notice_content_noticeBidTime-bidFileSubmitAddress dynamic-form-editor" id="_notice_content_noticeBidTime-bidFileSubmitAddress"> 内蒙古自治区政府采购网（政府采购云平台）</span>
</p>
<h4><strong>五、开启</strong></h4>
<p>时间：<span class="u-content  noticePurchaseTime-noticePurchaseTime _notice_content_noticePurchaseTime-noticePurchaseTime bidOpenTime1 dynamic-form-editor">
	
	2022年03月31日 09时50分00秒
</span>（北京时间）</p>
<p>地点：<span class="noticeBidTime-bidAddress _notice_content_noticeBidTime-bidAddress dynamic-form-editor" id="_notice_content_noticeBidTime-bidAddress">内蒙古自治区包头市市辖区包头市九原区建华南路公共资源交易大厅3楼第六开标室</span></p>
<h4><strong>六、公告期限</strong></h4>
<p>自本公告发布之日起<span class="u-content noticeTerm-noticeTerm _notice_content_noticeTerm-noticeTerm dynamic-form-editor" id="_notice_content_noticeTerm-noticeTerm">3</span>个工作日。</p>
<h4><strong>七、其他补充事宜</strong></h4>
<div class="otherSupplement-otherSupplement _notice_content_otherSupplement-otherSupplement dynamic-form-editor" id="_notice_content_otherSupplement-otherSupplement">
	
	<div><p>无</p>
</div>
	
</div>
<h4><strong>八、凡对本次采购提出询问，请按以下方式联系。</strong></h4>
<div class="innercontent">
<h6>1.釆购人信息</h6>
<p>名  称：<span class="u-content noticePurchase-purchaserOrgName _notice_content_noticePurchase-purchaserOrgName dynamic-form-editor" id="_notice_content_noticePurchase-purchaserOrgName">包头市青山区住房和城乡建设局</span></p>
<p>地  址：<span class="u-content noticePurchase-purchaserOrgAddress _notice_content_noticePurchase-purchaserOrgAddress dynamic-form-editor" id="_notice_content_noticePurchase-purchaserOrgAddress">青东路与文学道交叉口</span></p>
<p>联系方式：<span class="u-content noticePurchase-purchaserLinkTel _notice_content_noticePurchase-purchaserLinkTel dynamic-form-editor" id="_notice_content_noticePurchase-purchaserLinkTel">0472-3612285</span></p>
<h6>2.釆购代理机构信息</h6>
<p>名  称：<span class="u-content noticeAgency-agencyName _notice_content_noticeAgency-agencyName dynamic-form-editor" id="_notice_content_noticeAgency-agencyName">内蒙古金晨建设项目管理有限公司</span></p>
<p>地  址：<span class="u-content noticeAgency-agentAddress _notice_content_noticeAgency-agentAddress dynamic-form-editor" id="_notice_content_noticeAgency-agentAddress">内蒙古自治区包头市青山区少先路2号商会大厦2008</span></p>
<p>联系方式：<span class="u-content noticeAgency-agentLinkTel _notice_content_noticeAgency-agentLinkTel dynamic-form-editor" id="_notice_content_noticeAgency-agentLinkTel">18247245248</span></p>
<h6>3.项目联系方式 </h6>
<p>项目联系人：<span class="u-content projectContact-managerName _notice_content_projectContact-managerName dynamic-form-editor" id="_notice_content_projectContact-managerName">徐工</span></p>
<p>电  话：<span class="u-content projectContact-managerLinkPhone _notice_content_projectContact-managerLinkPhone dynamic-form-editor" id="_notice_content_projectContact-managerLinkPhone">18247245248</span></p>
</div>
<p style="text-align: right; ">内蒙古金晨建设项目管理有限公司</p>
<p style="text-align: right; "></p><p style="text-align:right;" name="releaseDateSpan">2022年03月19日</p><br><p></p>
</div><div>
	<style type="text/css">
		a {color: #337ab7;text-decoration: none;transition: 0.5 s;background-color: transparent;
		a:focus,a:hover {text-decoration: none;color: #23527c;}
		a:focus {outline: 5px auto -webkit-focus-ring-color;outline-offset: -2px;}
		a:active, a:hover {outline: 0;}
	</style>
  <span style="margin-left: 4px;">相关附件：</span> 
  <br> 
  <div style="margin-left: 22px;"> 
    <a href="http://39.104.85.103/gpx-bid-file/150204/gpx-tender/2022/3/14/402881cd7f828544017f8612f1cb358f.zip?accessCode=8c8028d694353382f3f361d1fd9b75b9">二零二北环路整体罩面工程--清单导出件.zip</a> 
  </div> 
  <div style="margin-left: 22px;"> 
    <a href="http://39.104.85.103/gpx-bid-file/150204/gpx-tender/2022/3/14/402881cc7f82850a017f8613f97647b4.zip?accessCode=e4c5146573f84d115979b44df4a34c1c">图纸.zip</a> 
  </div> 
  <div style="margin-left: 22px;"> 
    <a href="http://39.104.85.103/gpx-bid-file/150204/gpx-tender/2022/3/17/402881cc7f891502017f96e091823385.pdf?accessCode=180fb16f0233f3af9f2e385a3f7ae04e">二零二北环路整体罩面工程招标文件（2022031702）.pdf</a> 
  </div> 
</div></div>
                            </div>
                </div>
        <div id="articleTool">
            <span class="plus_font" onclick="plus_font()" parm="bigger" alt="字号" title="字号">字号</span>
            <!-- <span class="collect" alt="收藏" title="收藏" onclick="AddFavorite()">收藏</span> -->
            <span class="print" onclick="printWork()" alt="打印" title="打印">打印</span>
        </div>
    </div>
</div><!-- 底部信息 -->
    <div class="footer">
        <div class="footContent">
            <div class="linkTo">
                <div class="friendLink_model">
                    <input class="friendholder" readonly value="中国政府采购网">
                    <div class="friendchooselist">
                        <ul>
                            <li><a target="_blank" href="http://www.ccgp.gov.cn/">中国政府采购网</a></li>
                        </ul>
                    </div>
                </div>
                <div class="friendLink_model" id="zhangy">

                    <input class="friendholder" readonly value="全国各省政府采购网">
                    <div class="friendchooselist">
                        <ul>
                            <li><a href="http://www.ccgp-beijing.gov.cn/" target="_blank">北京市政府采购网</a></li>
                            <li><a href="http://www.ccgp-shanghai.gov.cn/" target="_blank">上海市政府采购网</a></li>
                            <li><a href="http://www.ccgp-tianjin.gov.cn/" target="_blank">天津市政府采购网</a></li>
                            <li><a href="http://www.ccgp-chongqing.gov.cn/" target="_blank">重庆市政府采购网</a></li>
                            <li><a href="http://www.ccgp-hebei.gov.cn/" target="_blank">河北政府采购网</a></li>
                            <li><a href="http://www.ccgp-henan.gov.cn" target="_blank">河南政府采购网</a></li>
                            <li><a href="http://www.ccgp-hubei.gov.cn/" target="_blank">湖北政府采购网</a></li>
                            <li><a href="http://www.ccgp-hunan.gov.cn" target="_blank">湖南政府采购网</a></li>
                            <li><a href="http://www.ccgp-shanxi.gov.cn/" target="_blank">山西政府采购网</a></li>
                            <li><a href="http://www.ccgp-shandong.gov.cn/" target="_blank">山东政府采购网</a></li>
                            <li><a href="http://www.ccgp-heilongj.gov.cn/" target="_blank">黑龙江政府采购网</a></li>
                            <li><a href="http://www.ccgp-jilin.gov.cn/" target="_blank">吉林政府采购网</a></li>
                            <li><a href="http://www.ccgp-liaoning.gov.cn/" target="_blank">辽宁政府采购网</a></li>
                            <li><a href="http://www.ccgp-guangdong.gov.cn/" target="_blank">广东政府采购网</a></li>
                            <li><a href="http://www.ccgp-hainan.gov.cn/" target="_blank">海南政府采购网</a></li>
                            <li><a href="http://www.ccgp-shaanxi.gov.cn/" target="_blank">陕西政府采购网</a></li>
                            <li><a href="http://www.ccgp-gansu.gov.cn/" target="_blank">甘肃政府采购网</a></li>
                            <li><a href="http://www.ccgp-qinghai.gov.cn/" target="_blank">青海政府采购网</a></li>
                            <li><a href="http://www.ccgp-ningxia.gov.cn" target="_blank">宁夏政府采购网</a></li>
                            <li><a href="http://www.ccgp-jiangxi.gov.cn" target="_blank">江西政府采购网</a></li>
                            <li><a href="http://www.ccgp-xinjiang.gov.cn/" target="_blank">新疆自治区政府采购网</a></li>
                            <li><a href="http://www.ccgp-xizang.gov.cn/" target="_blank">西藏自治区政府采购网</a></li>
                            <li><a href="http://www.ccgp-sichuan.gov.cn/" target="_blank">四川政府采购网</a></li>
                            <li><a href="http://www.ccgp-jiangsu.gov.cn/" target="_blank">江苏政府采购网</a></li>
                            <li><a href="http://www.ccgp-zhejiang.gov.cn/" target="_blank">浙江政府采购网</a></li>
                            <li><a href="http://www.ccgp-guangxi.gov.cn/" target="_blank">广西政府采购网</a></li>
                            <li><a href="http://www.ccgp-yunnan.gov.cn/" target="_blank">云南省政府采购网</a></li>
                            <li><a href="http://www.ccgp-fujian.gov.cn/" target="_blank">福建省政府采购网</a></li>
                            <li><a href="http://www.ccgp-guizhou.gov.cn/" target="_blank">贵州政府采购网</a></li>
                            <li><a href="http://www.ccgp-anhui.gov.cn" target="_blank">安徽省政府采购网</a></li>
                            <li><a href="http://www.ccgp-dalian.gov.cn" target="_blank">大连市政府采购网</a></li>
                            <li><a href="http://www.ccgp-xiamen.gov.cn/" target="_blank">厦门市政府采购网</a></li>
                            <li><a href="http://www.ccgp-qingdao.gov.cn/" target="_blank">青岛市政府采购网</a></li>
                            <li><a href="http://www.ccgp-ningbo.gov.cn" target="_blank">宁波市政府采购网</a></li>
                            <li><a href="http://www.ccgp-bingtuan.gov.cn" target="_blank">兵团采购网</a></li>
                        </ul>
                    </div> 
                </div>
                <div class="friendLink_model">
                    <input class="friendholder" readonly value="地方财政">
                    <div class="friendchooselist">
                        <ul>
                            <li><a target="_blank" href="http://czt.nmg.gov.cn/">内蒙古自治区财政厅</a></li>
                            <li><a target="_blank" href="http://czj.huhhot.gov.cn/">呼和浩特市财政局</a></li>
                            <li><a target="_blank" href="http://czj.baotou.gov.cn/">包头市财政局</a></li>
                            <li><a target="_blank" href="http://czj.ordos.gov.cn/">鄂尔多斯市财政局</a></li>
                            <li><a target="_blank" href="http://czj.wuhai.gov.cn/">乌海市财政局</a></li>
                            <li><a target="_blank" href="http://czj.bynr.gov.cn/">巴彦淖尔市财政局</a></li>
                            <li><a target="_blank" href="http://czj.als.gov.cn/">阿拉善盟财政局</a></li>
                            <li><a target="_blank" href="http://czj.wulanchabu.gov.cn/">乌兰察布市财政局</a></li>
                            <li><a target="_blank" href="http://czj.xlgl.gov.cn/">锡林郭勒盟财政局</a></li>
                            <li><a target="_blank" href="http://czj.chifeng.gov.cn/">赤峰市财政局</a></li>
                            <li><a target="_blank" href="http://czj.tongliao.gov.cn/">通辽市财政局</a></li>
                            <li><a target="_blank" href="http://czj.xam.gov.cn/">兴安盟财政局</a></li>
                            <li><a target="_blank" href="http://czj.hlbe.gov.cn/">呼伦贝尔市财政局</a></li>
                        </ul>
                    </div>
                </div>
                <div class="friendLink_model">
                    <input class="friendholder" readonly value="友情链接">
                    <div class="friendchooselist">
                        <ul>
                            <li><a target="_blank" href="http://www.mof.gov.cn/index.htm">中华人民共和国财政部</a></li>
							<li><a target="_blank" href="http://www.caigou2003.com/">政府采购信息网</a></li>
							<li><a target="_blank" href="http://ggzyjy.nmg.gov.cn/">内蒙古自治区公共资源交易网</a></li>
                            <li><a target="_blank" href="https://www.creditchina.gov.cn/">信用中国</a></li>
                            <li><a target="_blank" href="http://www.gsxt.gov.cn/">国家企业信用信息公示系统</a></li>
							<li><a target="_blank" href="http://www.cgpnews.cn/epapers">中国政府采购新闻网</a></li>
							<li><a target="_blank" href="http://zfcg.ggzyjy.nmg.gov.cn/">内蒙古自治区政府采购中心网站</a></li>
							<li><a target="_blank" href="https://www.fupin832.com">脱贫地区农副产品网络销售平台</a></li>
							<li><a target="_blank" href="https://cg.fupin832.com/login">脱贫地区农副产品网络销售平台采购人管理系统</a></li>
							<li><a target="_blank" href="http://www.cfen.com.cn/">中国财经报网</a></li>
                        </ul>
                    </div>
                </div>
            </div>
             <!--<div class="jiguan"><a><img src="http://202.99.230.233/wp-content/themes/zfcgw_red/images/jiguan.jpg" alt=""></a></div>-->
			 
			 <div class="jiguan"><a href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=15010502001204"><img src="http://202.99.230.233/wp-content/themes/zfcgw_red/images/guohui.png" alt="" style="width:64px;height:69px;"></a><a href="https://bszs.conac.cn/sitename?method=show&amp;id=BFC1D08BF3309DDCE05310291AAC2C98"><img src="http://202.99.230.233/wp-content/themes/zfcgw_red/images/jiguan.jpg" alt=""></a><script id="_jiucuo_" sitecode="1500000007" src="https://zfwzgl.www.gov.cn/exposure/jiucuo.js"></script></div>
            <div class="foottext1">
                <!-- <a class="storeWeb">收藏本站</a> -->
                <span id="fwlTotal"></span>
                <span id="fwlToday"></span>
                <!-- <a class="topTo">返回顶部</a> -->
            </div>
            <div class="footTitle">内蒙古自治区政府采购网</div>
            <div class="foottext2">
                <p>版权所有: 内蒙古自治区财政厅     主办单位: 内蒙古自治区财政厅     地址: 内蒙古呼和浩特市赛罕区敕勒川大街19号</p>
				<p>网站标识号：1500000007     蒙ICP备14005124号-2     蒙公网安备：15010502001204</p>
                <p><a href="/category/lxwm" style="color:unset;">联系我们</a>        运营支持单位: 博思数采科技发展有限公司内蒙古分公司        技术服务热线电话: 400-0471-010</p>
            </div>
        </div>  
    </div>
</body>
<script src="https://cdn.staticfile.org/popper.js/1.15.0/umd/popper.min.js"></script>
<script>
    // foot友情链接点击打开
    $(".friendLink_model>select").bind("change", function(){
        var option = this.options[this.selectedIndex];
        if(option.value) {
            window.open(option.value);
        }
    });
    $(document).click(function(){
        if($('.friendchooselist').show()) {
            $('.friendchooselist').hide();
        }
    })
    $(".friendLink_model .friendholder").click(function() {
        event.stopPropagation();
        if($(this).next("div").hide()) {
            $('.friendchooselist').hide();
            $(this).next("div").show();
        } else {
            $(this).next("div").hide();
        }
    })
    $(".friendchooselist li").click(function() {
        $(".friendchooselist").hide();
    })

    //控制分享功能只对于详情页面显示
    if($("#article_details").length>0 || $(".pszjContainer").length>0){
        $(".fi3").show();
    }
    
</script>
</html>
<div class="protect" id="noticeArea">
<style type="text/css">
        #noticeArea { line-height:32px; font-size: 16px;text-align: justify;font-family: '宋体';word-break: break-all;}
        #noticeArea h1, #noticeArea h2, #noticeArea h3, #noticeArea h4, #noticeArea h5, #noticeArea h6{ line-height:2; }
        #noticeArea  *{padding:0; margin:0;}
        #noticeArea  .focuscontent{ color:#337ab7;}
        #noticeArea  strong{ font-weight: bold;}
        #noticeArea  h2{font-size: 24px; text-align: center; margin-bottom: 20px;text-align: left;}
        #noticeArea  h3{font-size: 18px;font-weight: normal; text-align: left;}
        #noticeArea  h4{font-size: 16px;font-weight: normal; line-height: 50px; margin-top: 10px; text-align: left;}
        #noticeArea  h5{text-indent: 32px;font-size: 16px;font-weight: normal; text-align: left;}
        #noticeArea  h6{font-size: 16px;font-weight: normal; text-align: left;}
        #noticeArea  pre{font-size: 16px;background: none;border: none;line-height: 32px;}
        #noticeArea  p{ text-indent: 32px; font-size: 16px; line-height: 32px;}
        #noticeArea  table{font-size: 16px;border-collapse: collapse; border-spacing: 0; width:100%;margin:10px auto; word-break: normal; line-height: 24px;}
        #noticeArea  table tr td{border-collapse: collapse; border:1px solid #333;text-align: center;padding: 5px 8px; word-break: break-all;}
        #noticeArea  table tr th{ font-weight: bold; text-align: center; border:1px solid #333;padding: 5px 8px; word-break: break-all;}
        #noticeArea  table tr{height: 32px; word-break: break-all;}
        #noticeArea .innercontent{padding-left: 32px;}
        #noticeArea .cleardom{clear: both;height: 0;line-height: 0;overflow: hidden;}
        #noticeArea .alignright{ text-align: right;word-break: normal;}
        @media print {
            #noticeArea { font-family: '宋体'; line-height:1.8; font-size: 18px;text-align: justify;word-break: break-all;}
            #noticeArea  *{padding:0; margin:0;}
            #noticeArea h1, #noticeArea h2, #noticeArea h3, #noticeArea h4, #noticeArea h5, #noticeArea h6{ line-height: 2; }
            #noticeArea  .focuscontent{ color:#337ab7;}
            #noticeArea  h2{font-size: 34px; text-align: center; margin-bottom: 25px;font-family: SimHei; text-align: left;}
            #noticeArea  h3{font-size: 24px; font-weight: normal; text-align: left;}
            #noticeArea  h4{font-size: 21px; font-weight: normal; text-align: left;}
            #noticeArea  h5{font-size: 18px; text-indent: 36px; font-weight: normal; text-align: left;}
            #noticeArea  h6{font-size: 16px;font-weight: normal; text-align: left;}
                  #noticeArea  pre{font-size: 18px;background: none;border: none;line-height: 1.8;}
            #noticeArea  p{ text-indent: 36px; font-size: 18px; line-height: 32px;}
            #noticeArea  table{font-size: 16px;border-collapse: collapse; border-spacing: 0; width:100%;margin:15px auto; word-break: normal; line-height: 24px;}
            #noticeArea  table tr td{border-collapse: collapse; border:1px solid #333;text-align: center;padding: 2px 6px; word-break: break-all;}
            #noticeArea  table tr th{ font-weight: bold; text-align: center;padding: 2px 6px; word-break: break-all;}
            #noticeArea  table tr{height: 32px; word-break: break-all;}
            #noticeArea .innercontent{padding-left: 32px;}
            #noticeArea .cleardom{clear: both;height: 0;line-height: 0;overflow: hidden;}
            #noticeArea .alignright{ text-align: right;word-break: normal;}
            }
#noticeArea { }
@media print {
#noticeArea { }
}
</style>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<p data-v-6b13d514=""></p>

<div style="border: 1px solid black;padding: 12px;border-collapse:collapse;line-height: 28px;width: 98%;margin: 10px auto">
<h6><strong>
项目概况
</strong>
</h6>
<p>
<span>二零二北环路整体罩面工程</span>采购项目的潜在供应商应在<span class="noticeGetFile-getBidFileAddress _notice_content_noticeGetFile-getBidFileAddress content dynamic-form-editor">内蒙古自治区政府采购网</span>获取采购文件，并于<span class="noticePurchaseTime-noticePurchaseTime _notice_content_noticePurchaseTime-noticePurchaseTime bidFileSubmitTime dynamic-form-editor">
	
	2022年03月31日 09时50分
</span>（北京时间）前提交响应文件。
</p>
</div>
<h4><strong>一、项目基本情况</strong></h4>
<p>项目编号：BTZCQSS-C-G-220014</p>
<p>项目名称：二零二北环路整体罩面工程</p>
<p>采购方式：竞争性磋商</p>
<p>预算金额：1,508,658.00元</p>
<p>采购需求：</p>
<div class="noticeDemandExternal-noticeDemandExternal _notice_content_noticeDemandExternal-noticeDemandExternal dynamic-form-editor" id="_notice_content_noticeDemandExternal-noticeDemandExternal">
	<div id="noticeDemandExternal">
	<style type="text/css">
        #noticeDemandExternal { line-height:32px; font-size: 16px;text-align: justify;font-family: '宋体';}
        #noticeDemandExternal h1, #noticeDemandExternal h2, #noticeDemandExternal h3, #noticeDemandExternal h4, #noticeDemandExternal h5, #noticeDemandExternal h6{ line-height:2; }
        #noticeDemandExternal  *{padding:0; margin:0;}
        #noticeDemandExternal  .focuscontent{ color:#337ab7;}
        #noticeDemandExternal  strong{ font-weight: bold;}
        #noticeDemandExternal  h2{font-size: 24px; text-align: center; margin-bottom: 20px;}
        #noticeDemandExternal  h3{font-size: 18px;font-weight: normal;}
        #noticeDemandExternal  h4{font-size: 16px;font-weight: normal; line-height: 50px; margin-top: 10px;}
        #noticeDemandExternal  h5{text-indent: 32px;font-size: 16px;font-weight: normal;}
        #noticeDemandExternal  h6{font-size: 16px;font-weight: normal;}
        #noticeDemandExternal  pre{font-size: 16px;background: none;border: none;line-height: 32px;}
        #noticeDemandExternal  p{ text-indent: 32px; font-size: 16px; line-height: 32px;}
        #noticeDemandExternal  table{font-size: 16px;border-collapse: collapse; border-spacing: 0; width:100%;margin:10px auto;word-break: normal; line-height: 24px;}
        #noticeDemandExternal  table tr td{border-collapse: collapse; border:1px solid #333;text-align: center;padding: 5px 8px;}
        #noticeDemandExternal  table tr th{ font-weight: bold; text-align: center; border:1px solid #333;padding: 5px 8px;}
        #noticeDemandExternal  table tr{
        height: 32px;}
        #noticeDemandExternal .innercontent{padding-left: 32px;}
        #noticeDemandExternal .cleardom{clear: both;height: 0;line-height: 0;overflow: hidden;}
        #noticeDemandExternal .alignright{ text-align: right;word-break: normal;}
        @media print {
            #noticeDemandExternal { font-family: '宋体'; line-height:1.8; font-size: 18px;text-align: justify;}
            #noticeDemandExternal  *{padding:0; margin:0;}
            #noticeDemandExternal h1, #noticeDemandExternal h2, #noticeDemandExternal h3, #noticeDemandExternal h4, #noticeDemandExternal h5, #noticeDemandExternal h6{ line-height: 2; }
            #noticeDemandExternal  .focuscontent{ color:#337ab7;}
            #noticeDemandExternal  h2{font-size: 34px; text-align: center; margin-bottom: 25px;font-family: SimHei; }
            #noticeDemandExternal  h3{font-size: 24px; font-weight: normal;}
            #noticeDemandExternal  h4{font-size: 21px; font-weight: normal;}
            #noticeDemandExternal  h5{font-size: 18px; text-indent: 36px; font-weight: normal;}
            #noticeDemandExternal  h6{font-size: 16px;font-weight: normal;}
                  #noticeDemandExternal  pre{font-size: 18px;background: none;border: none;line-height: 1.8;}
            #noticeDemandExternal  p{ text-indent: 36px; font-size: 18px; line-height: 32px;}
            #noticeDemandExternal  table{font-size: 16px;border-collapse: collapse; border-spacing: 0; width:100%;margin:15px auto; word-break: normal; line-height: 24px;}
            #noticeDemandExternal  table tr td{border-collapse: collapse; border:1px solid #333;text-align: center;padding: 2px 6px; }
            #noticeDemandExternal  table tr th{ font-weight: bold; text-align: center;padding: 2px 6px;}
            #noticeDemandExternal  table tr{
                height: 32px;}
            #noticeDemandExternal .innercontent{padding-left: 32px;}
            #noticeDemandExternal .cleardom{clear: both;height: 0;line-height: 0;overflow: hidden;}
            #noticeDemandExternal .alignright{ text-align: right;word-break: normal;}
            }
    </style>
	<div class="innercontent">
	<p class="u-content">合同包1(二零二北环路 整体罩面工程):</p>
	<p style="text-indent:42px;">合同包预算金额：<span class="u-content">1,508,658.00元</span></p>
	
	<table width="100%" border="1" cellspacing="0">
		<thead>
			<tr style="height:36.4pt">
				<th style="width:80px;">品目号</th>
				<th style="width:300px;">品目名称</th>
				<th style="width:300px;">采购标的</th>
				<th style="width:100px;">数量（单位）</th>
				<th style="width:200px;">技术规格、参数及要求</th>
				<th style="width:120px;">品目预算(元)</th>
				<th style="width:120px;">最高限价(元)</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>1-1</td>
				<td>其他建筑工程</td>
				<td>1508658.00</td>
				<td>1(项)</td>
				<td>详见采购文件</td>
				<!-- 品目预算 -->
				<td class="alignright">
					
					<span>1,508,658.00</span>
				</td>
				<!-- 最高限价 -->
				<td class="alignright">
					<span>-</span>
					
				</td>
			</tr>
		</tbody>
	</table>
	<div>
		
		
	</div>
	<div>
		
		<p style="text-indent:42px;">
			本合同包<span class="u-content">不接受</span>联合体投标
		</p>
	</div>
	<div>
		<p style="text-indent:42px;">
			合同履行期限：<span class="u-content">自合同签订之日起13个月</span>
		</p>
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
	<div>
		
		
	</div>
</div>
</div>
	</div>
<h4><strong>二、申请人的资格要求：</strong></h4>
<div class="clauseLegalPackage-clauseLegalPackage _notice_content_clauseLegalPackage-clauseLegalPackage dynamic-form-editor" id="_notice_content_clauseLegalPackage-clauseLegalPackage">
<p>1.满足《中华人民共和国政府釆购法》第二十二条规定：</p>
<p>（1）具有独立承担民事责任的能力；</p>
<p>（2）具有良好的商业信誉和健全的财务会计制度；</p>
<p>（3）具有履行合同所必需的设备和专业技术能力；</p>
<p>（4）有依法缴纳税收和社会保障资金的良好记录；</p>
<p>（5）参加政府采购活动前三年内，在经营活动中没有重大违法记录；</p>
<p>（6）法律、行政法规规定的其他条件。</p>
<p>2.落实政府采购政策需满足的资格要求：

<span class="u-content">无。</span>
</p>
<p>3.本项目的特定资格要求：</p><div class="innercontent">
  <p>合同包1(二零二北环路 整体罩面工程)特定资格要求如下:</p>
  <div>
	<p>(1)响应供应商资质：需具有市政公用工程施工总承包三级及以上资质并具有有效的安全生产许可证。 项目负责人资质：需具有市政工程注册二级建造师并具有有效的安全考核证书。</p>
  </div>
</div><p></p>
</div>
<h4><strong>三、获取采购文件</strong></h4>
<p>时间：<span class="noticePurchaseTime-noticePurchaseTime _notice_content_noticePurchaseTime-noticePurchaseTime dynamic-form-editor" id="_notice_content_noticePurchaseTime-noticePurchaseTime"><span class="u-content">
	
	2022年03月19日
</span>至<span class="u-content">
	
	2022年03月25日
</span>，每天上午<span class="u-content">
	
	00:00:00
</span>至<span class="u-content">
	
	12:00:00
</span>，下午<span class="u-content">
	
	12:00:00
</span>至<span class="u-content">
	
	23:59:59
</span>（北京时间,法定节假日除外）</span></p>
<p>地点：<span class="u-content noticeGetFile-getBidFileAddress _notice_content_noticeGetFile-getBidFileAddress dynamic-form-editor" id="_notice_content_noticeGetFile-getBidFileAddress">内蒙古自治区政府采购网</span></p>
<p>方式：在线获取。获取采购文件时，需登录“政府采购云平台”，按照“执行交易→应标→项目应标→未参与项目”步骤，填写联系人相关信息确认参与后，即为成功“在线获取”。</p>
<p>售价：<span class="u-content noticeGetFile-bidFilePrice _notice_content_noticeGetFile-bidFilePrice dynamic-form-editor" id="_notice_content_noticeGetFile-bidFilePrice">
	
	免费获取
	
</span></p>
<h4><strong>四、响应文件提交</strong></h4>
<p>截止时间：<span class="u-content noticePurchaseTime-noticePurchaseTime _notice_content_noticePurchaseTime-noticePurchaseTime bidFileSubmitTime3 dynamic-form-editor">
	
	2022年03月31日 09时50分00秒
</span>（北京时间）</p>
<p>地点：<span class="u-content noticeBidTime-bidFileSubmitAddress _notice_content_noticeBidTime-bidFileSubmitAddress dynamic-form-editor" id="_notice_content_noticeBidTime-bidFileSubmitAddress"> 内蒙古自治区政府采购网（政府采购云平台）</span>
</p>
<h4><strong>五、开启</strong></h4>
<p>时间：<span class="u-content  noticePurchaseTime-noticePurchaseTime _notice_content_noticePurchaseTime-noticePurchaseTime bidOpenTime1 dynamic-form-editor">
	
	2022年03月31日 09时50分00秒
</span>（北京时间）</p>
<p>地点：<span class="noticeBidTime-bidAddress _notice_content_noticeBidTime-bidAddress dynamic-form-editor" id="_notice_content_noticeBidTime-bidAddress">内蒙古自治区包头市市辖区包头市九原区建华南路公共资源交易大厅3楼第六开标室</span></p>
<h4><strong>六、公告期限</strong></h4>
<p>自本公告发布之日起<span class="u-content noticeTerm-noticeTerm _notice_content_noticeTerm-noticeTerm dynamic-form-editor" id="_notice_content_noticeTerm-noticeTerm">3</span>个工作日。</p>
<h4><strong>七、其他补充事宜</strong></h4>
<div class="otherSupplement-otherSupplement _notice_content_otherSupplement-otherSupplement dynamic-form-editor" id="_notice_content_otherSupplement-otherSupplement">
	
	<div><p>无</p>
</div>
	
</div>
<h4><strong>八、凡对本次采购提出询问，请按以下方式联系。</strong></h4>
<div class="innercontent">
<h6>1.釆购人信息</h6>
<p>名  称：<span class="u-content noticePurchase-purchaserOrgName _notice_content_noticePurchase-purchaserOrgName dynamic-form-editor" id="_notice_content_noticePurchase-purchaserOrgName">包头市青山区住房和城乡建设局</span></p>
<p>地  址：<span class="u-content noticePurchase-purchaserOrgAddress _notice_content_noticePurchase-purchaserOrgAddress dynamic-form-editor" id="_notice_content_noticePurchase-purchaserOrgAddress">青东路与文学道交叉口</span></p>
<p>联系方式：<span class="u-content noticePurchase-purchaserLinkTel _notice_content_noticePurchase-purchaserLinkTel dynamic-form-editor" id="_notice_content_noticePurchase-purchaserLinkTel">0472-3612285</span></p>
<h6>2.釆购代理机构信息</h6>
<p>名  称：<span class="u-content noticeAgency-agencyName _notice_content_noticeAgency-agencyName dynamic-form-editor" id="_notice_content_noticeAgency-agencyName">内蒙古金晨建设项目管理有限公司</span></p>
<p>地  址：<span class="u-content noticeAgency-agentAddress _notice_content_noticeAgency-agentAddress dynamic-form-editor" id="_notice_content_noticeAgency-agentAddress">内蒙古自治区包头市青山区少先路2号商会大厦2008</span></p>
<p>联系方式：<span class="u-content noticeAgency-agentLinkTel _notice_content_noticeAgency-agentLinkTel dynamic-form-editor" id="_notice_content_noticeAgency-agentLinkTel">18247245248</span></p>
<h6>3.项目联系方式 </h6>
<p>项目联系人：<span class="u-content projectContact-managerName _notice_content_projectContact-managerName dynamic-form-editor" id="_notice_content_projectContact-managerName">徐工</span></p>
<p>电  话：<span class="u-content projectContact-managerLinkPhone _notice_content_projectContact-managerLinkPhone dynamic-form-editor" id="_notice_content_projectContact-managerLinkPhone">18247245248</span></p>
</div>
<p style="text-align: right; ">内蒙古金晨建设项目管理有限公司</p>
<p style="text-align: right; "></p><p style="text-align:right;" name="releaseDateSpan">2022年03月19日</p><br><p></p>
</div><div>
	<style type="text/css">
		a {color: #337ab7;text-decoration: none;transition: 0.5 s;background-color: transparent;
		a:focus,a:hover {text-decoration: none;color: #23527c;}
		a:focus {outline: 5px auto -webkit-focus-ring-color;outline-offset: -2px;}
		a:active, a:hover {outline: 0;}
	</style>
  <span style="margin-left: 4px;">相关附件：</span> 
  <br> 
  <div style="margin-left: 22px;"> 
    <a href="http://39.104.85.103/gpx-bid-file/150204/gpx-tender/2022/3/14/402881cd7f828544017f8612f1cb358f.zip?accessCode=8c8028d694353382f3f361d1fd9b75b9">二零二北环路整体罩面工程--清单导出件.zip</a> 
  </div> 
  <div style="margin-left: 22px;"> 
    <a href="http://39.104.85.103/gpx-bid-file/150204/gpx-tender/2022/3/14/402881cc7f82850a017f8613f97647b4.zip?accessCode=e4c5146573f84d115979b44df4a34c1c">图纸.zip</a> 
  </div> 
  <div style="margin-left: 22px;"> 
    <a href="http://39.104.85.103/gpx-bid-file/150204/gpx-tender/2022/3/17/402881cc7f891502017f96e091823385.pdf?accessCode=180fb16f0233f3af9f2e385a3f7ae04e">二零二北环路整体罩面工程招标文件（2022031702）.pdf</a> 
  </div> 
</div></div>
                            </div>
                </div>
        <div id="articleTool">
            <span class="plus_font" onclick="plus_font()" parm="bigger" alt="字号" title="字号">字号</span>
            <!-- <span class="collect" alt="收藏" title="收藏" onclick="AddFavorite()">收藏</span> -->
            <span class="print" onclick="printWork()" alt="打印" title="打印">打印</span>
        </div>
    </div>
</div><!-- 底部信息 -->
    <div class="footer">
        <div class="footContent">
            <div class="linkTo">
                <div class="friendLink_model">
                    <input class="friendholder" readonly value="中国政府采购网">
                    <div class="friendchooselist">
                        <ul>
                            <li><a target="_blank" href="http://www.ccgp.gov.cn/">中国政府采购网</a></li>
                        </ul>
                    </div>
                </div>
                <div class="friendLink_model" id="zhangy">

                    <input class="friendholder" readonly value="全国各省政府采购网">
                    <div class="friendchooselist">
                        <ul>
                            <li><a href="http://www.ccgp-beijing.gov.cn/" target="_blank">北京市政府采购网</a></li>
                            <li><a href="http://www.ccgp-shanghai.gov.cn/" target="_blank">上海市政府采购网</a></li>
                            <li><a href="http://www.ccgp-tianjin.gov.cn/" target="_blank">天津市政府采购网</a></li>
                            <li><a href="http://www.ccgp-chongqing.gov.cn/" target="_blank">重庆市政府采购网</a></li>
                            <li><a href="http://www.ccgp-hebei.gov.cn/" target="_blank">河北政府采购网</a></li>
                            <li><a href="http://www.ccgp-henan.gov.cn" target="_blank">河南政府采购网</a></li>
                            <li><a href="http://www.ccgp-hubei.gov.cn/" target="_blank">湖北政府采购网</a></li>
                            <li><a href="http://www.ccgp-hunan.gov.cn" target="_blank">湖南政府采购网</a></li>
                            <li><a href="http://www.ccgp-shanxi.gov.cn/" target="_blank">山西政府采购网</a></li>
                            <li><a href="http://www.ccgp-shandong.gov.cn/" target="_blank">山东政府采购网</a></li>
                            <li><a href="http://www.ccgp-heilongj.gov.cn/" target="_blank">黑龙江政府采购网</a></li>
                            <li><a href="http://www.ccgp-jilin.gov.cn/" target="_blank">吉林政府采购网</a></li>
                            <li><a href="http://www.ccgp-liaoning.gov.cn/" target="_blank">辽宁政府采购网</a></li>
                            <li><a href="http://www.ccgp-guangdong.gov.cn/" target="_blank">广东政府采购网</a></li>
                            <li><a href="http://www.ccgp-hainan.gov.cn/" target="_blank">海南政府采购网</a></li>
                            <li><a href="http://www.ccgp-shaanxi.gov.cn/" target="_blank">陕西政府采购网</a></li>
                            <li><a href="http://www.ccgp-gansu.gov.cn/" target="_blank">甘肃政府采购网</a></li>
                            <li><a href="http://www.ccgp-qinghai.gov.cn/" target="_blank">青海政府采购网</a></li>
                            <li><a href="http://www.ccgp-ningxia.gov.cn" target="_blank">宁夏政府采购网</a></li>
                            <li><a href="http://www.ccgp-jiangxi.gov.cn" target="_blank">江西政府采购网</a></li>
                            <li><a href="http://www.ccgp-xinjiang.gov.cn/" target="_blank">新疆自治区政府采购网</a></li>
                            <li><a href="http://www.ccgp-xizang.gov.cn/" target="_blank">西藏自治区政府采购网</a></li>
                            <li><a href="http://www.ccgp-sichuan.gov.cn/" target="_blank">四川政府采购网</a></li>
                            <li><a href="http://www.ccgp-jiangsu.gov.cn/" target="_blank">江苏政府采购网</a></li>
                            <li><a href="http://www.ccgp-zhejiang.gov.cn/" target="_blank">浙江政府采购网</a></li>
                            <li><a href="http://www.ccgp-guangxi.gov.cn/" target="_blank">广西政府采购网</a></li>
                            <li><a href="http://www.ccgp-yunnan.gov.cn/" target="_blank">云南省政府采购网</a></li>
                            <li><a href="http://www.ccgp-fujian.gov.cn/" target="_blank">福建省政府采购网</a></li>
                            <li><a href="http://www.ccgp-guizhou.gov.cn/" target="_blank">贵州政府采购网</a></li>
                            <li><a href="http://www.ccgp-anhui.gov.cn" target="_blank">安徽省政府采购网</a></li>
                            <li><a href="http://www.ccgp-dalian.gov.cn" target="_blank">大连市政府采购网</a></li>
                            <li><a href="http://www.ccgp-xiamen.gov.cn/" target="_blank">厦门市政府采购网</a></li>
                            <li><a href="http://www.ccgp-qingdao.gov.cn/" target="_blank">青岛市政府采购网</a></li>
                            <li><a href="http://www.ccgp-ningbo.gov.cn" target="_blank">宁波市政府采购网</a></li>
                            <li><a href="http://www.ccgp-bingtuan.gov.cn" target="_blank">兵团采购网</a></li>
                        </ul>
                    </div> 
                </div>
                <div class="friendLink_model">
                    <input class="friendholder" readonly value="地方财政">
                    <div class="friendchooselist">
                        <ul>
                            <li><a target="_blank" href="http://czt.nmg.gov.cn/">内蒙古自治区财政厅</a></li>
                            <li><a target="_blank" href="http://czj.huhhot.gov.cn/">呼和浩特市财政局</a></li>
                            <li><a target="_blank" href="http://czj.baotou.gov.cn/">包头市财政局</a></li>
                            <li><a target="_blank" href="http://czj.ordos.gov.cn/">鄂尔多斯市财政局</a></li>
                            <li><a target="_blank" href="http://czj.wuhai.gov.cn/">乌海市财政局</a></li>
                            <li><a target="_blank" href="http://czj.bynr.gov.cn/">巴彦淖尔市财政局</a></li>
                            <li><a target="_blank" href="http://czj.als.gov.cn/">阿拉善盟财政局</a></li>
                            <li><a target="_blank" href="http://czj.wulanchabu.gov.cn/">乌兰察布市财政局</a></li>
                            <li><a target="_blank" href="http://czj.xlgl.gov.cn/">锡林郭勒盟财政局</a></li>
                            <li><a target="_blank" href="http://czj.chifeng.gov.cn/">赤峰市财政局</a></li>
                            <li><a target="_blank" href="http://czj.tongliao.gov.cn/">通辽市财政局</a></li>
                            <li><a target="_blank" href="http://czj.xam.gov.cn/">兴安盟财政局</a></li>
                            <li><a target="_blank" href="http://czj.hlbe.gov.cn/">呼伦贝尔市财政局</a></li>
                        </ul>
                    </div>
                </div>
                <div class="friendLink_model">
                    <input class="friendholder" readonly value="友情链接">
                    <div class="friendchooselist">
                        <ul>
                            <li><a target="_blank" href="http://www.mof.gov.cn/index.htm">中华人民共和国财政部</a></li>
							<li><a target="_blank" href="http://www.caigou2003.com/">政府采购信息网</a></li>
							<li><a target="_blank" href="http://ggzyjy.nmg.gov.cn/">内蒙古自治区公共资源交易网</a></li>
                            <li><a target="_blank" href="https://www.creditchina.gov.cn/">信用中国</a></li>
                            <li><a target="_blank" href="http://www.gsxt.gov.cn/">国家企业信用信息公示系统</a></li>
							<li><a target="_blank" href="http://www.cgpnews.cn/epapers">中国政府采购新闻网</a></li>
							<li><a target="_blank" href="http://zfcg.ggzyjy.nmg.gov.cn/">内蒙古自治区政府采购中心网站</a></li>
							<li><a target="_blank" href="https://www.fupin832.com">脱贫地区农副产品网络销售平台</a></li>
							<li><a target="_blank" href="https://cg.fupin832.com/login">脱贫地区农副产品网络销售平台采购人管理系统</a></li>
							<li><a target="_blank" href="http://www.cfen.com.cn/">中国财经报网</a></li>
                        </ul>
                    </div>
                </div>
            </div>
             <!--<div class="jiguan"><a><img src="http://202.99.230.233/wp-content/themes/zfcgw_red/images/jiguan.jpg" alt=""></a></div>-->
			 
			 <div class="jiguan"><a href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=15010502001204"><img src="http://202.99.230.233/wp-content/themes/zfcgw_red/images/guohui.png" alt="" style="width:64px;height:69px;"></a><a href="https://bszs.conac.cn/sitename?method=show&amp;id=BFC1D08BF3309DDCE05310291AAC2C98"><img src="http://202.99.230.233/wp-content/themes/zfcgw_red/images/jiguan.jpg" alt=""></a><script id="_jiucuo_" sitecode="1500000007" src="https://zfwzgl.www.gov.cn/exposure/jiucuo.js"></script></div>
            <div class="foottext1">
                <!-- <a class="storeWeb">收藏本站</a> -->
                <span id="fwlTotal"></span>
                <span id="fwlToday"></span>
                <!-- <a class="topTo">返回顶部</a> -->
            </div>
            <div class="footTitle">内蒙古自治区政府采购网</div>
            <div class="foottext2">
                <p>版权所有: 内蒙古自治区财政厅     主办单位: 内蒙古自治区财政厅     地址: 内蒙古呼和浩特市赛罕区敕勒川大街19号</p>
				<p>网站标识号：1500000007     蒙ICP备14005124号-2     蒙公网安备：15010502001204</p>
                <p><a href="/category/lxwm" style="color:unset;">联系我们</a>        运营支持单位: 博思数采科技发展有限公司内蒙古分公司        技术服务热线电话: 400-0471-010</p>
            </div>
        </div>  
    </div>
</body>
<script src="https://cdn.staticfile.org/popper.js/1.15.0/umd/popper.min.js"></script>
<script>
    // foot友情链接点击打开
    $(".friendLink_model>select").bind("change", function(){
        var option = this.options[this.selectedIndex];
        if(option.value) {
            window.open(option.value);
        }
    });
    $(document).click(function(){
        if($('.friendchooselist').show()) {
            $('.friendchooselist').hide();
        }
    })
    $(".friendLink_model .friendholder").click(function() {
        event.stopPropagation();
        if($(this).next("div").hide()) {
            $('.friendchooselist').hide();
            $(this).next("div").show();
        } else {
            $(this).next("div").hide();
        }
    })
    $(".friendchooselist li").click(function() {
        $(".friendchooselist").hide();
    })

    //控制分享功能只对于详情页面显示
    if($("#article_details").length>0 || $(".pszjContainer").length>0){
        $(".fi3").show();
    }
    
</script>
</html>
'''

soup = BeautifulSoup(wordd,'lxml')
content = soup.prettify()
for i in soup.find_all(class_=re.compile("foot")):

    i.extract()
for i in soup.find_all('script'):
    i.extract()
for i in soup.find_all('div',attrs={'id':'articleTool'}):
    i.extract()
for i in soup.find_all('style'):
    i.extract()
for i in soup.find_all('meta'):
    i.extract()
print(soup.prettify())