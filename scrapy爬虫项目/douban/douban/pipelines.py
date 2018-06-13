# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import codecs
import json
from logging import log


class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item

# 保存json格式文件
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('douban.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item))+"\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close

# 存入数据库
class WebcrawlerScrapyPipeline(object):
    def __init__(self, dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams=dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',
            use_unicode=True,
            port=3306
        )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self._conditional_insert,item)#调用插入的方法
        query.addErrback(self._handle_error,item,spider)#调用异常处理方法
        return item

    #写入数据库中
    def _conditional_insert(self,tx,item):
        sql = "insert into book(url,isbn,name,author,image,publisher,pubdate,rating,price) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params=(item["url"],item["isbn"],item["name"],item["author"],item["image"],item["publisher"],item["pubdate"],item["rating"],item["price"])
        tx.execute(sql, params)
    #错误处理方法
    def _handle_error(self, failue, item, spider):
        print("--------------database operation exception!!-----------------")
        print("-------------------------------------------------------------")
        print(failue)
