// Modalの×、閉じるボタン押下時にウィンドウを閉じる
$(function(){
    $('.clossBtn').on('click',function(){
        $('.calendar_modal').fadeOut();
        return false;
    });
    $('.closeUpBtn').on('click',function(){
        $('.calendar_modal').fadeOut();
        return false;
    });
});