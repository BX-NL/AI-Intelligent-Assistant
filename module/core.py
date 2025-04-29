import requests
import logging
# import colorlog
# logging配置
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 系统核心不能以此方式运行
if __name__ == '__main__':
    logging.error('Error Running: 系统核心不能以此方式运行')
    input()

class Core:
    def __init__(self):
        # 导入系统设置
        from .config import setting
        # 读取系统设置
        settings = setting()
        # 读取分布式设置
        settings_distribute = settings.get('distribute')
        # 读取各模块设置
        self.settings_model = settings.get('model')
        self.settings_stt = settings.get('STT')
        self.settings_tts = settings.get('TTS')
        self.settings_control = settings.get('control')

        # 判断是否启用了分布式功能
        if settings_distribute == False:
            # 覆写分布式设置
            self.distribute_model = 'offline'
            self.distribute_stt = 'offline'
            self.distribute_tts = 'offline'
            self.distribute_control = 'offline'

        elif settings_distribute == True:
            # 读取分布式设置
            self.distribute_model = self.settings_model['mode']
            self.distribute_stt = self.settings_stt['mode']
            self.distribute_tts = self.settings_tts['mode']
            self.distribute_control = self.settings_control['mode']

        # 判断各模块分布式是否启用，初始化各模块或配置分布式接口
        # 初始化大模型处理模块
        if self.distribute_model == 'offline':
            if self.settings_model['LLM'] == 'offline':
                from .model_offline import Model
            elif self.settings_model['LLM'] == 'online':
                from .model_online import Model
            else:
                logging.error('Error Import: model')
            self.model = Model()
            logging.info('Module Local Model')
        elif self.distribute_model == 'online':
            IP = self.settings_model['IP']
            port = str(self.settings_model['port'])
            self.url_model = 'http://' + IP + ':' + port + '/model'
            logging.info('Module Distribute Model: ' + IP + ':' + port)

        # 初始化语音转文字模块
        if self.distribute_stt == 'offline':
            from .stt import STT
            self.stt = STT()
            logging.info('Module Local STT')
        elif self.distribute_stt == 'online':
            IP = self.settings_stt['IP']
            port = str(self.settings_stt['port'])
            self.url_stt = 'http://' + IP + ':' + port + '/stt'
            logging.info('Module Distribute STT: ' + IP + ':' + port)

        # 初始化文字转语音模块
        if self.distribute_tts == 'offline':
            from .tts import TTS
            self.tts = TTS()
            logging.info('Module Local TTS')
        elif self.distribute_tts == 'online':
            IP = self.settings_tts['IP']
            port = str(self.settings_tts['port'])
            self.url_tts = 'http://' + IP + ':' + port + '/tts'
            logging.info('Module Distribute TTS: ' + IP + ':' + port)

        # 初始化系统控制模块
        if self.distribute_control == 'offline':
            from .control import Control
            self.control = Control()
            logging.info('Module Local Control')
        elif self.distribute_control == 'online':
            IP = self.settings_control['IP']
            port = str(self.settings_control['port'])
            self.url_control = 'http://' + IP + ':' + port + '/control'
            logging.info('Module Distribute Control: ' + IP + ':' + port)

    # 配置各模块对应功能
    # 配置大模型处理模块-提示词注入
    def get_in_prompt(self):
        if self.distribute_model == 'offline':
            history = self.model.in_prompt()

        elif self.distribute_model == 'online':
            # 连接至大模型的分布式接口
            response = requests.get(self.url_model)
            history = response.json()['history']
        else:
            logging.error('Error Setting: Model')

        return history

    # 配置大模型处理模块-大模型推理
    def generate_response(self, history, text):
        logging.info('大模型推理中')
        if not text:
            text = '继续'

        # ? 忘了当初为什么用的self.history，能跑就先别动，有空再改
        if self.distribute_model == 'offline':
            new_message, self.history = self.model.generate(history, text)

        elif self.distribute_model == 'online':
            # 连接至大模型的分布式接口
            data = {'history': history, 'user_message': text}
            response = requests.post(self.url_model, json=data)
            new_message = response.json()['new_message']
            self.history = response.json()['history']
        else:
            logging.error('Error Setting: Model')

        return new_message, self.history

    # 配置语音转文字
    def transcribe_audio(self, audio_path):
        logging.info('语音识别中')
        if self.distribute_stt == 'offline':
            text = self.stt.save_and_transcribe(audio_path)

        elif self.distribute_stt == 'online':
            # 以二进制模式打开文件
            with open(audio_path, 'rb') as tmpfile:
                # 使用 multipart/form-data 格式上传文件
                file = {'tmpfile': tmpfile}
                # 连接至STT的分布式接口
                response = requests.post(self.url_stt, files=file)
                tmpfile.close()
            # 获取转换后的文字
            text = response.json()['user_message']
        else:
            logging.error('Error Setting: STT')

        return text

    # 配置文字转语音
    def synthesize(self, text):
        logging.info('语音合成中')
        if self.distribute_tts == 'offline':
            audio_data_base64 = self.tts.synthesize_and_play(text)

        elif self.distribute_tts == 'online':
            # 连接至TTS的分布式接口
            data = {'text': text}
            response = requests.post(self.url_tts, json=data)
            audio_data_base64 = response.json()['audio']

        else:
            logging.error('Error Setting: TTS')

        return audio_data_base64

    # 配置系统控制模块
    def system_control(self, text):
        if self.distribute_control == 'offline':
            type, message = self.control.extract_message(text)
            self.control.device_control(type, message)

        elif self.distribute_control == 'online':
            # 连接至控制模块的分布式接口
            data = {'text': text}
            requests.post(self.url_control, json=data)
        else:
            logging.error('Error Setting: Control')

    # 用于获取各模块运行状态
    # 脑子转不过来了，有空再弄，先这么跑着吧
    def get_module_status(self):
        status = []

        # model
        if self.distribute_model == 'offline':
            statu = 'Local'
        elif self.distribute_model == 'online':
            try:
                response = requests.get(self.url_model + '/status')
                if response.status_code == 200:
                    statu = 'Remote'
            except:
                statu = 'Error'
        else:
            logging.error('Error Setting: Model')
        status.append(statu)

        # STT
        if self.distribute_stt == 'offline':
            statu = 'Local'
        elif self.distribute_stt == 'online':
            try:
                response = requests.get(self.url_stt + '/status')
                if response.status_code == 200:
                    statu = 'Remote'
            except:
                statu = 'Error'
        else:
            logging.error('Error Setting: STT')
        status.append(statu)

        # TTS
        if self.distribute_tts == 'offline':
            statu = 'Local'
        elif self.distribute_tts == 'online':
            try:
                response = requests.get(self.url_tts + '/status')
                if response.status_code == 200:
                    statu = 'Remote'
            except:
                statu = 'Error'
        else:
            logging.error('Error Setting: TTS')
        status.append(statu)

        # control
        if self.distribute_control == 'offline':
            statu = 'Local'
        elif self.distribute_control == 'online':
            try:
                response = requests.get(self.url_control + '/status')
                if response.status_code == 200:
                    statu = 'Remote'
            except:
                statu = 'Error'
        else:
            logging.error('Error Setting: Control')
        status.append(statu)

        return status
