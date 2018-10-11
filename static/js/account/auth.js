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
            message.showError("手机号和密码不能为空");
        }
    });

    let $graphCaptchaBtn = $(".form-item .captcha-graph-img");
    let $captchaImg = $graphCaptchaBtn.find("img");
    $graphCaptchaBtn.click(function () {
        //获取现有src图片url
        let oldSrc = $captchaImg.attr("src");
        let newSrc = oldSrc.split("?")[0] + "?_=" + Date.now();
        //设置src为新图片url
        $captchaImg.attr("src", newSrc);
    });
});