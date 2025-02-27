# 基于ChatGLM的语音交互型人工智能助理的设计与实现

pip install requirement.txt

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

### 已知bug

0.大量功能写成一坨，~~趁着还能看明白赶紧改了~~

1.默认的快捷键F7会触发CMD的功能：历史输入，不影响使用，有空再处理，可在setting.yaml中修改快捷键

### Tree
    core.py
    main.py
    model.py
    model_online.py
    model_offline.py
    stt.py
    tts.py
    config.py
    setting.yaml

### changlog

2025-02-23 最小系统验证完成

2025-02-24 上传至仓库

2025-02-25 配置文件

2025-02-26 增加多线程输入

2025-02-27 优化部分代码

### templates

[ChatGLM3](https://github.com/THUDM/ChatGLM3)