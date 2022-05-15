# coding=utf-8
import json
import pprint
import datetime, time
import requests
import gzip
import re
import sys
from bs4 import BeautifulSoup
from urllib import parse as urlparse
from requests.adapters import HTTPAdapter
import os
import logging
from file_walk import regexFanhao
fhSeachurl = "https://www.busjav.fun/"
headers_Word = '''
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,zh-TW;q=0.8

user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36
'''
HEA = dict(line.split(": ", 1) for line in headers_Word.split("\n") if line != '')

LOGINGFOMAT = '''ERROR massage:\t%(message)s
ERROR LEVEL:\t%(levelname)s
ERROR LOCATION:\t%(pathname)s\t%(lineno)d
%(funcName)s
ERROR TIME:\t%(asctime)s
-----------------------------------------------------------
'''
logging.basicConfig(filename='requests_Error.log', format=LOGINGFOMAT)

req = requests.session()
# 设置requests请求头文件
req.headers = {'Cookie': 'existmag=all'}

# requests超时重试四次
req.mount('http://', HTTPAdapter(max_retries=3))
req.mount('https://', HTTPAdapter(max_retries=3))


hhtml = '''
	<html><head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="renderer" content="webkit">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - JavBus</title>
<meta name="keywords" content="OFJE-266,S1 NO.1 STYLE,S1 GIRLS COLLECTION,高畫質,DMM獨家,美少女,4小時以上作品,口交,合集,苗條,偶像藝人">
<meta name="description" content="【發行日期】2020-09-17，【長度】480分鐘，(OFJE-266)ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間">
<link rel="alternate" href="https://www.busjav.fun/en/OFJE-266" hreflang="en">
<link rel="alternate" href="https://www.busjav.fun/ja/OFJE-266" hreflang="ja">
<link rel="alternate" href="https://www.busjav.fun/ko/OFJE-266" hreflang="ko">
<link rel="alternate" href="https://www.busjav.fun/OFJE-266" hreflang="zh">
<link rel="alternate" href="https://www.busjav.fun/OFJE-266" hreflang="x-default">
<link rel="canonical" href="https://www.busjav.fun/OFJE-266">
<link rel="preconnect" href="https://poweredby.jads.co" crossorigin="">
<link rel="dns-prefetch" href="https://poweredby.jads.co">
<link rel="stylesheet" href="https://www.busjav.fun/css/bootstrap.min.css">
<link rel="stylesheet" href="https://www.busjav.fun/css/bootstrap-theme.min.css">
<link rel="stylesheet" href="https://www.busjav.fun/css/css-slider.css?v=8.26.1">
<link rel="stylesheet" href="https://www.busjav.fun/css/nav.overlay.css?v=3.9.8">
<link rel="stylesheet" href="https://www.busjav.fun/css/magnific-popup.css">
<link rel="stylesheet" href="https://www.busjav.fun/css/base.css?v=7.15">
<script src="https://www.busjav.fun/js/jquery.min.js"></script>
<script src="https://www.busjav.fun/js/jquery.magnific-popup.min.js"></script>
<script src="https://www.busjav.fun/js/bootstrap.min.js" defer=""></script>
<script src="https://www.busjav.fun/js/jquery.cookie.min.js" defer=""></script>
<script src="https://www.busjav.fun/js/base.js" defer=""></script>
<script src="https://www.busjav.fun/js/bootstrap-hover-dropdown.js" defer=""></script>
<script src="https://www.busjav.fun/js/nav.overlay.js?v=10.30.3" defer=""></script>
<!--[if lt IE 9]> <script src="https://www.busjav.fun/js/html5shiv.min.js"></script><script src="https://www.busjav.fun/js/respond.min.js"></script><![endif]-->
<style type="text/css" abt="234"></style><style>.swal2-popup.swal2-toast{flex-direction:row;align-items:center;width:auto;padding:.625em;overflow-y:hidden;background:#fff;box-shadow:0 0 .625em #d9d9d9}.swal2-popup.swal2-toast .swal2-header{flex-direction:row;padding:0}.swal2-popup.swal2-toast .swal2-title{flex-grow:1;justify-content:flex-start;margin:0 .6em;font-size:1em}.swal2-popup.swal2-toast .swal2-footer{margin:.5em 0 0;padding:.5em 0 0;font-size:.8em}.swal2-popup.swal2-toast .swal2-close{position:static;width:.8em;height:.8em;line-height:.8}.swal2-popup.swal2-toast .swal2-content{justify-content:flex-start;padding:0;font-size:1em}.swal2-popup.swal2-toast .swal2-icon{width:2em;min-width:2em;height:2em;margin:0}.swal2-popup.swal2-toast .swal2-icon .swal2-icon-content{display:flex;align-items:center;font-size:1.8em;font-weight:700}@media all and (-ms-high-contrast:none),(-ms-high-contrast:active){.swal2-popup.swal2-toast .swal2-icon .swal2-icon-content{font-size:.25em}}.swal2-popup.swal2-toast .swal2-icon.swal2-success .swal2-success-ring{width:2em;height:2em}.swal2-popup.swal2-toast .swal2-icon.swal2-error [class^=swal2-x-mark-line]{top:.875em;width:1.375em}.swal2-popup.swal2-toast .swal2-icon.swal2-error [class^=swal2-x-mark-line][class$=left]{left:.3125em}.swal2-popup.swal2-toast .swal2-icon.swal2-error [class^=swal2-x-mark-line][class$=right]{right:.3125em}.swal2-popup.swal2-toast .swal2-actions{flex-basis:auto!important;width:auto;height:auto;margin:0 .3125em}.swal2-popup.swal2-toast .swal2-styled{margin:0 .3125em;padding:.3125em .625em;font-size:1em}.swal2-popup.swal2-toast .swal2-styled:focus{box-shadow:0 0 0 1px #fff,0 0 0 3px rgba(50,100,150,.4)}.swal2-popup.swal2-toast .swal2-success{border-color:#a5dc86}.swal2-popup.swal2-toast .swal2-success [class^=swal2-success-circular-line]{position:absolute;width:1.6em;height:3em;transform:rotate(45deg);border-radius:50%}.swal2-popup.swal2-toast .swal2-success [class^=swal2-success-circular-line][class$=left]{top:-.8em;left:-.5em;transform:rotate(-45deg);transform-origin:2em 2em;border-radius:4em 0 0 4em}.swal2-popup.swal2-toast .swal2-success [class^=swal2-success-circular-line][class$=right]{top:-.25em;left:.9375em;transform-origin:0 1.5em;border-radius:0 4em 4em 0}.swal2-popup.swal2-toast .swal2-success .swal2-success-ring{width:2em;height:2em}.swal2-popup.swal2-toast .swal2-success .swal2-success-fix{top:0;left:.4375em;width:.4375em;height:2.6875em}.swal2-popup.swal2-toast .swal2-success [class^=swal2-success-line]{height:.3125em}.swal2-popup.swal2-toast .swal2-success [class^=swal2-success-line][class$=tip]{top:1.125em;left:.1875em;width:.75em}.swal2-popup.swal2-toast .swal2-success [class^=swal2-success-line][class$=long]{top:.9375em;right:.1875em;width:1.375em}.swal2-popup.swal2-toast .swal2-success.swal2-icon-show .swal2-success-line-tip{-webkit-animation:swal2-toast-animate-success-line-tip .75s;animation:swal2-toast-animate-success-line-tip .75s}.swal2-popup.swal2-toast .swal2-success.swal2-icon-show .swal2-success-line-long{-webkit-animation:swal2-toast-animate-success-line-long .75s;animation:swal2-toast-animate-success-line-long .75s}.swal2-popup.swal2-toast.swal2-show{-webkit-animation:swal2-toast-show .5s;animation:swal2-toast-show .5s}.swal2-popup.swal2-toast.swal2-hide{-webkit-animation:swal2-toast-hide .1s forwards;animation:swal2-toast-hide .1s forwards}.swal2-container{display:flex;position:fixed;z-index:1060;top:0;right:0;bottom:0;left:0;flex-direction:row;align-items:center;justify-content:center;padding:.625em;overflow-x:hidden;transition:background-color .1s;-webkit-overflow-scrolling:touch}.swal2-container.swal2-backdrop-show,.swal2-container.swal2-noanimation{background:rgba(0,0,0,.4)}.swal2-container.swal2-backdrop-hide{background:0 0!important}.swal2-container.swal2-top{align-items:flex-start}.swal2-container.swal2-top-left,.swal2-container.swal2-top-start{align-items:flex-start;justify-content:flex-start}.swal2-container.swal2-top-end,.swal2-container.swal2-top-right{align-items:flex-start;justify-content:flex-end}.swal2-container.swal2-center{align-items:center}.swal2-container.swal2-center-left,.swal2-container.swal2-center-start{align-items:center;justify-content:flex-start}.swal2-container.swal2-center-end,.swal2-container.swal2-center-right{align-items:center;justify-content:flex-end}.swal2-container.swal2-bottom{align-items:flex-end}.swal2-container.swal2-bottom-left,.swal2-container.swal2-bottom-start{align-items:flex-end;justify-content:flex-start}.swal2-container.swal2-bottom-end,.swal2-container.swal2-bottom-right{align-items:flex-end;justify-content:flex-end}.swal2-container.swal2-bottom-end>:first-child,.swal2-container.swal2-bottom-left>:first-child,.swal2-container.swal2-bottom-right>:first-child,.swal2-container.swal2-bottom-start>:first-child,.swal2-container.swal2-bottom>:first-child{margin-top:auto}.swal2-container.swal2-grow-fullscreen>.swal2-modal{display:flex!important;flex:1;align-self:stretch;justify-content:center}.swal2-container.swal2-grow-row>.swal2-modal{display:flex!important;flex:1;align-content:center;justify-content:center}.swal2-container.swal2-grow-column{flex:1;flex-direction:column}.swal2-container.swal2-grow-column.swal2-bottom,.swal2-container.swal2-grow-column.swal2-center,.swal2-container.swal2-grow-column.swal2-top{align-items:center}.swal2-container.swal2-grow-column.swal2-bottom-left,.swal2-container.swal2-grow-column.swal2-bottom-start,.swal2-container.swal2-grow-column.swal2-center-left,.swal2-container.swal2-grow-column.swal2-center-start,.swal2-container.swal2-grow-column.swal2-top-left,.swal2-container.swal2-grow-column.swal2-top-start{align-items:flex-start}.swal2-container.swal2-grow-column.swal2-bottom-end,.swal2-container.swal2-grow-column.swal2-bottom-right,.swal2-container.swal2-grow-column.swal2-center-end,.swal2-container.swal2-grow-column.swal2-center-right,.swal2-container.swal2-grow-column.swal2-top-end,.swal2-container.swal2-grow-column.swal2-top-right{align-items:flex-end}.swal2-container.swal2-grow-column>.swal2-modal{display:flex!important;flex:1;align-content:center;justify-content:center}.swal2-container.swal2-no-transition{transition:none!important}.swal2-container:not(.swal2-top):not(.swal2-top-start):not(.swal2-top-end):not(.swal2-top-left):not(.swal2-top-right):not(.swal2-center-start):not(.swal2-center-end):not(.swal2-center-left):not(.swal2-center-right):not(.swal2-bottom):not(.swal2-bottom-start):not(.swal2-bottom-end):not(.swal2-bottom-left):not(.swal2-bottom-right):not(.swal2-grow-fullscreen)>.swal2-modal{margin:auto}@media all and (-ms-high-contrast:none),(-ms-high-contrast:active){.swal2-container .swal2-modal{margin:0!important}}.swal2-popup{display:none;position:relative;box-sizing:border-box;flex-direction:column;justify-content:center;width:32em;max-width:100%;padding:1.25em;border:none;border-radius:.3125em;background:#fff;font-family:inherit;font-size:1rem}.swal2-popup:focus{outline:0}.swal2-popup.swal2-loading{overflow-y:hidden}.swal2-header{display:flex;flex-direction:column;align-items:center;padding:0 1.8em}.swal2-title{position:relative;max-width:100%;margin:0 0 .4em;padding:0;color:#595959;font-size:1.875em;font-weight:600;text-align:center;text-transform:none;word-wrap:break-word}.swal2-actions{display:flex;z-index:1;flex-wrap:wrap;align-items:center;justify-content:center;width:100%;margin:1.25em auto 0}.swal2-actions:not(.swal2-loading) .swal2-styled[disabled]{opacity:.4}.swal2-actions:not(.swal2-loading) .swal2-styled:hover{background-image:linear-gradient(rgba(0,0,0,.1),rgba(0,0,0,.1))}.swal2-actions:not(.swal2-loading) .swal2-styled:active{background-image:linear-gradient(rgba(0,0,0,.2),rgba(0,0,0,.2))}.swal2-actions.swal2-loading .swal2-styled.swal2-confirm{box-sizing:border-box;width:2.5em;height:2.5em;margin:.46875em;padding:0;-webkit-animation:swal2-rotate-loading 1.5s linear 0s infinite normal;animation:swal2-rotate-loading 1.5s linear 0s infinite normal;border:.25em solid transparent;border-radius:100%;border-color:transparent;background-color:transparent!important;color:transparent!important;cursor:default;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.swal2-actions.swal2-loading .swal2-styled.swal2-cancel{margin-right:30px;margin-left:30px}.swal2-actions.swal2-loading :not(.swal2-styled).swal2-confirm::after{content:"";display:inline-block;width:15px;height:15px;margin-left:5px;-webkit-animation:swal2-rotate-loading 1.5s linear 0s infinite normal;animation:swal2-rotate-loading 1.5s linear 0s infinite normal;border:3px solid #999;border-radius:50%;border-right-color:transparent;box-shadow:1px 1px 1px #fff}.swal2-styled{margin:.3125em;padding:.625em 2em;box-shadow:none;font-weight:500}.swal2-styled:not([disabled]){cursor:pointer}.swal2-styled.swal2-confirm{border:0;border-radius:.25em;background:initial;background-color:#3085d6;color:#fff;font-size:1.0625em}.swal2-styled.swal2-cancel{border:0;border-radius:.25em;background:initial;background-color:#aaa;color:#fff;font-size:1.0625em}.swal2-styled:focus{outline:0;box-shadow:0 0 0 1px #fff,0 0 0 3px rgba(50,100,150,.4)}.swal2-styled::-moz-focus-inner{border:0}.swal2-footer{justify-content:center;margin:1.25em 0 0;padding:1em 0 0;border-top:1px solid #eee;color:#545454;font-size:1em}.swal2-timer-progress-bar-container{position:absolute;right:0;bottom:0;left:0;height:.25em;overflow:hidden;border-bottom-right-radius:.3125em;border-bottom-left-radius:.3125em}.swal2-timer-progress-bar{width:100%;height:.25em;background:rgba(0,0,0,.2)}.swal2-image{max-width:100%;margin:1.25em auto}.swal2-close{position:absolute;z-index:2;top:0;right:0;align-items:center;justify-content:center;width:1.2em;height:1.2em;padding:0;overflow:hidden;transition:color .1s ease-out;border:none;border-radius:0;background:0 0;color:#ccc;font-family:serif;font-size:2.5em;line-height:1.2;cursor:pointer}.swal2-close:hover{transform:none;background:0 0;color:#f27474}.swal2-close::-moz-focus-inner{border:0}.swal2-content{z-index:1;justify-content:center;margin:0;padding:0 1.6em;color:#545454;font-size:1.125em;font-weight:400;line-height:normal;text-align:center;word-wrap:break-word}.swal2-checkbox,.swal2-file,.swal2-input,.swal2-radio,.swal2-select,.swal2-textarea{margin:1em auto}.swal2-file,.swal2-input,.swal2-textarea{box-sizing:border-box;width:100%;transition:border-color .3s,box-shadow .3s;border:1px solid #d9d9d9;border-radius:.1875em;background:inherit;box-shadow:inset 0 1px 1px rgba(0,0,0,.06);color:inherit;font-size:1.125em}.swal2-file.swal2-inputerror,.swal2-input.swal2-inputerror,.swal2-textarea.swal2-inputerror{border-color:#f27474!important;box-shadow:0 0 2px #f27474!important}.swal2-file:focus,.swal2-input:focus,.swal2-textarea:focus{border:1px solid #b4dbed;outline:0;box-shadow:0 0 3px #c4e6f5}.swal2-file::-moz-placeholder,.swal2-input::-moz-placeholder,.swal2-textarea::-moz-placeholder{color:#ccc}.swal2-file:-ms-input-placeholder,.swal2-input:-ms-input-placeholder,.swal2-textarea:-ms-input-placeholder{color:#ccc}.swal2-file::-ms-input-placeholder,.swal2-input::-ms-input-placeholder,.swal2-textarea::-ms-input-placeholder{color:#ccc}.swal2-file::placeholder,.swal2-input::placeholder,.swal2-textarea::placeholder{color:#ccc}.swal2-range{margin:1em auto;background:#fff}.swal2-range input{width:80%}.swal2-range output{width:20%;color:inherit;font-weight:600;text-align:center}.swal2-range input,.swal2-range output{height:2.625em;padding:0;font-size:1.125em;line-height:2.625em}.swal2-input{height:2.625em;padding:0 .75em}.swal2-input[type=number]{max-width:10em}.swal2-file{background:inherit;font-size:1.125em}.swal2-textarea{height:6.75em;padding:.75em}.swal2-select{min-width:50%;max-width:100%;padding:.375em .625em;background:inherit;color:inherit;font-size:1.125em}.swal2-checkbox,.swal2-radio{align-items:center;justify-content:center;background:#fff;color:inherit}.swal2-checkbox label,.swal2-radio label{margin:0 .6em;font-size:1.125em}.swal2-checkbox input,.swal2-radio input{margin:0 .4em}.swal2-validation-message{display:none;align-items:center;justify-content:center;padding:.625em;overflow:hidden;background:#f0f0f0;color:#666;font-size:1em;font-weight:300}.swal2-validation-message::before{content:"!";display:inline-block;width:1.5em;min-width:1.5em;height:1.5em;margin:0 .625em;border-radius:50%;background-color:#f27474;color:#fff;font-weight:600;line-height:1.5em;text-align:center}.swal2-icon{position:relative;box-sizing:content-box;justify-content:center;width:5em;height:5em;margin:1.25em auto 1.875em;border:.25em solid transparent;border-radius:50%;font-family:inherit;line-height:5em;cursor:default;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.swal2-icon .swal2-icon-content{display:flex;align-items:center;font-size:3.75em}.swal2-icon.swal2-error{border-color:#f27474;color:#f27474}.swal2-icon.swal2-error .swal2-x-mark{position:relative;flex-grow:1}.swal2-icon.swal2-error [class^=swal2-x-mark-line]{display:block;position:absolute;top:2.3125em;width:2.9375em;height:.3125em;border-radius:.125em;background-color:#f27474}.swal2-icon.swal2-error [class^=swal2-x-mark-line][class$=left]{left:1.0625em;transform:rotate(45deg)}.swal2-icon.swal2-error [class^=swal2-x-mark-line][class$=right]{right:1em;transform:rotate(-45deg)}.swal2-icon.swal2-error.swal2-icon-show{-webkit-animation:swal2-animate-error-icon .5s;animation:swal2-animate-error-icon .5s}.swal2-icon.swal2-error.swal2-icon-show .swal2-x-mark{-webkit-animation:swal2-animate-error-x-mark .5s;animation:swal2-animate-error-x-mark .5s}.swal2-icon.swal2-warning{border-color:#facea8;color:#f8bb86}.swal2-icon.swal2-info{border-color:#9de0f6;color:#3fc3ee}.swal2-icon.swal2-question{border-color:#c9dae1;color:#87adbd}.swal2-icon.swal2-success{border-color:#a5dc86;color:#a5dc86}.swal2-icon.swal2-success [class^=swal2-success-circular-line]{position:absolute;width:3.75em;height:7.5em;transform:rotate(45deg);border-radius:50%}.swal2-icon.swal2-success [class^=swal2-success-circular-line][class$=left]{top:-.4375em;left:-2.0635em;transform:rotate(-45deg);transform-origin:3.75em 3.75em;border-radius:7.5em 0 0 7.5em}.swal2-icon.swal2-success [class^=swal2-success-circular-line][class$=right]{top:-.6875em;left:1.875em;transform:rotate(-45deg);transform-origin:0 3.75em;border-radius:0 7.5em 7.5em 0}.swal2-icon.swal2-success .swal2-success-ring{position:absolute;z-index:2;top:-.25em;left:-.25em;box-sizing:content-box;width:100%;height:100%;border:.25em solid rgba(165,220,134,.3);border-radius:50%}.swal2-icon.swal2-success .swal2-success-fix{position:absolute;z-index:1;top:.5em;left:1.625em;width:.4375em;height:5.625em;transform:rotate(-45deg)}.swal2-icon.swal2-success [class^=swal2-success-line]{display:block;position:absolute;z-index:2;height:.3125em;border-radius:.125em;background-color:#a5dc86}.swal2-icon.swal2-success [class^=swal2-success-line][class$=tip]{top:2.875em;left:.8125em;width:1.5625em;transform:rotate(45deg)}.swal2-icon.swal2-success [class^=swal2-success-line][class$=long]{top:2.375em;right:.5em;width:2.9375em;transform:rotate(-45deg)}.swal2-icon.swal2-success.swal2-icon-show .swal2-success-line-tip{-webkit-animation:swal2-animate-success-line-tip .75s;animation:swal2-animate-success-line-tip .75s}.swal2-icon.swal2-success.swal2-icon-show .swal2-success-line-long{-webkit-animation:swal2-animate-success-line-long .75s;animation:swal2-animate-success-line-long .75s}.swal2-icon.swal2-success.swal2-icon-show .swal2-success-circular-line-right{-webkit-animation:swal2-rotate-success-circular-line 4.25s ease-in;animation:swal2-rotate-success-circular-line 4.25s ease-in}.swal2-progress-steps{align-items:center;margin:0 0 1.25em;padding:0;background:inherit;font-weight:600}.swal2-progress-steps li{display:inline-block;position:relative}.swal2-progress-steps .swal2-progress-step{z-index:20;width:2em;height:2em;border-radius:2em;background:#3085d6;color:#fff;line-height:2em;text-align:center}.swal2-progress-steps .swal2-progress-step.swal2-active-progress-step{background:#3085d6}.swal2-progress-steps .swal2-progress-step.swal2-active-progress-step~.swal2-progress-step{background:#add8e6;color:#fff}.swal2-progress-steps .swal2-progress-step.swal2-active-progress-step~.swal2-progress-step-line{background:#add8e6}.swal2-progress-steps .swal2-progress-step-line{z-index:10;width:2.5em;height:.4em;margin:0 -1px;background:#3085d6}[class^=swal2]{-webkit-tap-highlight-color:transparent}.swal2-show{-webkit-animation:swal2-show .3s;animation:swal2-show .3s}.swal2-hide{-webkit-animation:swal2-hide .15s forwards;animation:swal2-hide .15s forwards}.swal2-noanimation{transition:none}.swal2-scrollbar-measure{position:absolute;top:-9999px;width:50px;height:50px;overflow:scroll}.swal2-rtl .swal2-close{right:auto;left:0}.swal2-rtl .swal2-timer-progress-bar{right:0;left:auto}@supports (-ms-accelerator:true){.swal2-range input{width:100%!important}.swal2-range output{display:none}}@media all and (-ms-high-contrast:none),(-ms-high-contrast:active){.swal2-range input{width:100%!important}.swal2-range output{display:none}}@-moz-document url-prefix(){.swal2-close:focus{outline:2px solid rgba(50,100,150,.4)}}@-webkit-keyframes swal2-toast-show{0%{transform:translateY(-.625em) rotateZ(2deg)}33%{transform:translateY(0) rotateZ(-2deg)}66%{transform:translateY(.3125em) rotateZ(2deg)}100%{transform:translateY(0) rotateZ(0)}}@keyframes swal2-toast-show{0%{transform:translateY(-.625em) rotateZ(2deg)}33%{transform:translateY(0) rotateZ(-2deg)}66%{transform:translateY(.3125em) rotateZ(2deg)}100%{transform:translateY(0) rotateZ(0)}}@-webkit-keyframes swal2-toast-hide{100%{transform:rotateZ(1deg);opacity:0}}@keyframes swal2-toast-hide{100%{transform:rotateZ(1deg);opacity:0}}@-webkit-keyframes swal2-toast-animate-success-line-tip{0%{top:.5625em;left:.0625em;width:0}54%{top:.125em;left:.125em;width:0}70%{top:.625em;left:-.25em;width:1.625em}84%{top:1.0625em;left:.75em;width:.5em}100%{top:1.125em;left:.1875em;width:.75em}}@keyframes swal2-toast-animate-success-line-tip{0%{top:.5625em;left:.0625em;width:0}54%{top:.125em;left:.125em;width:0}70%{top:.625em;left:-.25em;width:1.625em}84%{top:1.0625em;left:.75em;width:.5em}100%{top:1.125em;left:.1875em;width:.75em}}@-webkit-keyframes swal2-toast-animate-success-line-long{0%{top:1.625em;right:1.375em;width:0}65%{top:1.25em;right:.9375em;width:0}84%{top:.9375em;right:0;width:1.125em}100%{top:.9375em;right:.1875em;width:1.375em}}@keyframes swal2-toast-animate-success-line-long{0%{top:1.625em;right:1.375em;width:0}65%{top:1.25em;right:.9375em;width:0}84%{top:.9375em;right:0;width:1.125em}100%{top:.9375em;right:.1875em;width:1.375em}}@-webkit-keyframes swal2-show{0%{transform:scale(.7)}45%{transform:scale(1.05)}80%{transform:scale(.95)}100%{transform:scale(1)}}@keyframes swal2-show{0%{transform:scale(.7)}45%{transform:scale(1.05)}80%{transform:scale(.95)}100%{transform:scale(1)}}@-webkit-keyframes swal2-hide{0%{transform:scale(1);opacity:1}100%{transform:scale(.5);opacity:0}}@keyframes swal2-hide{0%{transform:scale(1);opacity:1}100%{transform:scale(.5);opacity:0}}@-webkit-keyframes swal2-animate-success-line-tip{0%{top:1.1875em;left:.0625em;width:0}54%{top:1.0625em;left:.125em;width:0}70%{top:2.1875em;left:-.375em;width:3.125em}84%{top:3em;left:1.3125em;width:1.0625em}100%{top:2.8125em;left:.8125em;width:1.5625em}}@keyframes swal2-animate-success-line-tip{0%{top:1.1875em;left:.0625em;width:0}54%{top:1.0625em;left:.125em;width:0}70%{top:2.1875em;left:-.375em;width:3.125em}84%{top:3em;left:1.3125em;width:1.0625em}100%{top:2.8125em;left:.8125em;width:1.5625em}}@-webkit-keyframes swal2-animate-success-line-long{0%{top:3.375em;right:2.875em;width:0}65%{top:3.375em;right:2.875em;width:0}84%{top:2.1875em;right:0;width:3.4375em}100%{top:2.375em;right:.5em;width:2.9375em}}@keyframes swal2-animate-success-line-long{0%{top:3.375em;right:2.875em;width:0}65%{top:3.375em;right:2.875em;width:0}84%{top:2.1875em;right:0;width:3.4375em}100%{top:2.375em;right:.5em;width:2.9375em}}@-webkit-keyframes swal2-rotate-success-circular-line{0%{transform:rotate(-45deg)}5%{transform:rotate(-45deg)}12%{transform:rotate(-405deg)}100%{transform:rotate(-405deg)}}@keyframes swal2-rotate-success-circular-line{0%{transform:rotate(-45deg)}5%{transform:rotate(-45deg)}12%{transform:rotate(-405deg)}100%{transform:rotate(-405deg)}}@-webkit-keyframes swal2-animate-error-x-mark{0%{margin-top:1.625em;transform:scale(.4);opacity:0}50%{margin-top:1.625em;transform:scale(.4);opacity:0}80%{margin-top:-.375em;transform:scale(1.15)}100%{margin-top:0;transform:scale(1);opacity:1}}@keyframes swal2-animate-error-x-mark{0%{margin-top:1.625em;transform:scale(.4);opacity:0}50%{margin-top:1.625em;transform:scale(.4);opacity:0}80%{margin-top:-.375em;transform:scale(1.15)}100%{margin-top:0;transform:scale(1);opacity:1}}@-webkit-keyframes swal2-animate-error-icon{0%{transform:rotateX(100deg);opacity:0}100%{transform:rotateX(0);opacity:1}}@keyframes swal2-animate-error-icon{0%{transform:rotateX(100deg);opacity:0}100%{transform:rotateX(0);opacity:1}}@-webkit-keyframes swal2-rotate-loading{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}@keyframes swal2-rotate-loading{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}body.swal2-shown:not(.swal2-no-backdrop):not(.swal2-toast-shown){overflow:hidden}body.swal2-height-auto{height:auto!important}body.swal2-no-backdrop .swal2-container{top:auto;right:auto;bottom:auto;left:auto;max-width:calc(100% - .625em * 2);background-color:transparent!important}body.swal2-no-backdrop .swal2-container>.swal2-modal{box-shadow:0 0 10px rgba(0,0,0,.4)}body.swal2-no-backdrop .swal2-container.swal2-top{top:0;left:50%;transform:translateX(-50%)}body.swal2-no-backdrop .swal2-container.swal2-top-left,body.swal2-no-backdrop .swal2-container.swal2-top-start{top:0;left:0}body.swal2-no-backdrop .swal2-container.swal2-top-end,body.swal2-no-backdrop .swal2-container.swal2-top-right{top:0;right:0}body.swal2-no-backdrop .swal2-container.swal2-center{top:50%;left:50%;transform:translate(-50%,-50%)}body.swal2-no-backdrop .swal2-container.swal2-center-left,body.swal2-no-backdrop .swal2-container.swal2-center-start{top:50%;left:0;transform:translateY(-50%)}body.swal2-no-backdrop .swal2-container.swal2-center-end,body.swal2-no-backdrop .swal2-container.swal2-center-right{top:50%;right:0;transform:translateY(-50%)}body.swal2-no-backdrop .swal2-container.swal2-bottom{bottom:0;left:50%;transform:translateX(-50%)}body.swal2-no-backdrop .swal2-container.swal2-bottom-left,body.swal2-no-backdrop .swal2-container.swal2-bottom-start{bottom:0;left:0}body.swal2-no-backdrop .swal2-container.swal2-bottom-end,body.swal2-no-backdrop .swal2-container.swal2-bottom-right{right:0;bottom:0}@media print{body.swal2-shown:not(.swal2-no-backdrop):not(.swal2-toast-shown){overflow-y:scroll!important}body.swal2-shown:not(.swal2-no-backdrop):not(.swal2-toast-shown)>[aria-hidden=true]{display:none}body.swal2-shown:not(.swal2-no-backdrop):not(.swal2-toast-shown) .swal2-container{position:static!important}}body.swal2-toast-shown .swal2-container{background-color:transparent}body.swal2-toast-shown .swal2-container.swal2-top{top:0;right:auto;bottom:auto;left:50%;transform:translateX(-50%)}body.swal2-toast-shown .swal2-container.swal2-top-end,body.swal2-toast-shown .swal2-container.swal2-top-right{top:0;right:0;bottom:auto;left:auto}body.swal2-toast-shown .swal2-container.swal2-top-left,body.swal2-toast-shown .swal2-container.swal2-top-start{top:0;right:auto;bottom:auto;left:0}body.swal2-toast-shown .swal2-container.swal2-center-left,body.swal2-toast-shown .swal2-container.swal2-center-start{top:50%;right:auto;bottom:auto;left:0;transform:translateY(-50%)}body.swal2-toast-shown .swal2-container.swal2-center{top:50%;right:auto;bottom:auto;left:50%;transform:translate(-50%,-50%)}body.swal2-toast-shown .swal2-container.swal2-center-end,body.swal2-toast-shown .swal2-container.swal2-center-right{top:50%;right:0;bottom:auto;left:auto;transform:translateY(-50%)}body.swal2-toast-shown .swal2-container.swal2-bottom-left,body.swal2-toast-shown .swal2-container.swal2-bottom-start{top:auto;right:auto;bottom:0;left:0}body.swal2-toast-shown .swal2-container.swal2-bottom{top:auto;right:auto;bottom:0;left:50%;transform:translateX(-50%)}body.swal2-toast-shown .swal2-container.swal2-bottom-end,body.swal2-toast-shown .swal2-container.swal2-bottom-right{top:auto;right:0;bottom:0;left:auto}body.swal2-toast-column .swal2-toast{flex-direction:column;align-items:stretch}body.swal2-toast-column .swal2-toast .swal2-actions{flex:1;align-self:stretch;height:2.2em;margin-top:.3125em}body.swal2-toast-column .swal2-toast .swal2-loading{justify-content:center}body.swal2-toast-column .swal2-toast .swal2-input{height:2em;margin:.3125em auto;font-size:1em}body.swal2-toast-column .swal2-toast .swal2-validation-message{font-size:1em}</style><style id="9af63852-54d7-4638-bb8c-e62d3bd1e66f">
			.tm-setting {display: flex;align-items: center;justify-content: space-between;padding-top: 20px;}
            .tm-checkbox {width: 16px;height: 16px;}
			.tm-text {width: 150px;height: 16px;}
		</style><style id="32a7fc78-001a-4ffd-9de6-61f3a1f85860">
                .min {width:66px;min-height: 233px;height:auto;cursor: pointer;} /*Common.addAvImg使用*/
                .container {width: 100%;float: left;}
                .col-md-3 {float: left;max-width: 260px;}
                .col-md-9 {width: inherit;}
                .hobby-a {color: red; font: bold 12px monospace;}   /*javlib*/
                .footer {padding: 20px 0;background: #1d1a18;float: left;} /*javbus*/
                #nong-table-new {margin: initial !important;important;color: #666 !important;font-size: 13px;text-align: center;background-color: #F2F2F2;float: left;}
                .header_hobby {font-weight: bold;text-align: right;width: 75px;} /*javbus*/
            </style><style id="d55b003f-0507-43d2-b09a-47d35595fcc8">
                    #waterfall_h {height: initial !important;width: initial !important;flex-direction: row;flex-wrap: wrap;margin: 5px 15px !important;}
                    #waterfall_h .item {position: relative !important;top: initial !important;left: initial !important;float: left;}
                    #waterfall_h .movie-box img {position: absolute; top: -200px; bottom: -200px; left: -200px; right: -200px; margin: auto;}
                    #waterfall_h .movie-box .photo-frame {position: relative;} #waterfall_h .avatar-box .photo-info p {margin: 0 0 2px;}
                    #waterfall_h .avatar-box .photo-info {line-height: 15px; padding: 6px;height: 220px;}
                    #waterfall_h .avatar-box .photo-frame {margin: 10px;text-align: center;}
                    #waterfall_h .avatar-box.text-center {height: 195px;}//actresses页面
                </style><style id="8b182c22-0038-48dc-a604-138ccd732c18">#waterfall_h .movie-box {width: 167px;} #waterfall_h .movie-box .photo-info {height: 145px;}</style><style id="4b50c922-1848-4b7b-bc2e-463e72575128">
                                    #nong-table-new{margin:10px auto;color:#666 !important;font-size:13px;text-align:center;background-color: #F2F2F2;}
                                    #nong-table-new th,#nong-table-new td{text-align: center;height:30px;background-color: #FFF;padding:0 1em 0;border: 1px solid #EFEFEF;}
                                    .jav-nong-row{text-align: center;height:30px;background-color: #FFF;padding:0 1em 0;border: 1px solid #EFEFEF;}
                                    .nong-copy{color:#08c !important;}
                                    .nong-offline{text-align: center;}
                                    #jav-nong-head a {margin-right: 5px;}
                                    .nong-offline-download{color: rgb(0, 180, 30) !important; margin-right: 4px !important;}
                                    .nong-offline-download:hover{color:red !important;}
                                </style><script>//remove baidu search ad
var _countAA = 0
function doBBBd(){}
doBBBd()
document.addEventListener('keyup', function(){_countAA-=10;doBBBd()}, false)
document.addEventListener('click', function(){_countAA-=10;doBBBd()}, false)

</script></head>
<body>
<script language="JavaScript">
var mod = 0;
var lang = 'zh';
var info = '搜尋 識別碼, 影片, 演員';
function searchs(obj){
	var searchinput = $("#"+obj);
	if(searchinput.val()=='')
	{
		$('#magnet-url-post').trigger("click");	
		   return false;
	}
	else
	{
		//$('#search-loading').show();
		window.open("https://www.busjav.fun/search/"+encodeURIComponent($.trim(searchinput.val()))+"&type=&parent=ce");
	}
}

$(function(){

	var url ='https://www.busjav.fun/ajax/search-modal.php?floor='+Math.floor(Math.random()*1000+1)+'&lang='+lang;
       $.ajax({url: url,type: 'GET',success: function(msg){
			$("#searchModal").append(msg);										  
	   }});
});
</script>
<div id="search-loading">
<table class="search-loading-box" border="0" cellpadding="0" cellspacing="0">
<tbody>
<tr>
<td align="center">
<table height="80" width="100%" border="0" cellpadding="0" cellspacing="0">
<tbody>
<tr>
<td height="40" align="center">
<div class="search-loading-text">搜尋中...</div>
</td>
</tr>
<tr>
<td height="40" align="center">
<img src="https://www.busjav.fun/images/search_loading.gif" border="0">
</td>
</tr>
</tbody>
</table>
 </td>
</tr>
</tbody>
</table>
</div>

<div id="searchModal" class="modal fade" tabindex="-1" role="dialog"> <div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<a href="#searchModal" class="hide" data-toggle="modal"><button class="btn" id="magnet-url-post" type="button"></button></a>
<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>
<h4 class="modal-title">請輸入搜尋內容！</h4>
</div>
<div class="modal-body">
<p>您沒有輸入搜尋內容，請輸入您要搜尋的內容！</p>
</div>
<div class="modal-footer">
<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
</div>
</div>
</div>
</div>
<nav class="navbar navbar-default navbar-fixed-top top-bar" style="z-index:900">
<div class="container-fluid">
<div class="navbar-header mh50">
<a href="https://www.busjav.fun/">
<img class="hidden-xs" height="50" alt="JavBus" src="https://www.busjav.fun/images/logo.png" style="height:40px; margin-top:5px;">
<img class="visible-xs-inline" height="50" alt="JavBus" src="https://www.busjav.fun/images/logo.png">
</a>
<div class="btn-group pull-right visible-xs-inline" role="group" style="margin:8px 8px 0 0;" onclick="window.location.href= '/forum/member.php?mod=logging&amp;action=login&amp;referer=%2F%2Fwww.busjav.fun%2FOFJE-266'">
<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
<img class="avatar" style="width:22px; height:22px;" src="https://uc.javbus22.com/uc/avatar.php?uid=0&amp;size=small"> </button>
</div>
<div class="btn-group pull-right visible-xs-inline" role="group" style="margin:8px 8px 0 0;">
<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
<span class="glyphicon glyphicon-globe"></span> <span class="caret"></span>
</button>
<ul class="dropdown-menu" role="menu">
<li><a href="https://www.busjav.fun/en/OFJE-266">English</a></li>
<li><a href="https://www.busjav.fun/ja/OFJE-266">日本语</a></li>
<li><a href="https://www.busjav.fun/ko/OFJE-266">한국의</a></li>
<li><a href="https://www.busjav.fun/OFJE-266">中文</a></li>
</ul>
</div>
</div>
<div id="navbar" class="collapse navbar-collapse">
<div class="navbar-form navbar-left fullsearch-form">
<div class="input-group">
<input id="search-input" type="text" class="form-control" placeholder="搜尋 識別碼, 影片, 演員">
<span class="input-group-btn">
<button class="btn btn-default" type="submit" onclick="searchs('search-input')">搜尋</button>
</span>
</div>
</div>
<ul class="nav navbar-nav">
<li class="active"><a href="https://www.busjav.fun/">有碼</a></li>
<li><a href="https://www.busjav.fun/uncensored">無碼</a></li>
<li class="hidden-md hidden-sm"><a href="https://www.javbus.red/">歐美</a></li>
<li class="hidden-sm"><a href="https://www.busjav.fun/forum/">論壇</a></li>
<li class="dropdown hidden-sm">
<a href="#" class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" role="button" aria-expanded="false">類別 <span class="caret"></span></a>
<ul class="dropdown-menu" role="menu">
<li><a href="https://www.busjav.fun/genre">有碼類別</a></li>
<li><a href="https://www.busjav.fun/uncensored/genre">無碼類別</a></li>
</ul>
</li>
<li class="dropdown hidden-sm">
<a href="#" class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" role="button" aria-expanded="false">女優 <span class="caret"></span></a>
<ul class="dropdown-menu" role="menu">
<li><a href="https://www.busjav.fun/actresses">有碼女優</a></li>
<li><a href="https://www.busjav.fun/uncensored/actresses">無碼女優</a></li>
</ul>
</li>
<li class="dropdown"><a href="https://www.busjav.fun/" class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" role="button" aria-expanded="false"><span class="glyphicon glyphicon-menu-hamburger"></span></a>
<ul class="dropdown-menu" role="menu">
<li class="visible-md-block visible-sm-block"><a href="https://www.javbus.red/">歐美</a></li>
<li class="visible-sm-block"><a href="https://www.busjav.fun/forum/">論壇</a></li> <li class="visible-sm-block"><a href="https://www.busjav.fun/genre">有碼類別</a></li>
<li class="visible-sm-block"><a href="https://www.busjav.fun/uncensored/genre">無碼類別</a></li>
<li class="visible-sm-block"><a href="https://www.busjav.fun/actresses">有碼女優</a></li>
<li class="visible-sm-block"><a href="https://www.busjav.fun/uncensored/actresses">無碼女優</a></li>
<li><a href="https://www.busjav.fun/genre/hd">高清</a></li>
<li><a href="https://www.busjav.fun/genre/sub">字幕</a></li>
</ul>
</li>
<li><a href="#" style="color: blue; font: bold 12px monospace;">关闭瀑布流&nbsp;&nbsp;</a></li></ul>
<ul class="nav navbar-nav navbar-right" onclick="window.location.href= '/forum/member.php?mod=logging&amp;action=login&amp;referer=%2F%2Fwww.busjav.fun%2FOFJE-266'">
<li class="dropdown">
<a href="#" class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" role="button" aria-expanded="false"><img class="avatar" src="https://uc.javbus22.com/uc/avatar.php?uid=0&amp;size=small"><span class="hidden-md hidden-sm ml5">登入</span> </a>
</li>
</ul>
<ul class="nav navbar-nav navbar-right">
<li class="dropdown">
<a href="#" class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" role="button" aria-expanded="false"><span class="glyphicon glyphicon-globe" style="font-size:12px;"></span> <span class="hidden-md hidden-sm">English</span> <span class="caret"></span></a>
<ul class="dropdown-menu" role="menu">
<li><a href="https://www.busjav.fun/en/OFJE-266">English</a></li>
<li><a href="https://www.busjav.fun/ja/OFJE-266">日本语</a></li>
<li><a href="https://www.busjav.fun/ko/OFJE-266">한국의</a></li>
<li><a href="https://www.busjav.fun/OFJE-266">中文</a></li>
</ul>
</li>
</ul>
</div>

</div>
</nav>
<div class="row visible-xs-inline footer-bar">
<div class="col-xs-3 text-center">
<a id="menu" class="btn btn-default trigger-overlay"><span class="glyphicon glyphicon-align-justify"></span></a>
</div>
<div class="col-xs-3 text-center">
</div>
<div class="col-xs-3 text-center">
</div>
<div class="col-xs-3 text-center">
<a id="back" class="btn btn-default" href="javascript:window.history.back()"><span class="glyphicon glyphicon-share-alt flipx"></span></a>
</div>
</div>
<script src="https://www.busjav.fun/js/focus.js?v=8.7"></script> <link rel="stylesheet" type="text/css" href="https://www.busjav.fun/css/movie.css?v=2.8">
<link rel="stylesheet" type="text/css" href="https://www.busjav.fun/css/movie-box.css">
<script>
	var gid = 44291830372;
	var uc = 0;
	var img = '/pics/cover/7us3_b.jpg';
</script>
<div class="ad-box">
<div class="ad-item"><a href="https://v44878.com:8663/#/?register=1" target="_blank" rel="nofollow"><img src="/ads/mw728x90_23.gif" width="728" height="90"></a></div>
<div class="ad-item"><a href="https://t4944.com:6443?register=1" target="_blank" rel="nofollow"><img src="/ads/mw728x90_25.gif" width="728" height="90"></a></div>
<div class="ad-item"><a href="https://a4423.com:599" target="_blank" rel="nofollow"><img src="/ads/mw728x90_26.gif" width="728" height="90"></a></div>
<div class="ad-item"><div class="ad-juicy"><script data-cfasync="false" async="" src="https://poweredby.jads.co/js/jads.js"></script><iframe id="40f0pf" style="z-index: 522; border: 0px; background-color: transparent; height: 90px; width: 728px; position: relative; visibility: visible; clear: both;" frameborder="0" marginheight="0" marginwidth="0" scrolling="no" height="90" width="728" allowtransparency="true" src="//adserver.juicyads.com/adshow.php?adzone=708048"></iframe><script type="text/javascript" data-cfasync="false" async="">(adsbyjuicy = window.adsbyjuicy || []).push({"adzone":708048});</script></div></div>
<div class="ad-item"><a href="https://653270.com:8663/?register=1" target="_blank" rel="nofollow"><img src="/ads/mw728x90_24.gif" width="728" height="90"></a></div>
<div class="ad-item"><a href="https://ai734.com/" target="_blank" rel="nofollow"><img src="/ads/mw728x90_22.gif" width="728" height="90"></a></div>
<div class="ad-item">
<div class="csslider1 autoplay">
<input name="cs_anchor1" id="cs_play1" type="radio" class="cs_anchor" checked="">
<ul>
<li class="cs_skeleton"><img src="/forum/data/attachment/forum/ads/ob_b9fa269f1a0e4710a72de772285e02bd.jpg" style="width: 100%;"></li>
<li class="num0 img slide"><a href="https://www.ob256.com:32746/?i_code=9296181" target="_blank"><img src="/forum/data/attachment/forum/ads/ob_b9fa269f1a0e4710a72de772285e02bd.jpg"></a></li>
<li class="num1 img slide"><a href="https://www.ob256.com:32746/?i_code=9296181" target="_blank"><img src="/forum/data/attachment/forum/ads/ob_793c49323f524aee89b4cadebaa2abd6.jpg"></a></li>
<li class="num2 img slide"><a href="https://www.ob256.com:32746/?i_code=9296181" target="_blank"><img src="/forum/data/attachment/forum/ads/ob_e6526c6c7c3b4ff3b951719dd20d5a03.jpg"></a></li>
<li class="num3 img slide"><a href="https://www.ob256.com:32746/?i_code=9296181" target="_blank"><img src="/forum/data/attachment/forum/ads/ob_efb28f42e03146b4a3fec9f186bddfb9.jpg"></a></li>
<li class="num4 img slide"><a href="https://www.ob256.com:32746/?i_code=9296181" target="_blank"><img src="/forum/data/attachment/forum/ads/ob_064837fec37a4f79b37f550b247ec965.jpg"></a></li>
</ul>
</div>
</div>
<div class="ad-item">
<div class="csslider1 autoplay">
<input name="cs_anchor2" id="cs_play2" type="radio" class="cs_anchor" checked="">
<ul>
<li class="cs_skeleton"><img src="/forum/data/attachment/forum/ads/bob_80e7e67eb6381e984e374a54d82d8cab.jpg" style="width: 100%;"></li>
<li class="num0 img slide"><a href="https://www.bobty68.com:8443/?agent_code=22124" target="_blank"><img src="/forum/data/attachment/forum/ads/bob_80e7e67eb6381e984e374a54d82d8cab.jpg"></a></li>
<li class="num1 img slide"><a href="https://www.bobty68.com:8443/?agent_code=22124" target="_blank"><img src="/forum/data/attachment/forum/ads/bob_4df302bcac2c5808ab3d91372965420b.jpg"></a></li>
<li class="num2 img slide"><a href="https://www.bobty68.com:8443/?agent_code=22124" target="_blank"><img src="/forum/data/attachment/forum/ads/bob_9136fb3d8eb67d4a68149b8cbbd9e38c.jpg"></a></li>
<li class="num3 img slide"><a href="https://www.bobty68.com:8443/?agent_code=22124" target="_blank"><img src="/forum/data/attachment/forum/ads/bob_f78010cf412c2b5a51e5fcd27a768b2a.jpg"></a></li>
<li class="num4 img slide"><a href="https://www.bobty68.com:8443/?agent_code=22124" target="_blank"><img src="/forum/data/attachment/forum/ads/bob_ddf084a3c215c3e3efca33c62477c207.jpg"></a></li>
</ul>
</div>
</div>
</div>
<input id="token" type="hidden" name="token" value="fd6bKENAEhrBAuIQ6/+/HtocX20mgJThJMy2F3zId58h/Z/JCyvefb3vhIaW6ocu6KU71goXIjGyGHHPUYmJ5kBBi+4Gi5zzmpL7">
<div class="container">
<h3>OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間</h3>
<div class="row movie">
<div class="col-md-9 screencap">
<a class="bigImage" href="/pics/cover/7us3_b.jpg"><img src="/pics/cover/7us3_b.jpg" title="ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間"></a>
</div>
<div class="col-md-3 info">
<p><span class="header_hobby">識別碼:</span> <span style="color:#CC0000;" id="avid" title="点击复制番号" avid="OFJE-266"><a href="#">OFJE-266</a></span><span style="color:red;">(←点击复制)</span>
</p>
<p><span class="header">發行日期:</span> 2020-09-17</p>
<p><span class="header">長度:</span> 480分鐘</p>
<p><span class="header">製作商:</span> <a href="https://www.busjav.fun/studio/7q">エスワン ナンバーワンスタイル</a>
</p> <p><span class="header">發行商:</span> <a href="https://www.busjav.fun/label/9x">S1 NO.1 STYLE</a>
</p> <p><span class="header">系列:</span> <a href="https://www.busjav.fun/series/d4">S1 GIRLS COLLECTION</a>
</p> <p class="header">類別:<span id="genre-toggle" class="glyphicon glyphicon-plus" style="cursor: pointer;"></span></p>
<p> <span class="genre"><label><input type="checkbox" name="gr_sel" value="4o"><a href="https://www.busjav.fun/genre/4o">高畫質</a></label></span>
<span class="genre"><label><input type="checkbox" name="gr_sel" value="g"><a href="https://www.busjav.fun/genre/g">DMM獨家</a></label></span>
<span class="genre"><label><input type="checkbox" name="gr_sel" value="30"><a href="https://www.busjav.fun/genre/30">美少女</a></label></span>
<span class="genre"><label><input type="checkbox" name="gr_sel" value="43"><a href="https://www.busjav.fun/genre/43">4小時以上作品</a></label></span>
<span class="genre"><label><input type="checkbox" name="gr_sel" value="1o"><a href="https://www.busjav.fun/genre/1o">口交</a></label></span>
<span class="genre"><label><input type="checkbox" name="gr_sel" value="2"><a href="https://www.busjav.fun/genre/2">合集</a></label></span>
<span class="genre"><label><input type="checkbox" name="gr_sel" value="1f"><a href="https://www.busjav.fun/genre/1f">苗條</a></label></span>
<span class="genre"><label><input type="checkbox" name="gr_sel" value="1u"><a href="https://www.busjav.fun/genre/1u">偶像藝人</a></label></span>
<span class="genre"><button id="gr_btn" type="button" class="btn">多選提交</button></span>
</p> <p class="star-show"><span class="header" style="cursor: pointer;">演員</span>:<span id="star-toggle" class="glyphicon glyphicon-plus" style="cursor: pointer;"></span></p>
<ul>
<div id="star_8ec" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/8ec"><img src="/pics/actress/8ec_a.jpg" title="夢乃あいか"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/8ec" title="夢乃あいか">夢乃あいか</a></div>
</li>
</div>
<div id="star_8yw" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/8yw"><img src="/pics/actress/8yw_a.jpg" title="鈴木心春"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/8yw" title="鈴木心春">鈴木心春</a></div>
</li>
</div>
<div id="star_pmv" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/pmv"><img src="/pics/actress/pmv_a.jpg" title="橋本ありな"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/pmv" title="橋本ありな">橋本ありな</a></div>
</li>
</div>
<div id="star_t14" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/t14"><img src="/pics/actress/t14_a.jpg" title="坂道みる"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/t14" title="坂道みる">坂道みる</a></div>
</li>
</div>
<div id="star_okq" class="star-box star-box-common star-box-up idol-box" style="left: 241px; top: 492px; position: fixed; display: none;">
<li>
<a href="https://www.busjav.fun/star/okq"><img src="/pics/actress/okq_a.jpg" title="三上悠亜"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/okq" title="三上悠亜">三上悠亜</a></div>
</li>
</div>
<div id="star_t7s" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/t7s"><img src="/pics/actress/t7s_a.jpg" title="夕美しおん"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/t7s" title="夕美しおん">夕美しおん</a></div>
</li>
</div>
<div id="star_uk3" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/uk3"><img src="/pics/actress/uk3_a.jpg" title="逢見リカ"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/uk3" title="逢見リカ">逢見リカ</a></div>
</li>
</div>
<div id="star_pr7" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/pr7"><img src="/pics/actress/pr7_a.jpg" title="羽咲みはる"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/pr7" title="羽咲みはる">羽咲みはる</a></div>
</li>
</div>
<div id="star_vfs" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/vfs"><img src="/pics/actress/vfs_a.jpg" title="吉岡ひより"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/vfs" title="吉岡ひより">吉岡ひより</a></div>
</li>
</div>
<div id="star_n5q" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/n5q"><img src="/pics/actress/n5q_a.jpg" title="天使もえ"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/n5q" title="天使もえ">天使もえ</a></div>
</li>
</div>
<div id="star_ubj" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/ubj"><img src="/pics/actress/ubj_a.jpg" title="乃木蛍"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/ubj" title="乃木蛍">乃木蛍</a></div>
</li>
</div>
<div id="star_b6a" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/b6a"><img src="/pics/actress/b6a_a.jpg" title="辻本杏"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/b6a" title="辻本杏">辻本杏</a></div>
</li>
</div>
<div id="star_qz7" class="star-box star-box-common star-box-up idol-box" style="left: 76px; top: 395px; position: fixed; display: none;">
<li>
<a href="https://www.busjav.fun/star/qz7"><img src="/pics/actress/qz7_a.jpg" title="水卜さくら"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/qz7" title="水卜さくら">水卜さくら</a></div>
</li>
</div>
<div id="star_rxf" class="star-box star-box-common star-box-up idol-box">
<li>
<a href="https://www.busjav.fun/star/rxf"><img src="/pics/actress/rxf_a.jpg" title="架乃ゆら"></a>
<div class="star-name"><a href="https://www.busjav.fun/star/rxf" title="架乃ゆら">架乃ゆら</a></div>
</li>
</div>
</ul>
<p>
<span class="genre" onmouseover="hoverdiv(event,'star_8ec')" onmouseout="hoverdiv(event,'star_8ec')">
<a href="https://www.busjav.fun/star/8ec">夢乃あいか</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_8yw')" onmouseout="hoverdiv(event,'star_8yw')">
<a href="https://www.busjav.fun/star/8yw">鈴木心春</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_pmv')" onmouseout="hoverdiv(event,'star_pmv')">
<a href="https://www.busjav.fun/star/pmv">橋本ありな</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_t14')" onmouseout="hoverdiv(event,'star_t14')">
<a href="https://www.busjav.fun/star/t14">坂道みる</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_okq')" onmouseout="hoverdiv(event,'star_okq')">
<a href="https://www.busjav.fun/star/okq">三上悠亜</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_t7s')" onmouseout="hoverdiv(event,'star_t7s')">
<a href="https://www.busjav.fun/star/t7s">夕美しおん</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_uk3')" onmouseout="hoverdiv(event,'star_uk3')">
<a href="https://www.busjav.fun/star/uk3">逢見リカ</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_pr7')" onmouseout="hoverdiv(event,'star_pr7')">
<a href="https://www.busjav.fun/star/pr7">羽咲みはる</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_vfs')" onmouseout="hoverdiv(event,'star_vfs')">
<a href="https://www.busjav.fun/star/vfs">吉岡ひより</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_n5q')" onmouseout="hoverdiv(event,'star_n5q')">
<a href="https://www.busjav.fun/star/n5q">天使もえ</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_ubj')" onmouseout="hoverdiv(event,'star_ubj')">
<a href="https://www.busjav.fun/star/ubj">乃木蛍</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_b6a')" onmouseout="hoverdiv(event,'star_b6a')">
<a href="https://www.busjav.fun/star/b6a">辻本杏</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_qz7')" onmouseout="hoverdiv(event,'star_qz7')">
<a href="https://www.busjav.fun/star/qz7">水卜さくら</a>
</span>
<span class="genre" onmouseover="hoverdiv(event,'star_rxf')" onmouseout="hoverdiv(event,'star_rxf')">
<a href="https://www.busjav.fun/star/rxf">架乃ゆら</a>
</span>
 </p>
<a href="https://www.javlibrary.com/cn/vl_searchbyid.php?keyword=OFJE-266" style="color: rgb(204, 0, 0);">JavLibrary&nbsp;</a></div><table id="nong-table-new"><tr class="jav-nong-row" id="jav-nong-head"><th><select><option value="btsow.rest" selected="selected">btsow.rest</option><option value="www.btdig.com">www.btdig.com</option><option value="sukebei.nyaa.si">sukebei.nyaa.si</option><option value="www.torrentkitty.app">www.torrentkitty.app</option><option value="javdb.com">javdb.com</option></select></th><th><a href="https://btsow.rest/search/OFJE-266">大小</a></th><th><a>操作</a></th><th><a>离线下载</a></th></tr><tr class="jav-nong-row" maglink="magnet:?xt=urn:btih:ECBADC4A44B4DFD6629B8DB26375D9F9027953A6"><td><div title="OFJE-266-HD"><a href="magnet:?xt=urn:btih:ECBADC4A44B4DFD6629B8DB26375D9F9027953A6">OFJE-266-HD</a></div></td><td><a href="https://btsow.rest/magnet/detail/hash/ECBADC4A44B4DFD6629B8DB26375D9F9027953A6">229.28MB</a></td><td><div><a class="nong-copy" href="magnet:?xt=urn:btih:ECBADC4A44B4DFD6629B8DB26375D9F9027953A6">复制</a></div></td><td><div class="nong-offline"><a class="nong-offline-download" target="_blank" href="http://115.com/?tab=offline&amp;mode=wangpan">115离线</a></div></td></tr><tr class="jav-nong-row" maglink="magnet:?xt=urn:btih:7D7F6BB815DE506ECD14DE3466D37B83B1E49351"><td><div title="ofje-266 Loli With Big Tits, Chubby S*********ls, Little Devil Girls - All The .mp4"><a href="magnet:?xt=urn:btih:7D7F6BB815DE506ECD14DE3466D37B83B1E49351">ofje-266 Loli With B...</a></div></td><td><a href="https://btsow.rest/magnet/detail/hash/7D7F6BB815DE506ECD14DE3466D37B83B1E49351">4.44GB</a></td><td><div><a class="nong-copy" href="magnet:?xt=urn:btih:7D7F6BB815DE506ECD14DE3466D37B83B1E49351">复制</a></div></td><td><div class="nong-offline"><a class="nong-offline-download" target="_blank" href="http://115.com/?tab=offline&amp;mode=wangpan">115离线</a></div></td></tr><tr class="jav-nong-row" maglink="magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A"><td><div title="OFJE-266.HD"><a href="magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A">OFJE-266.HD</a></div></td><td><a href="https://btsow.rest/magnet/detail/hash/EBE4346338D995DDE5642CCF1B026E03CD049E4A">12.07GB</a></td><td><div><a class="nong-copy" href="magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A">复制</a></div></td><td><div class="nong-offline"><a class="nong-offline-download" target="_blank" href="http://115.com/?tab=offline&amp;mode=wangpan">115离线</a></div></td></tr><tr class="jav-nong-row" maglink="magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B"><td><div title="OFJE-266.mp4"><a href="magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B">OFJE-266.mp4</a></div></td><td><a href="https://btsow.rest/magnet/detail/hash/C766C52FAF462CD6A1F047D4754BB35F3F159C0B">4.44GB</a></td><td><div><a class="nong-copy" href="magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B">复制</a></div></td><td><div class="nong-offline"><a class="nong-offline-download" target="_blank" href="http://115.com/?tab=offline&amp;mode=wangpan">115离线</a></div></td></tr><tr class="jav-nong-row" maglink="magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53"><td><div title="ofje-266"><a href="magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53">ofje-266</a></div></td><td><a href="https://btsow.rest/magnet/detail/hash/7616455CB655285F53DC1CF86771F73FC45FDB53">19.86GB</a></td><td><div><a class="nong-copy" href="magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53">复制</a></div></td><td><div class="nong-offline"><a class="nong-offline-download" target="_blank" href="http://115.com/?tab=offline&amp;mode=wangpan">115离线</a></div></td></tr></table>
</div>
<div id="star-div">
<h4 id="star-hide" style="cursor: pointer;">演員 <span class="glyphicon glyphicon-minus"></span></h4>
<div id="avatar-waterfall">
<a class="avatar-box" href="https://www.busjav.fun/star/8ec">
<div class="photo-frame">
<img src="/pics/actress/8ec_a.jpg" title="夢乃あいか">
</div>
<span>夢乃あいか</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/8yw">
<div class="photo-frame">
<img src="/pics/actress/8yw_a.jpg" title="鈴木心春">
</div>
<span>鈴木心春</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/pmv">
<div class="photo-frame">
<img src="/pics/actress/pmv_a.jpg" title="橋本ありな">
</div>
<span>橋本ありな</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/t14">
<div class="photo-frame">
<img src="/pics/actress/t14_a.jpg" title="坂道みる">
</div>
<span>坂道みる</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/okq">
<div class="photo-frame">
<img src="/pics/actress/okq_a.jpg" title="三上悠亜">
</div>
<span>三上悠亜</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/t7s">
<div class="photo-frame">
<img src="/pics/actress/t7s_a.jpg" title="夕美しおん">
</div>
<span>夕美しおん</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/uk3">
<div class="photo-frame">
<img src="/pics/actress/uk3_a.jpg" title="逢見リカ">
</div>
<span>逢見リカ</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/pr7">
<div class="photo-frame">
<img src="/pics/actress/pr7_a.jpg" title="羽咲みはる">
</div>
<span>羽咲みはる</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/vfs">
<div class="photo-frame">
<img src="/pics/actress/vfs_a.jpg" title="吉岡ひより">
</div>
<span>吉岡ひより</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/n5q">
<div class="photo-frame">
<img src="/pics/actress/n5q_a.jpg" title="天使もえ">
</div>
<span>天使もえ</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/ubj">
<div class="photo-frame">
<img src="/pics/actress/ubj_a.jpg" title="乃木蛍">
</div>
<span>乃木蛍</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/b6a">
<div class="photo-frame">
<img src="/pics/actress/b6a_a.jpg" title="辻本杏">
</div>
<span>辻本杏</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/qz7">
<div class="photo-frame">
<img src="/pics/actress/qz7_a.jpg" title="水卜さくら">
</div>
<span>水卜さくら</span>
</a>
<a class="avatar-box" href="https://www.busjav.fun/star/rxf">
<div class="photo-frame">
<img src="/pics/actress/rxf_a.jpg" title="架乃ゆら">
</div>
<span>架乃ゆら</span>
</a>
</div>
</div>
<h4 id="mag-submit-show" style="cursor: pointer;">磁力連結投稿 <span id="mag-submit-toggle" class="glyphicon glyphicon-plus"></span></h4>
<div id="mag-submit" class="movie" style="padding:30px 20px 30px 5px;">
<div id="mag-submit-hide" class="close" style="margin:-25px -13px 0 0;">×</div>
<div class="col-md-11 col-xs-10">
<div class="input-group">
<div class="input-group-addon">magnet地址:</div>
<input type="text" class="form-control" id="appendedInputButton">
</div>
</div>
<button type="button" class="btn btn-default col-md-1 col-xs-2" onclick="checktxt()" data-toggle="modal" data-target="#magneturlpost">分享</button>
</div>

<div id="magneturlpost" class="modal fade" tabindex="-1" role="dialog"></div>
<div class="movie" style="padding:12px; margin-top:15px">
<table id="magnet-table" class="table table-condensed table-striped table-hover" style="margin-bottom:0;">
<tbody><tr style="font-weight:bold;">
<td>磁力名稱 <span class="glyphicon glyphicon-magnet"></span></td>
<td style="text-align:center;white-space:nowrap">檔案大小</td>
<td style="text-align:center;white-space:nowrap">分享日期</td>
<td style="text-align:center;white-space:nowrap">操作</td><td style="text-align:center;white-space:nowrap">离线下载</td></tr>
</tbody>
<tr onmouseover="this.style.backgroundColor='#F4F9FD';this.style.cursor='pointer';" onmouseout="this.style.backgroundColor='#FFFFFF'" height="35px" style=" border-top:#DDDDDD solid 1px" maglink="magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A&amp;dn=OFJE-266.HD">
<td width="70%" onclick="window.open('magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A&amp;dn=OFJE-266.HD','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A&amp;dn=OFJE-266.HD">
OFJE-266.HD </a><a class="btn btn-mini-new btn-primary disabled" title="包含高清HD的磁力連結">高清</a> 
</td>
<td style="text-align:center;white-space:nowrap" onclick="window.open('magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A&amp;dn=OFJE-266.HD','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A&amp;dn=OFJE-266.HD">
12.07GB </a>
</td>
<td style="text-align:center;white-space:nowrap" onclick="window.open('magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A&amp;dn=OFJE-266.HD','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A&amp;dn=OFJE-266.HD">
2020-10-03 </a>
</td>
<td style="text-align:center;"><div><a class="nong-copy" href="magnet:?xt=urn:btih:EBE4346338D995DDE5642CCF1B026E03CD049E4A&amp;dn=OFJE-266.HD">复制</a></div></td><td><div class="nong-offline"><a class="nong-offline-download" target="_blank" href="http://115.com/?tab=offline&amp;mode=wangpan">115离线</a></div></td></tr>
<tr onmouseover="this.style.backgroundColor='#F4F9FD';this.style.cursor='pointer';" onmouseout="this.style.backgroundColor='#FFFFFF'" height="35px" style=" border-top:#DDDDDD solid 1px" maglink="magnet:?xt=urn:btih:96F68376B3C15923569A18DF72E52230FC91D53C&amp;dn=HD_ofje-266">
<td width="70%" onclick="window.open('magnet:?xt=urn:btih:96F68376B3C15923569A18DF72E52230FC91D53C&amp;dn=HD_ofje-266','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:96F68376B3C15923569A18DF72E52230FC91D53C&amp;dn=HD_ofje-266">
HD_ofje-266 </a><a class="btn btn-mini-new btn-primary disabled" title="包含高清HD的磁力連結">高清</a> 
</td>
<td style="text-align:center;white-space:nowrap" onclick="window.open('magnet:?xt=urn:btih:96F68376B3C15923569A18DF72E52230FC91D53C&amp;dn=HD_ofje-266','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:96F68376B3C15923569A18DF72E52230FC91D53C&amp;dn=HD_ofje-266">
8.90GB </a>
</td>
<td style="text-align:center;white-space:nowrap" onclick="window.open('magnet:?xt=urn:btih:96F68376B3C15923569A18DF72E52230FC91D53C&amp;dn=HD_ofje-266','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:96F68376B3C15923569A18DF72E52230FC91D53C&amp;dn=HD_ofje-266">
2020-09-24 </a>
</td>
<td style="text-align:center;"><div><a class="nong-copy" href="magnet:?xt=urn:btih:96F68376B3C15923569A18DF72E52230FC91D53C&amp;dn=HD_ofje-266">复制</a></div></td><td><div class="nong-offline"><a class="nong-offline-download" target="_blank" href="http://115.com/?tab=offline&amp;mode=wangpan">115离线</a></div></td></tr>
<tr onmouseover="this.style.backgroundColor='#F4F9FD';this.style.cursor='pointer';" onmouseout="this.style.backgroundColor='#FFFFFF'" height="35px" style=" border-top:#DDDDDD solid 1px" maglink="magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B&amp;dn=OFJE-266.mp4">
<td width="70%" onclick="window.open('magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B&amp;dn=OFJE-266.mp4','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B&amp;dn=OFJE-266.mp4">
OFJE-266.mp4 </a><a class="btn btn-mini-new btn-primary disabled" title="包含高清HD的磁力連結">高清</a> 
</td>
<td style="text-align:center;white-space:nowrap" onclick="window.open('magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B&amp;dn=OFJE-266.mp4','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B&amp;dn=OFJE-266.mp4">
4.44GB </a>
</td>
<td style="text-align:center;white-space:nowrap" onclick="window.open('magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B&amp;dn=OFJE-266.mp4','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B&amp;dn=OFJE-266.mp4">
2020-09-19 </a>
</td>
<td style="text-align:center;"><div><a class="nong-copy" href="magnet:?xt=urn:btih:C766C52FAF462CD6A1F047D4754BB35F3F159C0B&amp;dn=OFJE-266.mp4">复制</a></div></td><td><div class="nong-offline"><a class="nong-offline-download" target="_blank" href="http://115.com/?tab=offline&amp;mode=wangpan">115离线</a></div></td></tr>
<tr onmouseover="this.style.backgroundColor='#F4F9FD';this.style.cursor='pointer';" onmouseout="this.style.backgroundColor='#FFFFFF'" height="35px" style=" border-top:#DDDDDD solid 1px" maglink="magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53&amp;dn=ofje-266">
<td width="70%" onclick="window.open('magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53&amp;dn=ofje-266','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53&amp;dn=ofje-266">
ofje-266 </a><a class="btn btn-mini-new btn-primary disabled" title="包含高清HD的磁力連結">高清</a> 
</td>
<td style="text-align:center;white-space:nowrap" onclick="window.open('magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53&amp;dn=ofje-266','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53&amp;dn=ofje-266">
19.86GB </a>
</td>
<td style="text-align:center;white-space:nowrap" onclick="window.open('magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53&amp;dn=ofje-266','_self')">
<a style="color:#333" rel="nofollow" title="滑鼠右鍵點擊並選擇【複製連結網址】" href="magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53&amp;dn=ofje-266">
2020-09-17 </a>
</td>
<td style="text-align:center;"><div><a class="nong-copy" href="magnet:?xt=urn:btih:7616455CB655285F53DC1CF86771F73FC45FDB53&amp;dn=ofje-266">复制</a></div></td><td><div class="nong-offline"><a class="nong-offline-download" target="_blank" href="http://115.com/?tab=offline&amp;mode=wangpan">115离线</a></div></td></tr>
<script type="text/javascript">
			$('#movie-loading').hide();
			</script>
</table>
<div id="movie-loading" style="display: none;">
<table width="120" border="0" cellpadding="5" cellspacing="0">
<tbody>
<tr>
<td align="center">
<font class="ajax-text"><img src="https://www.busjav.fun/images/movie_loading.gif" border="0"></font>
</td>
<td align="center">
<font class="ajax-text">讀取中...</font>
</td>
</tr>
</tbody>
</table>
</div>
</div>
<h4>樣品圖像</h4>
<div id="sample-waterfall">
<a class="sample-box" href="https://pics.dmm.co.jp/digital/video/ofje00266/ofje00266jp-1.jpg"><div class="photo-frame"><img src="/pics/sample/7us3_1.jpg" title="OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - 樣品圖像 - 1"></div></a> <a class="sample-box" href="https://pics.dmm.co.jp/digital/video/ofje00266/ofje00266jp-2.jpg"><div class="photo-frame"><img src="/pics/sample/7us3_2.jpg" title="OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - 樣品圖像 - 2"></div></a> <a class="sample-box" href="https://pics.dmm.co.jp/digital/video/ofje00266/ofje00266jp-3.jpg"><div class="photo-frame"><img src="/pics/sample/7us3_3.jpg" title="OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - 樣品圖像 - 3"></div></a> <a class="sample-box" href="https://pics.dmm.co.jp/digital/video/ofje00266/ofje00266jp-4.jpg"><div class="photo-frame"><img src="/pics/sample/7us3_4.jpg" title="OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - 樣品圖像 - 4"></div></a> <a class="sample-box" href="https://pics.dmm.co.jp/digital/video/ofje00266/ofje00266jp-5.jpg"><div class="photo-frame"><img src="/pics/sample/7us3_5.jpg" title="OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - 樣品圖像 - 5"></div></a> <a class="sample-box" href="https://pics.dmm.co.jp/digital/video/ofje00266/ofje00266jp-6.jpg"><div class="photo-frame"><img src="/pics/sample/7us3_6.jpg" title="OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - 樣品圖像 - 6"></div></a> <a class="sample-box" href="https://pics.dmm.co.jp/digital/video/ofje00266/ofje00266jp-7.jpg"><div class="photo-frame"><img src="/pics/sample/7us3_7.jpg" title="OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - 樣品圖像 - 7"></div></a> <a class="sample-box" href="https://pics.dmm.co.jp/digital/video/ofje00266/ofje00266jp-8.jpg"><div class="photo-frame"><img src="/pics/sample/7us3_8.jpg" title="OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - 樣品圖像 - 8"></div></a> <a class="sample-box" href="https://pics.dmm.co.jp/digital/video/ofje00266/ofje00266jp-9.jpg"><div class="photo-frame"><img src="/pics/sample/7us3_9.jpg" title="OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - 樣品圖像 - 9"></div></a> <a class="sample-box" href="https://pics.dmm.co.jp/digital/video/ofje00266/ofje00266jp-10.jpg"><div class="photo-frame"><img src="/pics/sample/7us3_10.jpg" title="OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間 - 樣品圖像 - 10"></div></a> </div>
<div class="clearfix"></div>
<h4 style="position:relative">推薦 <a href="javascript:bootstr(1);"><span id="urad2" class="label label-default"><span class="left-urad2">投放廣告</span><span class="glyphicon glyphicon-envelope"></span></span></a></h4>
<div class="row">
<div class="col-xs-12 col-md-4 text-center ptb10"><script type="text/javascript" data-cfasync="false" async="" src="https://poweredby.jads.co/js/jads.js"></script><iframe id="6e6cwe" style="z-index: 566; border: 0px; background-color: transparent; height: 250px; width: 300px; position: relative; visibility: visible; clear: both;" frameborder="0" marginheight="0" marginwidth="0" scrolling="no" height="250" width="300" allowtransparency="true" src="//adserver.juicyads.com/adshow.php?adzone=464076"></iframe><script type="text/javascript" data-cfasync="false" async="">(adsbyjuicy = window.adsbyjuicy || []).push({"adzone":464076});</script></div><div class="col-xs-12 col-md-4 text-center ptb10"><script type="text/javascript" data-cfasync="false" async="" src="https://poweredby.jads.co/js/jads.js"></script><iframe id="wceecb" style="z-index: 566; border: 0px; background-color: transparent; height: 250px; width: 300px; position: relative; visibility: visible; clear: both;" frameborder="0" marginheight="0" marginwidth="0" scrolling="no" height="250" width="300" allowtransparency="true" src="//adserver.juicyads.com/adshow.php?adzone=706603"></iframe><script type="text/javascript" data-cfasync="false" async="">(adsbyjuicy = window.adsbyjuicy || []).push({"adzone":706603});</script></div><div class="col-xs-12 col-md-4 text-center ptb10"><script type="text/javascript" data-cfasync="false" async="" src="https://poweredby.jads.co/js/jads.js"></script><iframe id="woebh6" style="z-index: 566; border: 0px; background-color: transparent; height: 250px; width: 300px; position: relative; visibility: visible; clear: both;" frameborder="0" marginheight="0" marginwidth="0" scrolling="no" height="250" width="300" allowtransparency="true" src="//adserver.juicyads.com/adshow.php?adzone=796384"></iframe><script type="text/javascript" data-cfasync="false" async="">(adsbyjuicy = window.adsbyjuicy || []).push({"adzone":796384});</script></div>
</div>
<h4>同類影片</h4>
<div id="related-waterfall" class="mb20">
<a title="鉄板フェラチオBEST Vol.2" class="movie-box" href="https://www.busjav.fun/TOMN-012" style="display:inline-block; margin:5px;">
<div class="photo-frame">
<img src="/pics/thumb/4q64.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>鉄板フェラチオBEST Vol.2</span>
</div>
</a>
<a title="超濃厚ベロキスSEX 中年おじさんとひたすら舌を絡め求め合ったS級美少女の97本番たっぷり8時間スペシャル" class="movie-box" href="https://www.busjav.fun/OFJE-253" style="display:inline-block; margin:5px;">
<div class="photo-frame">
<img src="/pics/thumb/7qmp.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>超濃厚ベロキスSEX 中年おじさんとひたすら舌を絡め求め合ったS級美少女の97本番たっぷり8時間スペシャル</span>
</div>
</a>
<a title="S級女優にぶっかける！！射精直前の最高に気持ち良い大量顔面発射ラッシュ140連発8時間3＋射精後のお掃除フェラまでたっぷり収録スペシャル" class="movie-box" href="https://www.busjav.fun/OFJE-251" style="display:inline-block; margin:5px;">
<div class="photo-frame">
<img src="/pics/thumb/7pos.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>S級女優にぶっかける！！射精直前の最高に気持ち良い大量顔面発射ラッシュ140連発8時間3＋射精後のお掃除フェラまでたっぷり収録スペシャル</span>
</div>
</a>
<a title="「ダメぇぇ！今イッちゃったばかりだよぉ！」 絶頂直後の超敏感ヒクヒクおま●こを追撃しまくり！怒涛のイクイクおかわりピストンラッシュ103連発！" class="movie-box" href="https://www.busjav.fun/OFJE-249" style="display:inline-block; margin:5px;">
<div class="photo-frame">
<img src="/pics/thumb/7p1o.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>「ダメぇぇ！今イッちゃったばかりだよぉ！」 絶頂直後の超敏感ヒクヒクおま●こを追撃しまくり！怒涛のイクイクおかわりピストンラッシュ103連発！</span>
</div>
</a>
<a title="激イキ1，804回！痙攣56，225回！イキ潮52，206cc！鬼突き60，739ピストン！ S級美女 エロス覚醒 大・痙・攣スペシャル 最新13タイトルコンプリートBEST8時間" class="movie-box" href="https://www.busjav.fun/OFJE-245" style="display:inline-block; margin:5px;">
<div class="photo-frame">
<img src="/pics/thumb/7nfd.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>激イキ1，804回！痙攣56，225回！イキ潮52，206cc！鬼突き60，739ピストン！ S級美女 エロス覚醒 大・痙・攣スペシャル 最新13タイトルコンプリートBEST8時間</span>
</div>
</a>
<a title="S1 2019年 上半期＋下半期 まるごと100選100SEX 2019年のBEST OF BEST版" class="movie-box" href="https://www.busjav.fun/OFJE-243" style="display:inline-block; margin:5px;">
<div class="photo-frame">
<img src="/pics/thumb/7miz.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>S1 2019年 上半期＋下半期 まるごと100選100SEX 2019年のBEST OF BEST版</span>
</div>
</a>
</div>
<script language="JavaScript">
(function($){
	$('img.img').each(function(){
    var image=new Image();
    image.src=this.src;
    if(image.complete){
        cutImgz(this);
    } else{
        this.onload=function(){
            cutImgz(this);
        }
    }
	});
})(jQuery);

function cutImgz(obj){
    var image=new Image();
    image.src=obj.src;
    $this=$(obj);
	var w = image.width;
	var h = image.height;
	var p = w/h;
    if(p>1.38&&p<1.40){
        $this.addClass("m1000giri");
    }
    if(p>0.99&&p<1.01){
        $this.addClass("mpacopacomama");
    }
    if(p>1.11&&p<1.13){
        $this.addClass("mcaribbeancom");
    }
    if(p>1.77&&p<1.78){
        $this.addClass("mcaribbeancom2");
    }	
    if(p>0.59&&p<0.61){
        $this.addClass("m1pondo");
    }
    if(p>0.65&&p<0.67){
        $this.addClass("mtokyohot");
    }
    if(p>1.78&&p<1.79){
        $this.addClass("mheyzo");
    }									
}	
</script>
<h4>論壇熱帖</h4>
<div id="related-waterfall" class="mb20">
<a title="吞精影片分享，本人截止目前的收藏" class="movie-box" href="https://www.busjav.fun/forum/forum.php?mod=viewthread&amp;tid=90492" style="display:inline-block; margin:5px;">
<div class="photo-frame bforum">
<img class="mforum" src="https://www.busjav.fun/forum/data/attachment/forum/202110/Ds4pjnX.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;"> 
<span>吞精影片分享，本人截止目前的收藏</span>
</div>
</a>
<a title="分享个人认为最顶最榨汁的女优！！" class="movie-box" href="https://www.busjav.fun/forum/forum.php?mod=viewthread&amp;tid=90510" style="display:inline-block; margin:5px;">
<div class="photo-frame bforum">
<img class="mforum" src="https://www.busjav.fun/forum/data/attachment/forum/202110/64Hi1bN.png">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>分享个人认为最顶最榨汁的女优！！</span>
</div>
</a>
<a title="分享两部技校学生爱爱视频" class="movie-box" href="https://www.busjav.fun/forum/forum.php?mod=viewthread&amp;tid=90491" style="display:inline-block; margin:5px;">
<div class="photo-frame bforum">
<img class="mforum" src="https://www.busjav.fun/forum/data/attachment/forum/202110/Ahf5DQ0.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>分享两部技校学生爱爱视频</span>
</div>
</a>
<a title="（有彩蛋）一个很像泰迦奥特曼女主的av女优" class="movie-box" href="https://www.busjav.fun/forum/forum.php?mod=viewthread&amp;tid=90500" style="display:inline-block; margin:5px;">
<div class="photo-frame bforum">
<img class="mforum" src="https://www.busjav.fun/forum/data/attachment/forum/202110/P2Zh1D3.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>（有彩蛋）一个很像泰迦奥特曼女主的av女优</span>
</div>
</a>
<a title="上海知名导演沈某辉" class="movie-box" href="https://www.busjav.fun/forum/forum.php?mod=viewthread&amp;tid=90514" style="display:inline-block; margin:5px;">
<div class="photo-frame bforum">
<img class="mforum" src="https://www.busjav.fun/forum/data/attachment/forum/202110/5Yu2Bi4.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>上海知名导演沈某辉</span>
</div>
</a>
<a title="求大佬帮忙看看这个正装妹子是不是探花的车" class="movie-box" href="https://www.busjav.fun/forum/forum.php?mod=viewthread&amp;tid=90525" style="display:inline-block; margin:5px;">
<div class="photo-frame bforum">
<img class="mforum" src="https://www.busjav.fun/forum/data/attachment/forum/202110/Ar1oEq7.jpg">
</div>
<div class="photo-info" style="height:36px; overflow:hidden; text-align:center;">
<span>求大佬帮忙看看这个正装妹子是不是探花的车</span>
</div>
</a>
</div>
<script>
        (function($){
        $('.bigImage').magnificPopup({
            type: 'image',
            closeOnContentClick: true,
            closeBtnInside: false,
            fixedContentPos: true,
            mainClass: 'mfp-no-margins mfp-with-zoom',
            image: {
                verticalFit: true,
                titleSrc: function(item) {
                    return "OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間";
                }
            },
            zoom: {
                enabled: true,
                duration: 300
            }
        });

        $('#sample-waterfall').magnificPopup({
            delegate: 'a',
            type: 'image',
            closeOnContentClick: false,
            closeBtnInside: false,
            mainClass: 'mfp-with-zoom mfp-img-mobile',
            image: {
                verticalFit: true,
                titleSrc: function(item) {
                    return "OFJE-266 ロリ巨乳・うぶ女子生徒・小悪魔女子まで憧れの青春美少女とわいせつ制服50性交8時間";
                }
            },
            gallery: {
                enabled: true
            },
            zoom: {
                enabled: true,
                duration: 300,
                opener: function(element) {
                    return element.find('img');
                }
            }

        });
        })(jQuery);

		$("#gr_btn").click(function() {
			var t = "";
			$("input[name='gr_sel']:checkbox").each(function() {
				$(this).is(":checked") && (t += $(this).val() + "-")
			}), "" != t && (t = t.substring(0, t.length - 1), window.location.href = "genre/" + t)
		});
</script>
</div><div id="jl33p50355" style="border:0;padding:0;margin:0;width:1px;height:1px;display:inline-block;clear:none;position:absolute;left:-1063px;top:2326.5px;"></div><div id="0co0c7eecc" style="border:0;padding:0;margin:0;width:1px;height:1px;display:inline-block;clear:none;position:absolute;left:-1063px;top:3037px;"></div><div id="i5855w0wc9" style="border:0;padding:0;margin:0;width:1px;height:1px;display:inline-block;clear:none;position:absolute;left:-1063px;top:3292px;"></div><div id="uq5ii7abab" style="border:0;padding:0;margin:0;width:1px;height:1px;display:inline-block;clear:none;position:absolute;left:-1063px;top:3292px;"></div>
<div class="ad-box">
<div class="ad-item"><a href="https://bzc3e2b7.xyz?ch=jav" target="_blank" rel="nofollow"><img src="/ads/xhp_728x90_2.jpg" width="728" height="90"></a></div>
<div class="ad-item"><a href="https://51bo.xyz/#/?ai=157284" target="_blank" rel="nofollow"><img src="/ads/51fl_728x90_2.jpg" width="728" height="90"></a></div>
<div class="ad-item"><a href="https://bzc3e2b7.xyz?ch=jav" target="_blank" rel="nofollow"><img src="/ads/xhp_728x90_1.jpg" width="728" height="90"></a></div>
<div class="ad-item"><div class="ad-juicy"><script data-cfasync="false" async="" src="https://poweredby.jads.co/js/jads.js"></script><iframe id="ak022p" style="z-index: 627; border: 0px; background-color: transparent; height: 90px; width: 728px; position: relative; visibility: visible; clear: both;" frameborder="0" marginheight="0" marginwidth="0" scrolling="no" height="90" width="728" allowtransparency="true" src="//adserver.juicyads.com/adshow.php?adzone=365002"></iframe><script type="text/javascript" data-cfasync="false" async="">(adsbyjuicy = window.adsbyjuicy || []).push({"adzone":365002});</script></div></div>
<div class="ad-item"><a href="http://jav.yu77.com" target="_blank" rel="nofollow"><img src="/ads/twuu_728x90_2.gif" width="728" height="90"></a></div>
<div class="ad-item"><div class="ad-juicy"><script data-cfasync="false" async="" src="https://poweredby.jads.co/js/jads.js"></script><iframe id="fdikkp" style="z-index: 627; border: 0px; background-color: transparent; height: 90px; width: 728px; position: relative; visibility: visible; clear: both;" frameborder="0" marginheight="0" marginwidth="0" scrolling="no" height="90" width="728" allowtransparency="true" src="//adserver.juicyads.com/adshow.php?adzone=741662"></iframe><script type="text/javascript" data-cfasync="false" async="">(adsbyjuicy = window.adsbyjuicy || []).push({"adzone":741662});</script></div></div>
</div>
<script src="https://www.busjav.fun/js/gallery.js?v=2.9"></script><div id="ijdfjp2pkf" style="border:0;padding:0;margin:0;width:1px;height:1px;display:inline-block;clear:none;position:absolute;left:-1063px;top:4298.5px;"></div><div id="7tr83tt340" style="border:0;padding:0;margin:0;width:1px;height:1px;display:inline-block;clear:none;position:absolute;left:-1063px;top:4496.5px;"></div>
<footer class="footer hidden-xs">
<div class="container-fluid">
<p><a href="https://www.busjav.fun/doc/terms">Terms</a> / <a href="https://www.busjav.fun/doc/privacy">Privacy</a> / <a href="https://www.busjav.fun/doc/usc">2257</a> / <a href="http://www.rtalabel.org/" target="_blank" rel="external nofollow">RTA</a> / <a href="javascript:bootstr(1);" r="">廣告投放</a> / <a href="javascript:bootstr(2);">聯絡我們</a><br><a href="#formModal" id="adscontact" data-toggle="modal"></a>
Copyright © 2013 JavBus. All Rights Reserved. All other trademarks and copyrights are the property of their respective holders. The reviews and comments expressed at or through this website are the opinions of the individual author and do not reflect the opinions or views of JavBus. JavBus is not responsible for the accuracy of any of the information supplied here.</p>
</div>
</footer>
<div class="visible-xs-block footer-bar-placeholder"></div>
<script language="javascript">
    function bootstr(type){
    	ads = "廣告投放";
    	contact = "聯絡我們";
    	translate = "翻譯";
    	$("#adstype").val(type);
    	if(type==1){
    		$("#contactModalLab").html(ads);
    		$("#qqskype").show();
    		$("#transinfo").hide();
    		$("#translanguage").hide();
    		$("#mailcontent").show();		
    	}else if(type==2){
    		$("#contactModalLab").html(contact);
    		$("#qqskype").show();
    		$("#transinfo").hide();
    		$("#translanguage").hide();
    		$("#mailcontent").show();
    	}else if(type==3){
    		$("#contactModalLab").html(translate);
    		$("#qqskype").hide();
    		$("#transinfo").show();
    		$("#translanguage").show();
    		$("#mailcontent").hide();
    	}
    	$("#adscontact").trigger("click");
		getverifycode();    	
    };
    function getverifycode(){
       $('#verify').attr("src","/post/verify?"+Math.random()*10000);
    };
    function IsMail(mail){
     var remail= /^([a-zA-Z0-9_-])+(\.)?([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
     return(remail.test(mail));
    };
    function checkform(){
    	var post = true; 
      if($("#verifycode").val().length!=5){
    	  	alert("驗證碼輸入錯誤!") 
    		$("#verifycode").focus(); 
    		post = false;
    	  }
      if($("#contact").val().length>255){
    	  	alert("聯繫方式字數過多!") 
    		$("#contact").focus(); 
    		post = false;
    	  }

      if(!IsMail($("#mail").val())){
    	alert("請輸入正確的電郵地址!") 
     	$("#mail").focus(); 
        post = false;
      }

      if($("#intention").val().length>25500){
    	  	alert("投放意向字數過多!") 
    		$("#intention").focus(); 
    		post = false;
    	  }

      if($("#trans").val().length>255){
    	  	alert("Too many words in your language textbox!") 
    		$("#intention").focus(); 
    		post = false;
    	  }	  
      if(post== true){
    	  $("#modalclose").trigger("click");
    	  $("#postform").attr("action", "/post/contact");
    	  $("#postform").submit();
    	}
      return post;
    };
</script>
<script>
$("#showmag,#cellshowmag,#resultshowmag").click(function(){
	$.cookie("existmag", "mag",{expires:365,path:'/'}); 
	location.reload() 
});

$("#showall,#cellshowall,#resultshowall").click(function(){
	$.cookie("existmag", "all",{expires:365,path:'/'}); 
	location.reload() 
});
$("#showonline").click(function(){
	$.cookie("existmag", "online",{expires:365,path:'/'}); 
	location.reload() 
});
$(".info .mypointer").click(function(){
	var obj = $(this);
	var code = obj.attr('value');
	var token = $("#token").val();
	var e = "../ajax/addfavorite.php?code=" + encodeURIComponent(code) + "&token=" + encodeURIComponent(token) + "&floor=" + Math.floor(Math.random() * 1e3 + 1);
    $.ajax({
        url: e,
        type: "POST",
		//dataType: "json",
		cache:false,
        success: function (json) {
			//obj.html(json);
			ajaxobj=eval("("+json+")");
			if(ajaxobj.act=='err'){
				alert('收藏次數達上限，請稍候再試');	
			}else{
				obj.html(ajaxobj.act);
				obj.attr('value',ajaxobj.code);
				obj.attr('title',ajaxobj.title);
				$("#token").val(ajaxobj.token);
			}
        }
    });
});

$(".glyphicon-heart-empty").hover(function () {
    $(this).removeClass('glyphicon-heart-empty');
	$(this).addClass('glyphicon-heart');
}, function () {
    $(this).removeClass('glyphicon-heart');
    $(this).addClass('glyphicon-heart-empty');
});
$(".glyphicon-heart").hover(function () {
    $(this).removeClass('glyphicon-heart');
	$(this).addClass('glyphicon-heart-empty');
}, function () {
    $(this).removeClass('glyphicon-heart-empty');
    $(this).addClass('glyphicon-heart');
});
</script>

<div id="formModal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="formModalLabel" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
<button id="modalclose" type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>
<h4 class="modal-title" id="contactModalLab">聯絡我們</h4>
</div>
<div class="modal-body">
<form class="form-horizontal" name="postform" method="post" id="postform" enctype="multipart/form-data">
<fieldset>
<div class="form-group" id="qqskype">
<label class="col-sm-4 control-label" for="contact">QQ / Skype</label>
<div class="col-sm-6">
<input id="contact" name="contact" type="text" placeholder="" class="form-control">
</div>
</div>
<div class="form-group">
<label class="col-sm-4 control-label" for="mail">Email</label>
<div class="col-sm-6">
<input id="mail" name="mail" type="text" placeholder="" class="form-control">
</div>
</div>
<div class="form-group" id="translanguage">
<label class="col-sm-4 control-label" for="trans">Your Language</label>
<div class="col-sm-6">
<input id="trans" name="trans" type="text" placeholder="" class="form-control">
</div>
</div>
<div class="form-group" id="mailcontent">
<label class="col-sm-4 control-label" for="intention" id="inten-trans">內容</label>
<div class="col-sm-6">
<textarea id="intention" name="intention" rows="9" class="form-control"></textarea>
</div>
</div>
<div class="form-group">
<label class="col-sm-4 control-label" for="verify">驗證碼</label>
<div class="col-sm-6">
<input type="text" id="verifycode" name="verifycode" style="width:50px">
<img id="verify" src="" style="cursor: pointer; vertical-align:middle;" onclick="getverifycode()">
</div>
</div>
<input type="hidden" id="adstype" name="adstype" value="1">
</fieldset>
</form>
</div>
<div class="modal-footer">
<button type="button" button="" class="btn btn-primary" onclick="checkform()">送出</button>
<button type="button" button="" class="btn btn-default" data-dismiss="modal">關閉</button>
</div>
</div>
</div>
</div>

<div class="overlay overlay-contentscale">
<div class="row">
<div class="col-xs-12 text-center ptb20">
<div class="input-group col-xs-offset-2 col-xs-8">
<input id="search-input-mobile" type="text" class="form-control" placeholder="搜尋 識別碼, 影片, 演員">
<span class="input-group-btn">
<button class="btn btn-default" type="submit" onclick="searchs('search-input-mobile')">搜尋</button>
</span>
</div>
</div>
<div class="col-xs-6 text-center"><a href="https://www.busjav.fun/">有碼</a></div>
<div class="col-xs-6 text-center"><a href="https://www.busjav.fun/uncensored">無碼</a></div>
<div class="col-xs-6 text-center"><a href="https://www.busjav.fun/genre">有碼類別</a></div>
<div class="col-xs-6 text-center"><a href="https://www.busjav.fun/uncensored/genre">無碼類別</a></div>
<div class="col-xs-6 text-center"><a href="https://www.busjav.fun/actresses">有碼女優</a></div>
<div class="col-xs-6 text-center"><a href="https://www.busjav.fun/uncensored/actresses">無碼女優</a></div>
<div class="col-xs-6 text-center"><a href="https://www.javbus.red/">歐美</a></div>
<div class="col-xs-6 text-center"><a href="https://www.busjav.fun/forum/">論壇</a></div>
<div class="col-xs-12 text-center overlay-close">
 <i class="glyphicon glyphicon-remove"></i>
</div>
</div>
</div>

</body></html>
	'''


