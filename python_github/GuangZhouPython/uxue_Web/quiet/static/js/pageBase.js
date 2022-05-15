$(function(){
	//右侧悬浮窗鼠标经过图标
	$('.pageSideBar').find('li').hover(function(){
		 $(this).children(".img").addClass('active');
		 $(this).children(".mouseShow").stop().animate({width: "272",height:"145"}, 300);
	},function(){
	   $(this).children(".img").removeClass('active');
	   $(this).children(".mouseShow").stop().animate({width: "0",height:"0"}, 300);
	})
	
	//右侧悬浮窗导航切换
	tabNav(".pageSideBar .ewm .sideTabNav li",".pageSideBar .ewm .ewmDivList");
})
