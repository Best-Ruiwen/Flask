function setActive(id){
    $("#1").removeClass('active');
    $("#2").removeClass('active');
    $("#3").removeClass('active');
    if(id == 1){
        $("#1").addClass('active');
    }
    if(id == 2){

        $("#2").addClass('active');
    }
    if(id == 3){
        $("#3").addClass('active');
    }
}
function changeURL(id){
//    if (id == 1) window.location.href="http://localhost/user/" + $("#username").text();
//    if (id == 2) window.location.href="http://localhost/user/" + $("#username").text() + "/chart/";
//    if (id == 3) window.location.href="http://localhost/user/" + $("#username").text() + "/control/";
    if (id == 1) window.location.href="http://" + window.location.host + "/user/" + $("#username").text();
    if (id == 2) window.location.href="http://" + window.location.host + "/user/" + $("#username").text() + "/chart/";
    if (id == 3) window.location.href="http://" + window.location.host + "/user/" + $("#username").text() + "/control/";
}

$("#logout").click(function(){
    console.log($("#username").val())
    $.ajax({
        url:'/logout/',
        data:{"username":$("#username").val()},
        dataType:"json",
        success:function(data){
            data = 'http://' + window.location.host + data;
        }
    });
});
$(document).ready(function(){
    $("#homepage").attr("href", "http://" + window.location.host + "/user/" + $("#username").text())
    if(window.screen.width<400){
        $('#line').css('height', '300px');
        $('#pie').css('height', '300px');
    }
})