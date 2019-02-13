import json
import os
import uuid

'''配置文件生成'''

gateway_id = uuid.getnode()
local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
DBSERVICE = os.path.join(local_path, 'dbservice/dbservice.py')
LOGSERVICE = os.path.join(local_path, 'logservice/bin/loger.py')
SYSSERVICE = os.path.join(local_path, 'systemservice/sysservice.py')
WEBSERVICE = os.path.join(local_path, 'webservice/app/server.py')
UPLINKSERVICE = os.path.join(local_path, 'application/mqtt_service/src/mqtt_client.py')


config = {
    # 服务列表
    'service': [
        DBSERVICE,
        LOGSERVICE,
        # SYSSERVICE,
        WEBSERVICE,
        UPLINKSERVICE
    ],
    # 网关基础配置
    'gateway': {
        'GATEWAYID': str(uuid.uuid1(gateway_id))
    },
    # 数据库服务配置
    'dbconfig': {
        'DBPORT': 9000,            # 服务端口
        'DBIP': 'locaservicelhost'         # 服务地址
    },
    # 日志服务配置service
    'logconfig': {
        'LOGPORT': 9001,            # 服务端口
        'LOGIP': 'locservicealhost',       # 服务地址
        'OUT': 'stdouservicet',            # 输出位置
        'PRIORITY': 'INFO',              # 输出优先级
        'PACKAGE_INTERVAL': 1,      # 日志打包周期（天）
        'LOGFILE_FOLDER': os.path.join(os.path.dirname(LOGSERVICE), 'log')   # 输出日志目录
    },
    # 系统服务配置
    'systemconfig': {
        'SYSPORT': 9002,            # 系统服务端口
        'SYSIP': 'localhost',        # 系统服务IP
        'FIRMWARE_PATH': os.path.dirname(SYSSERVICE)  # 固件保存目录
    },
    # web服务配置
    'webconfig': {
        'WEBPORT': 8080,             # 服务端口
        'WEBIP': '0.0.0.0',         # 服务地址
        'ACCOUNT': {'USERNAME':'admin','PASSWD':'admin'}    # 默认登录用户名与密码
    },
    # 上行服务配置
    'uplinkconfig': {
        'MQTT_PORT': 1883,          # mqtt端口
        'MQTT_HOST': 'localhost',   # mqtt地址
        'UPLINK_IP': 'localhost',   # 上行服务端口
        'UPLINK_PORT': 9003
    }
}

try:
    path = os.path.join('config.json')
    with open(path,'w') as f:
        str = json.dumps(config, indent=4) 
        print(str)
        f.write(str)
except Exception as e:
    print(e)