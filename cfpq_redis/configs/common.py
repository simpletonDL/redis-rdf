import os
from configparser import ConfigParser


class Config:
    def __init__(self, conf_path):
        conf_parser = ConfigParser()
        conf_parser.read(conf_path)

        self.redis_path: str = conf_parser.get('common', 'redis_path')
        self.redis_dumps_path: str = conf_parser.get('common', 'redis_dumps_path')
        self.cfpq_data_path: str = conf_parser.get('common', 'CFPQ_Data_path')

        self.redis_bin: str = os.path.join(self.redis_path, 'src', 'redis-server')
        self.redis_conf: str = os.path.join(self.redis_path, 'redis.conf')
