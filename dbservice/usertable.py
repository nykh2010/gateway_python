from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 数据表 
class Terminal(Base):
    '''终端表'''
    __tablename__ = 'terminal'

    tid = Column(String, primary_key=True)      # 终端id
    ttype = Column(Integer, nullable=False)     # 终端类型
    tver = Column(String, nullable=False)        # 协议类型
    tstatus = Column(Integer, default=0)        # 终端状态
