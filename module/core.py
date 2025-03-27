# import os
# import sys
import requests
# # 获取当前文件的绝对路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
# # 获取项目根目录
# work_dir = os.path.dirname(current_dir)
# # 将项目根目录添加到sys.path
# sys.path.append(work_dir)
from .config import setting
# 导入模块
from .stt import STT
from .tts import TTS
from .control import Control
settings = setting().get('model')
if settings['LLM'] == 'offline':
    from .model_offline import Model
elif settings['LLM'] == 'online':
    from .model_online import Model
else:
    print('大模型加载失败')


class Core:
    def __init__(self):
        # 读取系统设置
        settings = setting()
        self.settings_model = settings.get('model')
        self.settings_stt = settings.get('STT')
        self.settings_tts = settings.get('TTS')
        self.settings_control = settings.get('control')
        # 读取分布式设置
        self.distribute_model = self.settings_model['mode']
        self.distribute_stt = self.settings_stt['mode']
        self.distribute_tts = self.settings_tts['mode']
        self.distribute_control = self.settings_control['mode']
        # 初始化各模块
        self.model = Model()
        self.stt = STT()
        self.tts = TTS()
        self.control = Control()
        pass

    def transcribe_audio(self, audio_path):
        if self.distribute_stt == 'online':
            text = self.stt.save_and_transcribe(audio_path)

        elif self.distribute_stt == 'offline':
            IP = self.settings_stt['IP']
            port = self.settings_stt['port']
            url = 'http://' + IP + ':' + port + '/stt'

            # 以二进制模式打开文件
            with open(audio_path, 'rb') as tmpfile:
                # 使用 multipart/form-data 格式上传文件
                file = {'tmpfile': tmpfile}
                response = requests.post(url, files=file)
                tmpfile.close()

            text = response.json()['user_message']
        else:
            print('mode error')

        return text

    def get_in_prompt(self):
        if self.distribute_model == 'online':
            history = self.model.in_prompt()

        elif self.distribute_model == 'offline':
            IP = self.settings_stt['IP']
            port = self.settings_stt['port']
            url = 'http://' + IP + ':' + port + '/model'

            response = requests.get(url)
            history = response.json()['history']

        return history

    def generate_response(self, history, text):
        if not text:
            text = '继续'

        # 忘了当初为什么用的self.history，能跑就先别动，有空再改
        if self.distribute_model == 'online':
            new_message, self.history = self.model.generate(history, text)

        elif self.distribute_model == 'offline':
            IP = self.settings_stt['IP']
            port = self.settings_stt['port']
            url = 'http://' + IP + ':' + port + '/model'

            data = {'history': history, 'user_message': text}
            response = requests.post(url, json=data)
            new_message = response.json()['new_message']
            self.history = response.json()['history']

        return new_message, self.history

    def synthesize_and_play(self, text):
        if self.distribute_tts == 'online':
            self.tts.synthesize_and_play(text)

        elif self.distribute_tts == 'offline':
            IP = self.settings_stt['IP']
            port = self.settings_stt['port']
            url = 'http://' + IP + ':' + port + '/tts'

            data = {'text': text}
            requests.post(url, json=data)

    def system_control(self, text):
        if self.distribute_control == 'online':
            type, message = self.control.extract_message(text)
            self.control.device_control(type, message)

        elif self.distribute_control == 'offline':
            IP = self.settings_stt['IP']
            port = self.settings_stt['port']
            url = 'http://' + IP + ':' + port + '/control'

            data = {'text': text}
            requests.post(url, json=data)
        

if __name__ == '__main__':
    print('core')
