$(function(){

	//banner图轮播
	bannerSwiper();
	
	//返回顶部
	$('.returnTopLi').click(function(){
		$('body,html').animate({scrollTop: 0}, 500);
	});
	
	//分享
	shareFn();
});

/**
 * banner图轮播
 */
function bannerSwiper(){
	var swiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination',
        paginationClickable: true,
        spaceBetween: 30,
        centeredSlides: true,
        autoplay: 2500,
        autoplayDisableOnInteraction: false
    })
}


