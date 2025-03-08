import re
import os
import time
import pyautogui


class Control:
    def __init__(self):
        self.list = {'浏览器': 'Microsoft Edge', }
        pass

    def extract_message(self, response_text):

        # 提取 type
        type_pattern = r'\[(.*?)\]'
        type_match = re.search(type_pattern, response_text)
        if type_match:
            type = type_match.group(1)
        else:
            type = 'ERROR'

        # 提取 message
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
            if message[0:2] == '打开':
                # 字符串切片获取目标程序
                file_name = message[2:-1]
                # 搜寻目标程序对应的文件名
                try:
                    if file_name in self.list:
                        file_name = self.list[file_name]
                        file_name += '.lnk'
                except:
                    pass
                
                # 生成文件路径
                file_path = os.path.join('C:\ProgramData\Microsoft\Windows\Start Menu\Programs', file_name)
                # 启动程序
                os.startfile(file_path)

        elif type == '文本':
            pyautogui.typewrite(message=message, interval=0.1)


if __name__ == '__main__':
    control = Control()
    response_text = '[文本]This is an test message!'
    response_text = '[指令]打开浏览器。'
    type, message = control.extract_message(response_text)
    control.device_control(type, message)
