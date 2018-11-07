$(function () {
    // 生成富文本编辑器  https://www.kancloud.cn/wangfupeng/wangeditor3/332599
    let E = window.wangEditor;
    let editor = new E('#news-content');
    editor.create();
    //获取文件上传框
    let $thumbnailUrl = $("#news-thumbnail-url");
//文件上传至服务器
    let $uploadThumbnail = $("#upload-news-thumbnail");
    $uploadThumbnail.change(function () {
        // 获取文件
        let file = this.files[0];
        // 创建一个 FormData
        let formData = new FormData();
        // 把文件添加进去
        formData.append("upload_file", file);
        // 发送请求
        $.ajax({
            url: "/admin/upload-file/",
            method: "post",
            data: formData,
            // 定义文件的传输
            processData: false,
            contentType: false,
            success: res => {
                console.log(res);
                if (res["code"] === 1) {
                    // 获取后台返回的 URL 地址
                    let thumbnailUrl = res["data"]["file_url"];
                    $thumbnailUrl.val('');
                    $thumbnailUrl.val(thumbnailUrl);
                }
            },
            error: err => {
                logError(err);
            }
        });
    });
    let $progressBar = $(".progress-bar");
    QINIU.upload({
        // 七牛空间域名
        "domain": "http://onj3s3zfw.bkt.clouddn.com/",
        // 后台返回 token的地址
        "uptoken_url": "/admin/up_token/",
        // 按钮
        "browse_btn": "upload-btn",
        // 成功
        "success": (up, file, info) => {
            let domain = up.getOption('domain');
            let res = JSON.parse(info);
            let filePath = domain + res.key;
            $thumbnailUrl.val('');
            $thumbnailUrl.val(filePath);
        },
        // 失败
        "error": (up, err, errTip) => {
            console.log('error');
            console.log(up);
            console.log(err);
            console.log(errTip);
            console.log('error');
        },
        // 上传文件的过程中 七牛对于 4M 秒传
        "progress": (up, file) => {
            let percent = file.percent;
            $progressBar.parent().css("display", 'block');
            $progressBar.css("width", percent + '%');
            $progressBar.text(parseInt(percent) + '%');
        },
        // 完成后 去掉进度条
        "complete": () => {
            $progressBar.parent().css("display", 'none');
            $progressBar.css("width", '0%');
            $progressBar.text('0%');
        }
    });
    let $newsBtn = $("#btn-pub-news");
    $newsBtn.click(function () {
        let titleVal = $("#news-title").val();
        let descVal = $("#news-desc").val();
        let tagId = $("#news-category").val();
        let thumbnailVal = $thumbnailUrl.val();
        let contentHtml = editor.txt.html();
        let contentText = editor.txt.text();
        if (tagId === '0') {
            ALERT.alertInfoToast('请选择新闻标签')
        }
        // console.log(`
        //   新闻标题: ${titleVal},
        //   新闻描述: ${descVal},
        //   新闻分类id: ${tagId},
        //   新闻缩略图地址: ${thumbnailVal}
        //   新闻内容html版: ${contentHtml},
        //   新闻内容纯文字版：${contentText}
        // `);

        $.ajax({
            url: "/admin/news_pub/",
            method: "post",
            data: {
                "title": titleVal,
                "desc": descVal,
                "tag_id": tagId,
                "thumbnail_url": thumbnailVal,
                "content": contentHtml,
            },
            dataType: "json",
            success: res => {
                // console.log(res);
                if (res["code"] === 1) {
                    ALERT.alertNewsSuccessCallback("新闻发表成功", '新闻管理', () => {
                        window.location.href = '/admin/new_tag_manage/';
                    });
                } else {
                    ALERT.alertErrorToast(res["msg"]);
                }
            },
            error: err => {
                logError(err)
            }
        })
    });
});

