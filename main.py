import os
import time
import keyboard
import pyaudio
import threading
import tempfile
import wave
# import uvicorn
from fastapi import FastAPI
from funasr import AutoModel
from module.core import Core
from module.stt import STT
from module.tts import TTS
from module.config import setting
from module.control import Control


def main():
    # 初始化各模块
    print('系统初始化中')
    # 初始化核心模块
    core = Core()
    # 初始化音频库
    audio = pyaudio.PyAudio()
    # 初始化大模型
    print('大模型初始化中')
    # 根据setting里选用的model和prompt
    history = core.get_in_prompt()

    # 存储用户输入的文本
    user_messsage = ''
    # 判断是否退出 # todo 这个可能要改
    exit_program = False
    # 进程锁，用于锁定输入
    input_lock = threading.Lock()
    # 进程锁，用于标记录音是否完成
    recording_complete = threading.Event()

    # 录音设置 # todo 考虑移到setting里
    # 16位音频格式、单声道、采样率、每个数据块包含的帧数
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    # 读取系统设置，快捷键
    settings = setting().get('STT')
    hotkey = settings['hotkey']

    # 录音输入
    def hotkey_to_record():

        nonlocal user_messsage, exit_program

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
                            with input_lock:
                                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
                                    wave_file = wave.open(tmpfile.name, 'wb')
                                    wave_file.setnchannels(CHANNELS)
                                    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
                                    wave_file.setframerate(RATE)
                                    wave_file.writeframes(b''.join(frames))
                                    wave_file.close()
                                    # 语音转文字
                                    user_messsage = core.transcribe_audio(tmpfile.name)
                                print('语音转文本:', user_messsage)
                                # 解除进程锁，标记录音完成
                                recording_complete.set()

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
        
        

    # 文本输入
    def listen_for_text():
        # 监听用户输入的文本
        nonlocal user_messsage, exit_program
        while not exit_program:
            # 使用 keyboard 监听实时输入
            user_input = input()
            # 可输入exit退出
            if user_input.lower() == 'exit':
                exit_program = True
                break
            with input_lock:
                user_messsage = user_input
                print('用户输入:', user_messsage)
                # 解除进程锁，标记文本输入完成
                recording_complete.set()

    # 开始监听进程
    threading.Thread(target=hotkey_to_record, daemon=True).start()
    threading.Thread(target=listen_for_text, daemon=True).start()

    # 开始
    while not exit_program:
        user_messsage = ''
        print('输入文本或按下', hotkey, '开始语音输入')
        # 进程锁
        recording_complete.wait()
        recording_complete.clear()

        # 可输入exit退出
        if user_messsage.lower() == 'exit':
            print('退出程序')
            break

        # 模型生成响应
        new_message, history = core.generate_response(history, user_messsage)
        print('大模型回复:', new_message)

        # 文本转语音并播放
        core.synthesize_and_play(new_message)
        print('语音播放完成。')

        # 执行命令
        core.system_control(new_message)
        print('指令执行完毕')

# 运行程序
if __name__ == '__main__':
    main()
