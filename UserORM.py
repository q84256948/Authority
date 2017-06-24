# coding=utf-8
__author__ = 'YU'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, UniqueConstraint, Index, BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# DATABASE = 'flaskr.db'
# DATABASE_PATH = os.path.join(basedir, DATABASE)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
# engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base = declarative_base()


# 创建单表
class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(16))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    __table_args__ = (
        UniqueConstraint('id', 'username', name='uix_id_name'),
        Index('ix_id_name', 'username', 'password'),
    )


class UserORMHelper(object):

    def __init__(self, database_name):
        DATABASE_PATH = os.path.join(basedir, database_name)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)

    def create_db(self):

        Base.metadata.create_all(self.engine)  # 创建表
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def drop_db(self):
        Base.metadata.drop_all(self.engine)   #删除表

    def addUser(self, users):
        # 插入数据
        isSucess=False
        usrsList=self.query_all_with_user_name_password(users)
        if(usrsList and len(usrsList)>0):#用户已经注册
           return False
        self.session.add(users)
        self.session.commit()
        isSucess=True
        return isSucess

    def delete(self,users):
        # 删除数据
        isSucess=False
        user1 = self.session.query(Users).filter_by(username=users.username,password=users.password).first()
        self.session.delete(user1)
        self.session.commit()
        isSucess=True
        return isSucess

    def query_all_with_user_name(self, users):
        # 查询所有相同name数据
        userList=self.session.query(Users).filter_by(username=users.username).all()
        return userList

    def query_all_with_user_name_password(self, users):
        # 查询所有相同于name，password数据
        userList=self.session.query(Users).filter_by(username=users.username,password=users.password).all()
        return userList

    def query_first_name_password(self, users):
        # 查询一个相同于name，password数据
        user=self.session.query(Users).filter_by(username=users.username,password=users.password).first()
        return user

    def query_all_with_user_extra(self, users):
        # 查询相同password数据
        userList = self.session.query(Users).filter_by(password=users.password).all()
        return userList

    def update_user_extra_by_user_name(self, users):
        # 匹配并且修改password
        isSucess = False
        self.session.query(Users).filter(Users.username == users.username).update({"password": users.password}, synchronize_session='evaluate')
        self.session.commit()
        isSucess=True
        return isSucess


    def update_user_name_by_user_extra(self, users):
        # 匹配并且修改name
        isSucess = False
        self.session.query(Users).filter(Users.password == users.password).update({"username": users.username}, synchronize_session='evaluate')
        self.session.commit()
        isSucess=True
        return isSucess















