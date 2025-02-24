import os
import time
from core import Core

def print_welcome():
    pass

def main():
    print('系统初始化')
    core = Core()  # 初始化核心模块
    print('大模型初始化完成')
    history = core.get_in_prompt()
    while True:
        frames = core.record_audio()
        if frames:
            print('录音完成')
        text = core.transcribe_audio(frames)
        if text:
            print('语音转文字完成')
            print(text)
        response = core.generate_response(text, history)
        if response:
            print('大模型回复完成')
            print(response)
        core.synthesize_and_play(response)

if __name__ == "__main__":
    main()