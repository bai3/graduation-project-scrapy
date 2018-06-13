# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
import requests
import time


# 代理中间件
class ProxyMiddleWare(object):
    def process_request(self,request,spider):
        proxy = self.get_proxy()
        request.meta['proxy'] = proxy

    def process_response(self,request, response, spider):
        if response.status != 200:
            proxy = self.get_proxy()
            request.meta['proxy'] = proxy
            return request
        return response

    def get_proxy(self):
        """从proxies.txt文件中随机获取proxy"""
        while 1:
            with open('F:\\py\\web-spider\\official\\douban\\douban\\proxies.txt', 'r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                time.sleep(1)
        proxy = random.choice(proxies).strip()
        return proxy

# 表头中间件
class MyUserAgentMiddleware(UserAgentMiddleware):
    """
    设置User-agent
    """
    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('USER_AGENT')
    )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        print(agent)
        request.headers['User-Agent'] = agent
