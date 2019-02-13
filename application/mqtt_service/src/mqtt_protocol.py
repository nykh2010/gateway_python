from socket import *
import json


class Protocol:
    def __init__(self, content):
        '''拆包'''
        c_dict = json.loads(content)
        print(c_dict['server'])
        if 'server' in c_dict:
            for k,v in c_dict['server'].items():
                self.__setattr__(k,v)
    
    def handler(self):
        if self.method == 'update-photo':
            return self.update_photo()

    def update_photo(self):
        '''更新图片'''
        pass