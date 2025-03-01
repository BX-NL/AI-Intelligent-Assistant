from transformers import AutoTokenizer, AutoModel
from cpm_kernels.kernels.base import round_up
import time
import config

class model():
    def __init__(self):
        self.setting = config.setting()
        model_path = self.setting.model('model_path')
        self.prompt = self.setting.model('prompt')
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        # int4量化测试可用
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(bits=4, device="cuda").cuda().eval()
        # 完整部署
        # model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        # 多显卡环境下部署
        # model = AutoModel.from_pretrained(model_path, trust_remote_code=True, device_map="auto").quantize(bits=8, device="cuda").cuda().eval()

    def in_prompt(self):
        print('提示词注入中')
        start_time = time.time()
        response, history = self.model.chat(self.tokenizer, self.prompt, history=[])
        print(response)
        print('用时', time.time()-start_time, '秒')
        return history

    def start(self, text, history):
        print('推理中')
        start_time = time.time()
        response, history = self.model.chat(self.tokenizer, text, history=history)
        # print(response)
        print('用时', time.time()-start_time, '秒')
        return response, history