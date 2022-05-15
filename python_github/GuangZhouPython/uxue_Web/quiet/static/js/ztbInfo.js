/**
 * 招投标公告
 */

// 标讯页码
var ztbInfoPageIndex = 1;

// 标讯每页记录数
var ztbInfoPageSize = 10;

// 标讯类型 1=招标公告 2=中标公告
var ztbType = "";

// 接口地址
var ztbInfoApiUrl = "https://umxh.xue2you.cn/mobile/api/ztb/ztbInfos/webPortalListInfo";

$(function () {

    restztbInfoIndex();
    postZtbInfoListApi();

    /**
     * 绑定点击更多点击事件
     */
    $(".latestNewsList .loadMoreBtn").unbind("click").on("click" , function () {
        ztbInfoLoadMore();
    });

    /**
     * 公告类型变化
     */
    $(".latestNews .newsTabNav ul li").unbind("click").on("click" , function () {
        if($(this).text() === "招标公告"){
            ztbType = 1;
        }else if($(this).text() === "中标公告"){
            ztbType = 2;
        }else if($(this).text() === "最新标讯"){
            ztbType = "";
        }

        restztbInfoIndex();
        postZtbInfoListApi();
    })

});

/**
 * 获取快讯新闻列表
 */
function getZtbInfoList(data) {

    if(data != null){
        var obj = data;
        for(var i = 0 ; i < obj.length ; i++){

            $(".latestNewsList ul").append(
                '<li>'+
                '<a href="https://umxh.xue2you.cn/mobile/ztb/email/tender.html?infoId=' + obj[i].id + '">'+
                '<div class="newsTitle">'+
                '<div class="time">' + getLocalTime(obj[i].purchaseDate) + '</div>'+
                '<div class="title"> '+
                '<span class="city">' + obj[i].areaOperation + '</span>'+
                '<i>' + obj[i].pageTitle + '</i>'+
                '</div>'+
                '</div>'+
                '<div class="newsCon">' + obj[i].pageTitle + '</div>'+
                '</a>'+
                '</li>'
            );

        }
    }

}

/**
 * postApi
 */
function postZtbInfoListApi() {

    //参数
    var param = '?type=' + ztbType + "&pageIndex=" + ztbInfoPageIndex + "&pageSize=" + ztbInfoPageSize + "&cb=getZtbInfoList";

    //创建script标签
    var script = document.createElement('script');
    //把输入框的值和方法名作为url参数
    script.src = ztbInfoApiUrl + param;
    //把script标签添加到body,那么就会执行代码
    document.body.appendChild(script);
}

/**
 * 加载更多按钮点击事件
 */
function ztbInfoLoadMore() {
    ztbInfoPageIndex++;
    postZtbInfoListApi();
}

/**
 * 重置页码
 */
function restztbInfoIndex() {
	$(".latestNewsList ul").html("");
    ztbInfoPageIndex = 1;
}