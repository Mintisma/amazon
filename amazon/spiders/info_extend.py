# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy.http import Request

from amazon.items import AmazonItem
from amazon.utils.get_cookie import get_browser_cookie
from amazon.utils.func_xpath import get_search_price


class InfoExtendSpider(scrapy.Spider):
    name = 'search_info'
    base_url = 'https://www.amazon.com/s?k='
    allowed_domains = ['www.amazon.com']

    def __init__(self, search_term='king_waterproof_mattress_pad', pages=3, category='king_waterproof_mattress_pad', **kwargs):
        super().__init__(**kwargs)
        search_term = search_term.replace('_', '+')
        url = self.base_url + search_term + '&page='
        urls = [url + str(page) for page in range(1, pages+1)]
        self.start_urls = urls
        self.category = category

    def start_requests(self):
        cookie_dict = get_browser_cookie(self.start_urls[0])
        for url in self.start_urls:
            yield Request(url , dont_filter=True, cookies=cookie_dict)

    def parse(self, response):
        products = response.xpath('//div[contains(@class, "s-result-list")]/div[@data-asin]')
        for product in products:
            asin = product.xpath('@data-asin').extract_first('')
            price = get_search_price(product)

            url_extend = product.xpath('div/span/div/div/span/a[@class="a-link-normal"]/@href').extract_first('')
            url_extend = '/'.join(url_extend.split('/')[:-1])
            url = urljoin(self.base_url, url_extend)
            yield Request(url, meta={'asin': asin, "price": price}, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        amazon_item = AmazonItem()

        title = response.xpath('//span[@id="productTitle"]/text()').extract_first('').strip()

        bullet_points = response.xpath('//span[@class="a-list-item"]/text()').extract()
        bullet_point_list = [bullet_point.strip() for bullet_point in bullet_points if len(bullet_point.strip()) > 0]
        bullet_points = ' '.join(bullet_point_list)

        price = response.meta.get('price', 0)
        asin = response.meta.get('asin', '')

        amazon_item['title'] = title
        amazon_item['bullet_points'] = bullet_points
        amazon_item['category'] = self.category
        amazon_item['price'] = price
        amazon_item['asin'] = asin

        yield amazon_item
