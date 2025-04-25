import os
import sys
import time
import logging
from transformers import AutoTokenizer, AutoModel
# ? 不知道干啥用的，好像是哪里忘记删了
# from cpm_kernels.kernels.base import round_up

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录
work_dir = os.path.dirname(current_dir)
# 将项目根目录添加到sys.path
sys.path.append(work_dir)
# 导入模块
from module.config import setting

class Model():
    def __init__(self):
        # 系统设置
        self.settings = setting().get('model')
        # 本地模型路径
        model_path = self.settings['model_path']
        # 预设的提示词
        self.prompt = self.settings['prompt']
        # 加载分词器
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        # int4量化测试可用
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(bits=4, device="cuda").cuda().eval()
        # 完整部署
        # self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        # 多显卡环境下部署
        # self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True, device_map="auto").quantize(bits=8, device="cuda").cuda().eval()

    def in_prompt(self):
        logging.info('提示词注入中')
        # 记录推理时间
        start_time = time.time()
        # 注入提示词
        response, history = self.model.chat(self.tokenizer, self.prompt, history=[])
        # 输出问候语
        print(response)
        logging.info('Time used: ' + time.time()-start_time + 's')
        # todo 返回问候语
        # return response, history
        return history

    def generate(self, history, user_message):
        logging.info('模型推理中')
        # 记录推理时间
        start_time = time.time()
        # 传入用户输入的文本并获取回复
        response, history = self.model.chat(self.tokenizer, user_message, history=history)
        # todo 移除语气或另外存放
        new_message = response
        logging.info('Time used: ' + time.time()-start_time + 's')
        return new_message, history

def debug():
    model = Model()
    history = model.in_prompt()
    while True:
        user_message = str(input('输入文本：'))
        new_message, history = model.generate(history, user_message)
        print(new_message)

def api():
    from fastapi import FastAPI, HTTPException, status
    from pydantic import BaseModel

    # 读取系统设置
    settings = setting().get('model')
    port = settings['port']

    # 定义请求体模型
    class ModelRequest(BaseModel):
        history: list
        user_message: str

    # 创建FastAPI应用
    app = FastAPI()
    # 创建Model实例
    model = Model()

    # 分布式-注入prompt
    @app.get('/model')
    def in_prompt_api():
        history = model.in_prompt()
        return {'history': history}

    # 分布式
    @app.post('/model')
    async def generate_api(request: ModelRequest):
        try:
            history = request.history
            user_message = request.user_message
            new_message, history = model.generate(history, user_message)
            return {'new_message': new_message, 'history': history}

        except Exception:
            raise HTTPException(status_code=500, detail=str(Exception))

    # 模块状态
    @app.get('/model/status')
    async def static():
        return status.HTTP_200_OK

    # 启动服务
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    if True:
        api()
    else:
        debug()


# demo 本地部署API用法，可用于分布式，有空再研究
import requests
class Model_ChatGLM_Offline_API:
    def __init__(self):
        self.api_url = 'http://localhost:8000'

    async def initialize(self):
        pass  # 这里可以实现一些初始化操作

    async def generate_response(self, text):
        response = requests.post(self.api_url, json={'text': text})
        if response.status_code == 200:
            return response.json()['response']
        else:
            raise Exception('API连接失败')