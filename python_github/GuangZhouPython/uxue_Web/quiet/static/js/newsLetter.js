/**
 * 快讯
 */

// 快讯页码
var newsLetterPageIndex = 1;

// 快讯每页记录数
var newsLetterPageSize = 1;

// 接口地址
var newsLetterApiUrl = "/api/newsLetterList";


$(function () {

    restNewsLetterIndex();
    getNewsLetterList();

    /**
     * 绑定点击更多点击事件
     */
    $(".newsLetter .loadMoreBtn").unbind("click").on("click" , function () {
        newsLetterLoadMore();
    });

});

/**
 * 获取快讯新闻列表
 */
function getNewsLetterList() {

    var param = {
        pageIndex : newsLetterPageIndex ,
        pageSize : newsLetterPageSize
    };

    ajax(dataApiUrl + newsLetterApiUrl , "post" , true , param , function(data){
        if(data != null){
            var obj = data;
            for(var i = 0 ; i < obj.length ; i++){

                $(".newsLetterList ul").append(
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
function newsLetterLoadMore() {
    newsLetterPageIndex++;
    getNewsLetterList();
}

/**
 * 重置页码
 */
function restNewsLetterIndex() {
	$(".newsLetterList ul").html("");
    newsLetterPageIndex = 1;
}