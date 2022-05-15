/**
 * 快讯
 */

// 快讯页码
var contentNewsLetterPageIndex = 1;

// 快讯每页记录数
var contentNewsLetterPageSize = 1;

// 接口地址
var contentNewsLetterApiUrl = "/api/newsLetterList";


$(function () {

    restContentNewsLetterIndex();
    getContentNewsLetterList();

    /**
     * 绑定点击更多点击事件
     */
    $(".latestNewsList .loadMoreBtn").unbind("click").on("click" , function () {
        contentNewsLetterLoadMore();
    });

});

/**
 * 获取快讯新闻列表
 */
function getContentNewsLetterList() {

    var param = {
        pageIndex : contentNewsLetterPageIndex ,
        pageSize : contentNewsLetterPageSize
    };

    ajax(dataApiUrl + contentNewsLetterApiUrl , "post" , true , param , function(data){
        if(data != null){
            var obj = data;
            for(var i = 0 ; i < obj.length ; i++){

                $(".latestNewsList ul").append(
                    '<li>'+
                    '<a href="' + obj[i].url + '">'+
                    '<div class="newsTitle">'+
                    '<div class="time">' + obj[i].datetime + '</div>'+
                    '<div class="title"> '+
                    '<span class="city">' + obj[i].city + '</span>'+
                    '<i>' + obj[i].title + '</i>'+
                    '</div>'+
                    '</div>'+
                    '<div class="newsCon">' + obj[i].summary + '</div>'+
                    '</a>'+
                    '</li>'
                );

            }
        }
    });

}

/**
 * 加载更多按钮点击事件
 */
function contentNewsLetterLoadMore() {
    contentNewsLetterPageIndex++;
    getContentNewsLetterList();
}

/**
 * 重置页码
 */
function restContentNewsLetterIndex() {
    contentNewsLetterPageIndex = 1;
	$(".latestNewsList ul").html("");
}