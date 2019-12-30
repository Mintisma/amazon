# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import pandas as pd


class InfoExtendSpider(scrapy.Spider):
    name = 'info_extend'
    allowed_domains = ['www.amazon.com']
    start_urls = ['http://www.amazon.com/']

    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.base_url = 'https://www.amazon.com/dp/'

    def start_requests(self):
        query_list = list(self.df['query'])

        yield

    def parse(self, response):
        pass
