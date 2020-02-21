import requests
from scrapy.selector import Selector


class AsinList:
    base_url = 'https://www.amazon.com/s?k='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    asin_list = []

    def asin_list_page(self, url):
        r = requests.get(url, headers=self.headers)
        selector = Selector(text=r.text)
        href_list = selector.xpath('//div/h2/a[@class="a-link-normal a-text-normal"]/@href').extract()
        asin_list = [href.split('/')[3] for href in href_list if not href.startswith('/gp/')]

        return asin_list

    def get_asin_list(self, query, pages):
        query = query.replace(' ', '+').replace('_', '+')
        print('query: {}'.format(query))
        query_list = [query + '&page={}'.format(page) for page in range(1, pages + 1)]
        url_list = [self.base_url + query for query in query_list]
        for url in url_list:
            asin_list_page = self.asin_list_page(url)
            self.asin_list.extend(asin_list_page)
        return self.asin_list


