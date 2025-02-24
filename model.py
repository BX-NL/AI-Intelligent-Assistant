from transformers import AutoModel, AutoTokenizer

class Model:
    def __init__(self):
        model_path = 'D:\ChatGLM3\THUDM\chatglm3-6b'
        # 加载本地部署的ChatGLM3-6b模型
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(bits=4, device="cuda").cuda().eval()

    def generate_response(self, input_text):
        # 将输入文本编码为模型输入
        inputs = self.tokenizer(input_text, return_tensors="pt")
        
        # 生成响应
        outputs = self.model.generate(**inputs)
        
        # 将模型输出解码为文本
        response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return response_text