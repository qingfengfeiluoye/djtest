let $change_passwordBtn = $(".form-item .change_password-btn");
//获取url？之后的参数作为一个变量
let tel_num = window.location.search;
//把字符串从=切开取第二项的电话号码
let telVal = tel_num.split("=")[1]
$change_passwordBtn.click(function () {
    console.log(telVal)
    let pwdVal = $("input[name=password]").val();
    let pwd_reVal = $("input[name=password_repeat]").val();
    if (pwdVal && pwd_reVal) {
        if (pwdVal === pwd_reVal) {
            let data = {
                "telephone": telVal,
                "password": pwdVal,
                "password_repeat": pwd_reVal,
            };
            $.ajax({
                url: "/account/change_password/",
                method: "put",
                data: data,
                dataType: "json",
                success: res => {
                    // console.log('success');
                    // console.log(res);
                    if (res["code"] === 1) {
                        message.showSuccess("密码修改成功")
                        setTimeout(() => {
                            window.location.href = "/";
                        }, 1500);
                    }
                    if (res["code"] === 0) {
                        message.showError(res["msg"])
                    }
                }, error: err => {
                    // // 当 ajax 出现问题的时候 返回
                    // console.log('error');
                    // console.log(err);
                    logError(err);
                }
            })
        } else {
            message.showError("两次密码输入不一致，请重新输入")
        }
    } else {
        message.showError("请输入密码")
    }
})
let $smsCaptchaBtn = $(".form-item .sms-captcha");
let $telephone = $("input[name=telephone]");
let reg = /^((1[3-9][0-9])+\d{8})$/;//用来判断手机号码的正则表达式
$smsCaptchaBtn.click(function () {
    let $status = $(this)[0].hasAttribute("disable");
    if ($status) {
        message.showInfo("验证码已经发送，请注意查收");
        return false
    }
    let telVal = $telephone.val();
    if (telVal && telVal.trim()) { //trim()去除字符串两端空白符
        if (reg.test(telVal)) {
            let data = {"telephone": telVal};
            // console.log(telVal)
            $.ajax({
                url: "/account/send_message/",
                method: "get",
                data: data,
                dataType: "json",
                success: res => {
                    // console.log('success');
                    // console.log(res);
                    let resmsg = JSON.parse(res)
                    console.log(resmsg);
                    if (resmsg["Code"] === "OK") {
                        message.showInfo(resmsg["Message"])
                    }
                    if (resmsg["Code"] === "isv.BUSINESS_LIMIT_CONTROL") {//手机号码发送次数达到上限
                        message.showError(resmsg["Message"])
                    }
                    let count = 60;
                    let $text = $(this).text();
                    $(this).attr("disable", true);
                    let timer = setInterval(() => {
                        $(this).text(count);
                        count--;
                        if (count <= 0) {
                            clearInterval(timer);
                            $(this).text($text);
                            $(this).removeAttr("disable");
                        }
                    }, 1000);
                },
                error: err => {
                    logError(err);
                }
            })
        }
        else {
            message.showError("手机号码格式不正确");
            $telephone.focus();//把光标聚焦到手机号输入栏，用户直接再次输入手机号码
        }
    } else {
        message.showError("请输入手机号码")
    }
});
let $check_captchaBtn = $(".form-item .check_captcha-btn");
$check_captchaBtn.click(function () {
    let telVal = $("input[name=telephone]").val();
    let sms_captchaVal = $("input[name=sms_captcha]").val();
    if (telVal && sms_captchaVal) {
        let data = {
            "telephone": telVal,
            "sms_captcha": sms_captchaVal,
        }
        $.ajax({
            url: "/account/change_password/",
            method: "post",
            data: data,
            dataType: "json",
            success: res => {
                // console.log('success');
                console.log(res);
                if (res["code"] === 1) {
                    setTimeout(() => {
                        //把手机号码从url传到下一个页面
                        window.location.href = "/account/change_password/?telephone=" + telVal;
                    }, 1000);
                }
                if (res["code"] === 0) {
                    message.showError(res["msg"])
                }
            }, error: err => {
                // // 当 ajax 出现问题的时候 返回
                // console.log('error');
                // console.log(err);
                logError(err);
            }
        })
    } else {
        message.showError("手机号码和验证码不能为空")
    }
});