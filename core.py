from stt import STT
from tts import TTS
import config

if config.setting().main('LLM') == 'offline':
    from model_offline import Model
elif config.setting().main('LLM') == 'online':
    from model_online import Model
else:
    print('大模型加载失败')


class Core:
    def __init__(self):
        # 初始化各模块
        self.model = Model()
        self.stt = STT()
        self.tts = TTS()
        pass

    # 该接口已弃用
    def record_audio(self):
        frames = self.stt.record_audio()
        return frames

    def transcribe_audio(self, frames):
        text = self.stt.save_and_transcribe(frames)
        return text

    def get_in_prompt(self):
        history = self.model.in_prompt()
        return history

    def generate_response(self, history, text):
        response, self.history = self.model.generate(history, text)
        return response

    def synthesize_and_play(self, text):
        self.tts.synthesize_and_play(text)


if __name__ == '__main__':
    print('core')
