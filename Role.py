# coding=utf-8
__author__ = 'Jay'

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
class Role(Base):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=True)
    role = Column(String(32))
    function = Column(String(16))

    def __init__(self, role, function):
        self.role = role
        self.function = function

    __table_args__ = (
        UniqueConstraint('id', 'role', name='uix_id_role'),
        Index('ix_id_role', 'role', 'function'),
    )


class RoleORMHelper(object):

    def __init__(self, database_name):
        DATABASE_PATH = os.path.join(basedir, database_name)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)

    def create_db(self):

        Base.metadata.create_all(self.engine)  # 创建表
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    # def drop_db(self):
    #     Base.metadata.drop_all(self.engine)   #删除表


    def addRole(self, role):
        # 插入数据
        isSucess=False
        usrsList=self.query_all_with_role_role_function(role)
        if(usrsList and len(usrsList)>0):#用户已经注册
           return False
        self.session.add(role)
        self.session.commit()
        isSucess=True
        return isSucess

    # def delete(self,users):
    #     # 删除数据
    #     isSucess=False
    #     user1 = self.session.query(Role).filter_by(role=users.role).first()
    #     self.session.delete(user1)
    #     self.session.commit()
    #     isSucess=True
    #     return isSucess


    def query_all_with_role_role_function(self, users):
        # 查询所有相同于name，password数据
        userList=self.session.query(Role).filter_by(role=users.role,function=users.function).all()
        return userList


    def query_all_role(self):
        userList=self.session.query(Role).all()
        return userList


    def queryRoleByRoleId(self, roleId):
        role = self.session.query(Role).filter_by(id=roleId).first()
        return role







