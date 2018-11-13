from flask import json
from sqlalchemy import Table, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from config import DB_URL

Base = declarative_base()
engine = create_engine(DB_URL)
metadata = MetaData(bind=engine)

class Member(Base):
    __table__ = Table('pre_common_member', metadata, autoload=True)

# 需要在discuz数据库中手动设置主键
class Session(Base):
    __table__ = Table('pre_common_session', metadata, autoload=True)

class Thread(Base):
    __table__ = Table('pre_forum_thread', metadata, autoload=True)

    def __repr__(self):
        return json.dumps({"thread info": {'subject ': self.subject, 'author': self.author}})

class Profile(Base):
    __table__ = Table('pre_common_member_profile', metadata, autoload=True)

    def __repr__(self):
        return json.dumps({"user profile": {'uid ': self.uid, 'gender': self.gender}})

class Message(Base):
    __table__ = Table('pre_ucenter_pm_lists', metadata, autoload=True)

    def __repr__(self):
        return json.dumps({"message": {'authorid': self.authorid, 'subject': self.subject}})
