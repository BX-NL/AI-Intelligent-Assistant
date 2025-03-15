import yaml


class setting():
    def __init__(self):
        with open('./setting.yaml', 'r', encoding='utf-8') as f:
            self.setting = yaml.load(f.read(), Loader=yaml.FullLoader)
        pass

    def main(self, key):
        return (self.setting[key])

    def model(self, key):
        return (self.setting[key])

    def TTS(self, key):
        pass

    def STT(self, key):
        return (self.setting[key])
        pass


class debug():
    def __init__(self):
        pass


if __name__ == '__main__':
    # demo demo
    key = 'prompt'
    print(setting().main(key))
