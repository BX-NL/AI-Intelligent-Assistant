import requests

import edge_tts
import edge_playback
import logging
import asyncio


text = ''
output = 'test.mp3'
voice = 'zh-CN-XiaoxiaoNeural'  # 可选'zh-CN-XiaoxiaoNeural'|'zh-CN-XiaoyiNeural'
rate = '+0%'  # 语速，可以根据需求调整，如'+10%'、'-10%'等

# todo 缺少播放功能
class TTS_EdgeTTS:
    def __init__(self):
        self.voice = voice
        self.rate = rate

    async def initialize(self):
        pass  # 不需要额外的初始化

    async def synthesize(self, text):
        # 新版EdgeTTS需要海外代理
        communicate = edge_tts.Communicate(text=text, voice=self.voice, rate=self.rate, proxy='http://127.0.0.1:7890')
        await communicate.save('output.mp3')
        # communicate.playback()

    def play_audio(file_path):
        edge_playback.Communicate(file_path)
        # playsound.playsound(file_path)

    def main(self, text):
        asyncio.run(TTS_EdgeTTS().synthesize(text=text))
        # TTS_EdgeTTS().play_audio('output.mp3')




# 有点麻烦，以后再弄
# class TTS_AzureTTS:
#     def __init__(self):
#         self.api_url = 'https://azure-tts.api.endpoint'  # Azure TTS API地址

#     async def synthesize(self, text : str):
#         # 向Azure TTS请求合成语音
#         response = requests.post(self.api_url, json={'text': text})
#         if response.status_code == 200:
#             return response.content  # 返回生成的音频
#         else:
#             raise Exception('TTS synthesis failed')