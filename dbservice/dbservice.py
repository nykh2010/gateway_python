from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from socketserver import UDPServer, DatagramRequestHandler
from usertable import Base, Terminal
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config.json')

DBPORT = 9000
DBIP = 'localhost'

Session = None

class ParamError(Exception):
    '''参数错误'''
    def __init__(self, code=400, msg="参数错误"):
        self.code = code
        self.msg = msg
        super().__init__(self, code, msg)

class DBServer(DatagramRequestHandler):
    '''数据库服务接口'''
    status_code = 200
    status_msg = ""
    status_result = None
    dbsession = None
    def protocol(self, content):
        '''协议处理'''
        session = Session()
        c = json.loads(content.decode('utf-8'))
        con = c['dbservice']
        if con['method'] == 'add':
            
            if con['tableName'] == 'terminal':
                
                try:
                    tstatus = None
                    tid = con['args']['id']
                    ttype = con['args']['type']
                    tver = con['args']['ver']
                    if 'status' in con['args']:
                        tstatus = con['args']['status']
                    terminal = Terminal(tid=tid, ttype=ttype, \
                                    tver=tver)
                    session.add(terminal)
                    session.commit()
                except Exception as e:
                    print(e)
                    raise ParamError()
        elif con['method'] == 'delete':
            
            terminals = []
            if 'id' in con['args']:
                
                terminals = session.query(Terminal).filter_by(tid=con['args']['id']).all()
            elif 'type' in con['args']:
                terminals = session.query(Terminal).filter_by(ttype=con['args']['type']).all()
            elif 'ver' in con['args']:
                terminals = session.query(Terminal).filter_by(ttype=con['args']['ver']).all()
            elif 'status' in con['args']:
                terminals = session.query(Terminal).filter_by(ttype=con['args']['status']).all()
            else:
                raise ParamError()
            print(terminals)
            for terminal in terminals:
                session.delete(terminal)
            session.commit()
        elif con['method'] == 'modify':
            
            if 'id' not in con:
                raise ParamError()
            terminal = session.query(Terminal).filter_by(tid=con['id']).first()
            if 'id' in con['args']:
                terminal.tid = con['args']['id']
            if 'type' in con['args']:
                terminal.ttype = con['args']['type']
            if 'ver' in con['args']:
                terminal.tver = con['args']['ver']
            if 'ver' in con['args']:
                terminal.tstatus = con['args']['status']
            session.commit()

        elif con['method'] == 'query':
            
            r_dict = {}
            terminals = session.query(Terminal).filter_by(tid=con['id']).first()
            print(type(terminals.__dict__))
            for k,v in terminals.__dict__.items():
                if k[0] == '_':
                    continue
                else:
                    r_dict[k] = v
            return r_dict

        else:
            raise ParamError()

    def handle(self):
        try:
            content = self.rfile.read(-1)
            print(content)
            self.status_result = self.protocol(content)
        except Exception as e:
            print(e)
            # self.status_code = e.code
            # self.status_msg = e.msg
        return
    
    def finish(self):
        r_dict = {
            'status':self.status_code,
            'msg':self.status_msg,
            'result':self.status_result
        }
        r = json.dumps(r_dict)
        self.wfile.write(r.encode('utf-8'))
        super().finish()

if __name__ == "__main__":
    print('%s start...' % __file__)
    
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = f.read(1024)
            c_dict = json.loads(config)
            DBPORT = c_dict['dbconfig']['DBPORT']
            DBIP = c_dict['dbconfig']['DBIP']
    except:
        DBIP = 'localhost'
        DBPORT = 9000
    
    
    dbserver = UDPServer((DBIP,DBPORT), DBServer)
    
    
    try:
        engine = create_engine(r'sqlite:///gateway.db?check_same_thread=False', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
    except Exception as e:
        print(e)

    dbserver.serve_forever()