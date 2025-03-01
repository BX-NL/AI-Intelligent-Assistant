import requests
import config
from zhipuai import ZhipuAI


class Model_ChatGLM_Online:
    def __init__(self):
        # 导入设置
        self.setting = config.setting()
        # 智普清言的设置
        self.api_key = self.setting.model('zhipuAI_API_key')
        self.model = self.setting.model('zhipuAI_model')
        
        prompt = self.setting.model('prompt')
        self.messages = [
            {'role': 'system', 'content': prompt},
            # {'role': 'user', 'content': '从现在开始，我的名字是Ninglog，你将作为我的个人语音助理，如果你明白以上规则，请回复:我明白了。'},
            # {'role': 'assistant', 'content': '我明白了。'},
            # {'role': 'user', 'content': '请介绍一下你自己。'},
        ]

    def run(self, user_message):
        new_message = ''
        client = ZhipuAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages +
            [{'role': 'user', 'content': user_message}],
            stream=True
        )
        # print(response)
        # 这个是流式输出，先占个坑位，万一用得上
        for chunk in response:
            text = chunk.choices[0].delta.content
            new_message = new_message + text
            print(text)
        print(new_message)
        self.messages += {'role': 'assistant', 'content': new_message}
        return new_message


if __name__ == '__main__':
    while True:
        user_message = str(input('输入文本：'))
        new_message = Model_ChatGLM_Online().run(user_message)


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
            raise Exception('Failed to connect to model API')
