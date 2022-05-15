
//封装的ajax方法
/**
 *
 * @param url 链接地址
 * @param type 提交类型
 * @param async 是否异步
 * @param param 参数
 * @param successFn 成功后执行函数
 * @param errorFn 失败后执行函数
 * @param isTips 是否显示提示文本
 * @param allFn 不管成功失败都执行
 */
function ajax(url, type, async, param, successFn, errorFn, isTips , allFn) {

    //错误内容
    var errorData = "";
    //错误网址
    var errorUrl = "";
    //ajax是否处理完毕
    var loadSuccess = false;
    //时钟
    var timer = null;

    //默认显示
    if (isTips == null) {
        isTips = true;
    }

    $.ajax({
        url: url, //请求地址
        type: type,
        async: async,
        dataType:'json',
        data: param,
        success: function (data) {
            /*if (data.code == 0) {
                if (successFn != null) {
                    successFn(data);
                } else {
                    console.log("ajax 成功！,未发现成功回调函数");
                }

            } else if (data.code == 302) {
                var link = location.href;
                if (data.msg.indexOf("?") != -1) {
                    link = data.msg + '&src=' + encodeURIComponent(location.href);
                } else {
                    link = data.msg + '?src=' + encodeURIComponent(location.href);
                }
                location.href = link;
            } else {
                if (isTips) {
                    $(".errorTips").html(data.msg).show();
                    setTimeout(function () {
                        $(".errorTips").hide();
                    }, 3000);
                }
                console.error("出现错误:" + data.msg);
                //code不等于0的时候的错误
                if (errorFn != null) {
                    errorFn(data);
                } else {
                    console.log("ajax 发现错误！,没有错误回调函数")
                }
            }*/

            successFn(data);

            if(allFn != null){
                allFn(data);
            }

            //执行完毕
            loadSuccess = true;

        },
        error: function (data) {
            if (isTips) {
                errorData = data.responseText;
                if(data.responseText == null || data.responseText == undefined){
                    errorData = data;
                }
                errorUrl = url;
            }

            try{
				if(data != null && data.responseText != null){
					var erroJson = JSON.parse(data.responseText);
					if(erroJson != undefined && erroJson.exception != undefined && erroJson.exception == "org.apache.shiro.authz.UnauthenticatedException"){
						location.href = urlPrefix + "/login/login.html";
					}
				}
            }catch(e){
                console.error(e + " , 服务器繁忙,请稍后再试");
            }

            //$(".errorTips").html("出现错误").show();
            console.error("服务器繁忙,请稍后再试");
            setTimeout(function () {
                $(".errorTips").hide();
            }, 3000);
            //请求错误
            if (errorFn != null) {
                errorFn(data);
            } else {
                console.log("ajax 发现错误！,没有错误回调函数")
            }

            if(allFn != null){
                allFn(data);
            }

            //执行完毕
            loadSuccess = true;

        }
    });


    /*timer = setInterval(function () {
        if (loadSuccess) {
            if (errorData != undefined && errorData != null && errorData != "" && errorUrl != undefined && errorUrl != null && errorUrl != "") {
                $.ajax({
                    url: urlPrefix+"/api/errorLog",
                    type: "post",
                    async: false,
                    data: {url: errorUrl, msg: errorData}
                });
            }
            clearInterval(timer);
        }
    }, 1000);*/

}
