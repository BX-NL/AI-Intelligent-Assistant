from transformers import AutoTokenizer, AutoModel
from cpm_kernels.kernels.base import round_up
import time
import config

class Model():
    def __init__(self):
        # 系统设置
        self.setting = config.setting()
        # 本地模型路径
        model_path = self.setting.model('model_path')
        # 预设的提示词
        self.prompt = self.setting.model('prompt')
        # tokenizer.py，原理暂不明确
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        # int4量化测试可用
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(bits=4, device="cuda").cuda().eval()
        # 完整部署
        # model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        # 多显卡环境下部署
        # model = AutoModel.from_pretrained(model_path, trust_remote_code=True, device_map="auto").quantize(bits=8, device="cuda").cuda().eval()

    def in_prompt(self):
        print('提示词注入中')
        # 记录推理时间
        start_time = time.time()
        # 注入提示词
        response, history = self.model.chat(self.tokenizer, self.prompt, history=[])
        # 输出问候语
        print(response)
        print('用时', time.time()-start_time, '秒')
        return history

    def generate(self, history, text):
        print('推理中')
        # 记录推理时间
        start_time = time.time()
        # 传入用户输入的文本并获取回复
        response, history = self.model.chat(self.tokenizer, text, history=history)
        # print(response)
        print('用时', time.time()-start_time, '秒')
        return response, history
    
if __name__ == '__mian__':
    pass