import paho.mqtt.client as mqtt
import json
import uuid
from mqtt_protocol import Protocol
import threading
from queue import Queue
from socket import *
import time
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../../config.json')
MQTT_HOST = None
MQTT_PORT = None

class MyMqtt(mqtt.Client):
    '''上行连接'''
    queue = None
    def on_connect(self,client,userdata,flags,rc):
        print("connected with result code", str(rc))
        self.subscribe("test1")
    
    def on_message(self,client,userdata,msg):
        msg_content = msg.payload.decode('utf-8')
        print(msg.topic+" "+msg_content)
        self.queue.put_nowait(msg_content)      # 推送至协议处理单元
    
    def on_disconnect(self, client, userdata, rc):
        self.connect(MQTT_HOST,MQTT_PORT)
    
    def on_publish(self, client, userdata, mid):
        pass

    def send(self, msg):
        '''发布消息，向服务端推送'''
        self.publish('test',msg)

class DownLink(socket):
    '''下行连接'''
    def __init__(self, *args, **kwargs):
        SOCK_IP = c_dict['uplinkconfig']['UPLINK_IP']
        SOCK_PORT = c_dict['uplinkconfig']['UPLINK_PORT']
        self.client = client        # 上行通道
        self.msg_queue = msg_queue
        super().__init__(AF_INET, SOCK_DGRAM, proto=IPPROTO_UDP)
        self.bind((SOCK_IP, SOCK_PORT))
        self.__hservice_recv = threading.Thread(target=self.service_recv, name="service_recv")
        self.__huplink_recv = threading.Thread(target=self.uplink_recv, name="uplink_recv")      

    def service_recv(self):
        '''接收来自其它服务的消息'''
        while True:
            data, address = self.recvfrom(1024)
            p = Protocol(data)      # 包解析
            ret = p.handler()       # 协议处理
            if ret:     # 有需要上传的数据
               self.client.send(ret)
            s_dict = {'status':'ok'}
            self.sendto(json.dumps(s_dict), address)
            print("service_recv")
    
    def uplink_recv(self):
        '''接收来自上行的消息'''
        while True:
            try:
                msg = self.msg_queue.get()       # 从消息队列中提取一个数据包
            except:
                continue
            p = Protocol(msg)
            data, address = p.handler()
            if data:
                self.sendto(data, address)          # 向其它服务发送消息
            print("uplink_recv")

    def loop_forever(self):
        self.__hservice_recv.start()
        self.__huplink_recv.start()

if __name__ == "__main__":
    print('%s start...' % __file__)
    # 获取配置文件
    try:
        with open(CONFIG_PATH,'r') as f:
            content = f.read(-1)
            c_dict = json.loads(content)
            MQTT_HOST = c_dict['uplinkconfig']['MQTT_HOST']
            MQTT_PORT = c_dict['uplinkconfig']['MQTT_PORT']
    except:
        print('appconfig read failed')
        exit(1)
    
    msg_queue = Queue()
    # 创建服务端连接
    client = MyMqtt(str(uuid.uuid1()))
    # 创建下行连接
    downlink = DownLink(c_dict, client, msg_queue)
    downlink.loop_forever()

    client.queue = msg_queue
    try:
        client.connect(MQTT_HOST,MQTT_PORT)
        client.loop_forever()
    except:
        client.disconnect()
    
