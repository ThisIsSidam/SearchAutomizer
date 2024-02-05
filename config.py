import configparser
import os


CONFIG_FILE = "config.ini"

def read_config():
    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        loop_count = config.get('UserSettings', 'iterations')
        return loop_count
    else: 
        return 0
    
def write_config(loop_count):
    config = configparser.ConfigParser()
    config['UserSettings'] = {'iterations': loop_count}

    with open(CONFIG_FILE, 'w') as config_file:
        config.write(config_file)


