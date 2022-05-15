/**
 * 文章加载js
 */

// 当前页码
var articlePageIndex = 1;
// 每页记录数
var articlePageSize = 20;
// 选中的栏目
var articleCategorie = "";
// 接口地址
var articleApiUrl = "/api/posts";

$(function(){

    restArticleIndex();
    getArticles();

    /**
     * 绑定点击更多点击事件
     */
    $(".articleList .loadMoreBtn").unbind("click").on("click" , function () {
		articleLoadMore();
    });

});

/**
 * 加载文章列表
 */
function getArticles(){
	var param = {
		categorie : articleCategorie ,
		pageIndex : articlePageIndex ,
		pageSize : articlePageSize
	};
	
	ajax(dataApiUrl + articleApiUrl , "post" , true , param , function(data){
		if(data != null){
			var obj = data;
			for(var i = 0 ; i < obj.length ; i++){

				var topping = ""; //"<span class=\"topping\">置顶</span>";

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
function articleLoadMore() {
    articlePageIndex++;
    getArticles();
}

/**
 * 重置文章页码
 */
function restArticleIndex() {
    $(".articleList ul").html("");
	articlePageIndex = 1;
}
