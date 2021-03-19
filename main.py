import json
from plugins import plugin_mysql


def load_configfile():
    '''
    Load the main config file for the whole backup system
    '''
    with open('config.json') as config_file:
        data = json.load(config_file)
    return data

def load_plugins():
    '''
    Load the config file for any plugins configured
    '''
    with open('plugins.json') as config_file:
        data = json.load(config_file)
    return data

def run_backup():
    '''
    This is for the moment the main application point
    '''
    config = load_configfile()
    print("Loaded config. TestValue: ", config['test']," BackupFolder: ", config['targetfolder'])
    
    plugins = load_plugins()

    # MYSQL 
    if "mysql" in plugins:
        print("Plugin: ", plugins['mysql']['name'], " active.")

        mysql = plugin_mysql.Plugin_MYSQL(plugins['mysql'])
        mysql.process()
    
    # TS3
    if "ts3" in plugins:
        print("Module: ", plugins['ts3']['name'], " active.")




if __name__ == "__main__":
    run_backup();
    
