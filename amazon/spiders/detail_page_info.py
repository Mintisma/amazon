# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import pickle

from scrapy import Spider
from scrapy.http import Request

from amazon.items import AmazonItem
from amazon.utils.get_cookie import get_browser_cookie


class detailpageinfospider(Spider):
    name = 'top_100_info'
    base_url = 'https://www.amazon.com/dp/'

    def __init__(self, asin='B07RTX288X', category='foam_pillow', **kwargs):
        self.start_urls = [self.base_url + asin, ]
        self.category = category
        super().__init__(**kwargs)

    def start_requests(self):
        # yield request with address set
        cookie_dict = get_browser_cookie(self.start_urls[0])
        yield Request(self.start_urls[0], dont_filter=True, cookies=cookie_dict)

    def parse(self, response):
        top_asin_url = response.xpath('//a[contains(@href, "gp/bestsellers")]/@href').extract()[-1]
        top_asin_url = urljoin(self.base_url, top_asin_url)
        yield Request(url=top_asin_url, callback=self.parse_top_asins)

    def parse_top_asins(self, response):
        listing_detail_url_list = [urljoin(self.base_url, item) for item in response.xpath('//a[@class="a-link-normal"]/@href').extract()
                         if 'product-reviews' not in item][:-3]

        price_list_temp = response.xpath('//span[@class="p13n-sc-price"]/text()').extract()
        price_list = []
        # price_list = [float(price.replace('$', '').replace(',', '')) for price in price_list]
        for price in price_list_temp:
            if isinstance(price, int):
                price_list.append(price)
            else:
                price_list.append(float(0))

        for i in range(len(listing_detail_url_list)):
            listing_detail_url = listing_detail_url_list[i]
            price = price_list[i]
            if listing_detail_url.split('/')[-3].startswith('B'):
                asin = listing_detail_url.split('/')[-3]
            else:
                asin = listing_detail_url.split('/')[-2]
            yield Request(listing_detail_url, meta={'price': price, 'asin': asin}, callback=self.parse_detail_page)

        page_2_url = response.xpath('//a[text()="Next page" and contains(@href, "Best")]/@href').extract_first('')
        if page_2_url:
            yield Request(page_2_url, callback=self.parse_top_asins)

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