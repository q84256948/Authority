# coding=utf-8
__author__ = 'YU'
import os
import unittest
from ArticleORM import Article,ArticleORMHelper




TEST_DB = 'test.db'

class ArticleORMHelperTestCase(unittest.TestCase):



    def setUp(self):
        """Set up a blank temp database before each test"""

        self.helper=ArticleORMHelper("Article.db")
        self.helper.drop_db()
        self.helper.create_db()



    def tearDown(self):
        """Destroy blank temp database after each test"""
        self.helper.drop_db()

    def test_add(self):
        # 插入测试
        isSuccess=self.helper.addArticle(Article("tome", "tom jobn"))
        self.assertTrue(isSuccess)
        isSuccess=self.helper.addArticle(Article("tome", "tom jobn"))
        self.assertTrue(isSuccess)


    def test_query_all(self):
        # 查询所有相同name数据测试
         isSuccess=self.helper.addArticle(Article("tome", "tom jobn"))
         self.assertTrue(isSuccess)
         isSuccess=self.helper.addArticle(Article("tome", "tom jobn2"))
         self.assertTrue(isSuccess)
         isSuccess=self.helper.addArticle(Article("tome", "tom jobn3"))
         self.assertTrue(isSuccess)
         userList=self.helper.query_all_with_article_name_password(Article("tome", "tom jobn"))
         # print userList
         self.assertEqual(len(userList),1)


    def test_query(self):
        # 查看表里面的所有数据
        isSuccess = self.helper.addArticle(Article("tome", "tom jobn"))
        self.assertTrue(isSuccess)
        userList = self.helper.query_all_articles()
        self.assertGreater(len(userList), 0)


    def test_delete(self):
        # 删除测试
         isSuccess = self.helper.addArticle(Article("tome", "tom jobn"))
         self.assertTrue(isSuccess)
         isSucess=self.helper.delete(Article("tome", "tom jobn"))
         self.assertTrue(isSucess)



if __name__ == '__main__':
    unittest.main()
