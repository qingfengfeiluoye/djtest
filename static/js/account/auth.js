$(function () {
    let $loginBtn = $(".login-btn");
    $loginBtn.click(function () {
        // 验证会做两层 前端防止频繁的发送请求
        let telVal = $("input[name=telephone]").val();
        let pwdVal = $("input[name=password]").val();
        let $remember = $("input[name=remember]");
        // console.log(`${telVal}, ${pwdVal}`)
        if (telVal && pwdVal) {
            let status = $remember.is(":checked");
            let data = {
                "telephone": telVal,
                "password": pwdVal,
            };
            if (status) {
                data["remember"] = status;
            }
            ;
            $.ajax({
                url: "/account/login/",
                method: "post",
                data: data,
                dataType: "json",
                success: res => {
                    // console.log('success');
                    // console.log(res);
                    if (res["code"] === 1) {
                        message.showSuccess("登录成功")
                        setTimeout(() => {
                            window.location.href = "/";
                        }, 1500);
                    }
                    if (res["code"] === 0) {
                        message.showError(res["msg"])
                    }
                },
                error: err => {
                    // // 当 ajax 出现问题的时候 返回
                    // console.log('error');
                    // console.log(err);
                    logError(err);
                }
            })
        } else {
            message.showError("手机号和密码都不能为空");
        }
    });

    let $graphCaptchaBtn = $(".form-item .captcha-graph-img");
    let $captchaImg = $graphCaptchaBtn.find("img");
    // console.log($graphCaptchaBtn)
    $graphCaptchaBtn.click(function () {
        //获取现有src图片url
        let oldSrc = $captchaImg.attr("src");
        let newSrc = oldSrc.split("?")[0] + "?_=" + Date.now();
        //设置src为新图片url
        $captchaImg.attr("src", newSrc);
    });
    //获取手机号码传至后台，符合要求后发送信息
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
    })
    let $registerBtn = $(".form-item .register-btn");
    $registerBtn.click(function () {
        let telVal = $("input[name=telephone]").val();
        let sms_captchaVal = $("input[name=sms_captcha]").val();
        let usernameVal = $("input[name=username]").val();
        let pwdVal = $("input[name=password]").val();
        let pwd_reVal = $("input[name=password_repeat]").val();
        let img_captcha = $("input[name=captcha_graph]").val();
        console.log(pwd_reVal, pwdVal)
        if (telVal && sms_captchaVal && usernameVal && pwdVal && pwd_reVal && img_captcha) {
            if (pwdVal === pwd_reVal) {
                let data = {
                    "telephone": telVal,
                    "sms_captcha": sms_captchaVal,
                    "username": usernameVal,
                    "password": pwdVal,
                    "password_repeat": pwd_reVal,
                    "img_captcha": img_captcha
                }
                $.ajax({
                    url: "/account/register/",
                    method: "post",
                    data: data,
                    dataType: "json",
                    success: res => {
                        // console.log('success');
                        // console.log(res);
                        if (res["code"] === 1) {
                            message.showSuccess("注册成功")
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
            message.showError("请输入完整注册信息")
        }
    })
});