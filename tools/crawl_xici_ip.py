import requests
from fake_useragent import UserAgent
from scrapy.selector import Selector
import pymysql
import time
import random

conn = pymysql.connect(host='localhost', user='root', password="zz6901877",
                       database='books', port=3306)
cursor = conn.cursor()


def sleep_time():
    s_time = random.uniform(0.1,0.5)
    return s_time


def crawl_ip():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    for i in range(100):
        time.sleep(sleep_time())
        r = requests.get('https://www.xicidaili.com/nn/{}'.format(i), headers=headers)
        s = Selector(text=r.text)

        ip_lst = []

        all_trs = s.xpath('//table[@id="ip_list"]/tr')
        for tr in all_trs[1:]:
            ip = tr.xpath('td[2]/text()').extract_first('')
            port = tr.xpath('td[3]/text()').extract_first('')
            speed = float(tr.xpath('td[7]/div/@title').extract_first('').replace('秒', ''))
            proxy_type = tr.xpath('td[text()="高匿"]/following-sibling::td[1]/text()').extract_first('')
            if len(proxy_type) <= 5:
                ip_lst.append((ip, port, speed, proxy_type))

        for ip_info in ip_lst:
            eles = ['ip', 'port', 'speed', 'proxy_type']
            insert_sql = 'insert into proxy_ip ({eles}) values({values}) ON DUPLICATE KEY UPDATE '.format(eles=', '.join(eles), values=', '.join(['%s']*4))
            update = ', '.join(['{ele}=%s'.format(ele=ele) for ele in eles])
            insert_sql += update
            cursor.execute(insert_sql, ip_info*2)
            conn.commit()

    conn.close()


class GetIP:
    def delete_ip(self, ip):
        delete_sql = 'delete from proxy_ip where ip = {ip}'.format(ip=ip)
        cursor.execute(delete_sql)
        conn.commit()

    def judge_ip(self, ip, port):
        http_url = 'https://www.baidu.com/'
        proxy_url = 'http:{0}:{1}'.format(ip, port)
        try:
            proxy_dict = {
                'http': proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print('invalid ip and port')
            self.delete_ip(ip)
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print('effective ip')
                print('ip: ', ip)
                print('port: ', port)
                return True
            else:
                print('invalid ip and port')
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        get_sql = 'select ip, port from proxy_ip where proxy_type="HTTP" and speed<1 ORDER BY RAND() LIMIT 1'
        cursor.execute(get_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return 'http://{0}:{1}'.format(ip, port)
            # else:
            #     return self.get_random_ip()


