import time

import requests
from scrapy.selector import Selector


class AsinList:
    base_url = 'https://www.amazon.com/s?k='
    amazon_url = 'https://www.amazon.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer': "www.google.com".encode(),
    }
    asin_list = []
    s = requests.session()

    def asin_list_page(self, url):
        time.sleep(1)
        # 优化header的referer信息
        previews_url = self.get_previews_url(url)
        self.headers['Referer'] = previews_url.encode()

        r = self.s.get(url, headers=self.headers)
        r.encoding = 'utf8'
        selector = Selector(text=r.text)
        href_list = selector.xpath('//div/h2/a[@class="a-link-normal a-text-normal"]/@href').extract()
        asin_list = [href.split('/')[3] for href in href_list if not href.startswith('/gp/')]

        return asin_list

    def get_asin_list(self, query, pages):
        # 获取cookie
        self.get_cookie()

        # 正式访问
        query = query.replace(' ', '+').replace('_', '+')
        print('query: {}'.format(query))
        query_list = [query + '&page={}'.format(page) for page in range(1, pages + 1)]
        url_list = [self.base_url + query for query in query_list]
        for url in url_list:
            asin_list_page = self.asin_list_page(url)
            self.asin_list.extend(asin_list_page)
        return self.asin_list

    def get_cookie(self):
        self.s.get(self.amazon_url, headers=self.headers)

    def get_previews_url(self, url):
        page = url[-1]
        if int(page) > 1:
            previews_page = int(page) - 1
            new_page = str(previews_page)
            previews_url = url.replace(page, new_page)
        else:
            previews_url = 'https://www.amazon.com/'
        return previews_url


