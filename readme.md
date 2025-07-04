## 基于ChatGLM的语音交互型人工智能助理的设计与实现

## The design and implementation of AI-Intelligent-Assistant which base on ChatGLM

---

### 介绍 About

这是一段介绍

Here is an introduction

一个人工智能助理，支持ChatGLM，支持智普清言API，缝合了FunASR、Edge-TTS，代码跟史一样，将就着用。

An AI intelligence assistant that base on ChatGLM, supports Zhipu Qingyan API, with the FunASR and Edge-TTS, and the code is a mess, and will be used.

---

### 安装依赖 Install dependencies

Python >= 3.9

    pip install requirement.txt

>上面这行大概率会报错，需要手动安装pytorch相关库

>This command will probably make an error, you will need to manually install torch and etc.

>文件是自动生成的，可能有几个不需要的也被塞进去了，建议照着程序代码手动安装

>The file is automatically generated, and there may be a few unwanted things in it, it is recommended to install it manually according to the program source code.

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

>1.修改setting.yaml的distribute为True以启用分布式功能

>1.Set 'distribute' as True to turn on distribute mode in setting.yaml

>2.修改各个模块的mode选项

>2.Switch mode of each module

>3.单独运行你需要使用的分布式的模块

>3.Run each module that you need to use

>module: control、model_offline|model_online、stt、tts

    python [module].py

>4.启动命令行模式或网页模式

>4.Start CLI or Web-UI

    python main.py|app.py

>后面应该会考虑加个脚本用于处理

>I think I'll consider to add a script for it

---

### 已知问题 Known bug

>-1.如果有什么我没发现的问题，可以创建一个issue或pullrequest。

>-1.If you find something that I didn't know, please new a issue or pullrequest.

>0.大量功能写成一坨，~~趁着还能看明白赶紧改了~~

>1.默认的快捷键F7会触发CMD的功能：历史输入，不影响使用，有空再处理，可在setting.yaml中修改快捷键

>2.Flask后端app.py中启动应用时，当debug值为True时，各模块会被实例化两次，暂不影响使用，实际部署时可改为False

>3.部分库版本不符可能会出现错误，请按照requirement安装依赖，不要使用最新版

---

### 文件树 Tree
    module/
        __init__.py
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
        js/
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
    2025-03-22 调整部分代码，重置了部分过往的Commits
    2025-03-23 开始构建core的分布式功能
    2025-03-24 完善setting适配分布式功能
    2025-03-25 完善core适配分布式功能
    2025-03-26 修复bug，调整setting结构
    2025-03-27 修复分布式端口的bug，完成分布式功能
    2025-03-28 整合部分设置
    2025-03-29 修复重复实例化的bug，修复若干bug
    2025-03-30 调整文字转语音的范围，修复分布式的若干bug，调整core部分代码
    2025-03-31 修复分布式的bug，尝试重构core适应双模式
    2025-04-01 修复bug，完善代码和注释
    2025-04-02 修改readme.md部分内容
    2025-04-03 调整部分代码
    2025-04-04 增加模块运行状态的接口
    2025-04-05 修复bug，增加查询模块运行状态的功能
    2025-04-06 修复bug，调整prompt
    2025-04-07 调整错误信息，修复空信息的bug
    2025-04-08 完成运行状态的接口
    2025-04-09 修复bug，现在分布式和网页可以正常跨设备了，完善代码及注释
    2025-04-10 完善代码及注释
    2025-04-11 完善代码及注释，修复bug，完善iodraw文件
    2025-04-12 修复若干bug
    2025-04-13 更新Readme，添加License
    2025-04-14 更新网页模式的获取模块状态功能
    2025-04-15 莫名其妙修复了一个莫名其妙的bug，为命令行模式加入模块状态功能
    2025-04-16 修复昨天那个莫名其妙的bug，应该是彻底修好了吧，微调prompt
    2025-04-17 完善代码和注释，优化分布式接口的获取方式
    2025-04-18 完善代码和注释，音频播放功能转入前端
    2025-04-19 更新Readme，添加了一些Todo
    2025-04-20 修复一个Playsound导致的报错，需要更换版本，添加logging记录日志
    2025-04-21 增加一堆logging
    2025-04-22 完善代码及注释
    2025-04-23 测试系统可用性，完善代码及注释
    2025-04-24 修复混合模式的bug，添加一堆logging，调整main，修复控制模块不能输入中文的bug
    2025-04-25 调整部分代码，修复bug，添加了一些Todo
    2025-04-26 演示时冒出来个bug，修复了一些问题，但没完全修
    2025-04-27 系统测试，整了几个bug
    2025-04-28 修复一个问题，但没完全修
    2025-04-29 重构core的init，现在能正常混合使用分布式功能了，还塞了一堆logging，更新了依赖文件
    2025-04-30 更新readme.md
    2025-05-01 完善代码及注释
    2025-05-02 完善代码及注释
    2025-05-03 调整部分代码
    2025-05-04 完善代码及注释
    2025-05-05 完善代码及注释
    2025-05-06 完善代码及注释
    2025-05-07 完善代码及注释
    2025-05-08 打包发布Release，暂时停更
    2025-05-21 添加一点docstrings，添加代码规范
    2025-05-28 调整__init__.py

---

### 未来可期 Todo

加个spark-TTS

交互终端：pyQt

保存聊天记录到MySQL

允许从MySQL读取聊天记录并提取核心实现长期记忆

过滤器Filter

控制模块做个打游戏的功能

控制模块加个画图功能，生成参数丢SD里

语音合成可以尝试用RVC

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

>感谢我那张壮烈牺牲的GeForce GTX1060-6GD5，炼个丹要老命了

### 协议 License

GNU GPLv3
[License](./LICENSE)