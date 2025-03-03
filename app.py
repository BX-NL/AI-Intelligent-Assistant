from flask import Flask, render_template, request, jsonify
from core import Core
import base64
import wave
import io

app = Flask(__name__)

# 初始化核心模块
core = Core()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    audio_data = data.get('audio_data')

    if audio_data:
        # 解码音频数据
        audio_bytes = base64.b64decode(audio_data.split(',')[1])
        # 将音频数据保存为临时文件
        with io.BytesIO(audio_bytes) as audio_file:
            with wave.open(audio_file, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio_file.read())
            # 语音转文字
            user_input = core.transcribe_audio(audio_file.getvalue())

    # 生成响应
    history = core.get_in_prompt()
    response_text = core.generate_response(history, user_input)

    # 语音播放
    core.synthesize_and_play(response_text)

    return jsonify({
        'user_input': user_input,
        'response': response_text
    })

if __name__ == '__main__':
    app.run(debug=True)