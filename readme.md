## 基于ChatGLM的语音交互型人工智能助理的设计与实现

## The design and implementation of AI-Intelligent-Assistant which base on ChatGLM

### 介绍 About

这是一段介绍

Here is an introduction

---

### 安装依赖 Install dependencies

Python >= 3.9

    pip install requirement.txt

>上面这行大概率会报错，需要手动安装pytorch相关库

>This command will probably make an error, you will need to manually install torch and etc.

>根据自己的cuda版本修改命令，cpu版本或其它需求请自己研究：[PyTorch](https://pytorch.org/)

>Modify this command according to your own CUDA version, CPU version or other, please research yourself: [PyTorch](https://pytorch.org/)

    pip3 install torch==2.5.1+cu124 torchvision==0.20.1+cu124 torchaudio==2.5.1+cu124 --index-url https://download.pytorch.org/whl/cu124

>我还没测试过安装这块的内容，如果还是安装失败，可以创建一个issue

>I had never test this part. If the installation still fails, you can create an issue

---

### 运行 Run

命令行模式 CLI

    python main.py

网页模式 Web-UI

    python app.py

分布式部署模式 Distributed mode

    # 单独运行各模块 Run each module separately
    python [module].py

>[module]: core、control、model_offline|model_online、stt、tts

>后面应该会考虑加个脚本用于处理

>I think I'll consider to add a script for it

---

### 已知问题 Known bug

>-1.如果有什么我没发现的问题，可以创建一个issue或pullrequest。

>-1.If you find something that I didn't know, please new a issue or pullrequest.

>0.大量功能写成一坨，~~趁着还能看明白赶紧改了~~

>1.默认的快捷键F7会触发CMD的功能：历史输入，不影响使用，有空再处理，可在setting.yaml中修改快捷键

>2.Flask后端app.py中启动应用时，当debug值为True时，各模块会被实例化两次，暂不影响使用，实际部署时可改为False

---

### 文件树 Tree
    module/
        config.py
        control.py
        core.py
        model_offline.py
        model_online.py
        stt.py
        tts.py
    templates/
        index.html
        chat.html
    static/
        css/
            style.css
        js/
            script.js
    main.py
    app.py
    readme.md
    requirements.txt
    setting.yaml

---

### 更新日志 Changlog

    2025-02-23 最小系统验证完成
    2025-02-24 上传至仓库
    2025-02-25 配置文件
    2025-02-26 增加多线程输入
    2025-02-27 优化部分代码
    2025-02-28 调整部分代码结构
    2025-03-01 增加在线大模型功能
    2025-03-02 将在线大模型功能加入，并可随时切换
    2025-03-03 前端初期测试中
    2025-03-04 尝试部署分布式
    2025-03-05 开始设计操控功能
    2025-03-06 增加操控-输入文本功能
    2025-03-07 增加操控-控制设备功能
    2025-03-08 优化部分代码
    2025-03-09 增加更多程序路径选择
    2025-03-10 完善操控功能
    2025-03-11 完善代码及注释
    2025-03-12 重置前端部分、修改部分代码
    2025-03-13 修复部分问题，新增网站主页，改了一些乱七八糟的东西，重置了过往的Commits
    2025-03-14 调整部分代码，为文本转语音增加接口
    2025-03-15 规范模块的debug和api功能，规范代码结构，为在线大模型增加接口
    2025-03-15-Alpha 新增Alpha分支，重建代码结构，尝试整合各模块
    2025-03-16-Alpha 修复几个因重构导致的bug，调整prompt，重写设置
    2025-03-16 确认正常，开始合并分支
    2025-03-17 修复一个因重构导致的bug，为语音转文本增加接口
    2025-03-18 格式化部分代码，完善setting
    2025-03-19 调整部分代码，为本地大模型增加接口
    2025-03-20 调整部分代码，为设备控制增加接口
    2025-03-21 新增requirements.txt，完善readme.md
    2025-03-22 调整部分代码

---

### 参考 Templates

[ChatGLM3](https://github.com/THUDM/ChatGLM3)

[FunASR](https://github.com/modelscope/FunASR)

[EdgeTTS](https://github.com/rany2/edge-tts)

---

### 感谢 Thanks

[智谱AI开放平台](https://bigmodel.cn/)

>免费的ChatGLM-API，好

[Neuro](https://github.com/kimjammer/Neuro)

>感谢Neuro-sama与Vedal与Evil-Neuro提供的灵感，虽然效果相差有亿点大，但我会尝试继续追赶的。

[显卡]()

>感谢我那张壮烈牺牲的iGame GeForce GTX1060 雷暴鲨-6GD5，炼个丹要老命了