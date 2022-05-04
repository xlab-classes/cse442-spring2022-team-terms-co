// userid & username for access:
const username = "";
const userid = "";

function edit_task(new_task) {

    // Tag for edited tasks
    var tag = document.createElement("p"); // <p></p>
    tag.setAttribute("id", "edit-p");
    //

    var input_text_value = document.getElementsByClassName("input_text_field")[0].value;        // debugging
    var input_time_value = document.getElementsByClassName("input_time_field")[0].value;        // debugging


    console.log("input_text_value: " + input_text_value);               // debugging
    console.log("input_time_value: " + input_time_value);               // debugging

    var input_text_array = document.getElementsByClassName("input_text_field");
    var input_time_array = document.getElementsByClassName("input_time_field");

    console.log("length of time array: " + input_time_array.length);

    var buttons_array = document.getElementsByClassName("edit-button");

    // couple the two arrays together:
    var target_button;
    console.log("Button clicked = " + new_task);                        // First button number = 0
    for (var i = 0; i < buttons_array.length; i++){
        for (var j = 0; j < input_text_array.length; j++){
            if (i === j){
                if (input_text_array[j].value !== "" && input_time_array[j].value !== "") {
                //    alert("the edit button: " + i + " matches the input field: " + j + " and the input is: " + input_text_array[j].value);
                    // DEMO
                    var text = document.createTextNode(input_text_array[j].value + " @" + input_time_array[j].value);
                    console.log("The new text: " + text);
                    console.log("children of tag before: " + tag.children.length);
                    tag.appendChild(text); // <p>TEST TEXT</p>
                    var element = document.getElementsByClassName("todo-item")[i];           // new
                    console.log("booool: " + element.hasChildNodes());
                    if (element.hasChildNodes()){
                        console.log("children before: " + element.children.length);
                        element.replaceChild(tag, element.lastChild.previousSibling.previousSibling); // WORKS
                        console.log("children after : " + element.children.length);
                    }
                    input_text_array[j].value = "";
                    input_time_array[j].value = "";
                }
            }
        }
    }
}

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

var completed_flag = false;         // NEW

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

            // NEW: RAMI'S TASK, EDIT BUTTON

            completed_flag = false;         // Reset flag
            console.log("completed_flag under all task: " + completed_flag);

            var elms = document.getElementsByClassName("edit");
            Array.from(elms).forEach((x) => {
                x.style.display = "block";
            })

            var elms2 = document.getElementsByClassName("input_text")

            Array.from(elms2).forEach((x) => {
                x.style.display = "block";
            })
            // END

        });

        $('.todo-nav .active-task').click(function() {
            $('.todo-list').removeClass('only-complete');
            $('.todo-list').addClass('only-active');
            $('.todo-nav li.active').removeClass('active');
            $(this).addClass('active');

            // NEW: RAMI'S TASK, EDIT BUTTON

            completed_flag = false;         // Reset flag
            console.log("completed_flag under active: " + completed_flag);
            var elms = document.getElementsByClassName("edit");

            Array.from(elms).forEach((x) => {
                x.style.display = "block";
            })

            var elms2 = document.getElementsByClassName("input_text")

            Array.from(elms2).forEach((x) => {
                x.style.display = "block";
            })
            // END
        });

        $('.todo-nav .completed-task').click(function() {
            $('.todo-list').removeClass('only-active');
            $('.todo-list').addClass('only-complete');
            $('.todo-nav li.active').removeClass('active');
            $(this).addClass('active');

            // NEW: RAMI'S TASK, EDIT BUTTON
            completed_flag = true;         // Reset flag
            console.log("completed_flag under completed: " + completed_flag);

            var elms = document.getElementsByClassName("edit");

            Array.from(elms).forEach((x) => {
                x.style.display = "none";
            })

            var elms2 = document.getElementsByClassName("input_text")

            Array.from(elms2).forEach((x) => {
                x.style.display = "none";
            })
            // END
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
    var edit_counter = 0;   // NEW: RAMI'S TASK, EDIT BUTTON

    $(".submit-btn").click(function (e) {
        console.log(e.which)
        if ((!$(".add-task").val().length == 0)) {
            $('<div class="todo-item"><div class="checker"><span class="checked"><input type="checkbox" id="chk"></span></div> <span>' + $(".add-task").val() + ' @' + $(".add-task1").val() + '</span> <a href="javascript:void(0);" class="float-right remove-todo-item"><i class="icon-close"></i></a></div>').appendTo('.todo-list');

            // NEW: RAMI'S TASK, EDIT BUTTON
            var button_id = 1;
            var text_id = "text"+edit_counter;
           if (!completed_flag){
                console.log("completed_flag when buttons are added: " + completed_flag);

                $('<div class="edit"><span class=""><input type="submit" class="edit-button" onclick="edit_task(\'' + edit_counter+ '\')" value="Edit"></span></div>').appendTo('.todo-list')
               $('<span class="input_text"><input id="text1" class="input_text_field" placeholder="New Task..."></span></div>').appendTo('.todo-list');
                $('<span class="input_text"><input id="text2" class="input_time_field" placeholder="at time(HH:MM am/pm)"></span></div>').appendTo('.todo-list');

           } else {
               $('<div class="edit"><span class=""><input type="submit" class="edit-button" onclick="edit_task(\'' + edit_counter+ '\')" value="Edit"></span></div>').appendTo('.todo-list')
               $('<span class="input_text"><input id="text1" class="input_text_field" placeholder="New Task..."></span></div>').appendTo('.todo-list');
               $('<span class="input_text"><input id="text2" class="input_time_field" placeholder="at time(HH:MM am/pm)"></span></div>').appendTo('.todo-list');

               var elms = document.getElementsByClassName("edit");

               Array.from(elms).forEach((x) => {
                   x.style.display = "none";
               })

               var elms2 = document.getElementsByClassName("input_text")

               Array.from(elms2).forEach((x) => {
                   x.style.display = "none";
               })
           }

            button_id++;
            edit_counter++;
            // END

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
