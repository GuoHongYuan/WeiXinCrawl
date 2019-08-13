# -*- coding: utf-8 -*-
import re
import scrapy
import redis
from bs4 import BeautifulSoup
from ..items import *


class WeixinpageSpider(scrapy.Spider):
    name = 'WeiXinPage'

    def __init__(self):
        self.conn = redis.Redis(host="127.0.0.1", port=6379, db=1)

    def start_requests(self):

        while self.conn.llen('人工智能') > 0: #如果还有连接
            url = self.conn.lpop('人工智能').decode()
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        titem = ContextItem()
        #pitem = PictureItem()
        soup = BeautifulSoup(response.body, 'lxml',fromEncoding="utf-8")
        titem['context'] = ''.join(re.findall('[\u4e00-\u9fa5]',str(soup.find('div', id="img-content")))) #汉字部分提取
        titem['title'] = soup.find('h2',id='activity-name').text
        yield titem
        #pitem['ImgUrl'] = soup.find_all('img')['src']  #图片的链接
        #yield pitem
        pass


