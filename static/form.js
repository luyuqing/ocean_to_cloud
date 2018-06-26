$(document).ready(function(){
    $("#mainForm").submit(function(event){
        $.ajax({
            type : "POST",
            url : '/wtcal',
            data: $("#mainForm").serialize(),
            success: function (data) {
                $("#test").text(data);
                var obj = $("#result").text(data.result);
                obj.html(obj.html().replace(/\n/g, '<br/>'));
                obj.html(obj.html().replace('...', '&nbsp&nbsp'));
                obj.html(obj.html().replace('...', '&nbsp&nbsp'));
                obj.html(obj.html().replace('...', '&nbsp&nbsp'));
                obj.html(obj.html().replace('...', '&nbsp&nbsp'));
                obj.html(obj.html().replace('...', '&nbsp&nbsp'));
            }
        });
        event.preventDefault();
    });
});