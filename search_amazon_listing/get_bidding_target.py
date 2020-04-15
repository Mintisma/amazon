from urllib.parse import urljoin
from time import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from parsel import Selector
import requests


class ListingDetail:
    amazon_url = 'https://www.amazon.com/'
    base_url = 'https://www.amazon.com/s?k='

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer': "www.google.com".encode(),
    }

    s = requests.session()

    def get_cookie(self):
        self.s.get(self.amazon_url, headers=self.headers)

    def get_search_urls(self, search_term='bluetooth_speaker', pages=3):
        # 返回所有搜索页
        search_term = search_term.replace('_', '+')
        url = self.base_url + search_term + '&page='
        # search_url_list = [url + str(page) + '&qid=' + str(round(time())) + '&ref=sr_pg_' + str(page) for page in range(1, pages+1)]
        search_url_list = [url + str(page) + "&ref=nb_sb_noss_2" for page in range(1, pages+1)]
        return search_url_list

    def get_detail_urls(self, url_search):
        # 返回单个搜索页的所有asin_url
        # url_search = self.refresh_url_qid(url_search)
        r = self.s.get(url_search, headers=self.headers)
        select = Selector(text=r.text)
        url_detail_list = select.xpath('//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]/a[@class="a-link-normal a-text-normal"]/@href').extract()
        url_detail_list = [urljoin(self.amazon_url, url) for url in url_detail_list]

        return url_detail_list

    @staticmethod
    def refresh_url_qid(url):
        qid_start = url.index('qid') + 4
        qid_end = qid_start + 10
        url_new = url[:qid_start] + str(round(time())) + url[qid_end:]
        return url_new

    def get_detail_data(self, url):
        url = self.refresh_url_qid(url)

        r = self.s.get(url, headers=self.headers)
        select_listing = Selector(text=r.text)
        price = select_listing.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first('')
        if not price:
            price = select_listing.xpath('//span[@id="priceblock_saleprice"]/text()').extract_first('')
        print(price)
        return price


if __name__ == '__main__':
    ld = ListingDetail()
    ld.get_cookie()

    # search_term = input('please input the search_term you want to search \n')
    # pages = input('please input the pages you want to search \n')
    search_term = "bluetooth_speaker"
    pages = 3

    search_url_list = ld.get_search_urls(search_term,  int(pages))
    for search_url in search_url_list:
        print("search_url: ", search_url)

    detail_url_list = []

    print('进入with语句')
    i = 0
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(ld.get_detail_urls, search_url) for search_url in search_url_list]
        for future in as_completed(futures):
            detail_url_page = future.result()
            if detail_url_page:
                print('detail_page_{}存在'.format(i + 1))
                i += 1
                detail_url_list.extend(detail_url_page)
    print('结束with语句')
