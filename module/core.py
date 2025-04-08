import requests
import warnings
from .config import setting
# 读取系统设置
settings = setting()
# 读取分布式设置
settings_distribute = settings.get('distribute')
# 判断是否需要导入本地模块
if settings_distribute == False:
    # 导入模块
    from .stt import STT
    from .tts import TTS
    from .control import Control

    # 读取大模型设置
    settings_model = settings.get('model')
    if settings_model['LLM'] == 'offline':
        from .model_offline import Model
    elif settings_model['LLM'] == 'online':
        from .model_online import Model
    else:
        print('Error Import: model')


class Core:
    def __init__(self):
        # 读取各模块设置
        self.settings_model = settings.get('model')
        self.settings_stt = settings.get('STT')
        self.settings_tts = settings.get('TTS')
        self.settings_control = settings.get('control')
        if settings_distribute == True:
            # 读取分布式设置
            self.distribute_model = self.settings_model['mode']
            self.distribute_stt = self.settings_stt['mode']
            self.distribute_tts = self.settings_tts['mode']
            self.distribute_control = self.settings_control['mode']
        else:
            # 覆写分布式设置
            self.distribute_model = 'offline'
            self.distribute_stt = 'offline'
            self.distribute_tts = 'offline'
            self.distribute_control = 'offline'
            # 初始化各模块
            self.model = Model()
            self.stt = STT()
            self.tts = TTS()
            self.control = Control()

    def transcribe_audio(self, audio_path):
        if self.distribute_stt == 'offline':
            text = self.stt.save_and_transcribe(audio_path)

        elif self.distribute_stt == 'online':
            # 配置STT的分布式接口
            IP = self.settings_stt['IP']
            port = str(self.settings_stt['port'])
            url = 'http://' + IP + ':' + port + '/stt'

            # 以二进制模式打开文件
            with open(audio_path, 'rb') as tmpfile:
                # 使用 multipart/form-data 格式上传文件
                file = {'tmpfile': tmpfile}
                response = requests.post(url, files=file)
                tmpfile.close()
            # 获取转换后的文字
            text = response.json()['user_message']
        else:
            print('Error Setting: [STT]')

        return text

    def get_in_prompt(self):
        if self.distribute_model == 'offline':
            history = self.model.in_prompt()

        elif self.distribute_model == 'online':
            # 配置大模型的分布式接口
            IP = self.settings_model['IP']
            port = str(self.settings_model['port'])
            url = 'http://' + IP + ':' + port + '/model'

            response = requests.get(url)
            history = response.json()['history']
        else:
            print('Error Setting: [model]')

        return history

    def generate_response(self, history, text):
        if not text:
            text = '继续'

        # ? 忘了当初为什么用的self.history，能跑就先别动，有空再改
        if self.distribute_model == 'offline':
            new_message, self.history = self.model.generate(history, text)

        elif self.distribute_model == 'online':
            # 配置大模型的分布式接口
            IP = self.settings_model['IP']
            port = str(self.settings_model['port'])
            url = 'http://' + IP + ':' + port + '/model'

            data = {'history': history, 'user_message': text}
            response = requests.post(url, json=data)
            new_message = response.json()['new_message']
            self.history = response.json()['history']
        else:
            print('Error Setting: [model]')

        return new_message, self.history

    def synthesize_and_play(self, text):
        if self.distribute_tts == 'offline':
            self.tts.synthesize_and_play(text)

        elif self.distribute_tts == 'online':
            # 配置TTS的分布式接口
            IP = self.settings_tts['IP']
            port = str(self.settings_tts['port'])
            url = 'http://' + IP + ':' + port + '/tts'

            data = {'text': text}
            requests.post(url, json=data)
        else:
            print('Error Setting: [TTS]')

    def system_control(self, text):
        if self.distribute_control == 'offline':
            type, message = self.control.extract_message(text)
            self.control.device_control(type, message)

        elif self.distribute_control == 'online':
            # 配置控制模块的分布式接口
            IP = self.settings_control['IP']
            port = str(self.settings_control['port'])
            url = 'http://' + IP + ':' + port + '/control'

            data = {'text': text}
            requests.post(url, json=data)
        else:
            print('Error Setting: [control]')
    
    def get_module_status(self):
        # 脑子转不过来了，有空再弄，先这么跑着吧
        status = []

        # model
        if self.distribute_model == 'offline':
            statu = 'Local'
        elif self.distribute_model == 'online':
            IP = self.settings_model['IP']
            port = str(self.settings_model['port'])
            url = 'http://' + IP + ':' + port + '/model/status'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    statu = 'Remote'
            except:
                statu = 'Error'
        else:
            print('Error Setting: [model]')
        status.append(statu)

        # STT
        if self.distribute_stt == 'offline':
            statu = 'Local'
        elif self.distribute_stt == 'online':
            IP = self.settings_stt['IP']
            port = str(self.settings_stt['port'])
            url = 'http://' + IP + ':' + port + '/stt/status'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    statu = 'Remote'
            except:
                statu = 'Error'
        else:
            print('Error Setting: [STT]')
        status.append(statu)

        # TTS
        if self.distribute_tts == 'offline':
            statu = 'Local'
        elif self.distribute_tts == 'online':
            IP = self.settings_tts['IP']
            port = str(self.settings_tts['port'])
            url = 'http://' + IP + ':' + port + '/tts/status'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    statu = 'Remote'
            except:
                statu = 'Error'
        else:
            print('Error Setting: [TTS]')
        status.append(statu)

        # control
        if self.distribute_control == 'offline':
            statu = 'Local'
        elif self.distribute_control == 'online':
            IP = self.settings_control['IP']
            port = str(self.settings_control['port'])
            url = 'http://' + IP + ':' + port + '/control/status'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    statu = 'Remote'
            except:
                statu = 'Error'
        else:
            print('Error Setting: [control]')
        status.append(statu)

        return status
        

if __name__ == '__main__':
    print('Error Running: core')