def file_name_walk(file_dir=None):
	noListsuffix = [
		# "JPG", 'PNG', 'JPEG',
		# 'DMP', 'ZIP', 'RAR', 'MOV', 'TORRENT', 'TXT', 'ASF'
	]
	listpath = []
	for root, dirs, files in os.walk(file_dir):
		dictTemp = {}
		dictTemp['root'] = root  # 当前目录路径
		# dictTemp['dirs'] = dirs  # 当前路径下所有子目录
		dictTemp['files'] = files  # 当前路径下所有非目录子文件
		fh = root.split('\\')[-1]
		dictTemp['fanhao'] = fh.replace('00-Chinese_', '')

		if not files and not dirs:
			os.rmdir(root)

		if 'other' in root or not files:
			continue

		yield dictTemp


def imgDownLoad(imgUrl='', Info=''):
	if isinstance(imgUrl, str):
		try:
			imgBrow = req.get(imgUrl, timeout=(10, 10))
		except requests.exceptions.ConnectTimeout as ff:
			msg = 'Requests ERROR_img_str\n' + ff + '\n' + imgUrl
			logging.error(msg=msg)
			return None
		imgName = Info['fanhao'] + '_COVER.JPG'
		imgPath = os.path.join(Info['root'], imgName)
		with open(imgPath, 'wb') as imgF:
			imgF.write(imgBrow.content)
		return imgPath.replace('\\', '/')

	elif isinstance(imgUrl, list):
		llist = []
		for num, imgAct in enumerate(imgUrl):
			try:
				imgBrow = req.get(imgAct, timeout=(10, 10), headers=HEA)
			except requests.exceptions.ConnectTimeout as ff:
				msg = 'Requests ERROR_img_list\n' + ff + '\n' + imgAct + "---\t" + str(num)
				logging.error(msg=msg)
				return None
			imgName = Info['fanhao'] + '_img_{}.JPG'.format(str(num + 1))
			imgPath = os.path.join(Info['root'], imgName)
			with open(imgPath, 'wb') as imgF:
				imgF.write(imgBrow.content)
			llist.append(imgPath.replace('\\', '/'))
		if llist:
			return llist
	else:
		raise 'imgUrl must Str or List'


