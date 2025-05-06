# import pyaudio
import tempfile
import logging
# import colorlog
from flask import Flask, render_template, request, jsonify
from module.core import Core

# logging配置
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 初始化核心模块
core = Core()

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
    # 获取用户输入的文本
    user_input = data.get('message')

    # 生成响应
    response_text, history = core.generate_response(history, user_input)
    # 生成音频数据
    audio_data_base64 = core.synthesize(response_text)
    # 发送系统控制指令
    # ! 这行好像用不了
    # core.system_control(response_text)

    # 返回音频数据的base64
    # todo 尝试异步，先返回再发送系统控制命令
    return jsonify({'response': response_text, 'audio': audio_data_base64})


# ! 好像录音按钮有bug，有空再改
# 处理音频上传
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    # 判断是否录制成功
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    # 获取录制的音频文件
    audio_file = request.files['audio']
    # 音频数据保存至临时文件
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
        audio_file.save(tmpfile.name)
        # 调用语音转文字
        # ? 这个name其实是完整路径
        text = core.transcribe_audio(tmpfile.name)
        # 返回识别到的文本
        return jsonify({'text': text})


# 获取模块状态
@app.route('/get_status', methods=['GET'])
def get_status():
    # 获取模块状态
    status_list = core.get_module_status()
    # todo 顺序好像有点问题，有空再改
    # 写入模块状态数据
    try:
        status = {
            '服务端': 'Local',
            '当前连接': 'Local',
            'Model': status_list[0],
            'STT': status_list[1],
            'TTS': status_list[2],
            'control': status_list[3],
        }
    # core那边try过了，这里可以不要
    except:
        logging.error('Some Module was not client')
    # 返回模块状态数据
    return jsonify(status)


if __name__ == '__main__':
    # ! 当debug =True时，各个模块会被实例化两次，暂不影响使用，实际部署时可改为False
    app.run(debug=False, host='0.0.0.0')

# todo 需要语音中断功能