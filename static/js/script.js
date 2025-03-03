document.addEventListener('DOMContentLoaded', function () {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const voiceBtn = document.getElementById('voice-btn');

    let mediaRecorder;
    let audioChunks = [];

    // 初始化录音功能
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = () => {
                    const base64Audio = reader.result;
                    sendMessage('', true, base64Audio);
                };
                audioChunks = [];
            };
        })
        .catch(error => {
            console.error('无法访问麦克风:', error);
        });

    // 发送文本消息
    sendBtn.addEventListener('click', function () {
        const message = userInput.value.trim();
        if (message) {
            sendMessage(message, false);
            userInput.value = '';
        }
    });

    // 发送语音消息
    voiceBtn.addEventListener('click', function () {
        if (mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            voiceBtn.textContent = '🎤';
        } else {
            audioChunks = [];
            mediaRecorder.start();
            voiceBtn.textContent = '⏹';
        }
    });

    // 发送消息到后端
    function sendMessage(message, isVoice, audioData = null) {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                is_voice: isVoice,
                audio_data: audioData
            }),
        })
        .then(response => response.json())
        .then(data => {
            addMessageToHistory('user', isVoice ? '语音输入' : data.user_input);
            addMessageToHistory('assistant', data.response);
        });
    }

    // 添加消息到聊天记录
    function addMessageToHistory(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        messageDiv.textContent = content;
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});