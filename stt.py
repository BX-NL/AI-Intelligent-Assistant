import pyaudio
import wave
import keyboard
import tempfile
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
class STT():
    def __init__(self):
        # 模型初始化
        model_dir = 'iic/SenseVoiceSmall'
        self.model = AutoModel(
            model=model_dir,
            vad_model='fsmn-vad',
            vad_kwargs={'max_single_segment_time': 30000},
            device='cuda:0',
        )

        # 录音设置
        self.FORMAT = pyaudio.paInt16  # 16位音频格式
        self.CHANNELS = 1              # 单声道
        self.RATE = 16000              # 采样率
        self.CHUNK = 1024              # 每个数据块包含的帧数

    def record_audio(self):
        # 录音功能，按下F7开始和结束录音
        audio = pyaudio.PyAudio()
        frames = []
        stream = None
        is_recording = False
        print('按F7键开始录音，再次按下F7键结束录音.')

        try:
            while True:
                if keyboard.is_pressed('F7'):
                    if not is_recording:
                        # 开始录音
                        print('开始录音...')
                        is_recording = True
                        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                            rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
                        frames = []
                    else:
                        # 结束录音
                        print('录音结束.')
                        is_recording = False
                        break

                if is_recording and stream is not None:
                    data = stream.read(self.CHUNK)
                    frames.append(data)

        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            audio.terminate()

        return frames

    def save_and_transcribe(self, frames):
        # 保存录音到临时文件并进行语音转文字
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
            wave_file = wave.open(tmpfile.name, 'wb')
            wave_file.setnchannels(self.CHANNELS)
            wave_file.setsampwidth(pyaudio.PyAudio().get_sample_size(self.FORMAT))
            wave_file.setframerate(self.RATE)
            wave_file.writeframes(b''.join(frames))
            wave_file.close()

            # 语音转文字
            response = self.model.generate(
                input=tmpfile.name,
                cache={},
                language='auto',
                use_itn=True,
                batch_size_s=60,
                merge_vad=True,
                merge_length_s=15,
            )
            text = rich_transcription_postprocess(response[0]['text'])
            print('识别结果:', text)
            return text

if __name__ == '__main__':
    frames = STT().record_audio()
    text = STT().save_and_transcribe(frames)
    print(text)


# test FunASR demo
def demo():
    from funasr import AutoModel
    from funasr.utils.postprocess_utils import rich_transcription_postprocess


    model_dir = 'iic/SenseVoiceSmall'

    model = AutoModel(
        model=model_dir,
        vad_model='fsmn-vad',
        vad_kwargs={'max_single_segment_time': 30000},
        device='cuda:0',
    )

    # en
    response = model.generate(
        input='/example/en.mp3',
        cache={},
        language='auto',  # 'zn', 'en', 'yue', 'ja', 'ko', 'nospeech'
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,  #
        merge_length_s=15,
    )
    text = rich_transcription_postprocess(response[0]['text'])
    print(text)