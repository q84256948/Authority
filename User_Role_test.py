# coding=utf-8
__author__ = 'Jay'


import os
import unittest
from User_Role import User_Role,UserRoleORMHelper





class UserORMHelperTestCase(unittest.TestCase):



    def setUp(self):
        """Set up a blank temp database before each test"""
        self.helper=UserRoleORMHelper("User_Role.db")
        self.helper.drop_db()
        self.helper.create_db()


    def tearDown(self):
        """Destroy blank temp database after each test"""
        self.helper.drop_db()

    def test_add(self):
        # 插入测试
        isSuccess=self.helper.addUserRole(User_Role("tome", "tom jobn"))
        self.assertTrue(isSuccess)
        isSuccess=self.helper.addUserRole(User_Role("tome", "tom jobn"))
        self.assertFalse(isSuccess)


    def test_delete(self):
        # 删除测试
        isSuccess = self.helper.addUserRole(User_Role("tome", "tom jobn"))
        self.assertTrue(isSuccess)
        isSucess=self.helper.delete(User_Role("tome", "tom jobn"))
        self.assertTrue(isSucess)

    def test_query_all(self):
        # 查询所有相同name数据测试
         isSuccess=self.helper.addUserRole(User_Role("tome", "tom jobn"))
         self.assertTrue(isSuccess)
         isSuccess=self.helper.addUserRole(User_Role("tome", "tom jobn2"))
         self.assertTrue(isSuccess)
         isSuccess=self.helper.addUserRole(User_Role("tome", "tom jobn3"))
         self.assertTrue(isSuccess)
         userList=self.helper.query_all_with_role_role_function(User_Role("tome", "tom jobn"))
         # print userList
         self.assertEqual(len(userList),1)





    def test_query_all_userId(self):
        # 查询所有相同userId数据测试
         isSuccess=self.helper.addUserRole(User_Role("tome", "tom jobn"))
         self.assertTrue(isSuccess)
         isSuccess=self.helper.addUserRole(User_Role("tome", "tom jobn2"))
         self.assertTrue(isSuccess)
         isSuccess=self.helper.addUserRole(User_Role("tome", "tom jobn3"))
         self.assertTrue(isSuccess)
         userList=self.helper.query_first_userId("tome")
         # print userList
         self.assertIsNotNone(userList)




















if __name__ == '__main__':
    unittest.main()