def get_issueTime(strhtml):
	issueTime = re.findall("</span>.*(\d{4}-\d{2}-\d{2}).*</p>", strhtml, re.M | re.S)
	if not issueTime:
		issueTime = re.findall("】(\d{4}-\d{2}-\d{2})", strhtml, re.M | re.S)
	if not issueTime:
		return None
	return issueTime[0]


def get_duration(strhtml):
	issueTime = re.findall("(\d{1,3})分", strhtml, re.M | re.S)
	if not issueTime:
		return None
	return issueTime[0]


def get_actor(soup):
	actorList = soup.find_all(class_='star-name')
	llist = []
	for i in actorList:
		ddict = {}
		hreff = i.a.get('href')
		ddict['actorID'] = hreff.split('/')[-1]
		ddict['actorName'] = i.a.get_text()
		ddict['actorImgUrl'] = urlparse.urljoin(fhSeachurl, i.parent.find('img').get('src'))
		llist.append(ddict)
	return llist


def use_FanHaoInfo_get_VideoInfo(fanhaoInfo):

	if fanhaoInfo['fanhao'] == '.actors':
		return None
	fanhaoInfo['fanhao'] = regexFanhao(fanhaoInfo['fanhao'])
	reqUrl = fhSeachurl + fanhaoInfo['fanhao']



	print(reqUrl)
	try:
		brow = req.get(url=reqUrl, timeout=(10, 10))
		if brow.status_code > 300:
			msg = 'Requests ERROR_code{}\n'.format(str(brow.status_code)) + reqUrl
			logging.error(msg=msg)
			return None

	except Exception as ff:
		msg = 'Requests ERROR_hub\n' + '\n' + reqUrl
		print(ff)
		# logging.error(msg=msg)
		return None
	hhtml = brow.text.encode(brow.encoding).decode('utf-8')
	soup = BeautifulSoup(brow.text, 'lxml')
	print(soup.prettify())
	ddict = {}
	try:
		ddict['fanhao'] = fanhaoInfo['fanhao']
		ddict['title'] = soup.h3.get_text()
	except:
		errjsonFile = 'ERROR_info.json'
		errjsonPath = os.path.join(fanhaoInfo['root'], errjsonFile)
		with open(errjsonPath, 'w', encoding='utf-8') as ff:
			json.dump(ddict, ff, ensure_ascii=False)
			ff.flush()
			ff.close()
		print('ERROR Request')
		print(fanhaoInfo)
		return None

	bigImage = soup.find(class_='bigImage').get('href')
	ddict['cover_OriginalUrl'] = urlparse.urljoin(fhSeachurl, bigImage)
	ddict['cover'] = imgDownLoad(imgUrl=ddict['cover_OriginalUrl'], Info=fanhaoInfo)
	illustration = soup.find_all(class_='sample-box')
	ddict['illustration_OriginalUrl'] = [urlparse.urljoin(fhSeachurl, x.get('href')) for x in illustration]
	ddict['illustration'] = imgDownLoad(imgUrl=ddict['illustration_OriginalUrl'], Info=fanhaoInfo)

	ddict['issueTime'] = get_issueTime(soup.prettify())
	ddict['duration'] = get_duration(soup.prettify()) + "分钟"
	keys = soup.find('meta', attrs={'name': 'keywords'}).get('content')
	ddict['keys'] = keys.split(',')
	ddict['keys'].remove(ddict['fanhao'])
	ddict['actor'] = get_actor(soup)
	jsonFile = 'info.json'
	jsonPath = os.path.join(fanhaoInfo['root'], jsonFile)
	with open(jsonPath, 'w', encoding='utf-8') as ff:
		json.dump(ddict, ff, ensure_ascii=False)
		ff.flush()
		ff.close()
	return ddict


