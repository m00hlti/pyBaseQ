
class Plugin_Base:
    name = ""

    def __init__(self, config):
        name = config['name']

    def process(self):
        print("base process")
        