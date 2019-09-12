# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy.http import Request

from amazon.items import AmazonItem


class DetailPageInfoSpider(scrapy.Spider):
    name = 'detail_page_info'
    allowed_domains = ['www.amazon.com']
    start_urls = ['http://www.amazon.com/']
    base_url = 'http://www.amazon.com/dp/'

    def __init__(self, asin, category='', **kwargs):
        self.start_urls = [self.base_url + asin, ]
        self.category = category
        super().__init__(**kwargs)

    def parse(self, response):
        top_asin_url = response.xpath('//a[contains(@href, "gp/bestsellers")]/@href').extract()[-1]
        top_asin_url = urljoin(self.base_url, top_asin_url)
        yield Request(url=top_asin_url, callback=self.parse_top_asins)

    def parse_top_asins(self, response):
        listing_detail_url_list = [urljoin(self.base_url, item) for item in response.xpath('//a[@class="a-link-normal"]/@href').extract()
                         if 'product-reviews' not in item][:-3]
        for listing_detail_url in listing_detail_url_list:
            yield Request(listing_detail_url, callback=self.parse_detail_page)

        page_2_url = response.xpath('//a[text()="Next page" and contains(@href, "Best")]/@href').extract_first('')
        if page_2_url:
            yield Request(page_2_url, callback=self.parse_top_asins)

    def parse_detail_page(self, response):
        amazon_item = AmazonItem()

        title = response.xpath('//span[@id="productTitle"]/text()').extract_first('').strip()

        bullet_points = response.xpath('//span[@class="a-list-item"]/text()').extract()
        bullet_point_list = [bullet_point.strip() for bullet_point in bullet_points if len(bullet_point.strip()) > 0]
        bullet_points = ' '.join(bullet_point_list)

        amazon_item['title'] = title
        amazon_item['bullet_points'] = bullet_points
        amazon_item['category'] = self.category

        yield amazon_item