import json
from socket import *
import uuid

tsock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
tsock.bind(('0.0.0.0',0))

# s_dict = {
#     'dbservice':{
#         'name':__file__,
#         'method':'add',
#         'tableName':'terminal',
#         'args':{
#             'id':str(uuid.uuid1()),
#             'type':0,
#             'ver':"version 1.0"
#         }
#     }
# }
# s_dict = {
#     'dbservice':{
#         'name':__file__,
#         'method':'delete',
#         'tableName':'terminal',
#         'args':{
#             # 'id':str(uuid.uuid1()),
#             'type':0,
#             'ver':"version 1.0",
#             'status':0
#         }
#     }
# }
s_dict = {
    'dbservice':{
        'name':__file__,
        'method':'query',
        'tableName':'terminal',
        'id':"3f8b23b6-189a-11e9-a4a4-4c0bbe2d8ca1"
    }
}

content = json.dumps(s_dict)
tsock.sendto(content.encode('utf-8'),('localhost',9000))

try:
    while True:
        data, address = tsock.recvfrom(1024)
        if data:
            print(data)
            break
except Exception as e:
    print(e)
    exit(0)
