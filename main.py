import os
import time
import keyboard
import pyaudio
import threading
from funasr import AutoModel
import config
from core import Core
from stt import STT


def print_welcome():
    pass


def main():
    print('系统初始化中')
    core = Core()  # 初始化核心模块
    # || 这行不能删，不然跑不起来，我也不知道为什么Core那边没把这玩意也init
    stt = STT()  # 初始化语音转文字模块
    audio = pyaudio.PyAudio() # 初始化音频库
    print('大模型初始化中')
    history = core.get_in_prompt()

    text = ''
    exit_program = False
    input_lock = threading.Lock()  # 用于锁定输入
    recording_complete = threading.Event()  # 用于标记录音是否完成

    # 录音设置
    FORMAT = pyaudio.paInt16  # 16位音频格式
    CHANNELS = 1              # 单声道
    RATE = 16000              # 采样率
    CHUNK = 1024              # 每个数据块包含的帧数

    # 系统设置
    setting = config.setting()
    hotkey = setting.STT('hotkey')

    def hotkey_to_record():

        nonlocal text, exit_program

        frames = []
        stream = None
        is_recording = False

        try:
            while not exit_program:
                if keyboard.is_pressed(hotkey=hotkey):
                    if not is_recording:
                        # 开始录音
                        print('开始录音')
                        is_recording = True
                        stream = audio.open(format=FORMAT, channels=CHANNELS,
                                            rate=RATE, input=True, frames_per_buffer=CHUNK)
                        frames = []
                    else:
                        # 结束录音
                        print('录音结束')
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

        with input_lock:
            text = core.transcribe_audio(frames)
            print('get:', text)
            recording_complete.set()  # 标记录音完成

    def listen_for_text():
        # 监听用户输入的文本
        nonlocal text, exit_program
        while not exit_program:
            # 使用 keyboard 监听实时输入
            user_input = input()
            if user_input.lower() == 'exit':
                exit_program = True
                break
            with input_lock:
                text = user_input
                print('用户输入:', text)
                recording_complete.set()  # 标记文本输入完成

    threading.Thread(target=hotkey_to_record, daemon=True).start()
    threading.Thread(target=listen_for_text, daemon=True).start()

    while not exit_program:
        print('输入文本或按下F7开始语音输入')
        recording_complete.wait()
        recording_complete.clear()

        if text.lower() == 'exit':
            print('退出程序')
            break

        # 模型生成响应
        response_text = core.generate_response(text, history)
        print('AI 响应:', response_text)

        # 文本转语音并播放
        core.synthesize_and_play(response_text)
        print('语音播放完成。')


if __name__ == '__main__':
    main()
