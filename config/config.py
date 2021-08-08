import os
import configparser
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('/ship_discovery_agent/env_vars.env')
load_dotenv(dotenv_path=dotenv_path)

class Config:
    def __init__(self):
        self.repeat_timer = os.environ.get('REPEAT_TIMER')
        self.conf_file_path = os.environ.get('CONF_FILE')
        self.conf_file_contents = self.read_config()

    def read_config(self):
        # open config file
        try:
            config = configparser.ConfigParser()
            config.read(self.conf_file_path)
            config.sections()
            return config
        except IOError:
            log.critical("*********** ERROR reading config file **********")
            exit(1)
