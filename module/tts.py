import edge_tts
import asyncio
import io
import time
from playsound import playsound
import tempfile
import os
import sys

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录
work_dir = os.path.dirname(current_dir)
# 将项目根目录添加到sys.path
sys.path.append(work_dir)
# 导入模块
from module.config import setting

class TTS:
    def __init__(self):
        # 读取系统设置
        self.settings = setting().get('TTS')
        self.voice = self.settings['voice']
        self.proxy = self.settings['proxy']

    # 文本转语音，异步
    async def synthesize(self, text):
        # 大陆内使用EdgeTTS需要代理，请设置
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            proxy=self.proxy
        )

        # 将音频数据保存到内存中
        audio_data = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.write(chunk["data"])

        stream = audio_data.getvalue()

        return stream

    def synthesize_and_play(self, text):
        # 合成语音时去除回复类型
        if '[' in text or ']' in text:
            text = text[4:]

        # 异步合成语音
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # audio_data = loop.run_until_complete(self.synthesize(text))

        audio_data = asyncio.run(self.synthesize(text))

        # 将音频数据保存到临时文件
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmpfile:
            tmpfile.write(audio_data)
            tmpfile_path = tmpfile.name
            # 等待0.5秒避免文件未写入完成
            time.sleep(0.5)

        # 使用 playsound 播放音频
        # 可换pygame库避免临时文件
        playsound(tmpfile_path)

def debug():
    tts = TTS()
    text = input('input:')
    tts.synthesize_and_play(text)
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

    app = FastAPI()
    # 创建 TTS 实例
    tts = TTS()

    @app.post("/tts")
    async def synthesize_and_play_api(request: TTSRequest):
        try:
            text = request.text
            # 合成语音时去除回复类型
            if '[' in text or ']' in text:
                text = text[4:]
            # 异步合成语音
            audio_data = await tts.synthesize(text)
            # todo 为了分布式进行的妥协，后续尝试不用playsound，异步套异步会报错
            # 将音频数据保存到临时文件
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmpfile:
                tmpfile.write(audio_data)
                tmpfile_path = tmpfile.name
                # 等待0.5秒避免文件未写入完成
                time.sleep(0.5)

            # 使用 playsound 播放音频
            playsound(tmpfile_path)
            return {'message': '语音播放成功'}
        except Exception:
            raise HTTPException(status_code=500, detail=str(Exception))
    
    @app.get('/tts/status')
    async def static():
        return status.HTTP_200_OK

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=port)

if __name__ == '__main__':
    if True:
        api()
    else:
        debug()