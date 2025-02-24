import pyaudio
import wave
import keyboard
import tempfile
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

# 模型初始化
model_dir = 'iic/SenseVoiceSmall'
model = AutoModel(
    model=model_dir,
    vad_model='fsmn-vad',
    vad_kwargs={'max_single_segment_time': 30000},
    device='cuda:0',
)

# 录音设置
FORMAT = pyaudio.paInt16  # 16位音频格式
CHANNELS = 1              # 单声道
RATE = 16000              # 采样率
CHUNK = 1024              # 每个数据块包含的帧数

def record_audio():
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

    return frames

def save_and_transcribe(frames):
    # 保存录音到临时文件并进行语音转文字
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
        wave_file = wave.open(tmpfile.name, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

        # 语音转文字
        response = model.generate(
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

def stt():
    frames = record_audio()
    return save_and_transcribe(frames)

if __name__ == '__main__':
    text = stt()
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