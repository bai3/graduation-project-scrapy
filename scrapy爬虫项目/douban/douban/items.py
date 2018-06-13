# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()            # 豆瓣图书id
    isbn = scrapy.Field()           # 图书isbn
    name = scrapy.Field()           # 图书名称
    author = scrapy.Field()         # 图书作者
    image = scrapy.Field()          # 图书图片链接
    publisher = scrapy.Field()      # 图书出版社
    pubdate = scrapy.Field()        # 图书出版时间
    rating = scrapy.Field()         # 图书评分
    price = scrapy.Field()          # 图书定价
    pass
