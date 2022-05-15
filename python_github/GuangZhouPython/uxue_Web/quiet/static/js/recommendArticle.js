/**
 * 推荐文章
 */


// 当前页码
var recommendArticlePageIndex = 1;
// 每页记录数
var recommendArticlePageSize = 20;
// 接口地址
var recommendArticleApiUrl = "/api/recommendPosts";


$(function () {

	$(".articleList ul").html("");
    getRecommendArticleList();

    /**
     * 绑定点击更多点击事件
     */
    $(".hotArticleList .loadMoreBtn").unbind("click").on("click" , function () {
        contentRecommendArticleLoadMore();
    });

});

/**
 * 加载作者热门文章列表
 */
function getRecommendArticleList() {

    var param = {
        pageIndex : recommendArticlePageIndex ,
        pageSize : recommendArticlePageSize
    };

    ajax(dataApiUrl + recommendArticleApiUrl , "post" , true , param , function(data){
        if(data != null){
            var obj = data;
            $(".articleList ul").html("");
            for(var i = 0 ; i < obj.length ; i++){

                $(".articleList ul").append(
                    '<li>'+
                    '<a href="' + obj[i].url + '">'+
                    '<div class="articleTitle">' + topping + '<i>' + obj[i].title + '</i></div>'+
                    '<div class="articleCon">' + obj[i].summary + '</div>'+
                    '<div class="articleMsg">'+
                    '<div class="articleAuthor">'+
                    '<img src="' + obj[i].authorImg + '"/>'+
                    //'<span class="authorName">通信皮皮虾</span>'+
                    '</div>'+
                    '<div class="articleSource">' + obj[i].category + '</div>'+
                    //'<div class="articleOriginal">原创</div>'+
                    '<div class="clearDiv"></div>'+
                    '<div class="articleReleaseTime">' + obj[i].datetime + '</div>'+
                    '</div>'+
                    '<div class="cl_f"></div>'+
                    '<div class="articleBanner"><img src="' + obj[i].articlePreviewImg + '"/></div>'+
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
function contentRecommendArticleLoadMore() {
    recommendArticlePageIndex++;
    getRecommendArticleList();
}