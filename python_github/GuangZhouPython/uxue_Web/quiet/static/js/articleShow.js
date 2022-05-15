var commentBtnStatus = true;
$(function(){
	//pc端评论框可回复的字数
    $(".saytext").keyup(function() {	
		var textareaNum = $(this).val().length;
		textareaLength = 500-textareaNum
		$(this).parent().find(".textNum span").text(textareaLength);
	});
    
    //分享
	shareFn();
    
    /*评论-点击点赞按钮*/
    likeClickFn(".articleShow .commentStatus .likeBtn");
    
    /*移动端文章-点击点赞按钮*/
    likeClickFn(".articleShow .articleDiv .articleFotDivMobile .likeBtn");  
   
   /*点击评论按钮*/
   $(".articleShow .commentResultPc .commentBtn").unbind("click").bind("click",function(){ 
   	if(commentBtnStatus){
   		$(this).addClass("active");
   		$(this).parents(".commentItem").next(".commentTextCommon").slideDown(); 
   		commentBtnStatus = false;
   	}else{
   		commentBtnStatus = true;
   		$(this).removeClass("active");
   		$(this).parents(".commentItem").next(".commentTextCommon").slideUp(); 
   	}
	   
   })
   
  //移动端
  $(".moblieSideBarNav li a").unbind("click").bind("click",function(){
	   	if($(this).hasClass("active")){
	   		$(this).removeClass("active");
	   		
	   	}else{
	   		$(this).addClass("active");
	   	}  	   
   })
  
   /*分享弹窗*/
   $(".moblieSideBarNav .shareBtn").unbind("click").bind("click",function(){
	   $(".moblieSideBarShare").stop().animate({bottom: "0"}, 300);
	   $(".moblieSideBarShare .layoutBg").show();	   
   })
   
   $(".moblieSideBarShare .cancelBtn").unbind("click").bind("click",function(){
   	 $(".moblieSideBarShare .layoutBg").fadeOut();
	 $(".moblieSideBarShare").stop().animate({bottom: "-100%"}, 500);
	 $(".moblieSideBarNav .shareBtn a").removeClass("active");
	  	   
   })
   
   // 移动端发表评论弹窗 
   $(".moblieSideBarNav .commentBtn").unbind("click").bind("click",function(){
	   $(".moblieSideBarComment").fadeIn();	   
   })
   
    $(".moblieSideBarComment .layoutBg").unbind("click").bind("click",function(){
	   $(".moblieSideBarComment").fadeOut();	   
   })
    $(".moblieSideBarComment .closeBtn").unbind("click").bind("click",function(){
	   $(".moblieSideBarComment").fadeOut();	   
   })
   
})

function likeClickFn(likeBtn,likeNum){
   /*点击点赞按钮*/
   $(likeBtn).unbind("click").bind("click",function(){
	   	if($(this).hasClass("active")){
	   		$(this).removeClass("active");
	   		
	   	}else{
	   		$(this).addClass("active");
	   	}  	   
   })
}
