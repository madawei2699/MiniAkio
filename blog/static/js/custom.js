/*---------------------------Comment-----------------*/
function replyOne(username,commid){
        replyContent = $("#comment");
        oldContent = replyContent.val();
        var atid = '"#comment-' + commid + '"';
        prefix = "<a href=" + atid + ">@" + username + " </a>  ";
        newContent = ''
        if(oldContent.length > 0){
            if (oldContent != prefix) {
                newContent = prefix + oldContent;
            }
        } else {
            newContent = prefix
        }
        replyContent.focus();
        replyContent.val(newContent);
    }

$(function() {
      $("input[name=author]").select();
      $("form#comment_form").submit(function() {
          var required = ["author","email","comment"];
          var form = $(this).get(0);
          for (var i = 0; i < required.length; i++) {
              if (!form[required[i]].value) {
                  $(form[required[i]]).select();
                  return false;
              }
          }
          return true;
      });
    });
jQuery(document).ready(function($){
$(document).ready(function(){
  $("#comment_form").hide();
  $("#response").click(function(){
    $(this).next().slideToggle('fast');return false;
  });
  });
})
jQuery(document).ready(function($){
$(document).ready(function(){
  $(".post ul.hidearch").hide();
  $(".post h4.downarch").click(function(){
    $(this).next().slideToggle('fast');return false;
  });
  });
})
/*----------------------------------Scroll-------------------------*/
 jQuery(document).ready(function($) {

$body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');// 这行是 Opera 的补丁, 少了它 Opera 是直接用跳的而且画面闪烁 by willin

$('.tocomments').click(function(){
  $body.animate({scrollTop: $('#comments').offset().top}, 1000);
  return false;// 返回false可以避免在原链接后加上#
});
})