# -*- coding: utf-8 -*-
from urllib.parse import urljoin
from datetime import datetime

import scrapy
from scrapy.http import Request

from amazon.items import AmazonItem
from amazon.utils.get_cookie import get_browser_cookie
from amazon.utils.func_xpath import get_search_price, get_detail_rating, get_detail_reviews, get_detail_url
from amazon.utils.func import get_url


class InfoExtendSpider(scrapy.Spider):
    name = 'search_info'

    def __init__(self, search_term, category, country='us',  pages=3,  **kwargs):
        super().__init__(**kwargs)
        # 模拟签名，伪造search_url
        urls = [get_url(country, search_term, page) for page in range(1, int(pages)+1)]
        self.start_urls = urls
        self.category = category
        self.country = country

    def start_requests(self):
        cookie_dict = get_browser_cookie(self.country, self.start_urls[0])
        for url in self.start_urls:
            yield Request(url , dont_filter=True, cookies=cookie_dict)

    def parse(self, response):
        products = response.xpath('//div[contains(@class, "s-result-list")]/div[@data-asin != ""]')
        for product in products:
            asin = product.xpath('@data-asin').extract_first('')
            price = get_search_price(product, self.country)
            url = get_detail_url(product, self.country)

            yield Request(url, meta={'asin': asin, "price": price}, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        amazon_item = AmazonItem()

        title = response.xpath('//span[@id="productTitle"]/text()').extract_first('').strip()

        bullet_points = response.xpath('//div[@id="feature-bullets"]/ul/li/span[@class="a-list-item"]/text()').extract()
        bullet_point_list = [bullet_point.strip() for bullet_point in bullet_points if len(bullet_point.strip()) > 0]
        bullet_points = ' '.join(bullet_point_list)

        rating = get_detail_rating(response)
        reviews = get_detail_reviews(response)

        price = response.meta.get('price', 0)
        asin = response.meta.get('asin', '')

        amazon_item['title'] = title
        amazon_item['bullet_points'] = bullet_points
        amazon_item['category'] = self.category
        amazon_item['price'] = price
        amazon_item['asin'] = asin
        amazon_item['rating'] = rating
        amazon_item['reviews'] = reviews
        amazon_item['date'] = datetime.now().date()
        amazon_item['country'] = self.country

        yield amazon_item
