from transformers import AutoTokenizer, AutoModel
from cpm_kernels.kernels.base import round_up
import time
import os
import sys

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
        # self.setting = config.setting()
        self.setting = setting()
        # 本地模型路径
        model_path = self.setting.get('model_path')
        # 预设的提示词
        self.prompt = self.setting.get('prompt')
        # tokenizer.py，原理暂不明确
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        # int4量化测试可用
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(bits=4, device="cuda").cuda().eval()
        # 完整部署
        # model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        # 多显卡环境下部署
        # model = AutoModel.from_pretrained(model_path, trust_remote_code=True, device_map="auto").quantize(bits=8, device="cuda").cuda().eval()

    def in_prompt(self):
        print('提示词注入中')
        # 记录推理时间
        start_time = time.time()
        # 注入提示词
        response, history = self.model.chat(self.tokenizer, self.prompt, history=[])
        # 输出问候语
        print(response)
        print('用时', time.time()-start_time, '秒')
        return history

    def generate(self, history, user_message):
        print('推理中')
        # 记录推理时间
        start_time = time.time()
        # 传入用户输入的文本并获取回复
        response, history = self.model.chat(self.tokenizer, user_message, history=history)
        new_message = response
        print('用时', time.time()-start_time, '秒')
        return new_message, history

def debug():
    model = Model()
    history = model.in_prompt()
    while True:
        user_message = str(input('输入文本：'))
        new_message, history = model.generate(history, user_message)
        print(new_message)

def api():
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel

    # 定义请求体模型
    class ModelRequest(BaseModel):
        history: list
        user_message: str

    app = FastAPI()
    # 创建 Model 实例
    model = Model()

    @app.get('/model')
    def in_prompt_api():
        history = model.in_prompt()
        return {'history': history}

    @app.post('/model')
    async def generate_api(request: ModelRequest):
        history = request.history
        user_message = request.user_message
        try:
            new_message, history = model.generate(history, user_message)
            return {'new_message': new_message, 'history': history}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8500)

if __name__ == '__mian__':
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