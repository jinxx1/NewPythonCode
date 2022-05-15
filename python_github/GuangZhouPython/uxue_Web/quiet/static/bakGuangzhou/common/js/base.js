/*tab菜单切换－start*/
function tabNav(navBtn,navShowList){
    $(navBtn).on("click",function (event) {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
        //显示
        /*var dd = $(this).parent().parent().next(".tabList").children("div");*/
        var dd = $(navShowList).children("div");
         dd.hide();
         dd.eq($(this).index()).show();       
    });
}
/*tab菜单切换－end*/