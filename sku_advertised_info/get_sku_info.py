import time

import requests
from scrapy import Selector
from selenium import webdriver

from sqlHelper import Sqlhelper
from request_attributes_ES import request_data

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Referer': "www.google.com",
}

sqlHelper = Sqlhelper()
base_url = 'https://www.amazon.com/dp/'
TABLE = 'advertised_listing_info'


def get_asin_data(asin):
    url = base_url + asin
    browser = webdriver.Chrome(executable_path='/Users/ted/Desktop/chromedriver')
    browser.get(url)

    time.sleep(10)
    # r = requests.get(url, headers=headers)
    selector = Selector(text=browser.page_source)
    browser.close()

    title = selector.xpath('//span[@id="productTitle"]/text()').extract_first('').strip()
    bullet_points = selector.xpath('//span[@class="a-list-item"]/text()').extract()
    bullet_point_list = [bullet_point.strip() for bullet_point in bullet_points if len(bullet_point.strip()) > 0]
    bullet_points = ' '.join(bullet_point_list)

    data = {
        'title': title,
        'bullet_points': bullet_points,
        'asin': asin,
    }
    insert_data(data)


def insert_data(data):
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    # 插入数据库
    insert_sql = 'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=TABLE, keys=keys, values=values)
    update = ','.join([" {key}=VALUES ({key})".format(key=key) for key in list(data.keys())])
    insert_sql += update
    try:
        sqlHelper.modify(insert_sql, args=tuple(data.values(), ))
    except Exception as e:
        print(e, '\n', data)

    sqlHelper.close()


def main(asin):
    insert_dict = request_data(asin)
    insert_data(insert_dict)


if __name__ == '__main__':
    asin = input('please input the ASIN you want to advertise \n')
    # get_asin_data(asin)
    main(asin)
