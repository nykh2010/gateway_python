import paho.mqtt.client as mqtt
import json
import uuid

URL = 'localhost'

# 
test_msg = {"server":{
            "method":"update-photo",
            "id":str(uuid.uuid1()),
            "url":"http://106.12.220.232/test.bmp",
            "list":[0,1,2,3,4,5,6]
            }
        }

class MyMqtt(mqtt.Client):
    '''上行连接'''
    queue = None
    def on_connect(self,client,userdata,flags,rc):
        print("connected with result code", str(rc))
        self.subscribe("test")
        msg = test_msg
        print("dict msg: ",msg)
        content = json.dumps(msg)
        print(content)
        self.publish('test1', content)
    
    def on_message(self,client,userdata,msg):
        msg_content = msg.payload.decode('utf-8')
        print(msg.topic+" "+msg_content)
        self.queue.put_nowait(msg_content)      # 推送至协议处理单元
    
    def on_disconnect(self, client, userdata, rc):
        self.connect(URL)
    
    def on_publish(self, client, userdata, mid):
        print("publish success")

    def send(self, msg):
        '''发布消息，向服务端推送'''
        self.publish('test1',msg)

if __name__ == "__main__":
    client = MyMqtt()
    client.connect(URL)
    client.loop_forever()
    