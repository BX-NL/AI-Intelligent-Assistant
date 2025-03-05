import re

def extract_message(response_text):

    # response_text = "[test] This is an test message!"

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

def device_Control(type, message):
    pass