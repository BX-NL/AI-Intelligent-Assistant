from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_audio", methods=["POST"])
def send_audio():
    audio_data = request.files["audio_data"].read()
    
    # 将音频数据发送到核心模块进行处理
    response = requests.post("http://localhost:8000/process_input", files={"audio_data": audio_data})
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to process audio"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)