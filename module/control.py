import re
import os
import sys
import pyautogui

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录
work_dir = os.path.dirname(current_dir)
# 将项目根目录添加到sys.path
sys.path.append(work_dir)
# 导入模块
from module.config import setting

class Control:
    def __init__(self):
        # 系统开始菜单快捷方式
        self.list_sys = {'浏览器': 'Microsoft Edge', }
        # 获取用户名
        self.username = os.environ.get('USERNAME')
        # 用户开始菜单快捷方式
        self.list_usr = {'Onedrive': 'OneDrive - Personal', }
        # 自定义路径
        self.list_cus = {'test': 'testtest', }
        pass

    def extract_message(self, response_text):

        # 正则表达式提取type
        type_pattern = r'\[(.*?)\]'
        type_match = re.search(type_pattern, response_text)
        if type_match:
            type = type_match.group(1)
        else:
            type = 'ERROR'

        # 提取message
        message_pattern = r'\]\s*(.*)'
        message_match = re.search(message_pattern, response_text)
        if message_match:
            message = message_match.group(1)
        else:
            message = 'None'

        return type, message

    def device_control(self, type, message):
        # 分类文本类型
        if type == '对话':
            pass

        elif type == '指令':
            if message[0:2] == '启动':
                # 字符串切片获取目标程序
                file_name = message[2:]
                # 搜寻目标程序对应的文件名
                try:
                    if file_name in self.list_sys:
                        file_name = self.list_sys[file_name] + '.lnk'
                        # 生成文件路径
                        file_path = os.path.join('C:/ProgramData/Microsoft/Windows/Start Menu/Programs', file_name)
                    elif file_name in self.list_usr:
                        file_name = self.list_usr[file_name] + '.lnk'
                        # 生成文件路径
                        file_path = os.path.join(f'C:/Users/{self.username}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs', file_name)
                    elif file_name in self.list_cus:
                        file_name = self.list_cus[file_name] + '.lnk'
                        # 生成文件路径
                        file_path = os.path.join('../', file_name)
                    print(file_path)
                except:
                    print('ERROR')
            # 启动程序
            os.startfile(file_path)

        elif type == '文本':
            # 控制设备输入文本，暂时只支持Windows
            pyautogui.typewrite(message=message, interval=0.1)

        elif type == 'ERROR':
            print('回复文本不符合格式，请检查大模型。')

        else:
            print('文本错误')

def debug():
    control = Control()
    response_text = '[文本]This is an test message!'
    response_text = '[指令]启动浏览器'
    type, message = control.extract_message(response_text)
    print(type, message)
    control.device_control(type, message)

def api():
    from fastapi import FastAPI, HTTPException, status
    from pydantic import BaseModel

    # 读取系统设置
    settings = setting().get('control')
    port = settings['port']

    # 定义请求体模型
    class ModelRequest(BaseModel):
        text: str

    # 创建FastAPI应用
    app = FastAPI()
    # 创建Control实例
    control = Control()

    # 分布式
    @app.post('/control')
    async def device_control_api(request: ModelRequest):
        try:
            text = request.text
            # 获取文本类型和信息
            type, message = control.extract_message(text)
            # 控制设备
            control.device_control(type, message)
            return {'type': type, 'message': message}

        except Exception:
            raise HTTPException(status_code=500, detail=str(Exception))

    # 模块状态
    @app.get('/control/status')
    async def get_status():
        return status.HTTP_200_OK

    # 启动服务
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    if True:
        api()
    else:
        debug()
