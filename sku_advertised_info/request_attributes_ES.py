import time
import hashlib
from datetime import datetime

import requests


def request_data(asin):
    """
    :param asin: asin we want to get info;
    :return:
    """
    if not isinstance(asin, str):
        raise ValueError('asin should be of string format')

    # get query url
    time_param = int(datetime.now().timestamp())
    sign_str = 'sm5a70d9b0174909d3cdb1' + str(time_param) + '4b2ede6b-a5f5-3cd9-8c25-e086a14f92ef'
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    params = {'sign': sign, 'timestamp': time_param, 'aid': 'sm5a70d9b0174909d3cdb1', 'asin': asin,
              'countryCode': 'us'}

    query_list = [k + '=' + str(v) for k, v in params.items()]
    query_string = '&'.join(query_list)

    url = "https://beta.sellermotor.com/selection/index/big-data" + '?' + query_string

    # request & get result dict
    res = requests.get(url)

    result_dict = res.json()
    try:
        result_dict['data'][0]
    except IndexError as e:
        result_dict['data'].append({'asin': asin, 'title': '', 's_about': '', 'price': '', 'rating': '', 'reviews': 0})

    result_dict = result_dict['data'][0]

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

    except KeyError as e:
        print('ES data missed')
        print(e)

    return insert_dict