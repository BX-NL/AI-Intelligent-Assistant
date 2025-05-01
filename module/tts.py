import io
import os
import sys
import base64
import asyncio
import edge_tts
import logging
# import colorlog

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录
work_dir = os.path.dirname(current_dir)
# 将项目根目录添加到sys.path
sys.path.append(work_dir)
# 导入模块
from module.config import setting

# logging配置
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TTS:
    def __init__(self):
        # 读取系统设置
        self.settings = setting().get('TTS')
        self.voice = self.settings['voice']
        self.proxy = self.settings['proxy']

    # 文本转语音，异步
    async def synthesize(self, text):
        # 大陆内使用EdgeTTS需要代理，需要修改设置
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            proxy=self.proxy
        )

        # 将音频数据保存到内存中
        audio_data = io.BytesIO()
        # 音频帧合成音频流
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.write(chunk["data"])

        # 获取音频数据
        stream = audio_data.getvalue()
        # 返回音频数据
        return stream

    # todo 整不明白异步，临时使用这个转回同步来使用
    def synthesize_and_play(self, text):
        # 合成语音时去除回复类型
        if '[' in text or ']' in text:
            text = text[4:]

        # 异步合成语音，异步套异步会炸，先用着下面那种
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # audio_data = loop.run_until_complete(self.synthesize(text))

        # 异步合成语音
        audio_data = asyncio.run(self.synthesize(text))
        # 将音频数据转为base64编码
        audio_data_base64 = base64.b64encode(audio_data).decode('utf-8')
        # 返回音频数据
        return audio_data_base64

def debug():
    tts = TTS()
    text = input('input:')
    audio_data_base64 = tts.synthesize_and_play(text)
    print(audio_data_base64)
    print('output sucess')

def api():
    from fastapi import FastAPI, HTTPException, status
    from pydantic import BaseModel

    # 读取系统设置
    settings = setting().get('TTS')
    port = settings['port']

    # 定义请求体模型
    class TTSRequest(BaseModel):
        text: str

    # 创建FastAPI应用
    app = FastAPI()
    # 创建TTS实例
    tts = TTS()

    # 分布式
    @app.post("/tts")
    async def synthesize_and_play_api(request: TTSRequest):
        try:
            # 获取传入的文本
            text = request.text
            # 合成语音时去除回复类型
            if '[' in text or ']' in text:
                text = text[4:]
            # 异步合成语音
            audio_data = await tts.synthesize(text)
            # 将音频数据转为base64编码
            audio_data_base64 = base64.b64encode(audio_data).decode('utf-8')
            # 返回音频数据
            return {'audio': audio_data_base64}

        except Exception:
            raise HTTPException(status_code=500, detail=str(Exception))

    # 模块状态
    @app.get('/tts/status')
    async def static():
        return status.HTTP_200_OK

    # 启动服务
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    if True:
        api()
    else:
        debug()