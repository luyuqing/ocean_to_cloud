$(document).ready(function(){
    $("form").submit(function(event){

        $.ajax({
            type : "POST",
            url : '/',
            data: $('form').serialize(),
            success: function (data) {
                var obj = $("#result").text(data.result);
                obj.html(obj.html().replace(/\n/g, '<br/>'));
            }
        });
        event.preventDefault();
    });
});