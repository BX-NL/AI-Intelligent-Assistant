import re
import os
import time
import pyautogui


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

        # 提取type
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
                    pass
            # 启动程序
            os.startfile(file_path)

        elif type == '文本':
            pyautogui.typewrite(message=message, interval=0.1)

        elif type == 'ERROR':
            print('回复文本不符合格式，请检查大模型。')
        
        else:
            print('文本错误')


if __name__ == '__main__':
    control = Control()
    response_text = '[文本]This is an test message!'
    response_text = '[指令]启动浏览器'
    type, message = control.extract_message(response_text)
    print(type, message)
    control.device_control(type, message)
