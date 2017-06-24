# coding=utf-8
__author__ = 'Jay'
import os
import unittest

from APP import app,User_helper,User_Role_helper,Article_helper

from UserORM import Users
from User_Role import User_Role
from ArticleORM import Article






class BasicTestCase(unittest.TestCase):


    def test_database(self):
        """inital test. ensure that the database exists"""
        tester = os.path.exists("flaskr.db")
        self.assertTrue(tester)


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database before each test"""
        basedir = os.path.abspath(os.path.dirname(__file__))
        print "the basedir ---->",basedir
        app.config['TESTING'] = True
        self.app = app.test_client()


    def tearDown(self):
        """Destroy blank temp database after each test"""
        self.app=None


    def signUp(self, username, password,roleId):
        """Login helper function"""
        return self.app.post('/signUp', data=dict(
            username=username,
            password=password,
            roleId=roleId
        ), follow_redirects=True)

    def Login(self, username, password):
        """Login helper function"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def Change(self, username, old_password,new_password):
        """Login helper function"""
        return self.app.post('/Change', data=dict(
            username=username,
            old_password =old_password,
            new_password =new_password
        ), follow_redirects=True)

    def addArticle(self,title,text):
        """Logout helper function"""
        return self.app.post('/addArticle', data=dict(
            title=title,
            text=text,
        ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/logout', follow_redirects=True)

    def allMusic(self):
        """Logout helper function"""
        return self.app.get('/allMusic', follow_redirects=True)



    def testSignUpUser(self):
        # 注册成功
        rv = self.signUp("tom2333", "tom%@","1")

        user = User_helper.query_first_name_password(Users("tom2333", "tom%@"))
        User_Role_helper.delete(User_Role(user.id,"1"))
        User_helper.delete(Users("tom2333", "tom%@"))
        self.assertIn("User registration successful!", rv.data)


    def testSignUpUserLose(self):
        # 注册失败
        self.signUp("tom2333", "tom12333", "1")
        rv = self.signUp("tom2333", "tom12333", "1")
        user = User_helper.query_first_name_password(Users("tom2333", "tom12333"))
        User_Role_helper.delete(User_Role(user.id,"1"))
        User_helper.delete(Users("tom2333", "tom12333"))
        self.assertIn("User registration failed!", rv.data)


    def testLoginUser(self):
        # 登陆成功

        user = User_helper.query_first_name_password(Users("tom2333", "%@123"))
        if user:
           User_Role_helper.delete(User_Role(user.id , "1"))
           User_helper.delete(Users("tom2333", "%@123"))


        self.signUp("tom2333", "%@123", "1")
        rv=self.Login("tom2333", "%@123")

        self.assertIn("Login Success", rv.data)



    def testLoginUserNonentity(self):
        # 登录失败   用户不存在
        rv=self.Login("tom789","tom123456789")
        self.assertIn("Login Failed!", rv.data)




    def test_Change(self):
        # 修改密码成功
        self.signUp("Jar123", "Jar1234", "1")
        rv=self.Login("Jar123", "Jar1234")
        self.assertIn("Login Success", rv.data)
        rv = self.Change("Jar123", "Jar1234","Jar456")
        user = User_helper.query_first_name_password(Users("Jar123", "Jar456"))
        User_Role_helper.delete(User_Role(user.id, "1"))
        User_helper.delete(Users("Jar123", "Jar456"))
        self.assertIn('Change Success', rv.data)

    def test_Change_Fail(self):
        # 修改密码失败
        self.signUp("Jar123", "Jar1234", "1")
        rv=self.Login("Jar123", "Jar1234")
        self.assertIn("Login Success", rv.data)
        rv = self.Change("Jar123", "Jar123","Jar456")
        user = User_helper.query_first_name_password(Users("Jar123", "Jar1234"))
        User_Role_helper.delete(User_Role(user.id, "1"))
        User_helper.delete(Users("Jar123", "Jar1234"))
        self.assertIn('Change Fail', rv.data)

    def test_allArticle(self):
        # 发表文章
        self.signUp("Jar123", "Jar1234", "1")
        rv = self.Login("Jar123", "Jar1234")
        self.assertIn("Login Success", rv.data)
        rv = self.addArticle("fish","fish is good!")
        user = User_helper.query_first_name_password(Users("Jar123", "Jar1234"))
        User_Role_helper.delete(User_Role(user.id, "1"))
        User_helper.delete(Users("Jar123", "Jar1234"))
        Article_helper.delete(Article("fish", "fish is good!"))
        self.assertIn("text published successfully", rv.data)




    def test_userLogout(self):
        # 注销测试
        self.signUp("Jar123", "Jar1234", "1")
        rv=self.Login("Jar123", "Jar1234")
        user = User_helper.query_first_name_password(Users("Jar123", "Jar1234"))
        User_Role_helper.delete(User_Role(user.id,"1"))
        User_helper.delete(Users("Jar123", "Jar1234"))
        self.assertIn("Login Success", rv.data)
        rv = self.logout()
        self.assertIn(b'You were logged out', rv.data)


















if __name__ == '__main__':
    unittest.main()


