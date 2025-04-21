import os
import sys
import wave
import pyaudio
import logging
import keyboard
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录
work_dir = os.path.dirname(current_dir)
# 将项目根目录添加到sys.path
sys.path.append(work_dir)
# 导入模块
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
        logging.info('识别结果:' + text)
        # print('识别结果:', text)
        return text


def debug():
    # demo 此处仅用于测试
    import time
    import tempfile

    # 初始化STT
    stt = STT()
    # 初始化音频库
    audio = pyaudio.PyAudio()

    # 存储用户输入的文本
    user_messsage = ''
    # 判断是否退出
    exit_program = False

    # 录音设置 # todo 考虑移到setting里
    # 16位音频格式、单声道、采样率、每个数据块包含的帧数
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    # 读取系统设置，快捷键
    settings = setting().get('STT')
    hotkey = settings['hotkey']

    # 音频帧
    frames = []
    # 音频流
    stream = None
    # 标记录音状态
    is_recording = False
    # 初始化按键时长
    last_press_time = 0
    # 按键冷却时间
    debounce_time = 0.5

    print('waiting...')
    try:
        while not exit_program:
            # 判断按下快捷键开始或停止录音
            if keyboard.is_pressed(hotkey=hotkey):
                # 按键冷却，避免误触
                current_time = time.time()
                if current_time - last_press_time > debounce_time:
                    last_press_time = current_time

                    if not is_recording:
                        # 开始录音
                        print('开始录音')
                        # 标记录音状态
                        is_recording = True
                        # 开始记录音频流
                        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
                        # 清空上一次录音留下的音频帧
                        frames = []
                    else:
                        # 结束录音
                        print('录音结束')
                        # 标记录音状态
                        is_recording = False
                        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
                            wave_file = wave.open(tmpfile.name, 'wb')
                            wave_file.setnchannels(CHANNELS)
                            wave_file.setsampwidth(audio.get_sample_size(FORMAT))
                            wave_file.setframerate(RATE)
                            wave_file.writeframes(b''.join(frames))
                            wave_file.close()
                            # 语音转文字
                            user_messsage = stt.save_and_transcribe(tmpfile.name)
                        print('语音转文本:', user_messsage)

            # 判断是否录音成功
            if is_recording and stream is not None:
                # 记录音频数据
                data = stream.read(CHUNK)
                frames.append(data)

    finally:
        # 用于结束录音
        if stream:
            stream.stop_stream()
            stream.close()
        # 终止录音，关闭麦克风
        audio.terminate()

def api():
    from fastapi import FastAPI, File, UploadFile, HTTPException, status
    from pydantic import BaseModel

    # 读取系统设置
    settings = setting().get('STT')
    port = settings['port']

    # 创建FastAPI应用
    app = FastAPI()
    # 创建STT实例
    stt = STT()

    # 分布式
    @app.post('/stt')
    async def save_and_transcribe_api(tmpfile: UploadFile = File(...)):
        try:
            # ? 用不了相对路径，有空再研究
            tmpfile_path = f'D:/{tmpfile.filename}'
            # 保存文件到临时路径
            with open(tmpfile_path, 'wb') as file:
                file.write(await tmpfile.read())
                if file:
                    print('get:', file.name)
                    pass
            # 语音转文字
            user_message = stt.save_and_transcribe(tmpfile_path)
            return {'user_message': user_message}

        except Exception:
            raise HTTPException(status_code=500, detail=str(Exception))

    # 模块状态
    @app.get('/stt/status')
    async def static():
        return status.HTTP_200_OK

    # 启动服务
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    if True:
        api()
    else:
        debug()