
var contextPath = "/";

var dataApiUrl = "http://120.79.192.168:6800";

/*tab菜单切换－start*/
function tabNav(navBtn,navShowList){
    $(navBtn).on("click",function (event) {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
        //显示
        /*var dd = $(this).parent().parent().next(".tabList").children("div");*/
        var dd = $(navShowList).children("div");
         dd.hide();
         dd.eq($(this).index()).show();
    });
}
/*tab菜单切换－end*/

/*判断文本框输入的字数-start*/
  function textareaBox(textareaName,textareaSize){  
  	  //判断是否为ios系统
	  if(/ipad|iphone|mac/i.test(navigator.userAgent)) {
			document.getElementById(textareaName).addEventListener('input', function(e) {　　
				var value = e.target.value;		
				var textareaNum = $(this).val().length;
				textareaLength = 500-textareaNum
				$(this).parent().find(textareaSize).text(textareaLength);
			});
	
		} else {
			$(textareaName).keyup(function() {	
				var textareaNum = $(this).val().length;
				textareaLength = 500-textareaNum
				$(this).parent().find(textareaSize).text(textareaLength);
			});
		}     
	}   

/*判断文本框输入的字数-end*/

/*分享*/
function shareFn(){
	 window._bd_share_config = { "common": { "bdSnsKey": {}, "bdText": "", "bdMini": "2", "bdMiniList": false, "bdPic": "", "bdStyle": "0", "bdSize": "16" }, "share": {} }; with (document) 0[(getElementsByTagName('head')[0] || body).appendChild(createElement('script')).src = 'http://bdimg.share.baidu.com/static/api/js/share.js?v=89860593.js?cdnversion=' + ~(-new Date() / 36e5)];
}
function tsina() { document.getElementById("tsina").click(); }
function qzone() { document.getElementById("qzone").click(); }
function weixin() { document.getElementById("weixin").click(); }


/*移动端*/

/*移动端下拉加载效果（参考微信ui，网站：http://jqweui.com/extends#popup）-start*/
var loading = false;
var synStatus = false;
function listLoad($bodyName, statusFn, fn) {
    $bodyName.infinite().unbind("infinite").bind("infinite", function () {   /*"document.body"*/
        var status = false;
        if (statusFn != null) {
            status = statusFn();
        }

        //锁定加载状态
        if(synStatus){
            return;
        }

        synStatus = true;

        if (status && loading) {
            return;
        }

        loading = true;
        if (status) {
            $bodyName.destroyInfinite();
            loading = true;
            setTimeout(function () {
                $(".weui-loadmore").hide();
                synStatus = false;
            }, 1000);
        } else {
            if (fn != null) {
                setTimeout(function () {
                    fn();
                    loading = false;
                    synStatus = false;
                }, 1000);
            }
        }
    });
}
/*下拉加载效果-end*/

/*时间戳转成日期格式*/
function getLocalTime(nS) {
    var nS = nS / 1000;
    return dateStr(new Date(parseInt(nS) * 1000), "yyyy-MM-dd");
}

//自定义时间格式
function timeStr(nS, str) {
    var nS = nS / 1000;
    return dateStr(new Date(parseInt(nS) * 1000), str);
}

// <summary>
// 格式化显示日期时间
// </summary>
// <param name="x">待显示的日期时间，例如new Date()</param>
// <param name="y">需要显示的格式，例如yyyy-MM-dd hh:mm:ss</param>
function dateStr(x, y) {
    var z = {
        y: x.getFullYear(),
        M: x.getMonth() + 1,
        d: x.getDate(),
        h: x.getHours(),
        m: x.getMinutes(),
        s: x.getSeconds()
    };
    return y.replace(/(y+|M+|d+|h+|m+|s+)/g, function (v) {
        return ((v.length > 1 ? "0" : "") + eval('z.' + v.slice(-1))).slice(-(v.length > 2 ? v.length : 2))
    });
}