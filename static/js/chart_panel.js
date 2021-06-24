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
    if (id == 1) window.location.href="http://" + window.location.host + "/user/" + $("#username").text();
    if (id == 2) window.location.href="http://" + window.location.host + "/user/" + $("#username").text() + "/chart/";
    if (id == 3) window.location.href="http://" + window.location.host + "/user/" + $("#username").text() + "/control/";
}


function drawLineChart(data){
    var temp=[];
    var len = data.length;
    for(var i=0;i<len;i++){
        temp.push([i, data[i]]);
    }
    echarts.init(document.getElementById('line')).setOption({
    tooltip: {},
    toolbox: {},
    xAxis: {},
    yAxis: {},
    series: [{
            type: 'line',
            smooth: false,
            data: temp
    }]
    });
} 

function drawPieChart(pie){

    var dom = document.getElementById('pie');
    var data = [];
    option = null;
    if(pie[0]){
        data[0] = {name: '低温\n(低于18℃)', value: pie[0]}
    }
    if(pie[1]){
        data[1] = {name: '舒适\n(18-25℃)', value: pie[1]}
    }
    if(pie[2]){
        data[2] = {name: '高温\n(高于25℃)', value: pie[2]}
    }
    if(window.screen.width>1024){
        option = {
            series: {
                silent:true,
                type: 'pie',
                data: data,
            }
        }; 
    }
    else{
        option = {
            series: {
                silent:true,
                type: 'pie',
                data: data,
                label:{
                    normal:{
                        position:"inner"
                    }
                }
            }
        }; 
    }
    chart = echarts.init(dom);
    chart.setOption(option, true); 
}  

function drawTable(data, time){
    var table = "<table class=\"m-auto\" style=\"position: relative; top: 50%;transform: translateY(-50%);\" border=\"1px\"><thead><tr style=\"text-align: center;\"><th><font style="+
                "vertical-align: inherit;\"><font style=\"vertical-align: inherit;\">时间</font>" +
                "</font></th><th><font style=\"vertical-align: inherit;\"><font style=\"vertical-align: inherit;\">数据</font>"+
                "</font></th></tr></thead><tbody style=\"text-align: center;\">";
    var len=data.length;
    for (var i=0;i<len;i++){
        var date = new Date(time[i]*1000);
        Y = date.getFullYear() + '-';
        M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
        D = date.getDate() + ' ';
        h = date.getHours() + ':';
        m = date.getMinutes() + ':';
        s = date.getSeconds(); 
        table = table + "<tr>     <td><p>" +Y+M+D+h+m+s+ "</p></td>   <td><p>" +data[i] + "</p></td></tr>";
    }
    table = table + "</tbody></table>";
    $("#sheet").html(table); 
    var he = $("#sheet").height() + 50 + "px"
    $("#sheet").css("height",he)
    $("#sheet").html(table); 
}  

function selectNode_mobile(node){
    for(var i=1;i<6;i++){
        if($("#"+"t_mobile"+String(i)).is(":checked")){
            $('#b2').text(node);
            $.ajax({
            url:'/'+ $("#username").text() +'/node/',
            data:{'node':node, "time":i},
            dataType:'json',
            success:function(ret){
                var data = ret['data']
                var time = ret['time']
                var pie = ret['pie']
                drawTable(data, time);
                drawPieChart(pie);
                drawLineChart(data);
                } 
            });
            return
        }
    }
    alert("请选择时间段!")
}

$(document).ready(function(){
    $("#homepage").attr("href", "http://" + window.location.host + "/user/" + $("#username").text())
    $("#download").attr("href", "http://" + window.location.host + "/download/" + $("#username").text())
    if(window.screen.width<400){
        $('#line').css('height', '300px');
        $('#pie').css('height', '300px');
    }
})

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

// 选择节点，从服务器获取数据并画图
function selectNode(gateway, node, data_type){
    for(var i=0;i<5;i++){
        if($("#"+"t"+String(i)).is(":checked")){
            // $('#nodeName').text(node);
            $.ajax({
            url:'/'+ $("#username").text() +'/node/',
            data:{
                'node':node, 
                "time":i,
                "gateway":gateway,
                "dtype":data_type
            },
            dataType:'json',
            success:function(ret){
                var data = ret['data']
                var time = ret['time']
                var pie = ret['pie']
                drawTable(data, time);
                drawPieChart(pie);
                drawLineChart(data);
                } 
            });
            return
        }
    }
    alert("请选择时间段!");
    return -1;
}

// 选择温度还是湿度
function select_t_or_h(button){
    // 分别调整温度和湿度按钮的属性
    if (button == 't'){
        $("#web_temperature").addClass('active');
        $("#web_humidity").removeClass('active');
    }
    else{
        $("#web_humidity").addClass('active');
        $("#web_temperature").removeClass('active');
    }

    var gateway_device = JSON.parse($('#gateway_device').text());
    var len = $("#gateways").find('li').length;
    var index_gateway_active = 0;   //用于记录激活的网关的li的下标

    // 遍历ul，查找哪个li具有active class，也就是查找哪个网关是激活状态
    for(index_gateway_active = 0; index_gateway_active < len; index_gateway_active++){
        if ($($("#gateways").find('li')[index_gateway_active]).hasClass("active")){
            var active_gateway = $($("#gateways").find('li')[index_gateway_active]).text()
            break;
        }
    }

    // 确保当 index_gateway_active=0，第0个li确实有active class
    if ($($("#gateways").find('li')[index_gateway_active]).hasClass("active") == false){
        alert("请选择网关！");
    }

    // 查找哪个设备被选中了
    var nodes_list = gateway_device[active_gateway];
    for(var i=0;i<nodes_list.length;i++){
        if($("#"+nodes_list[i]).is(":checked")){
            if (button == 't') {
                var ret = selectNode(gateway=active_gateway, node=nodes_list[i], data_type='temperature');
                if (ret == -1) return;
            }
            else{
                var ret = selectNode(gateway=active_gateway, node=nodes_list[i], data_type='humidity');
                if (ret == -1) return;
            }
            return;
        }
    }
    alert("请选择设备！");
}

// 点击温度时的响应
$("#web_temperature").click(function(){
    select_t_or_h(button='t');
})

// 点击湿度时的响应
$("#web_humidity").click(function(){
    select_t_or_h(button='h');
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