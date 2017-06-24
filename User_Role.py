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
class User_Role(Base):
    __tablename__ = 'User_Role'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    roleId = Column(Integer)

    def __init__(self, userId, roleId):
        self.userId = userId
        self.roleId = roleId

    __table_args__ = (
        UniqueConstraint('id', 'userId', name='uix_id_userId'),
        Index('ix_id_userId', 'userId', 'roleId'),
    )

class UserRoleORMHelper(object):

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


    def addUserRole(self, users):
        # 插入数据
        isSucess=False
        usrsList=self.query_all_with_role_role_function(users)
        if(usrsList and len(usrsList)>0):#用户已经注册
           return False
        self.session.add(users)
        self.session.commit()
        isSucess=True
        return isSucess

    def delete(self,users):
        # 删除数据
        isSucess=False
        user1 = self.session.query(User_Role).filter_by(userId=users.userId).first()
        self.session.delete(user1)
        self.session.commit()
        isSucess=True
        return isSucess


    def query_all_with_role_role_function(self, users):
        # 查询所有相同于name，password数据
        userList=self.session.query(User_Role).filter_by(userId=users.userId,roleId=users.roleId).all()
        return userList

    def query_first_userId(self, userId):
        # 查询所有相同name数据
        user_Role=self.session.query(User_Role).filter_by(userId=userId).first()
        return user_Role
