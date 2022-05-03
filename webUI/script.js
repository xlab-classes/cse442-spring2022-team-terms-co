function redirect(){
  var paramArray = window.location.search.substring(1).split("&");
  if (paramArray.length < 2){
    window.location.href = './error.html';
  }
}

$( document ).ready(function() {
    
    "use strict";
    
    var todo = function() { 
        $('.todo-list .todo-item input').click(function() {
        if($(this).is(':checked')) {
            $(this).parent().parent().parent().toggleClass('complete');
        } else {
            $(this).parent().parent().parent().toggleClass('complete');
        }
    });
    
    $('.todo-nav .all-task').click(function() {
        $('.todo-list').removeClass('only-active');
        $('.todo-list').removeClass('only-complete');
        $('.todo-nav li.active').removeClass('active');
        $(this).addClass('active');
    });
    
    $('.todo-nav .active-task').click(function() {
        $('.todo-list').removeClass('only-complete');
        $('.todo-list').addClass('only-active');
        $('.todo-nav li.active').removeClass('active');
        $(this).addClass('active');
    });
    
    $('.todo-nav .completed-task').click(function() {
        $('.todo-list').removeClass('only-active');
        $('.todo-list').addClass('only-complete');
        $('.todo-nav li.active').removeClass('active');
        $(this).addClass('active');
    });
    
    $('#uniform-all-complete input').click(function() {
        if($(this).is(':checked')) {
            $('.todo-item .checker span:not(.checked) input').click();
        } else {
            $('.todo-item .checker span.checked input').click();
        }
    });
    
    $('.remove-todo-item').click(function() {
        $(this).parent().remove();
    });
    };
    
    todo();
    
    $(".submit-btn").click(function (e) {
      console.log(e.which)
        if ((!$(".add-task").val().length == 0)) {
            $('<div class="todo-item"><div class="checker"><span class="checked"><input type="checkbox" id="chk"></span></div> <span>' + $(".add-task").val() + ' @' + $(".add-task1").val() + '</span> <a href="javascript:void(0);" class="float-right remove-todo-item"><i class="icon-close"></i></a></div>').appendTo('.todo-list');
            $(".add-task").val('');
        } else if(e.which == 1) {
            alert('Please enter new task');
        }
        $(document).on('.todo-list .todo-item.added input').click(function() {
            if($(".add-task").is(':checked')) {
                $(".add-task").parent().parent().parent().toggleClass('complete');
            } else {
                $(".add-task").parent().parent().parent().toggleClass('complete');
            }
        });
        $('.todo-list .todo-item.added .remove-todo-item').click(function() {
            $(".add-task").parent().remove();
        });
    });
  
  $(".todo-list .todo-item").click(function() {
    $("#cmplt").append('<li><a href="#">'+$(this).text()+'</a></li>');
    $("#completed").css("display", "block");
    alert('Completed ' + $(this).text());
    $(this).remove();
  });
});