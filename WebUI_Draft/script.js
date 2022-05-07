// userid & username for access:
const username = "NAME";  // NEW: changed "" to "NAME" just for testing how the page will look
const userid = "";

function redirect(){
    var paramArray = window.location.search.substring(1).split("&");
    if (paramArray.length < 2){
        window.location.href = './error.html';
    }

    const params = new URLSearchParams(window.location.search)
    console.log("Testing query parameters: ")
    for (const param of params){
        console.log(param);
        if(param[0] == "username"){
            username = param[1];
        }
        if(param[0] == "userid"){
            userid = param[1];
        }
    }

    document.getElementById('uname').innerHTML = username;
    console.log("The userid is: "+ userid);
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
            // NEW: when "All" is clicked, display the entire schedule
            document.getElementById("user_data").style.display = "block";
            document.getElementById("completed_data").style.display = "block";
            document.getElementById("overdue_data").style.display = "block";
            //
        });

        $('.todo-nav .active-task').click(function() {
            $('.todo-list').removeClass('only-complete');
            $('.todo-list').addClass('only-active');
            $('.todo-nav li.active').removeClass('active');
            $(this).addClass('active');

            // NEW: when "Active" is clicked, display only the completed tasks schedule
           document.getElementById("user_data").style.display = "block";
            document.getElementById("completed_data").style.display = "none";
            document.getElementById("overdue_data").style.display = "none";
            //
        });

        $('.todo-nav .completed-task').click(function() {
            $('.todo-list').removeClass('only-active');
            $('.todo-list').addClass('only-complete');
            $('.todo-nav li.active').removeClass('active');
            $(this).addClass('active');

            // NEW: when "Completed" is clicked, display only the completed tasks schedule
            document.getElementById("user_data").style.display = "none";
            document.getElementById("completed_data").style.display = "block";
            document.getElementById("overdue_data").style.display = "none";
            //

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