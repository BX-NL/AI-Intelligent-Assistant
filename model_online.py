import requests
import config
import time
from zhipuai import ZhipuAI


class Model:
    def __init__(self):
        # 系统设置
        self.setting = config.setting()
        # 智普清言的APIkey
        self.api_key = self.setting.model('zhipuAI_API_key')
        # test api_key
        if self.api_key == '':
            with open("api_key.txt", "r") as f:
                self.api_key = f.readline()
        # 智普清言的模型选用
        self.model = self.setting.model('zhipuAI_model')
        # 设置连接
        self.client = ZhipuAI(api_key=self.api_key)

        # 预设的提示词
        prompt = self.setting.model('prompt')
        # 输入的格式
        self.messages = [
            {'role': 'system', 'content': prompt},
            # {'role': 'user', 'content': '从现在开始，我的名字是Ninglog，你将作为我的个人语音助理，如果你明白以上规则，请回复:我明白了。'},
            # {'role': 'assistant', 'content': '我明白了。'},
            # {'role': 'user', 'content': '请介绍一下你自己。'},
        ]

    # 注入提示词
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
        # print(response)
        # 流式输出 # todo 先占个坑位，万一用得上
        for chunk in response:
            text = chunk.choices[0].delta.content
            new_message = new_message + text
            # print(text)
        print(new_message)
        # 记录历史信息
        history.append({'role': 'assistant', 'content': new_message})
        # print(history)
        return new_message, history


if __name__ == '__main__':
    model = Model()
    history = model.in_prompt()
    # print(history)
    while True:
        user_message = str(input('输入文本：'))
        new_message = model.generate(history, user_message)


# demo 本地部署API用法，可用于分布式，有空再研究
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
