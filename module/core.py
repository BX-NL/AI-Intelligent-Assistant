import os
import sys
# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录
work_dir = os.path.dirname(current_dir)
# 将项目根目录添加到sys.path
sys.path.append(work_dir)
# 导入模块
from module.stt import STT
from module.tts import TTS
from module.config import setting
from module.control import Control

if setting().get('LLM') == 'offline':
    from module.model_offline import Model
elif setting().get('LLM') == 'online':
    from module.model_online import Model
else:
    print('大模型加载失败')


class Core:
    def __init__(self):
        # 初始化各模块
        self.model = Model()
        self.stt = STT()
        self.tts = TTS()
        self.control = Control()
        pass

    def transcribe_audio(self, audio_path):
        text = self.stt.save_and_transcribe(audio_path)
        return text

    def get_in_prompt(self):
        history = self.model.in_prompt()
        return history

    def generate_response(self, history, text):
        if not text:
            text = '继续'
        response, self.history = self.model.generate(history, text)
        return response, self.history

    def synthesize_and_play(self, text):
        self.tts.synthesize_and_play(text)

    def system_control(self, text):
        type, message = self.control.extract_message(text)
        self.control.device_control(type, message)


if __name__ == '__main__':
    print('core')
