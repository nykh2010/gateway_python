import json
from socketserver import UDPServer, DatagramRequestHandler
import threading
from multiprocessing import Process
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config.json')
c_dict = {}
pid_list = []

def start_proc(path):
    print('start_proc', path)
    os.execl('/usr/bin/python', 'python', path)

def serviceStartHandler():
    '''服务启动线程'''
    for path in c_dict['service']:
        p = Process(target=start_proc, args=(path,))
        pid_list.append(p)
        p.start()
    for pid in pid_list:
        pid.join()

class SysServer(DatagramRequestHandler):
    '''消息处理'''
    def handle(self):
        data = self.rfile.read(-1)
        d_dict = json.loads(data)
        # 协议处理
        method = d_dict['systemservice']['method']
        if method == 'time':
            # 校时
            self.on_time(time=d_dict['systemservice']['time'])
        elif method == 'upgrade':
            # 升级
            url = None
            if 'url' in d_dict['systemservice']:
                url = d_dict['systemservice']['url']
            self.on_upgrade(url=url, restore=d_dict['systemservice']['restore'])
        elif method == 'config':
            # 配置修改
            pass
        elif method == 'restart':
            pass
        else:
            raise NameError()
    
    def finish(self):
        pass
    
    def on_time(self, time):
        '''@time: 校时时间'''
        pass

    def on_upgrade(self, url=None, restore=False):
        '''
        @url: 固件源位置
        @restore: 
        '''
        if url:
            # 将固件下载至指定位置
            os.system('wget %s -O %s' % (url, c_dict['systemconfig']['FIRMWARE_PATH']))
        pass

if __name__ == "__main__":
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = f.read(-1)
            c_dict = json.loads(config)
            SYSPORT = c_dict['systemconfig']['SYSPORT']
            SYSIP = c_dict['systemconfig']['SYSIP']
    except:
        SYSIP = 'localhost'
        SYSPORT = 9002
    # 创建服务启动线程
    serviceStartThread = threading.Thread(target=serviceStartHandler,name='serviceStartHandler')
    sysserver = UDPServer((SYSIP,SYSPORT), SysServer)

    serviceStartThread.start()
    sysserver.serve_forever()
    
