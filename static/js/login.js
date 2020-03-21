$(document).ready(function(){
    var pubic_key = $("#pubkey").val();
    var encrypt = new JSEncrypt();
    encrypt.setPublicKey(pubic_key);           
    $("#sub").click(function(){
        var unencrypted_username = $("#usr").val();
        var unencrypted_password = $('#psd').val();
        var encrypted_username = encrypt.encrypt(unencrypted_username);
        var encrypted_password = encrypt.encrypt(unencrypted_password);
        var send = {"username":encrypted_username, "password":encrypted_password};
    //console.log(send)
        $.ajax({
            url:"/submit/",
            data:send,
            dataType:"json",
            success:function(data){
                if (data == 0){
                    console.log("您的账号已登录，请勿重复登录");
                }
                else if (data == -1){
                    console.log("账号或密码不正确！");
                }
                else{
                    // console.log(window.location.host+data);
                    data = 'http://' + window.location.host + data;
                    // console.log(data);
                    window.location.href=data;
                }
            }
        });
    })
})