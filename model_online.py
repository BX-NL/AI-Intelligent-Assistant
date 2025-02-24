import requests
from zhipuai import ZhipuAI

class Model_ChatGLM_Online:
    def __init__(self):
        self.api_key='26fc89e9250b0009c3d6aa32efc6af94.hpx9aZVj2hDMRCX6'
        self.model = 'glm-4-flash'

    def run(self):
        new_message = ''
        client = ZhipuAI(api_key=self.api_key)  # 请填写您自己的APIKey
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {'role': 'system', 'content': '你是一个AI Vtuber, 你的名字是Luna Alice，乐于回答各种问题的小助手，你的任务是提供有趣的建议。'},
                {'role': 'user', 'content': '从现在开始，我的名字是Ninglog，你将作为我的个人语音助理，如果你明白以上规则，请回复:我明白了。'},
                # {'role': 'assistant', 'content': '我明白了。'},
                # {'role': 'user', 'content': '请介绍一下你自己。'},
            ],
            stream=True,
        )
        # print(response)
        for chunk in response:
            text = chunk.choices[0].delta.content
            new_message = new_message + text
            print(text)
        print(new_message)



if __name__ == '__main__':
    Model_ChatGLM_Online().run()




class Model_ChatGLM_Offline:
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
