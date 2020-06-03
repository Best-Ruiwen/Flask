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
    // title:{text:'温度变化趋势'},
    series: [{
            type: 'line',
            smooth: false,
            data: temp
    }]
    });
}  //折线图

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
}  //饼状图

         
function drawTable(data, time){
    var table =  "<table class=\"m-auto\" style=\"position: relative; top: 50%;transform: translateY(-50%);\" border=\"1px\"><thead><tr style=\"text-align: center;\"><th><font style="+
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
    $("#sheet").html(table); // 绘制表格完成
    var he = $("#sheet").height() + 50 + "px"
    $("#sheet").css("height",he)
    $("#sheet").html(table); // 绘制表格完成
}   //表格

function selectNode(node){
    for(var i=1;i<6;i++){
        if($("#"+"t"+String(i)).is(":checked")){
            $('#nodeName').text(node);
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

function selectNode_mobile(node){
    console.log($("#t_mobile1").children("label").text())
    for(var i=1;i<6;i++){
        if($("#"+"t_mobile"+String(i)).is(":checked")){
            $('#b2').text(node);
            
            // $("#b3").text($("#"+"t_mobile"+String(i)).text())
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