if __name__ == '__main__':
	h = "YSN-463㊥ ハミチンしていた僕を指摘しながらも含み笑いを浮かべ、敏感なチ●ポをイタズラ 並木杏梨 百合華 真白愛梨2017-fanart.jp"

	w = '㊥'
	print(w in h)

	exit()
	mosaic_root = r"Z:\x299\寄生虫.720p.1080p.HD中字\6v电影APP 有他不迷路\appsiteweb\PIDEO_ROOT\mosaic"
	nonmosaic_root = r"Z:\x299\寄生虫.720p.1080p.HD中字\6v电影APP 有他不迷路\appsiteweb\PIDEO_ROOT\non_mosaic"
	rootPath = [mosaic_root, nonmosaic_root]
	video_root = r"Z:\x299\寄生虫.720p.1080p.HD中字\6v电影APP 有他不迷路\appsiteweb\PIDEO_ROOT"
	video_root = r"D:\BT_download\sucess"

	mark = 0
	for fDict in file_name_walk(video_root):
		# if mark > 12:
		# 	break
		if 'info.json' in fDict['files']:
			continue
		if 'CARIB' in fDict['fanhao'] or 'HEYZO' in fDict['fanhao'] or '10MUSUME' in fDict['fanhao'] or 'PONDO' in \
				fDict['fanhao']:
			continue
		if 'ERROR_info.json' in fDict['files']:
			continue
		if '.actors' == ['fanhao']:
			continue

		# try:
		print(fDict)
		videoInfo = use_FanHaoInfo_get_VideoInfo(fanhaoInfo=fDict)
		# except:
		# 	time.sleep(60 * 5)
		# videoInfo = use_FanHaoInfo_get_VideoInfo(fanhaoInfo=fDict)
		# # pprint.pprint(videoInfo)
		# print(fDict['root'])
		# print('------------------')
		mark += 1

	print(mark)

	exit()

	getInfo = {'fanhao': 'OFJE-266',
	           'files': ['OFJE-266.MP4'],
	           'root': 'D:/PythonCode/home/testVideoFolder'}
