import yaml


class setting():
    def __init__(self):
        with open('./setting.yaml', 'r', encoding='utf-8') as file:
            self.setting = yaml.load(file.read(), Loader=yaml.FullLoader)
            file.close()
        pass


    def get(self, key):
        return (self.setting[key])


class debug():
    def __init__(self):
        pass


if __name__ == '__main__':
    # demo demo
    key = 'debug'
    print(setting().get(key))
