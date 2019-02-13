import json
import os

PATH = os.path.join(os.path.dirname(__file__), '../config.json')

class Config:
    '''配置文件'''
    config_file = ""
    def __init__(self,path):
        '''@path：配置文件路径'''
        self.path = path
        with open(path, 'r') as f:
            config_file = f.read(-1)
            config_dict = json.loads(config_file)
        for k, v in config_dict.items():
            self.k = v
    
    def save(self):
        with open(self.path, 'w') as f:
            data = json.dumps(self.__dict__)
            f.write(data)
