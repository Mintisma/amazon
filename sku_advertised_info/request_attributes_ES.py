import time
import hashlib
from datetime import datetime

import requests


def request_data(asin, country='us'):
    """
    :param asin: asin we want to get info;
    :return:
    """
    if not isinstance(asin, str):
        raise ValueError('asin should be of string format')

    # 挚哥的API
    headers = {
        'Authorization': 'eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJhdWQiOiJzbWRhdGEiLCJyb2xlIjoiMyIsImV4cCI6MTY3MjEzMzA4NCwidXNlcmlkIjoiMSIsInVzZXJuYW1lIjoiYWR2ZXJ0In0.kGjVZjatFkbdbScJn_LF87OD806CeRwAI4i27YxvgQ8'
    }
    url_dict = {
        'us': 'http://52.82.24.19:8181/usdata/product/byAsin?site=1&asin={asin}'.format(asin=asin),
        'uk': 'https://api.sellermotor.com/v1/amazon/product/sqlquery2?site=2&sql=SELECT asin,title,s_about,price,rating,reviews from product_uk where asin = {asin}'.format(asin=asin),
        'de': 'https://api.sellermotor.com/v1/amazon/product/sqlquery2?site=2&sql=SELECT asin,title,s_about,price,rating,reviews from product_de where asin = {asin}'.format(asin=asin),
        'fr': 'https://api.sellermotor.com/v1/amazon/product/sqlquery2?site=2&sql=SELECT asin,title,s_about,price,rating,reviews from product_fr where asin = {asin}'.format(asin=asin),
    }

    # request & get result dict
    url = url_dict[country]
    res = requests.get(url, headers=headers)

    result_dict = res.json()

    if not result_dict['data']:
        result_dict['data'] = dict()
        result_dict['data']['asin'] = asin
        result_dict['data']['title'] = ''
        result_dict['data']['s_about'] = ''
        result_dict['data']['price'] = ''
        result_dict['data']['rating'] = ''
        result_dict['data']['reviews'] = 0

    result_dict = result_dict['data']

    insert_dict = dict()
    try:
        insert_dict['asin'] = result_dict['asin']
        insert_dict['title'] = result_dict['title']
        insert_dict['price'] = result_dict['price']
        insert_dict['rating'] = result_dict['rating']
        insert_dict['reviews'] = result_dict['reviews']
        bullet_points = result_dict['s_about']
        bullet_point_list = [bullet_point.strip() for bullet_point in bullet_points if len(bullet_point.strip()) > 0]
        bullet_points = ' '.join(bullet_point_list)
        insert_dict['bullet_points'] = bullet_points
        insert_dict['country'] = country

    except KeyError as e:
        print('ES data missed')
        print(e)

    return insert_dict