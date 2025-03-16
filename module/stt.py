import pyaudio
import wave
import keyboard
import tempfile
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
# import config
from module.config import setting


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
        # 音频格式，要和录音端保持一致
        self.FORMAT = pyaudio.paInt16  # 16位音频格式
        self.CHANNELS = 1              # 单声道
        self.RATE = 16000              # 采样率
        self.CHUNK = 1024              # 每个数据块包含的帧数

    # backup
    # def save_and_transcribe(self, frames):
    #     # 保存录音到临时文件并进行语音转文字
    #     with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
    #         wave_file = wave.open(tmpfile.name, 'wb')
    #         wave_file.setnchannels(self.CHANNELS)
    #         wave_file.setsampwidth(pyaudio.PyAudio().get_sample_size(self.FORMAT))
    #         wave_file.setframerate(self.RATE)
    #         wave_file.writeframes(b''.join(frames))
    #         wave_file.close()

    #         # 语音转文字
    #         response = self.model.generate(
    #             input=tmpfile.name,
    #             cache={},
    #             language='auto',
    #             use_itn=True,
    #             batch_size_s=60,
    #             merge_vad=True,
    #             merge_length_s=15,
    #         )
    #         # 获取返回结果
    #         text = rich_transcription_postprocess(response[0]['text'])
    #         print('识别结果:', text)
    #         return text

    def save_and_transcribe(self, audio_path):
        # 语音转文字
        response = self.model.generate(
            input=audio_path,
            cache={},
            language='auto',
            use_itn=True,
            batch_size_s=60,
            merge_vad=True,
            merge_length_s=15,
        )
        # 获取返回结果
        text = rich_transcription_postprocess(response[0]['text'])
        print('识别结果:', text)
        return text


if __name__ == '__main__':
    # demo 此处仅用于测试
    # ! 312重置后不能使用，有空再改
    stt = STT()
    # 录音设置 # todo 存在重复，以后再优化
    FORMAT = pyaudio.paInt16  # 16位音频格式
    CHANNELS = 1              # 单声道
    RATE = 16000              # 采样率
    CHUNK = 1024              # 每个数据块包含的帧数

    # 系统设置
    hotkey = setting().get('hotkey')

    # 录音功能，按下指定按键开始和结束录音
    audio = pyaudio.PyAudio()
    frames = []
    stream = None
    is_recording = False
    print('点击', hotkey, '键开始录音，再次按下', hotkey, '键结束录音。')

    try:
        while True:
            if keyboard.is_pressed(hotkey=hotkey):
                if not is_recording:
                    # 开始录音
                    print('开始录音...')
                    is_recording = True
                    stream = audio.open(format=FORMAT, channels=CHANNELS,
                                        rate=RATE, input=True, frames_per_buffer=CHUNK)
                    frames = []
                else:
                    # 结束录音
                    print('录音结束.')
                    is_recording = False
                    break

            if is_recording and stream is not None:
                data = stream.read(CHUNK)
                frames.append(data)

    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        audio.terminate()

    print('开始转换')
    text = stt.save_and_transcribe(frames)
    print(text)
