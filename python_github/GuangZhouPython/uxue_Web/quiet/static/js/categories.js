/**
 * 分类类别加载
 */

// 分类接口地址
var categoriesApiUrl = "/api/categories";

$(function () {

    $("#articleNav .swiper-wrapper").html("");
    getCategoriesList();

});

/**
 * 加载分类列表
 */
function getCategoriesList() {

    ajax(dataApiUrl + categoriesApiUrl , "post" , true , null , function (data) {
        if(data != null){
            var obj = data;
            $("#articleNav .swiper-wrapper").html("");
            for(var i = 0 ; i < obj.length ; i++){
                $("#articleNav .swiper-wrapper").append(
                    '<div class="swiper-slide"><span>' + obj[i].category + '</span></div>'
                );
            }
        }

        // 绑定分类的点击事件
        $("#articleNav .swiper-wrapper div span").unbind("click").on("click",function () {
            articleCategorie = $(this).text();

            restArticleIndex();
            getArticles();
        });

        //最新标讯导航切换初始化
        tabNav(".newsTabNav li");

        //导航滑动
        tabNavSwiper();

    });

}

/**
 * 导航滑动js
 */
function tabNavSwiper(){
    var mySwiper = new Swiper('#articleNav', {
        freeMode: true,
        freeModeMomentumRatio: 0.5,
        slidesPerView: 'auto',

    });

    swiperWidth = mySwiper.container[0].clientWidth
    maxTranslate = mySwiper.maxTranslate();
    maxWidth = -maxTranslate + swiperWidth / 2

    $(".swiper-container").on('touchstart', function(e) {
        e.preventDefault()
    })

    mySwiper.on('tap', function(swiper, e) {

        slide = swiper.slides[swiper.clickedIndex]
        slideLeft = slide.offsetLeft
        slideWidth = slide.clientWidth
        slideCenter = slideLeft + slideWidth / 2
        // 被点击slide的中心点
        mySwiper.setWrapperTransition(300)
        if (slideCenter < swiperWidth / 2) {
            mySwiper.setWrapperTranslate(0)
        } else if (slideCenter > maxWidth) {
            mySwiper.setWrapperTranslate(maxTranslate)
        } else {
            nowTlanslate = slideCenter - swiperWidth / 2
            mySwiper.setWrapperTranslate(-nowTlanslate)
        }
        $("#articleNav  .active").removeClass('active')
        $("#articleNav .swiper-slide").eq(swiper.clickedIndex).addClass('active')

    })
}

