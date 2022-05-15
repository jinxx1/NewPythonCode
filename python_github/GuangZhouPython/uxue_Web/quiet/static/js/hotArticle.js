/**
 * 作者热门文章
 */

// 当前页码
var hotArticlePageIndex = 1;
// 每页记录数
var hotArticlePageSize = 20;
// 接口地址
var hotArticleApiUrl = "/api/hotArticles";


$(function () {

	$(".hotArticleList ul").html("");
    getHotArticleList();

    /**
     * 绑定点击更多点击事件
     */
    $(".hotArticleList .showMoreBtn").unbind("click").on("click" , function () {
        contentHotArticleLoadMore();
    });

});

/**
 * 加载作者热门文章列表
 */
function getHotArticleList() {

    var param = {
        pageIndex : hotArticlePageIndex ,
        pageSize : hotArticlePageSize
    };

    ajax(dataApiUrl + hotArticleApiUrl , "post" , true , param , function(data){
        if(data != null){
            var obj = data;
            $(".hotArticleList ul").html("");
            for(var i = 0 ; i < obj.length ; i++){

                $(".hotArticleList ul").append(
                    '<li><a href="' + obj[i].url + '"><em></em><i>' + obj[i].title + '</i></a></li>'
                );

            }
        }
    });

}

/**
 * 加载更多按钮点击事件
 */
function contentHotArticleLoadMore() {
    hotArticlePageIndex++;
    getHotArticleList();
}