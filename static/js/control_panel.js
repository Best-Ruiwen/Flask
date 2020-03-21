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

function uploadData(node, order){
    $.ajax({
        url:"/user/" + $("#username").text() + "/order/",
        data:{'node':node, 'order':order},
        dataType:"json",
        success:function(ret){
            if(ret==1){
                alert("操作成功！设备已经响应您的命令");
            }
            else{
                alert("操作失败！设备未响应您的命令");
            }
        }
    });
}

function control(){
    var tst = JSON.parse( $('#tables').text());
    for(var i=0;i<tst.length;i++){
        if($("#"+tst[i]).is(":checked")){
            if($("#start").is(":checked")){
                // console.log(1);
                uploadData(tst[i], 1);
            }
            else if($("#stop").is(":checked")){
                // console.log(0);
                uploadData(tst[i], 0);
            }
            else if($("#upload").is(":checked")){
                //console.log(-1);
                uploadData(tst[i], -1);
            }
            else{
                //console.log(1);
                alert("请选择操作！");
            }
            return;
        }   
    }
    alert("请选择设备！");
}

// function changeURL(id){
//    if (id == 1) window.location.href="http://192.168.2.102/user/" + $("#username").text();
//    if (id == 2) window.location.href="http://192.168.2.102/user/" + $("#username").text() + "/chart/";
//    if (id == 2) window.location.href="http://192.168.2.102/user/" + $("#username").text() + "/control/";
// }

function checkAndSubmit(){
    var reg = new RegExp(/^[a-zA-Z]([-_a-zA-Z0-9]{6,20})$/);
    var obj = $("#deviceName").val();
    if(!reg.test(obj)) {
        alert("设备名格式错误！");
    }
    else{
        $.ajax({
            url:"/user/" + $("#username").text() + "/adddevice/",
            data:{"node":obj},
            dataType:'json',
            success:function(data){
                alert(data);
            }
        });
    }
}

function deleteDevice(){
    var tst = JSON.parse( $('#tables').text());
    for(var i=0;i<tst.length;i++){
        if($("#"+tst[i]+"_delete").is(":checked")){
            if(confirm("警告！！！你正在尝试删除设备"+ tst[i])){
                $.ajax({
                    url:"/user/" + $("#username").text() + "/delete/",
                    data:{"node":tst[i]},
                    dataType:'json',
                    success:function(data){
                        alert(data);
                    }
                });
            }
        }
    }
}

$("#logout").click(function(){
    console.log($("#username").val())
    $.ajax({
        url:'/logout/',
        data:{"username":$("#username").val()},
        dataType:"json",
        success:function(data){
            window.location.href=data;
        }
    });
});
