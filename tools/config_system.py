import json
import os
import uuid
from time import time

PATH = os.path.join(os.path.dirname(__file__), '../default_config.json')

config_content = {
    'gateway':{
        'id':str(uuid.uuid1()),
        'mac':str(uuid.uuid1()).split('-')[-1],
        'key':str(uuid.uuid4()).split('-')[-1],
    },
    'firmware':{
        'version':'v1.2'
    },
    'auth':{
        'username':'admin',      # 加密存储?
        'passwd':'Boe888888'
    },
    'radio':{
        'key':str(uuid.uuid4()),
        # 'mode':0,               # Lora模式
        'mode':1,               # FSK模式
        'preamble':2346,        # 前导码
        'sf':7,                 # 扩频因子
        'bw':10.4,              # 带宽
        'cr':"4/6",               # 编码率
        'frequency':433,        # 频点
        'crc':True,             # crc使能
        'power':17,             # 功率
        'sync':hex(65535),      # 同步字
    },
    'server':{
        'host':'127.0.0.1',
        'port':'1883',
        'auth_key':'',
        'wireless':False,
        'ssid':'',
        'passwd':''
    },
    'wifi':{
        'enable':False,
        'ssid':'360',
        'lbl':'3',           # 验证方式 0：无 3：WPA2-PSK AES 4: WPA/WPA2-PSK AES
        'passwd': 'Boe888888',
    }
}

with open(PATH, 'w') as f:
    data = json.dumps(config_content, indent=4)
    print(data)
    print(PATH)
    f.write(data)
