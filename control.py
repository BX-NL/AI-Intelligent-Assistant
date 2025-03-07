import re
import os
import time
import pyautogui


def extract_message(response_text):

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


def device_control(type, message):
    if type == '对话':
        pass
    elif type == '指令':
        if message[0:2] == '打开':
            file_name = message[2:-1] + '.lnk'
            if file_name == '浏览器.lnk': file_name = 'Microsoft Edge.lnk'
            # print(file_name)
            file_path = os.path.join('C:\ProgramData\Microsoft\Windows\Start Menu\Programs', file_name)
            os.startfile(file_path)
        pass
    elif type == '文本':
        pyautogui.typewrite(message=message, interval=0.1)


if __name__ == '__main__':
    response_text = '[文本] This is an test message!'
    response_text = '[指令]打开浏览器。'
    type, message = extract_message(response_text)
    device_control(type, message)
