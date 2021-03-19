from plugins import plugin_base

class Plugin_MYSQL(plugin_base.Plugin_Base):

    def __init__(self, config):
        super().__init__(config)
    
    def process(self):
        print("MySQL Plugin.")
