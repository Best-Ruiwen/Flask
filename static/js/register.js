$(document).ready(function(){
    var sub_lv = 0;
    var pubic_key = $("#pubkey").val();
    var encrypt = new JSEncrypt();
    encrypt.setPublicKey(pubic_key);           
    $("#sub_register").click(function(){
        var unencrypted_username = $("#usr").val();
        var unencrypted_password = $("#psd").val();
        var unencrypted_email = $("#email").val();
        var verify_code = $("#verify_code").val();
        var reg = new RegExp((/^[a-zA-Z]([-_a-zA-Z0-9]{5,20})$/))
        if(!reg.test(unencrypted_username)) {
            alert("用户名格式错误！");
            return
        }
        if (sub_lv < 2){
            alert("密码过于简单！")
            return
        }
        var re_password = $("#re_psd").val();
        if(unencrypted_password != re_password){
            alert("两次输入的密码不一致！")
            return
        }
        var encrypted_username = encrypt.encrypt(unencrypted_username);
        var encrypted_password = encrypt.encrypt(unencrypted_password);
        var encrypted_email = encrypt.encrypt(unencrypted_email);

        var send = {"username":encrypted_username, "password":encrypted_password, "email":encrypted_email, "verify_code":verify_code};
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
        var wait = 60;
        var unencrypted_email = $('#email').val();
        var reg = new RegExp(/^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/)
        if(!reg.test(unencrypted_email)){
            alert("错误的邮箱格式！");
            return;
        }

        time(this);
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
        var encrypted_email = encrypt.encrypt(unencrypted_email);
        var send = {"email":encrypted_email, "status":"register"}
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

    if(window.screen.width<768){
        $("#user_form").html("<div class=\"col-12\">\
                                    <input id=\"usr\" class=\"form-control\" placeholder=\"用户名:6-20位，字母开头，只能有数字字母下划线\">\
                                </div>")
        $("#password_form").html("<div class=\"col-12\">\
                                    <input id=\"psd\" class=\"form-control\" type=\"password\" placeholder=\"密码:6-20，至少包含字母、数组、特殊字符中两种\">\
                                </div>")
        $("#re_password_form").html("<div class=\"col-12\">\
                                        <input id=\"re_psd\" class=\"form-control\" type=\"password\" placeholder=\"确认密码\">\
                                    </div>")
        $("#verify_form").html("<div class=\"col-5\">\
                                        <input id=\"verify_code\" class=\"form-control\" placeholder=\"验证码\">\
                                </div>")
        $("#email_form").html("<div class=\"col-12\" id=\"email\" type=\"email\">\
                                    <input id=\"usr\" class=\"form-control\" placeholder=\"邮箱:email@abc.com\">\
                                    <p> </p>\
                                    <button id=\"sub_verify\" class=\"btn btn-outline-success col-12 querybtn btn-block\" type=\"button\">获取验证码</button>\
                                </div>")
    }

    function PasswordStrength(passwordID, strengthID) {
        this.init(strengthID);
        var _this = this;
        document.getElementById(passwordID).onkeyup = function () {
        _this.checkStrength(this.value);
        }
    };
    PasswordStrength.prototype.init = function (strengthID) {
        var id = document.getElementById(strengthID);
        var div = document.createElement('div');
        var strong = document.createElement('strong');
        this.oStrength = id.appendChild(div);
        this.oStrengthTxt = id.parentNode.appendChild(strong);
    };
    PasswordStrength.prototype.checkStrength = function (val) { 
        var aLvTxt = ['', '不安全', '一般', '安全'];
        var lv = 0; 
        if (val.match(/[a-z]/g)) { lv++;} 
        if (val.match(/[0-9]/g)) { lv++; } 
        if (val.match(/(.[^a-z0-9])/g)) { lv++; } 
        if (val.length < 6) { lv = 0; } 
        if (lv > 3) { lv = 3; } 
        sub_lv=lv; 
        this.oStrength.className = 'strengthLv' + lv;  
        this.oStrengthTxt.innerHTML = aLvTxt[lv];  
    };
    new PasswordStrength('psd','pwdStrength');
})
