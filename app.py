from flask import Flask, render_template, request, jsonify
import threading
import pyaudio
import keyboard
from core import Core
from stt import STT
import tempfile
import wave

app = Flask(__name__)

# 初始化核心模块
core = Core()
stt = STT()  # 必须初始化，否则无法运行
audio = pyaudio.PyAudio()

# 全局变量
history = core.get_in_prompt()  # 初始化 history
input_lock = threading.Lock()
recording_complete = threading.Event()

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# 处理用户输入
@app.route('/send_message', methods=['POST'])
def send_message():
    global history  # 使用全局的 history 变量
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

if __name__ == '__main__':
    app.run(debug=True)