import logging
import json
from socketserver import UDPServer,DatagramRequestHandler
from queue import Queue
import os
import time

'''
@protocol
@json
{
    'name':name,
    'method':write/read/zip,
    'time':time,
    'priority':TRACE/WARNING/ERROR,
    'content':str
}
'''

PATH = os.path.join(os.path.dirname(__file__), '../../config.json')
# print(PATH)
LOGFOLDER = ""
LOGLEVEL = ""

class LoggerInstance(object):
    '''日志服务实例'''
    def __init__(self,name,tm):
        '''
        @name:日志名称
        @tm：时间
        '''
        self.name = name
        self.time = tm
        
        # 判断是否存在相同文件名
        self.logger = logging.getLogger(name=name)
        self.logger.setLevel(LOGLEVEL)
        self.handler = logging.FileHandler(os.path.join(LOGFOLDER,self.name))
        fmt = logging.Formatter('[%(levelname)s]:%(message)s')
        self.handler.setFormatter(fmt)
        self.logger.addHandler(self.handler)

    def __del__(self):
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

    def write_log_file(self,logtm,prio,content):
        '''
        @logtm：日志产生时间
        @prio：日志优先级
        @content：日志内容
        '''
        if prio == 'INFO':
            self.logger.info("%s - %s",logtm,content)
        elif prio == 'WARNING':
            self.logger.warning("%s - %s",logtm,content)
        elif prio == 'FATAL':
            self.logger.fatal("%s - %s",logtm,content)
        else:
            pass
    def get_log_file(self):
        '''获取对应日志文件'''
        pass
    def zip_log_file(self):
        '''日志打包'''
        pass
    def del_log_file(self):
        '''日志删除'''
        pass

class LogRequestHandler(DatagramRequestHandler):
    '''日志服务处理流程'''
    def handle(self):
        try:
            data = self.rfile.getvalue()
            data = data.decode('utf-8')
            log_record = json.loads(data)
            logger_instance = LoggerInstance(log_record['name'],log_record['time'])
            if (log_record['method'] == 'write'):
                # 写日志
                logger_instance.write_log_file(
                    log_record['time'],
                    log_record['priority'],
                    log_record['content']
                )
            elif (log_record['method'] == 'zip'):
                # 日志打包
                logger_instance.zip_log_file()
                pass
            elif (log_record['method'] == 'create'):
                # 创建日志
                pass
            self.wfile.write('status:ok'.encode())
        except Exception as e:
            self.wfile.write(('status:%s' % e.__repr__()).encode())

class LogService(UDPServer):
    '''
    日志服务
    '''
    def __init__(self,path):
        '''
        @解析配置文件
        @path配置文件路径
        '''
        global LOGFOLDER
        global LOGLEVEL
        try:
            with open(PATH,"r+") as f:
                self.config = json.loads(f.read(-1))
                server_address = (self.config['logconfig']['LOGIP'],self.config['logconfig']['LOGPORT'])    # 日志服务端口
                LOGFOLDER = os.path.join(os.pardir,self.config['logconfig']['LOGFILE_FOLDER']) # 日志保存位置
                LOGLEVEL = self.config['logconfig']['PRIORITY']
                print(server_address)
                super().__init__(server_address,LogRequestHandler)
        except Exception as e:
            print(e)
            # exit()
    def start(self):
        print("log service start!")
        self.serve_forever()

if __name__ == "__main__":
    print('%s start...' % __file__)
    logService = LogService(PATH)
    # print(LOGFOLDER)
    logService.start()