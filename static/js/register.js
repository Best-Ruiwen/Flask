$(document).ready(function(){
    var pubic_key = $("#pubkey").val();
    var encrypt = new JSEncrypt();
    encrypt.setPublicKey(pubic_key);           
    $("#sub_register").click(function(){
        var unencrypted_username = $("#usr").val();
        var unencrypted_password = $("#psd").val();
        var unencrypted_email = $("#email").val();
        var verify_code = $("#verify_code").val();

        // 正则验证部分
        var reg = new RegExp((/^[a-zA-Z]([-_a-zA-Z0-9]{6,20})$/))
        if(!reg.test(unencrypted_username)) {
            alert("用户名格式错误！");
            return
        }

        // 验证两次输入的密码是否一致
        var re_password = $("#re_psd").val();
        if(unencrypted_password != re_password){
            alert("两次输入的密码不一致！")
            return
        }

        var encrypted_username = encrypt.encrypt(unencrypted_username);
        var encrypted_password = encrypt.encrypt(unencrypted_password);
        var encrypted_email = encrypt.encrypt(unencrypted_email);

        var send = {"username":encrypted_username, "password":encrypted_password, "email":encrypted_email, "verify_code":verify_code};
    //console.log(send)
        $.ajax({
            url:"/register/submit/",
            data:send,
            dataType:"json",
            success:function(data){
                if(data == -1){
                    alert("验证码错误！")
                }
                else if(data == 0){
                    alert("注册失败！")
                }
                else{
                    data = 'http://' + window.location.host + data;
                    window.location.href=data;
                }
            }
        });
    })

    $("#sub_verify").click(function(){
        var unencrypted_email = $('#email').val();
        var reg = new RegExp(/^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/)
        if(!reg.test(unencrypted_email)){
            alert("错误的邮箱格式！");
            return;
        }

        var encrypted_email = encrypt.encrypt(unencrypted_email);
        var send = {"email":encrypted_email}
        $.ajax({
            url:"/register/verify/",
            data:send,
            dataType:"json",
            success:function(data){
                if(data == -1){
                    alert("该邮箱已被注册")
                }
                else{
                    alert("验证码已发送，请查收，注意垃圾箱。")
                }
            }
        })
    })
})
