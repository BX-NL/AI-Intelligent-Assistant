from flask import Flask, render_template, request, jsonify
import threading
import pyaudio
# import keyboard
from module.core import Core
# from module.stt import STT
# from module.tts import TTS
# from module.config import setting
# from module.control import Control
import tempfile
# import wave

# 创建Flask应用
app = Flask(__name__)

# 初始化核心模块
core = Core()
# 初始化音频模块
audio = pyaudio.PyAudio()

# 初始化 history
history = core.get_in_prompt()
# 忘记用来做什么的了，先留个注释
# input_lock = threading.Lock()
# recording_complete = threading.Event()


# 首页路由
@app.route('/')
def home():
    return render_template('index.html')


# 聊天页面路由
@app.route('/chat')
def chat():
    return render_template('chat.html')


# 处理用户输入
@app.route('/send_message', methods=['POST'])
def send_message():
    # 使用全局的 history 变量
    global history
    # 获取用户输入
    data = request.json
    user_input = data.get('message')

    if user_input.lower() == 'exit':
        return jsonify({'response': '会话已结束'})

    # 生成响应
    response_text, history = core.generate_response(history, user_input)
    # todo 尝试修改为先返回再播放
    core.synthesize_and_play(response_text)
    # ! 这行好像用不了
    # core.system_control(response_text)

    return jsonify({'response': response_text})


# 处理音频上传
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio_file = request.files['audio']
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
        audio_file.save(tmpfile.name)
        # 调用语音转文字
        text = core.transcribe_audio(tmpfile.name)
        return jsonify({'text': text})


# 获取模块状态
@app.route('/get_status', methods=['GET'])
def get_status():
    # 获取模块状态
    status_list = core.get_module_status()
    # todo 顺序好像有点问题，有空再改
    status = {
        '服务端': 'Local',
        '当前连接': 'Local',
        'Model': status_list[0],
        'STT': status_list[1],
        'TTS': status_list[2],
        'control': status_list[3],
    }
    return jsonify(status)


if __name__ == '__main__':
    # ! 当debug =True时，各个模块会被实例化两次，暂不影响使用，实际部署时可改为False
    app.run(debug=True, host='0.0.0.0')
