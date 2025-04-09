import time
from zhipuai import ZhipuAI
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

class Model:
    def __init__(self):
        # 系统设置
        self.settings = setting().get('model')
        # 智普清言的APIkey
        self.api_key = self.settings['zhipuAI_API_key']
        # test api_key
        if self.api_key == '':
            try:
                with open("api_key.txt", "r") as f:
                    self.api_key = f.readline()
            except:
                print('缺少api_key')
        # 智普清言的模型选用
        self.model = self.settings['zhipuAI_model']
        # 设置连接
        self.client = ZhipuAI(api_key=self.api_key)

        # 预设的提示词
        prompt = self.settings['prompt']
        # 输入的格式 # todo 可以考虑做长期记忆
        self.messages = [
            {'role': 'system', 'content': prompt},
        ]

    # 注入提示词 # todo 增加问候语，这print太假了
    def in_prompt(self):
        print('提示词注入中')
        start_time = time.time()
        history = self.messages
        print('[对话]你好，我是爱丽丝')
        print('用时', time.time()-start_time, '秒')
        return history

    # 传入用户输入的文本并获取回复
    def generate(self, history, user_message):
        # 清空消息
        new_message = ''
        # 记录历史信息
        history.append({'role': 'user', 'content': user_message})
        # 传入用户输入的文本并获取回复
        response = self.client.chat.completions.create(model=self.model, messages=history, stream=True)
        # todo 移除语气或另外存放
        # 流式输出 # todo 先占个坑位，万一用得上
        for chunk in response:
            text = chunk.choices[0].delta.content
            new_message = new_message + text
            # print(text)
        # 记录历史信息
        history.append({'role': 'assistant', 'content': new_message})
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
