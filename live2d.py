import requests

class Live2D:
    def __init__(self):
        self.api_url = "http://localhost:8002/live2d"  # 假设的Live2D API地址

    async def initialize(self):
        pass

    async def update_expression(self, text):
        # 调用Live2D接口，根据文本更新表情
        response = requests.post(self.api_url, json={"text": text})
        if response.status_code != 200:
            raise Exception("Failed to update Live2D expression")
