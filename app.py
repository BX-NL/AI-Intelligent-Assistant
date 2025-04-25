# import pyaudio
import tempfile
from flask import Flask, render_template, request, jsonify
from module.core import Core
# import base64
# 创建Flask应用
app = Flask(__name__)

# 初始化核心模块
core = Core()
# 初始化音频模块
# audio = pyaudio.PyAudio()

# 初始化 history
history = core.get_in_prompt()

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

    # 生成响应
    response_text, history = core.generate_response(history, user_input)
    # todo 尝试修改为先返回再播放
    audio_data_base64 = core.synthesize(response_text)
    # ! 这行好像用不了
    # core.system_control(response_text)

    return jsonify({'response': response_text, 'audio': audio_data_base64})


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
    app.run(debug=False, host='0.0.0.0')

# todo 需要语音中断功能