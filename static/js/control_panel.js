function setActive(id){
    $("#1").removeClass('active');
    $("#2").removeClass('active');
    $("#3").removeClass('active');
    $("#4").removeClass('active');
    if(id == 1){
        $("#1").addClass('active');
    }
    if(id == 2){

        $("#2").addClass('active');
    }
    if(id == 3){
        $("#3").addClass('active');
    }
    if(id == 4){
        $("#4").addClass('active');
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
                uploadData(tst[i], 1);
            }
            else if($("#stop").is(":checked")){
                uploadData(tst[i], 0);
            }
            else if($("#upload").is(":checked")){
                uploadData(tst[i], -1);
            }
            else if($("#del").is(":checked")){
                deleteDevice();
            }

            else{
                alert("请选择操作！");
            }
            return;
        }   
    }
    alert("请选择设备！");
}


function checkAndSubmit(){
    var reg_device = new RegExp(/^[a-zA-Z]([-_a-zA-Z0-9]{6,20})$/);
    var reg_ip4 = new RegExp(/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/);
    // var reg_ip6 = new RegExp(/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|+1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/);
    var reg_ip6 = new RegExp(/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/);

    var devicename = $("#deviceName").val();
    var deviceip = $("#deviceip").val();
    var isIpv6 = false;
    var status = "4";

    if(reg_ip6.test(deviceip)){
        isIpv6 = true;
        status = "6";
	}

    if(!reg_device.test(devicename)) {
        alert("设备名格式错误！");
    }
    else{
        if((!reg_ip4.test(deviceip)) && (!isIpv6)){
            alert("错误的ip地址格式！")
            return;
        }
        $.ajax({
            url:"/user/" + $("#username").text() + "/adddevice/",
            data:{"node":devicename, "ip":deviceip,"status":status},
            dataType:'json',
            success:function(data){
                alert(data);
            }
        });
    }
}

function RectifyDeviceIP(){
    var reg_ip4 = new RegExp(/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/);
    var reg_ip6 = new RegExp(/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/);
    var ip = $("#deviceip_rectify").val();
    var status = "4";
    var isIpv6 = false;
    if(reg_ip6.test(ip)){
        isIpv6 = true;
        status = "6"
    }  
  
    if(!reg_ip4.test(ip) && !isIpv6){ 
        alert("错误的ip地址格式！")
        return;
    }
    var tst = JSON.parse( $('#tables').text());
    for(var i=0;i<tst.length;i++){
        if($("#"+tst[i]+"_rectify").is(":checked")){
            $.ajax({
                url:"/user/" + $("#username").text() + "/rectify/",
                data:{"node":tst[i], "ip":ip, "status":status},
                dataType:'json',
                success:function(data){
                    alert(data);
                }
            });
            return;
        }
    }
    alert("请选择设备！");
}

function deleteDevice(){
    var tst = JSON.parse( $('#tables').text());
    for(var i=0;i<tst.length;i++){
        if($("#"+tst[i]).is(":checked")){
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
            return;
        }
    }
    alert("请选择设备！");
}

$("#logout").click(function(){
    $.ajax({
        url:'/logout/',
        data:{"username":$("#username").val()},
        dataType:"json",
        success:function(data){
            window.location.href=data;
        }
    });
});

function changeURL(id){
    if (id == 1) window.location.href="http://" + window.location.host + "/user/" + $("#username").text();
    if (id == 2) window.location.href="http://" + window.location.host + "/user/" + $("#username").text() + "/chart/";
    if (id == 3) window.location.href="http://" + window.location.host + "/user/" + $("#username").text() + "/control/";
}
  
$(document).ready(function(){
    $("#homepage").attr("href", "http://" + window.location.host + "/user/" + $("#username").text())
    // if(window.screen.width>768){
    //     $("#delete_m").attr("hidden", "hidden")
    //     $("#add_m").attr("hidden", "hidden")
    //     $("#rectify_m").attr("hidden", "hidden")
    // }
})