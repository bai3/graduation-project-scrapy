# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/tag/?view=cloud']

    def parse(self, response):
        base_url = "https://book.douban.com"
        tags = response.xpath(r'//*[@id="content"]/div/div[1]/div[2]/div/table/tbody/tr[1]/td[1]/a/@href').extract()
        print('*************打印出所有热门分类****************')
        for tag in tags:
            next_url = base_url + tag
            print(next_url)
            yield scrapy.Request(next_url, callback=self.tag_item)
        pass 

    # 分类下目录书籍爬取
    def tag_item(self,response):
        base_url = "https://book.douban.com"
        books = response.xpath(r'//*[@id="subject_list"]/ul/li/div/h2/a/@href').extract()
        for book in books:
            yield scrapy.Request(book, callback=self.book_item)
        page = 1
        try:
            next_page = response.xpath('//*[@id="subject_list"]/div[@class="paginator"]/span[@class="next"]/a/@href').extract()[0]
        except:
            print('*********最后一页了*************')
        else:
            page = page + 1
            print(next_page)
            url = base_url+next_page
            yield scrapy.Request(url, callback=self.tag_item)
    
    # 书籍详情页
    def book_item(self,response):
        print('*****************数据打印*******************')
        rating = response.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()').extract()
        if rating :
            rating = rating[0]
            url = response.xpath('//*[@class="rec"]/a/@data-url').extract()[0]
            isbn = response.xpath(u'normalize-space(//*[@id="info"]/span[contains(./text(),"ISBN:")]/following::text()[1])').extract()[0]
            name = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract()[0]
            author = response.xpath('//*[@id="info"]/a[1]/text()').extract()
            if author:
                author = author[0].strip()
            else:
                author = response.xpath('//*[@id="info"]/span/a/text()').extract()[0].strip()
            image = response.xpath('//*[@id="mainpic"]/a/img/@src').extract()[0]
            publisher = response.xpath(u'//*[@id="info"]/span[contains(./text(),"出版社")]/following::text()[1]').extract()
            pubdate = response.xpath(u'//*[@id="info"]/span[contains(./text(),"出版年")]/following::text()[1]').extract()
            price = response.xpath(u'//*[@id="info"]/span[contains(./text(),"定价")]/following::text()[1]').extract()
            if publisher :
                publisher = publisher[0]
            else :
                publisher = ' '
            if pubdate:
                pubdate = pubdate[0]
            else :
                pubdate = ' '
            if price :
                price = price[0]
            else :
                price = ' '
            item = DoubanItem()
            item['url'] = url
            item['isbn'] = isbn
            item['name'] = name
            item['author'] = author
            item['image'] = image
            item['publisher'] = publisher
            item['pubdate'] = pubdate
            item['rating'] = rating
            item['price'] = price
            print('*********************************************')
            yield item
        else:
            print('书籍信息无效')
            pass



    
