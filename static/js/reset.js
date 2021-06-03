$(document).ready(function(){
    var pubic_key = $("#pubkey").val();
    var encrypt = new JSEncrypt();
    encrypt.setPublicKey(pubic_key);           
    $("#reset").click(function(){
        var unencrypted_password = $("#psd").val();
        var unencrypted_email = $("#email").val();
        var verify_code = $("#verify_code").val();

        // 验证两次输入的密码是否一致
        var re_password = $("#re_psd").val();
        if(unencrypted_password != re_password){
            alert("两次输入的密码不一致！")
            return
        }

        var encrypted_password = encrypt.encrypt(unencrypted_password);
        var encrypted_email = encrypt.encrypt(unencrypted_email);
        var send = {"email":encrypted_email, "password":encrypted_password, "verify_code":verify_code};
  
        $.ajax({
            url:"/resetpasswd/submit/",
            data:send,
            dataType:"json",
            success:function(ret){
                if (ret == -1){
                    alert("验证码错误！");
                }
                else{
                    if(confirm("修改成功！是否跳转至登录界面？")){
                        data = 'http://' + window.location.host + '/login/'
                        window.location.href = data;
                    }
                    return;
                }
            }
        });
    })


    $("#sub_verify").click(function(){
        var wait = 60;
        var flag = false;
        var unencrypted_email = $('#email').val();
        var reg = new RegExp(/^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/)
        if(!reg.test(unencrypted_email)){
            alert("错误的邮箱格式！");
            return;
        }

        var encrypted_email = encrypt.encrypt(unencrypted_email);
        var send = {"email":encrypted_email, "status":"reset"}
        $.ajax({
            url:"/register/verify/",
            data:send,
            dataType:"json",
            async:false,
            success:function(data){
                if(data == -1){
                    alert("邮箱错误！")
                }
                else{
                    alert("验证码已发送，请查收，注意垃圾箱。");
                    flag = true
                }
            }
        })

        if (flag){
            time(this);
        }
        
        function time(o) {
            if (wait == 0) {
                o.removeAttribute("disabled");
                o.innerHTML = "获取验证码";
                wait = 60;
            } 
            else {
                   o.setAttribute("disabled", true);
                       o.innerHTML = wait;
                     wait--;
                     setTimeout(function() {
                         time(o)
                    }, 1000)
                }
        }
    })


})