


// 修改设备信息未实现！！！


function alert_(message){
    $("#modal_text").text(message);
    $("#my_modal").modal('show');
}

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

function uploadData(gateway, node, order){
    $.ajax({
        url:"/user/" + $("#username").text() + "/order/",
        data:{
            'node':node,
            'order':order,
            'gateway':gateway
            },
        dataType:"json",
        success:function(ret){
            if(ret == 0){
                // alert_("操作成功！设备已经响应您的命令");
                alert_("操作成功！设备已经响应您的命令")
                
            }
            else if(ret == 1){
                alert_("操作失败！设备未响应您的命令");
            }
            else{
                alert_(ret);
            }
        }
    });
}

function control(){
    var gateway_device = JSON.parse($('#gateways_add').text());
    var len = $("#gateways").find('li').length;

    var index_gateway_active = 0;

    // 遍历ul，查找哪个li具有active class
    for(index_gateway_active = 0; index_gateway_active < len; index_gateway_active++){
        if ($($("#gateways").find('li')[index_gateway_active]).hasClass("active")){
            var active_gateway = $($("#gateways").find('li')[index_gateway_active]).text()
            break;
        }
    }

    if ($($("#gateways").find('li')[index_gateway_active]).hasClass("active") == false){
        alert_("请选择网关！");
        return;
    }

    // 查找哪个设备被选中了
    var nodes_list = gateway_device[active_gateway];
    for(var i=0;i<nodes_list.length;i++){
        if($("#"+nodes_list[i]).is(":checked")){
            if($("#start").is(":checked")){
                uploadData(active_gateway, nodes_list[i], 1);
            }
            else if($("#stop").is(":checked")){
                uploadData(active_gateway, nodes_list[i], 0);
            }
            else if($("#upload").is(":checked")){
                uploadData(active_gateway, nodes_list[i], -1);
            }
            else if($("#del").is(":checked")){
                deleteDevice(nodes_list[i], active_gateway);
            }
            else{
                alert_("请选择操作！");
            }
            return;
        }
    }
    alert_("请选择设备！");
    return;
}

// 添加设备
function add_device(){
    var tst = JSON.parse( $('#gateways_add').text());

    var device_name = $("#device_name").val();
    var device_id = $("#device_id").val();

    tst = (Object.keys(tst))

    // 设备名合法性验证
    var reg_device = new RegExp(/^[a-zA-Z]([-_a-zA-Z0-9]{3,20})$/);
    if(!reg_device.test(device_name)) {
        alert_("设备名格式错误！");
        return;
    }

    // 此for循环检查哪个网关被选中了，然后执行操作
    for(var i=0;i<tst.length;i++){
        if($("#"+tst[i]).is(":checked")){
            $.ajax({
                url:'/user/' + $("#username").text() + '/add/device/',
                data:{
                    "device_name":device_name,
                    "device_id":device_id,
                    "to_gateway":tst[i]
                },
                dataType:"json",
                success:function(data){
                    // 返回0表示添加成功，返回1表示设备名已存在
                    if(data == 0){
                        alert_("添加成功！");
                    }
                    else{
                        alert_("该设备名已存在！");
                    }
                }
            });
            return;
        }
    }

    // 没有选择网关
    alert_("请选择网关");
    return;
}

// 服务器返回值：1表示失败
//            -1表示未登录的账号
//            或者返回.txt文件，包含设备名和密钥

// 添加网关
function add_gateway(){
    var gateway_name = $("#gateway_name").val();
    var gateway_id = $("#gateway_id").val();

    // 设备名合法性验证
    var reg_device = new RegExp(/^[a-zA-Z]([-_a-zA-Z0-9]{3,20})$/);
    if(!reg_device.test(gateway_name)) {
        alert_("网关名格式错误！");
        return;
    }

    // 设备ID合法性验证
    if(gateway_id == ""){
        alert_("网关ID格式错误！");
        return;
    }

    $.ajax({
        url:"/user/" + $("#username").text() + "/add/gateway/",
        data:{
            "gateway_name":gateway_name,
            "gateway_id":gateway_id
            },
        dataType:'json',
        success:function(ret){
            if (ret == 1){
                alert_("添加失败！")
            }
            else {
                alert_("已为您自动下载接入设备时，使用的ID和密钥！")
                window.location.href = "http://" + window.location.host + ret
            }
        }
    });
    return;
}

function rectify_device(){}

function deleteDevice(device, gateway){
    $("#modal_text_del").text("你正在尝试删除设备"+ device + "！" + "此操作不可逆！");
    $("#my_modal_del").modal('show');
    $("#confirm_del").click(function(){
        $.ajax({
            url:"/user/" + $("#username").text() + "/delete/",
            data:{
                "node": device,
                "gateway": gateway
                },
            dataType:'json',
            success:function(data){
                alert_(data);
            }
        });
    })
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

$("#gateways li").click(function(){
    $(this).siblings('li').removeClass('active')
    $(this).addClass('active')
    $.ajax({
        url:"/" + $("#username").text() + '/' + $(this).text() + "/",
        dataType:'json',
        success:function(ret){
            var len = ret.length;
            var _html = "";
            var temp = "";
            for(var i = 0; i < len; i++){
                temp = "<div class=\"row\"><div class=\"col-sm-3 col-md-3 col-lg-5\"><p >" + ret[i] +
                "</p></div><div class=\"form-check  col-sm-3 col-md-3 col-lg-5\"><input class=\"form-check-input\" name=\"control\" type=\"radio\" id=\"" + ret[i] +
                "\"><label class=\"form-check-label\" for=\"" + ret[i] +
                "\">选择</label></div></div>"
                _html = _html + temp;
            }
            $("#nodes").html(_html);
        }
    });
})

