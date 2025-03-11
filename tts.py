import edge_tts
import asyncio
import io
import time
from playsound import playsound
import tempfile

class TTS:
    def __init__(self):
        # 默认音色
        self.voice = 'zh-CN-XiaoxiaoNeural'
        # 默认语速
        self.rate = '+0%'

    # 文本转语音，异步
    async def synthesize(self, text):
        # 大陆内使用EdgeTTS需要代理，请设置
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            proxy='http://127.0.0.1:7890'
        )

        # 将音频数据保存到内存中
        audio_data = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.write(chunk["data"])
        
        stream = audio_data.getvalue()

        return stream

    def synthesize_and_play(self, text):
        # 异步合成语音
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_data = loop.run_until_complete(self.synthesize(text))

        # 将音频数据保存到临时文件
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmpfile:
            tmpfile.write(audio_data)
            tmpfile_path = tmpfile.name
            # 等待0.5秒避免文件未写入完成
            time.sleep(0.5)

        # 使用 playsound 播放音频
        # 可换pygame库避免临时文件
        playsound(tmpfile_path)