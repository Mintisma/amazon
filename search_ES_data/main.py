import time
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed

from sqlHelper import Sqlhelper
from request_attributes_ES import request_data
from request_asin_amazon import AsinList


TABLE = 'amazon_listing_info'
sqlHelper = Sqlhelper()
al = AsinList()


def dict_2_sql(result_dict):
    keys = ', '.join(result_dict.keys())
    values = ', '.join(['%s'] * len(result_dict))
    insert_sql = 'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=TABLE, keys=keys, values=values)
    update = ','.join([" {key}=VALUES({key})".format(key=key) for key in list(result_dict.keys())])
    insert_sql += update
    return insert_sql


def get_product_data(category, query, pages):
    start_time = time.time()
    asin_list = al.get_asin_list(query, pages)
    print('amazon scraping costs {} seconds'.format(int(time.time()-start_time)))
    print('length of asin_list: {}'.format(len(asin_list)))
    print('asin_list: ', asin_list[0], asin_list[1])

    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(request_data, asin) for asin in asin_list]
        for future in as_completed(futures):
            result_dict = future.result()
            result_dict['category'] = category

            # 插入数据库
            insert_sql = dict_2_sql(result_dict)

            sqlHelper.modify(insert_sql, args=tuple(result_dict.values()))
        sqlHelper.close()
    print('ES API costs {} seconds'.format(int(time.time() - start_time)))


if __name__ == '__main__':
    category = sys.argv[1]
    query = sys.argv[2]
    pages = int(sys.argv[3])
    get_product_data(category, query, pages)
