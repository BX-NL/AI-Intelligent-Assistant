from stt import STT
# import model_offline
from model_offline import llm
from tts import TTS

class Core:
    def __init__(self):
        # 初始化各模块
        self.stt = STT()
        self.model = llm()
        self.tts = TTS()
        pass

    def record_audio(self):
        frames = self.stt.record_audio()
        return frames

    def transcribe_audio(self, frames):
        text = self.stt.save_and_transcribe(frames)
        return text

    def get_in_prompt(self):
        history = self.model.in_prompt()
        return history

    def generate_response(self, text, history):
        response, self.history = self.model.start(text, history)
        return response

    def synthesize_and_play(self, text):
        self.tts.synthesize_and_play(text)

if __name__ == '__main__':
    print('core')