# coding=utf-8
__author__ = 'Jay'

import os
import unittest
from Role import Role,RoleORMHelper




TEST_DB = 'test.db'

class UserORMHelperTestCase(unittest.TestCase):



    def setUp(self):
        """Set up a blank temp database before each test"""
        self.helper=RoleORMHelper("role.db")
        # self.helper.drop_db()
        self.helper.create_db()


    def tearDown(self):
        """Destroy blank temp database after each test"""
        # self.helper.drop_db()

    # def test_add(self):
    #     # 插入测试
    #     isSuccess=self.helper.addRole(Role("admin", "CRUD"))
    #     self.assertTrue(isSuccess)
    #     isSuccess=self.helper.addRole(Role("normal", "CR"))
    #     self.assertFalse(isSuccess)
    #     isSuccess=self.helper.addRole(Role("visitor", "R"))
    #     self.assertFalse(isSuccess)




    # def test_delete(self):
    #     # 删除测试
    #     isSuccess = self.helper.addRole(Role("tome", "tom jobn"))
    #     self.assertTrue(isSuccess)
    #     isSucess=self.helper.delete(Role("tome", "tom jobn"))
    #     self.assertTrue(isSucess)

    def test_query_all(self):
        # 查询所有相同name数据测试
        # isSuccess = self.helper.addRole(Role("admin", "CRUD"))
        # self.assertTrue(isSuccess)
        # isSuccess = self.helper.addRole(Role("normal", "CR"))
        # self.assertFalse(isSuccess)
        # isSuccess = self.helper.addRole(Role("visitor", "R"))
        # self.assertFalse(isSuccess)
        userList=self.helper.query_all_with_role_role_function(Role("admin", "CRUD"))
        # print userList
        self.assertEqual(len(userList),1)


    def test_query_all_role(self):
        userList=self.helper.query_all_role()
        self.assertGreater(len(userList),0)

    def test_query_all_ID(self):
        userList=self.helper.queryRoleByRoleId(1)
        self.assertGreater(userList,1)




















if __name__ == '__main__':
    unittest.main()


